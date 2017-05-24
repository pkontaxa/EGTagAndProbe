#!/bin/sh

from subprocess import call

command = "rfcp "
for i in range(1,1000):
    command = "rfcp /dpm/in2p3.fr/home/cms/trivcat/store/user/tstreble/TagAndProbeTrees/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/TagAndProbe_test2/170517_160631/0000/NTuple_" + str(i) + ".root ."
    print command
    call(command, shell=True)
for i in range(1000,1004):
    command = "rfcp /dpm/in2p3.fr/home/cms/trivcat/store/user/tstreble/TagAndProbeTrees/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/TagAndProbe_test2/170517_160631/0001/NTuple_" + str(i) + ".root ."
    print command
    call(command, shell=True)