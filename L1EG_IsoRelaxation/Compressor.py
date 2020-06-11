#!/usr/bin/env python
'''                                                                                                                                                                                                         DESCRIPTION:

 This script compresses Et, nTT and iEta variables.
 To be used with the custom L1 EG Tag & Probe package.

 USAGE:
 ./Compressor.py -f <input file>
 
 LAST USED:
 ./Compressor.py -f NTuple_366.root
'''
#=============================
# Imports
#=============================
import ROOT
import array
import math
import operator
import sys
import copy
import os
import re
from optparse import OptionParser
from ROOT import *

#=============================
# LUTs Files For Compression
#=============================
compressedIetaFile  = "./LUTs/egCompressEtaLUT_4bit_v4.txt"
compressedEFile     = "./LUTs/egCompressELUT_4bit_v4.txt"
compressedShapeFile = "./LUTs/egCompressShapesLUT_calibr_4bit_v4.txt"
calibrationLUT      = "./LUTs/FinalLUT.txt"

#=======================================
# TTree Name
#=======================================
treeName = "Ntuplizer/TagAndProbe"

#=======================================
# Output File
#=======================================
outputFileName = "IsoTreeOut.root"

#================================================================================================
# Function Definition
#================================================================================================
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def Verbose(msg, printHeader=True, verbose=False):
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return

def readCalibration(lutFileName):

    with open(lutFileName) as f:

        H3 = ROOT.TH3F("H3", "", 16, -0.5, 15.5, 16, -0.5 , 15.5, 16, -0.5, 15.5)
	for line in f:
	    word = []
	    word = line.replace('=',' ').replace(',',' ').split()
	    if len(word) != 13:
	        continue
            H3.SetBinContent(int(word[4]), int(word[6]), int(word[8]), float(word[1]))
    return H3


