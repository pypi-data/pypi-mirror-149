import yaml
import argparse
import typing
from dataclasses import dataclass, field
import logging
import os
from importlib.metadata import version


class ConfigError(Exception):
    pass


@dataclass
class Config:

    _categories = ["sampling", "pareto", "clustering", "visual", "format"]
    # Default values
    sampling_enable: bool = True
    sampling_nstructure: int = 1000
    sampling_temperature: float = 37.0
    sampling_slope: float = 1.3
    sampling_intercept: float = -0.4

    pareto_percent: float = 20.0
    pareto_zcutoff: float = 0.05

    clustering_max_diam: float = 7.0
    clustering_max_avg_diam: float = 7.0

    visual_models: bool = True
    visual_centroids: bool = True
    visual_probing: bool = True

    format_dbn_file_pattern: str = "output/{seqname}-Optimal-{idx}.dbn"
    format_dbn_centroid_file_pattern: str = (
        "output/centroid/{seqname}-Centroid-{idx}.dbn"
    )
    format_dbn_seq_name: str = (
        "{seqname}-{conditions} centroid:{centroid}"
        " cond:{condition} dG: {delta_g} bolzmann"
        " prob: {boltz_prob}"
    )

    @dataclass
    class ConditionConfig:
        name: str = "condition"
        alignement_file: str = None
        reactivity_file: str = None
        constr_file: str = None
        thermodyn_only: bool = False
        auto_discovery: bool = False

        def __hash__(self):
            return self.name

        def use_alifold(self):
            return self.alignement_file is not None

    config_file: str = "input/config.yaml"
    sequence_file: str = "input/sequence.fasta"
    # output_path: str = "output"
    log_file: str = "output/ipanemap.log"
    tmp_dir: str = "output/tmp"
    output_dir: str = "output"
    debug: str = False
    # End Default Values #
    # Categories
    _condition_dict = {}

    @property
    def conditions(self) -> typing.List[ConditionConfig]:
        return list(self._condition_dict.values())

    _argparser = None

    def parse_yaml(self, config_file):
        try:
            with open(config_file, "r") as conf:
                return yaml.safe_load(conf)

        except FileNotFoundError:
            raise self._argparser.error(
                f"Config file does not exists {config_file}"
            )
        except yaml.parser.ParserError as er:
            raise self._argparser.error(
                message=f"Invalid config file {config_file}\n\n {er.args}"
            )

    def sanity_check(self):
        error = 0
        if len(self._condition_dict) == 0:
            raise ConfigError("No sampling conditions available")
        for name, cond in self._condition_dict.items():
            nconstr = 0
            if cond.alignement_file is not None:
                if not os.path.isfile(cond.alignement_file):
                    logging.error(
                        f"{cond.alignement_file} was not found for "
                        f"{cond.name}"
                    )
                    error += 1
                nconstr += 1
            if cond.reactivity_file is not None:
                if not os.path.isfile(cond.reactivity_file):
                    logging.error(
                        f"{cond.reactivity_file} was not found for "
                        f"{cond.name}"
                    )
                    error += 1
                nconstr += 1
            if cond.constr_file is not None:
                if not os.path.isfile(cond.constr_file):
                    logging.error(
                        f"{cond.constr_file} was not found for " f"{cond.name}"
                    )
                    error += 1
                nconstr += 1

            if not cond.thermodyn_only and nconstr < 1:
                error += 1
                logging.error(
                    f"at least on of alignement file or shape file "
                    f"must be provided in order to run "
                    f"the condition {cond.name}, or you must enable "
                    f"thermodyn_only"
                )
        if error > 0:
            raise ConfigError("Invalid sampling conditions")

        if not os.path.isfile(self.sequence_file):
            logging.error(f"{self.sequence_file} was not found")
            raise FileNotFoundError(self.sequence_file)

    #    def __post_init__(self):

    def init_config(self):
        self.assign_config()
        self.set_additionnal_path()

    def set_additionnal_path(self):
        self.sampling_outsample_dir = (
            f"{self.tmp_dir}/output_samples_{self.sampling_nstructure}"
        )
        self.clustering_centroid_dir = os.path.dirname(
            self.format_dbn_centroid_file_pattern
        )
        self.pickled_dir = f"{self.tmp_dir}/pickled"
        self.sampling_samples_file = (
            f"{self.sampling_outsample_dir}/samples.txt"
        )
        self.clustering_dissimilarity_mat_file = (
            f"{self.tmp_dir}/dissmatrix_{self.sampling_nstructure}.mat"
        )

    def prepare_parse_args(self):
        self._argparser = argparse.ArgumentParser(
            argument_default=argparse.SUPPRESS
        )
        self.declare_main_args(self._argparser)
        self.declare_condition_args(self._argparser)
        self.declare_sampling_args(self._argparser)
        self.declare_pareto_args(self._argparser)
        self.declare_clustering_args(self._argparser)
        self.declare_visualization_args(self._argparser)

    def parse_args(self):
        self.prepare_parse_args()
        args = self._argparser.parse_args()

        return args

    def config_logging(self, args, config_yaml):
        if "log_file" in args:
            self.log_file = args.log_file
        elif "log_file" in config_yaml:
            self.log_file = config_yaml["log_file"]

        if "debug" in args:
            self.debug = args.debug
        elif "debug" in config_yaml:
            self.debug = config_yaml["debug"]

        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG if self.debug else logging.INFO,
        )

    def assign_config(self):
        args = self.parse_args()

        self.config_file = args.config_file
        config_yaml = self.parse_yaml(self.config_file)

        self.config_logging(args, config_yaml)

        # only fields can be assigned, except conditions
        dvar = typing.get_type_hints(self)

        #del dvar["_condition_dict"]
        allowed_keys = {
            key for key, value in dvar.items() if not key.startswith("_")
        }

        # Import config file
        # TODO : Sanity check on types
        for key, value in config_yaml.items():
            if type(value) is dict:
                if key in self._categories:
                    for ck, cv in value.items():
                        fk = f"{key}_{ck}"
                        if hasattr(self, fk):
                            self.__dict__[fk] = cv
                        else:
                            logging.warning(f"invalid configuration `{fk}`")
                elif key == "conditions":
                    for ck, cv in value.items():
                        aln = (
                            cv["alignement_file"]
                            if "alignement_file" in cv
                            else None
                        )
                        react = (
                            cv["reactivity_file"]
                            if "reactivity_file" in cv
                            else None
                        )
                        constr = (
                            cv["constr_file"] if "constr_file" in cv else None
                        )
                        cond = self.ConditionConfig(
                            name=ck,
                            alignement_file=aln,
                            reactivity_file=react,
                            constr_file=constr,
                        )
                        self._condition_dict[ck] = cond

                else:
                    logging.warning(f"invalid configuration item `{key}`")
            else:
                if hasattr(self, key):
                    self.__dict__[key] = value
                else:
                    logging.warning(f"invalid configuration item `{key}`")
        # print(self)
        # print(vars(args))
        # Import command line arguments
        self.__dict__.update(
            (key, value)
            for key, value in vars(args).items()
            if key in allowed_keys
        )

        if "defconditions" in args:

            conds_str = args.defconditions.split(",")

            for cs in conds_str:
                css = cs.split(":")
                assert(len(css) == 4)
                self._condition_dict[css[0]] = self.ConditionConfig(
                    name=css[0],
                    constr_file=None if css[1] == '' else css[1],
                    reactivity_file=None if css[2] == '' else css[2],
                    alignement_file=None if css[3] == '' else css[3],
                )

        if "activate_conditions" in args:
            actconds = args.activate_conditions
            self._condition_dict = {
                k: v for k, v in self._condition_dict.items() if k in actconds
            }
        
        self.sanity_check()

    def declare_main_args(self, parser):

        parser.add_argument(
            "--version",
            help="ipanemap version",
            action="version",
            version=f"IPANEMAP {version('wheel')}",
        )
        parser.add_argument(
            "-f",
            "--config",
            help="path to the config file",
            type=str,
            required=True,
            default=self.config_file,
            action="store",
            dest="config_file",
        )
        parser.add_argument(
            "--log",
            help="path to log file",
            type=str,
            required=False,
            action="store",
            dest="log_file",
        )
        parser.add_argument(
            "--tmp-dir",
            help="path to temporary directory",
            type=str,
            required=False,
            action="store",
            dest="tmp_dir",
        )
        parser.add_argument(
            "--out-dir",
            help="path to output directory",
            type=str,
            required=False,
            action="store",
            dest="tmp_dir",
        )

        parser.add_argument(
            "--debug",
            help="debug output",
            type=str,
            required=False,
            action="store",
            dest="log_file",
        )
        parser.add_argument(
            "-s" "--sequence",
            help="path to sequence file",
            type=str,
            required=False,
            action="store",
            dest="sequence_file",
        )
        parser.add_argument(
            "--dbn-pattern",
            help="file name pattern for dbn files",
            type=str,
            required=False,
            action="store",
            dest="format_dbn_pattern_file",
        )

        parser.add_argument(
            "--dbn-centroid-pattern",
            help="file name pattern for dbn files",
            type=str,
            required=False,
            action="store",
            dest="format_dbn_centroid_pattern_file",
        )

        parser.add_argument(
            "--dbn-seq-name",
            help="sequence name pattern in dbn file",
            type=str,
            required=False,
            action="store",
            dest="format_dbn_seq_name",
        )

    def declare_condition_args(self, parser):
        group = parser.add_argument_group("conditions")

        group.add_argument(
            "--cond-dir",
            help="define a dir where to find conditions",
            required=False,
            action="store",
            dest="cond_dir",
        )

        group.add_argument(
            "--def-conditions",
            help="Conditions separated by comma, with following format: "
            "`name:path/to/hard/constraints:path/to/reactivity:path/to/alignement`",
            required=False,
            action="store",
            dest="defconditions",
        )

        group.add_argument(
            "--conditions",
            help="Conditions separated by comma, if followed by colon, the"
            "following format is required : "
            "name:path/to/hard/constraints:path/to/reactivity:path/to/alignement",
            required=False,
            action="store",
            dest="activate_conditions",
        )

    def declare_sampling_args(self, parser):

        group = parser.add_argument_group("sampling")

        group.add_argument(
            "--nosampling",
            help="disable sampling",
            required=False,
            action="store_false",
            dest="sampling_enable",
        )

        group.add_argument(
            "--nstructure",
            help="number of structure to sample per conditions",
            type=int,
            required=False,
            action="store",
            dest="sampling_nstructure",
        )
        group.add_argument(
            "--temperature",
            help="RNAsubopt - rescale energy to a temperature",
            type=float,
            required=False,
            action="store",
            dest="sampling_temperature",
        )

        group.add_argument(
            "--slope",
            help="RNAsubopt - SHAPE slope 'm' parameter",
            type=float,
            required=False,
            action="store",
            dest="sampling_slope",
        )
        group.add_argument(
            "--intercept",
            help="RNAsubopt - SHAPE intercept 'b' parameter",
            type=float,
            required=False,
            action="store",
            dest="sampling_intercept",
        )

    def declare_pareto_args(self, parser):
        group = parser.add_argument_group("pareto")

        group.add_argument(
            "--percent",
            help="pareto percentage",
            type=float,
            required=False,
            action="store",
            dest="pareto_percent",
        )
        group.add_argument(
            "--zcutoff",
            help="pareto zcutoff",
            type=float,
            required=False,
            action="store",
            dest="pareto_zcutoff",
        )

    def declare_clustering_args(self, parser):
        group = parser.add_argument_group("clustering")

        group.add_argument(
            "--max-diam",
            help="min batch kmeans max diameter threshold",
            type=float,
            required=False,
            action="store",
            dest="clustering_max_diam",
        )
        group.add_argument(
            "--max-avg-diam",
            help="min batch kmeans max average threshold",
            type=float,
            required=False,
            action="store",
            dest="clustering_max_avg_diam",
        )

    def declare_visualization_args(self, parser):
        group = parser.add_argument_group("visualization")

        group.add_argument(
            "--nomodels",
            help="Do not output models",
            required=False,
            action="store_false",
            dest="visual_models",
        )

        group.add_argument(
            "--nocentroids",
            help="Do not output centroids",
            required=False,
            action="store_false",
            dest="visual_centroids",
        )

        group.add_argument(
            "--noprobing",
            help="Do not output probing",
            required=False,
            action="store_false",
            dest="visual_probing",
        )


# class StreamToLogger(object):
#    """
#    Fake file-like stream object that redirects writes to a logger instance.
#    """
#
#    def __init__(self, logger, level):
#        self.logger = logger
#        self.level = level
#        self.linebuf = ""
#
#    def write(self, buf):
#        for line in buf.rstrip().splitlines():
#            self.logger.log(self.level, line.rstrip())
#
#    def flush(self):
#        pass


def log_subprocess_output(pipe, name):
    for line in iter(pipe.readline, b""):  # b'\n'-separated lines
        logging.error(f"got line from {name}: {line}")


try:
    config = Config()
except ConfigError as e:
    print(e.args[0])
    exit(1)


if __name__ == "__main__":
    config.init_config()
    print(config)
