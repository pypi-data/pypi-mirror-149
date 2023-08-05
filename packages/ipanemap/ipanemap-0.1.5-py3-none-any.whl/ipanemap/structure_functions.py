from . import file_functions as FF
from .conf import config
from . import sampling as SP
from .progress import progress

import os
import numpy as np
from collections import defaultdict, Counter

# Base Pairs from dot bracket Secondary structure


def BasePairsFromStruct(
    Struct,
):  # return dic={structure:[liste de pairs de base ],....}
    lista = []
    stack = []
    for i in range(len(Struct)):  # sequence length
        if Struct[i] == "(":  # Opening base pair
            stack.append(i)
        elif Struct[i] == ")":  # Closing base pair
            k = stack.pop()
            lista.append((k, i))
    return set(lista)


# Parse an RNAsubopt file to extract Base pairs
def GetBasePairsFromStructFile(
    faPath,
):  # return dic={structure:[liste de pairs de base ],....}
    # print faPath
    DicStruct = {}
    lines = FF.Parsefile(faPath)
    # print lines
    SeqLen = len(lines[1]) - 1
    # print SeqLen,"seq length"
    rawStructs = []
    for j in range(len(lines)):
        sec_str = lines[j].strip().split(" ")[0]
        rawStructs.append(sec_str)
        DicStruct[j] = BasePairsFromStruct(sec_str)

    progress.Print(
        "Loaded %s structures (%s distinct)"
        % (len(rawStructs), len(set(rawStructs)))
    )
    return len(lines), DicStruct


def OccurenceBasePairs(ListPairs, Threshold):
    return [
        (elem[0], elem[1], Counter(ListPairs)[elem])
        for elem in Counter(ListPairs)
        if Counter(ListPairs)[elem] >= Threshold
    ]


def fromPairsToStruct(rna, Pairs):
    structure = ["." for i in range(len(rna))]
    for (i, j) in Pairs:
        structure[i] = "("
        structure[j] = ")"
    return "".join(structure)


def DistanceTwoStructs(Struct1, Struct2):
    return len(Struct1.symmetric_difference(Struct2))


# return len(set(Struct1).intersection(set(Struct2)) )


def dd():
    return 0


def aa():
    return defaultdict(dd)


def DistanceStruct(StructFile, SVMLFullPath, numberofsruct, constrainte):
    Redondantestructure = defaultdict(aa)
    MatDist = defaultdict(aa)
    Redondantestructure1 = {}
    Dicnumberofsruct = {}

    for i, v in enumerate(constrainte):
        Dicnumberofsruct[v] = numberofsruct

    total_nstruct, DicStruct = GetBasePairsFromStructFile(StructFile)

    progress.StartTask("Dissimilarity Loop")
    for i in range(0, total_nstruct):
        for j in range(i + 1, total_nstruct):
            MatDist[i][j] = DistanceTwoStructs(DicStruct[i], DicStruct[j])
            MatDist[j][i] = MatDist[i][j]

            ####### Check for redundancy
            if MatDist[i][j] == 0:
                jconstraint = int(j / numberofsruct)
                if (
                    j not in Redondantestructure1
                    and int(i / numberofsruct) == jconstraint
                ):  # To be sure that the redundant  structure belongs to the same probing condition
                    Dicnumberofsruct[constrainte[jconstraint]] -= 1
                    Redondantestructure1[j] = jconstraint
    progress.EndTask()

    progress.StartTask("Export dissimilarity matrix")
    for elem in Redondantestructure1:
        jconstraint = Redondantestructure1[elem]
        StructureNumber = elem - jconstraint * numberofsruct
        Redondantestructure[constrainte[jconstraint]][
            StructureNumber
        ] = 1  # we mark redundant structures by value 1

    # store the distance matrix in the  SVMLFile
    if os.path.isfile(SVMLFullPath):
        os.remove(SVMLFullPath)  # To clean the previous version
    o = open(SVMLFullPath, "w")
    for i in range(len(MatDist)):
        o.write("%i\t" % (i + 1))
        for j in range(len(MatDist)):
            if i != j:
                o.write("%i:%.4f\t" % (j + 1, MatDist[i][j]))
        o.write("\n")
    o.close()
    progress.EndTask()

    progress.StartTask("Pickle all data")
    FF.PickleVariable(MatDist, "dissmatrix.pickle")
    FF.PickleVariable(
        list(Redondantestructure1.keys()), "redondante_structures.pickle"
    )
    FF.PickleVariable(Redondantestructure, "redondante_structures_id.pickle")
    FF.PickleVariable(Dicnumberofsruct, "nstructure_per_condition.pickle")
    progress.EndTask()
    return 0


