import os
import sys
from collections import defaultdict
from .conf import config
from . import conf
from . import file_functions as FF
from . import sampling as SP
from . import structure_functions as SF
from . import visualization_tools as VT
from . import clusters_trait as CT
from . import optimize_clustering as OC
from .progress import progress

FASTA_EXTENSION = "fa"
SHAPE_EXTENSION = "shape"
DBN_DESC_FORMAT = (
    "Centroid {idx}, Sequence: {seqname}, dG: {deltaG}"
    ", Condition: {conds}, Boltzman Probability: {boltzprob}"
)


def prepare_data():
    FF.check_deps_binaries()

    # Create folders
    FF.CreateFold(config.output_dir)
    FF.CreateFold(config.tmp_dir)
    FF.CreateFold(config.pickled_dir)
    FF.CreateFold(config.clustering_centroid_dir)  # TODO create dir base on
    # centroid pattern
    if config.sampling_enable:
        FF.CreateFold(config.sampling_outsample_dir)


def sampling(samples_path: str, rnaname: str, rnaseq: str):

    progress.StartTask(f"Processing RNA {rnaname} at {config.sequence_file}")

    # Specify  whether to generate new sample or use a previously  generated one
    if config.sampling_enable:
        progress.StartTask(
            f"Sampling {config.sampling_nstructure} structures for each condition"
        )

        for cond in config.conditions:
            output_file = os.path.join(
                config.sampling_outsample_dir, f"{cond.name}.dbn"
            )
            gapped_output_file = os.path.join(
                config.sampling_outsample_dir, f"{cond.name}_gapped.dbn"
            )
            if cond.use_alifold():
                SP.alifold_sampling(
                    config.sampling_nstructure,
                    config.sampling_temperature,
                    config.sampling_slope,
                    config.sampling_intercept,
                    config.sequence_file,
                    cond.name,
                    output_file,
                    gapped_output_file=gapped_output_file,
                    react_file=cond.reactivity_file,
                    align_file=cond.alignement_file,
                    constr_file=cond.constr_file,
                )
            else:
                SP.subopt_sampling(
                    config.sampling_nstructure,
                    config.sampling_temperature,
                    config.sampling_slope,
                    config.sampling_intercept,
                    config.sequence_file,
                    cond.name,
                    output_file,
                    react_file=cond.reactivity_file,
                    constr_file=cond.constr_file,
                )

        progress.EndTask()
    else:
        progress.Print("Using existing sample")

    progress.Print(
        "Probing conditions: {conds}".format(
            conds=[cond.name for cond in config.conditions]
        )
    )

    ## TODO Reduce alifold structure to the current sequence

    output_samples = []
    for cond in config.conditions:
        output_samples += os.path.join(
            config.sampling_outsample_dir, cond.name
        )
    # Create a global file that contains structures sampled from the list of Probing conditions
    FF.MergeFiles(
        config.sampling_outsample_dir,
        samples_path,
        [f"{cond.name}.dbn" for cond in config.conditions],
        SP.NUM_HEADER_LINES,
    )


