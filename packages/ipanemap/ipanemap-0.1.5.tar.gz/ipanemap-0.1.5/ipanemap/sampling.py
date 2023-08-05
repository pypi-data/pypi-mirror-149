import subprocess
import logging
from . import file_functions as ff
from .progress import progress

NUM_HEADER_LINES = 2  ## TO REMOVe


def sampling_extra_args(
    slope,
    intercept,
    react_file=None,
    constr_file=None,
):
    command = ""
    if constr_file is not None:
        command += f" -C --enforceConstraint {constr_file}"

    if react_file is not None:
        command += (
            f" --shape {react_file}" f' --shapeMethod="Dm{slope}b{intercept}"'
        )

    return command


def subopt_sampling(
    nstructure,
    temperature,
    slope,
    intercept,
    sequence_file,
    condition_name,
    output_file,
    react_file=None,
    constr_file=None,
):
    progress.StartTask(f"Processing {condition_name} with RNAsubopt")
    cmd = (
        f"RNAsubopt -p {nstructure} -s -T {temperature}" f" -i {sequence_file}"
    )

    cmd += sampling_extra_args(slope, intercept, react_file, constr_file)

    # print(command)
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        shell=True,
    )
    if proc.stderr != "":
        logging.error(f"RNAsubopt: {proc.stderr}")
        progress.EndTask()
        raise RuntimeError("RNAsubopt failed")
    else:
        with (open(output_file, "w")) as out:
            out.write(proc.stdout)
    progress.EndTask()


def find_seq_in_align(sequence_file, align_file):
    nseq, seq = ff.get_first_fasta_seq(sequence_file)
    seq = seq.strip()
    idx = 0
    for name, aln in ff.fasta_iter(align_file):
        ugaln = aln.replace("-", "").strip()
        if ugaln != seq:
            idx += 1
        else:
            return idx, name, aln
    return None, None, None


# def gen_alifold_compat_struct(aligned_structs, aligned_seq):
#    for ist, struct in aligned_structs
#    for i
#    pass


def is_valid_bp(x, y):
    valid_bp_map = {
        "A": ["T", "U"],
        "C": ["G"],
        "T": ["A"],
        "U": ["A", "G"],
        "G": ["U", "C"],
        "W": ["W"],
        "S": ["S"],
        "K": ["K"],
        "N": ["A", "C", "G", "T", "U", "W", "S", "K", "N"],
    }

    return y in valid_bp_map[x]


def gen_ungapped_struct_from_seq(seq, struct):
    stack = []
    new_struct = list(struct)
    for i, pairing in enumerate(struct):
        if pairing == "(":
            stack.append(i)
        if pairing == ")":
            op = stack.pop()
            if seq[op] in ["_", "-"] or seq[i] in ["_", "-"]:
                new_struct[op] = "."
                new_struct[i] = "."
            else:
                if not is_valid_bp(seq[op], seq[i]):
                    new_struct[op] = "."
                    new_struct[i] = "."

    for i, nucl in enumerate(seq):
        if nucl in ["_", "-"]:
            new_struct[i] = "-"

    return "".join(new_struct).replace("-", "")


def gen_ungapped_structure_from_alifold(alifold_gapped_structures, refaln):
    lines = alifold_gapped_structures.splitlines()

    res = refaln.replace("_", "").replace("-", "") + "\n"

    # We don't use the consensus sequence, so we skip the first line.
    for struct in lines[1:]:
        sp = struct.split()
        ungapped_struct = gen_ungapped_struct_from_seq(refaln, sp[0].strip())
        res += ungapped_struct + "\n"
    return res


def alifold_sampling(
    nstructure,
    temperature,
    slope,
    intercept,
    sequence_file,
    condition_name,
    output_file,
    gapped_output_file=None,
    react_file=None,
    align_file=None,
    constr_file=None,
):
    progress.StartTask(f"Processing {condition_name} with RNAalifold")
    cmd = f"RNAalifold {align_file} -s {nstructure} -T {temperature}"

    refseqidx, refseqname, refseq = find_seq_in_align(
        sequence_file, align_file
    )

    if refseqidx is None:
        logging.error("RNAalifold: Reference sequence is not in alignement !")
        raise RuntimeError("RNAalifold failed")

    if react_file is not None:
        logging.warn(
            "Reactivity for alifold is not yet implemented and will"
            " be ignored."
        )

    # TODO add reactivity file here when implementing reactivity with alifold
    cmd += sampling_extra_args(slope, intercept, None, constr_file)

    # print(command)
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        shell=True,
    )
    if proc.returncode != 0:
        progress.EndTask()
        logging.error(f"RNAalifold: {proc.stderr}")
        raise RuntimeError("RNAalifold failed")
    else:
        ungapped_structs = gen_ungapped_structure_from_alifold(
            proc.stdout, refseq
        )
        with (open(output_file, "w")) as out:
            out.write(ungapped_structs)

        if gapped_output_file is not None:
            with (open(gapped_output_file, "w")) as gout:
                gout.write(proc.stdout)

    if proc.stderr != "":
        logging.info(f"RNAalifold: {proc.stderr}")

    progress.EndTask()