def readLUT(lutFileName):
    lut = {}
    with open(lutFileName, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[0]=='#': continue
            tokens = line.split()
            if len(tokens)!=2: continue
            lut[int(tokens[0])] = int(tokens[1])
    return lut


def sortShapes(shapeHisto):
    '''
    Description:
    
    
    '''
    numbers = {}
    nbins = shapeHisto.GetNbinsX()
    print "Number of Bins = ", nbins
    
    for b in range(1,nbins+1):
        numbers[b-1] = shapeHisto.GetBinContent(b)
        print "b=", b, " b-1=", b-1, " Bin Content=", numbers[b-1]
    #
    sortedShapes = sorted(numbers.iteritems(), key=operator.itemgetter(1))
    print " "
    print "Sorted Shapes ="
    print sortedShapes
    #
    zeros = []
    nonzeros = []
    for shape,n in sortedShapes:
        if n==0:
            zeros.append((shape,n))
        else:
            nonzeros.append((shape,n))
    #
    nonzeros.reverse()
    sortedShapes = nonzeros
    sortedShapes.extend(zeros)
    #
    lut = {}
    sortedShape = 0
    for shape,n in sortedShapes:
        lut[shape] = sortedShape
        sortedShape += 1
    #
    with open("compressedSortedShapes.txt", 'w') as f:
        for shape in range(0,128):
            sortedShape = lut[shape]
            print >>f, shape, sortedShape
    return lut


#===============
# Main
#===============
def main(opts):
    
    # Read LUT Compression Mapping for iEta, E and Shape
    compressedIeta  = readLUT(compressedIetaFile)
    compressedE     = readLUT(compressedEFile)
    compressedShape = readLUT(compressedShapeFile)
    
    # Read the calibration
    Calibration = readCalibration(calibrationLUT)
    
    # Read input trees 
    f = ROOT.TFile.Open(opts.inFile)
    t = f.Get(treeName)
    nEntries = t.GetEntriesFast()
    
    data = {"RawEt"                 :array.array('i', [0]  ),
            "iEta"                  :array.array('i', [0]  ),
            "nTT"                   :array.array('i', [0]  ),
            "rho"                   :array.array('d', [0.] ),
            "iso"                   :array.array('i', [0]  ),
            "nVtx"                  :array.array('f', [0.] ),
            "offlineEta"            :array.array('d', [0.] ),
            "offlineEt"             :array.array('d', [0.] ),
            "shape"                 :array.array('i', [0]  ),
            "compressedieta"        :array.array('i', [0]  ),
            "compressedE"           :array.array('i', [0]  ),
            "compressedshape"       :array.array('i', [0]  ),
            "compressedsortedshape" :array.array('i', [0]  ),
            "passShapeVeto"         :array.array('i', [0]  ),
            "CalibratedE"           :array.array('d', [0]  ),
            "Run2EleId"             :array.array('i', [0]  ),
            "UnpackedE"             :array.array('i', [0]  )
            }
    
    # Loop over all the entries
    for i in xrange(nEntries):
        
        t.GetEntry(i)
        
        # Consider only events with positive Raw ET values
        if (t.l1tEmuRawEt <= 0):
            continue
        
        data["RawEt"][0]      = int(t.l1tEmuRawEt)        # t.rawEt_EBEE_S2
        data["iEta"][0]       = int(t.l1tEmuTowerIEta)    # t.iEta_EBEE_S2
        data["nTT"][0]        = int(t.l1tEmuNTT)          # t.nTT_EBEE_S2
        data["iso"][0]        = int(t.l1tEmuIsoEt)        # t.iso_EBEE_S2
        data["nVtx"][0]       = int(t.Nvtx)               # t.n_vtx  
        data["offlineEta"][0] = t.hltEta                  # t.sc_eta_EBEE_S2
        data["offlineEt"][0]  = t.hltPt                   # t.sc_et_EBEE_S2 
        data["shape"][0]      = int(t.shape)              # t.shape_EBEE_S2
        
    # Filling compressed shape histo
    print "First pass: reading tree to build compressed shape histo"
    shapeHisto = ROOT.TH1F("compressedShapeHisto", "compressedShapeHisto", 128, -0.5, 127.5)
    
    # Sort compressed shapes and write in file
    compressedSortedShape = sortShapes(shapeHisto)
    
    print "Compressed Sorted Shape:"
    print compressedSortedShape
    print ""
    print "==================================="

    ## Reading and filling tree with compressed and sorted values
    outFile = ROOT.TFile.Open(outputFileName, "RECREATE")
    outTree = ROOT.TTree("TagAndProbe", "TagAndProbe")
    
    for name, a in data.items():
        outTree.Branch(name, a, "{0}/{1}".format(name, a.typecode.upper()))
    shapeHisto.Write()
    
    print "Second pass: reading tree for filling output tree"
    for i in xrange(nEntries):
        t.GetEntry(i)
        
        # Consider only events with positive Raw ET values
        if (t.l1tEmuRawEt <= 0):
            continue
        
        data["RawEt"][0]                 = int(t.l1tEmuRawEt)        # t.rawEt_EBEE_S2
        data["iEta"][0]                  = int(t.l1tEmuTowerIEta)    # t.iEta_EBEE_S2
        data["nTT"][0]                   = int(t.l1tEmuNTT)          # t.nTT_EBEE_S2
        data["iso"][0]                   = int(t.l1tEmuIsoEt)        # t.iso_EBEE_S2
        data["nVtx"][0]                  = int(t.Nvtx)               # t.n_vtx  
        data["offlineEta"][0]            = t.hltEta                  # t.sc_eta_EBEE_S2
        data["offlineEt"][0]             = t.hltPt                   # t.sc_et_EBEE_S2 
        data["shape"][0]                 = int(t.shape)              # t.shape_EBEE_S2
        data["compressedieta"][0]        = int(math.copysign(compressedIeta[abs(data["iEta"][0])], data["iEta"][0])) 
        data["compressedE"][0]           = compressedE[min(data["RawEt"][0],255)]
        data["compressedshape"][0]       = compressedShape[data["shape"][0]]
        data["compressedsortedshape"][0] = compressedSortedShape[data["compressedshape"][0]]
        
        tmp = Calibration.GetBinContent(abs(data["compressedieta"][0]), data["compressedE"][0], data["compressedshape"][0])
        if tmp > 511:
            data["passShapeVeto"][0] = 1
        else:
            data["passShapeVeto"][0] = 0
            
        data["CalibratedE"][0] = int(((tmp - data["passShapeVeto"][0]*512)/256.)*data["RawEt"][0]/2)
        outTree.Fill()

    outFile.cd()
    outTree.Write()
    Calibration.Write()
    outFile.Close()
    f.Close()



#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''
    
    # Default Settings
    VERBOSE   = False
    BATCHMODE = True
    
    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-f", "--input", dest="inFile", action="store", help="Path to the input file")
    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)
    
    (opts, parseArgs) = parser.parse_args()
    
    # Require at least one argument (path to input file)
    if len(sys.argv) < 1:
        parser.print_help()
        sys.exit(1)
        
    if opts.inFile == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)
        
    # Call the main function
    main(opts)