def main():

    # ******************************** Generate sample

    try:
        prepare_data()
        rnaname, rnaseq = FF.get_first_fasta_seq(config.sequence_file)

        probing_conditions_names = [cond.name for cond in config.conditions]
        sampling(config.sampling_samples_file, rnaname, rnaseq)

        # Create a distance matrix file
        progress.StartTask("Computing dissimilarity matrix")
        # Calculate distance and identify redundant structures within the same condition
        SF.DistanceStruct(
            config.sampling_samples_file,
            config.clustering_dissimilarity_mat_file,
            config.sampling_nstructure,
            probing_conditions_names,
        )
        progress.EndTask()

        # ################################ Calculate Conditional Boltzmann probabilities
        # for each condition, calculate Z over all non redundant structures
        # and return a conditional Boltzmann probability for all structures
        # with null value for redundant ones.
        progress.StartTask("Computing Boltzmann probabilities")
        BoltzmannFactor = defaultdict(lambda: defaultdict())
        ConditionalBoltzmannProbability = defaultdict(lambda: defaultdict())
        # Zprobabilities = defaultdict(lambda: defaultdict())
        Redondantestructure = FF.UnpickleVariable(
            "redondante_structures_id.pickle"
        )
        ConditionalBoltzmannProbability = SF.Boltzmann_Calc(
            probing_conditions_names,
            config.sampling_outsample_dir,
            config.sampling_nstructure,
            rnaseq,
            Redondantestructure,
        )
        progress.EndTask()

        # ################################ Clustering of structures based on their base pair distance
        progress.StartTask("Iterative clustering")
        # Load the pickled dissimilarity matrix
        DM = FF.UnpickleVariable("dissmatrix.pickle")
        # Get the list of redundant structures
        Redundant = []
        Redundant = FF.UnpickleVariable("redondante_structures.pickle")
        BoltzmannFactor = FF.UnpickleVariable("boltzman.pickle")
        method = "MiniBatchKMean"
        Clusters, CentroidStructure = OC.DefineNumberCluster(
            config.clustering_dissimilarity_mat_file,
            Redundant,
            method,
            DM,
            BoltzmannFactor,
            probing_conditions_names,
            rnaseq,
            config.sampling_nstructure,
            config.sampling_samples_file,
        )
        # Get Clusters from Pickled data
        # Clusters = FF.UnpickleVariable("Clusters" + method + ".pkl")
        progress.EndTask()

        progress.StartTask("Analyzing clusters/Drawing centroids")

        centroidPath = os.path.join(config.output_dir, "centroids.dbn")
        SF.StructsToRNAEvalInput(CentroidStructure, centroidPath, rnaseq)
        Centroids_Energies = SF.RunEval(centroidPath)

        CT.ClustersDistributions(
            Clusters,
            os.path.join(config.output_dir, "clusters_details"),
            probing_conditions_names,
            config.sampling_nstructure,
        )

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!Election of the best structures starting!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Calculate cumulated  Boltzmaan Energy for each cluster

        CumulBE = {}
        CardinalConditions = {}

        CumulBE = CT.CumulatedConditionalBoltzmannbyCluster(
            Clusters,
            ConditionalBoltzmannProbability,
            config.sampling_nstructure,
            probing_conditions_names,
        )
        # epsilon= 1/(n+1)
        Epsilon = 1.0 / float(len(Clusters) + 1)
        CardinalConditions = CT.GetCardinalConditions(
            Clusters,
            ConditionalBoltzmannProbability,
            probing_conditions_names,
            config.sampling_nstructure,
            Epsilon,
        )

        ImageFolder = os.path.join(config.output_dir, "img")
        if not os.path.isdir(ImageFolder):
            os.mkdir(ImageFolder)

        # Get first condition with shape data
        reactivity_data_file = None
        if config.visual_probing:
            for cond in config.conditions:
                if cond.reactivity_file is not None:
                    reactivity_data_file = cond.reactivity_file
                    break

        for index in CentroidStructure.keys():
            progress.Print(
                "%s\t%s\t%s\t%s\t%s"
                % (
                    index + 1,
                    CentroidStructure[index],
                    Centroids_Energies[index],
                    CardinalConditions[index],
                    CumulBE[index],
                )
            )
            if config.format_dbn_centroid_file_pattern is not None:
                fp = config.format_dbn_centroid_file_pattern.format(
                    idx=index + 1,
                    outputfolder=config.output_dir,
                    seqname=rnaname,
                )
                desc = config.format_dbn_seq_name.format(
                    conditions="".join(
                        [cond.name + "_" for cond in config.conditions][:-1]
                    ),
                    centroid=index,
                    seqname=rnaname,
                    delta_g=Centroids_Energies[index],
                    condition=config.conditions[CardinalConditions[index]- 1].name,
                    boltz_prob=CumulBE[index],
                )

                SF.WriteDBNFile(
                    filepath=fp,
                    description=desc,
                    sequence=rnaseq,
                    structure=CentroidStructure[index],
                )

            if config.visual_centroids:
                VT.drawStructure(
                    rnaseq,
                    CentroidStructure[index],
                    config.conditions[0].reactivity_file,
                    os.path.join(ImageFolder, "Centroid-{index + 1}.svg"),
                    config.output_dir,
                )

        progress.Print("Pareto optimal structure(s):")

        Dict = (
            {}
        )  # a dictionary that contains the three variables characterizing clusters (Criteria of optimization)
        for ClusterNumber in Clusters:
            Dict[ClusterNumber] = [
                CardinalConditions[ClusterNumber],
                CumulBE[ClusterNumber],
            ]  # only Two criterions are considered

        ListOptimalClusters = CT.Pareto(Dict)
        progress.Print(
            "Structure\tdG\t#SupportingConditions\tBoltzmannProbability",
            output=True,
        )
        i = 0
        for index in ListOptimalClusters:
            progress.Print(
                "%s\t%s\t%s\t%s"
                % (
                    CentroidStructure[index],
                    Centroids_Energies[index],
                    CardinalConditions[index],
                    CumulBE[index],
                ),
                output=True,
            )
            if config.format_dbn_file_pattern is not None:
                fp = config.format_dbn_file_pattern.format(
                    idx=i + 1, outputfolder=config.output_dir, seqname=rnaname
                )
                desc = config.format_dbn_seq_name.format(
                    conditions="".join(
                        [cond.name + "_" for cond in config.conditions][:-1]
                    ),
                    centroid=index,
                    seqname=rnaname,
                    delta_g=Centroids_Energies[index],
                    condition=config.conditions[CardinalConditions[index] - 1].name,
                    boltz_prob=CumulBE[index],
                )
                SF.WriteDBNFile(
                    filepath=fp,
                    description=desc,
                    sequence=rnaseq,
                    structure=CentroidStructure[index],
                )
            if config.visual_models:
                VT.drawStructure(
                    rnaseq,
                    CentroidStructure[index],
                    reactivity_data_file,
                    os.path.join(ImageFolder, "Optimal-%s.svg" % (i + 1)),
                    config.output_dir,
                )
            i += 1
        progress.EndTask()

    except FF.IPANEMAPError as e:
        progress.Print("Error: %s" % (e))
        progress.Flush()


def main_wrapper():
    config.init_config()
    main()


if __name__ == "__main__":
    main_wrapper()