def FromStructFiletoRNAEvalInput(StructFile, InputRNAeval, rna):
    lines = FF.Parsefile(StructFile)
    StructsToRNAEvalInput(lines[SP.NUM_HEADER_LINES :], InputRNAeval, rna)


def WriteDBNFile(filepath, description, sequence, structure):
    with open(filepath, "w") as dbn:
        dbn.write(
            ">{desc}\n{seq}\n{struct}".format(
                desc=description, seq=sequence, struct=structure
            )
        )


def StructsToRNAEvalInput(Structs, OutFile, rna):
    """generate intermediate file with sequence+strcuture , seq+strcture .... as the input format  to use RNAeval"""
    with open(OutFile, "w") as o:
        for i in range(len(Structs)):
            o.write("{seq}\n{struct}\n".format(seq=rna, struct=Structs[i]))


# StructFile contains the RNA sequence in the first line and list of corresponding structures by line
def EvalStructuresEnergies(StructFile, rna):
    # generate the rnaeval input file
    InputFile = os.path.join(config.tmp_dir, "InputRNAeval")
    FromStructFiletoRNAEvalInput(StructFile, InputFile, rna)
    return RunEval(InputFile)


def RunEval(InputFile):
    Energy = []
    # launch the RNaeval command
    energiesFile = os.path.join(config.tmp_dir, "energyvalues")
    os.system("RNAeval <" + InputFile + ">" + energiesFile)
    # Parse the RNAevaloutput to extract energy values
    lines = FF.Parsefile(energiesFile)
    for i in range(1, len(lines), 2):
        # i is the stucture number and 'lines[i].split(" ")[1][1:-2]' is  the  corresponding  energy value
        # print 'holla',(lines[i].split(" ")[1][1:-2])
        Energy.append(
            lines[i].split(" ", 1)[1][1:-2]
        )  # TODO ,1 is to get the first occurence of the space !!!
    return Energy


##Boltzmman energy   according to the formula B=exp^\frac{-e}{RT}
def BoltzmannFactor(Energy):
    T = 37 + 273.15
    R = 0.0019872370936902486
    val = np.exp(-float(Energy) / float(100.0 * R * T))
    return val


def Boltzmann_Calc(
    constraintes, StructfileDir, NumStructures, rna, Redondantestructure
):
    Energy = defaultdict(aa)
    Boltzman = defaultdict(aa)
    ConditionalBoltzman = defaultdict(aa)
    ZBolzman = defaultdict(aa)
    # Calculate structure energies in each condition sample
    for Condition in constraintes:

        # TODO: file management
        FileStructure = os.path.join(StructfileDir, Condition + ".dbn")
        Energy[Condition] = EvalStructuresEnergies(
            FileStructure, rna
        )  # list of energy values for the structures present in the Condition

    for Condition in constraintes:
        ListwithoutRedundnacy = []
        for i in range(NumStructures):
            Boltzman[Condition][i] = BoltzmannFactor(Energy[Condition][i])
            if (
                Redondantestructure[Condition][i] == 0
            ):  # if the structure is not redundant
                ListwithoutRedundnacy.append(Boltzman[Condition][i])

        # Calculate the normalization term as the sum over all Boltzmann probabilities for one copy of each structure
        ZBolzman[Condition] = sum(ListwithoutRedundnacy)  # Partition function

    # FF.PickleVariable(Boltzman, "Boltzman.pkl")
    listall = []
    for Condition in constraintes:  # to not count MFES
        lista = []
        for i in range(NumStructures):
            if (
                Redondantestructure[Condition][i] == 0
            ):  # a non redundnat structure
                lista.append(Boltzman[Condition][i] / ZBolzman[Condition])
            else:
                lista.append(
                    0.0
                )  # Redundant structures have a conditional Boltzmann value NULL
        listall += lista
        ConditionalBoltzman[Condition] = lista
        # print "Condition \t  ConditionalBoltzman", Condition, ConditionalBoltzman[Condition]
    FF.PickleVariable(Boltzman, "boltzman.pickle")
    FF.PickleVariable(ConditionalBoltzman, "conditional_boltzman.pickle")
    FF.PickleVariable(ZBolzman, "ZBolzman.pickle")

    return ConditionalBoltzman
