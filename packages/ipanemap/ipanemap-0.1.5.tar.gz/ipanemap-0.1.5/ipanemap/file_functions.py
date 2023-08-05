from .progress import progress
from .conf import config
import logging
from itertools import groupby
import os
import pickle
import platform
import subprocess
from itertools import islice
from os.path import isfile, join
import re


class BinaryNotFoundError(FileNotFoundError):
    def __init__(self, binary):
        self.binary = binary
        self.message = f"`{binary}` not found in current path, please install and add to path"
        super().__init__(self.message)


# create folder if it doesn't exist
def CreateFold(dir):
    try:
        os.stat(dir)
    except FileNotFoundError:
        os.mkdir(dir)


def check_deps_binaries():

    if check_deps_binary("RNAsubopt") != 0:
        raise BinaryNotFoundError("RNAsubopt")
    if check_deps_binary("RNAeval") != 0:
        raise BinaryNotFoundError("RNAeval")

    if check_deps_binary("java") != 0:
        logging.warning(
            "java not found in current path." " VARNA output will be disabled"
        )
        config.visual_models = False
        config.visual_centroids = False
        config.visual_probing = False


def check_deps_binary(binary: str):
    which = "where" if platform.system() == "Windows" else "which"
    ret = subprocess.call(
        [which, binary], stdout=open(os.devnull), stderr=open(os.devnull)
    )
    return ret


# get all files with a specific extension from a specific path
def GetListFile(PathFile, FileExtension):
    return [
        os.path.splitext(f)[0]
        for f in os.listdir(PathFile)
        if isfile(join(PathFile, f))
        and os.path.splitext(f)[1] == "." + FileExtension
    ]


def dbn_iter(dbn_file):
    with open(dbn_file, "r") as dh:
        faiter = (x[1] for x in groupby(dh, lambda line: line[0] == ">"))
    for header in faiter:
        # drop the ">"
        headerStr = header.__next__()[1:].strip()

        # join all sequence lines to one.
        seq = ""
        cur_struct = ""
        structs = []
        is_inside_seq = True
        for s in next(faiter):
            if is_inside_seq:
                if re.match(".*[A-z-]+", s) is not None:
                    seq = "".join(s.strip())
                else:
                    is_inside_seq = False
            else:
                cur_struct = cur_struct.join(s.strip())
                if len(cur_struct) > len(seq):
                    raise RuntimeError(
                        f"Invalid DBN file len(struct)"
                        f"({len(cur_struct)}) > seq ({len(seq)})"
                    )
                if len(cur_struct) == len(seq):
                    structs.append(cur_struct)
                    cur_struct = ""

        yield (headerStr, seq, structs)


# From https://www.biostars.org/p/710/
def fasta_iter(fasta_name):
    """
    modified from Brent Pedersen
    Correct Way To Parse A Fasta File In Python
    given a fasta file. yield tuples of header, sequence
    """
    "first open the file outside "
    with open(fasta_name, "r") as fh:
        # ditch the boolean (x[0]) and just keep the header or sequence since
        # we know they alternate.
        faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))

        for header in faiter:
            # drop the ">"
            headerStr = header.__next__()[1:].strip()

            # join all sequence lines to one.
            seq = "".join(s.strip() for s in faiter.__next__())

            yield (headerStr, seq)


def get_first_fasta_seq(path):

    sqiter = fasta_iter(path)
    return next(sqiter)


# Parse a file by returning lines it contains
def Parsefile(Path):
    with open(Path, "r") as fileIn:
        lines = [li.strip() for li in fileIn.readlines()]
        return lines
    return None


def GetlinefromFile(Path, Linenumber):
    return Parsefile(Path)[Linenumber]


def MergeFiles(Path, output, fileslist, Startline):
    progress.Print("Merging samples for conditions %s" % (fileslist))
    with open(output, "w") as outfile:
        for fname in [Path + "/" + i for i in fileslist]:
            with open(fname) as infile:
                for line in islice(infile, Startline, None):
                    outfile.write(line)
    return output


def MergespecificsFiles(Path, output, fileslist, Startline):
    with open(output, "w") as outfile:
        for fname in [Path + "/" + i for i in fileslist]:
            with open(fname) as infile:
                for line in islice(infile, Startline, None):
                    outfile.write(line)
    return output


def parseReactivityfile(fileinput):
    Reactvities = []
    lines = Parsefile(fileinput)
    for it in range(len(lines)):
        data = lines[it].split()
        if len(data) > 1:
            Reactvities.append(data[1])
    return Reactvities


def PickleVariable(variable, file):
    with open(os.path.join(config.pickled_dir, file), "wb") as fileOut:
        pickle.dump(
            variable, fileOut, -1
        )  # -1 specifies highest binary protocol


def UnpickleVariable(file):
    with open(os.path.join(config.pickled_dir, file), "rb") as fileIn:
        unpickled = pickle.load(fileIn)
    return unpickled


class IPANEMAPError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
