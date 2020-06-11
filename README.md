# EGTagAndProbe
Set of tools to evaluate L1EG trigger performance on T&amp;P

Based on TauTagAndProbe package developed by L. Cadamuro & O. Davignon

### Install instructions
```
cmsrel CMSSW_11_0_2
cd CMSSW_11_0_2/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline l1t-integration-CMSSW_11_0_2
git cms-merge-topic -u cms-l1t-offline:l1t-integration-v103.2
git cms-addpkg L1Trigger/L1TCommon
git cms-addpkg L1Trigger/L1TMuon
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TMuon.git L1Trigger/L1TMuon/data
git cms-addpkg L1Trigger/L1TCalorimeter
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TCalorimeter.git L1Trigger/L1TCalorimeter/data

scram b -j 8

git clone https://github.com/pkontaxa/EGTagAndProbe

scram b -j4
```

### Producing TagAndProbe ntuples with unpacked L1EG (no re-emulation)
Set flag isMC and isMINIAOD according to sample in test/test.py
HLT path used specified in python/MCAnalysis_cff.py (MC) or python/tagAndProbe_cff.py (data)
Launch test.py


### Producing TagAndProbe ntuples with emulated L1EG
Under development


### Submit job on the Grid
Modify crab3_config.py: change requestName, inputDataSet, outLFNDirBase, outputDatasetTag, storageSite
```
cd CMSSW_11_0_2/src/EGTagAndProbe/EGTagAndProbe/test
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init -voms cms
crab submit -c crab3_config.py
```

### Producing turn-on plots
Create configuration file base on test/fitter/run/stage2_turnOnEG_fitter_test.par
```
cd CMSSW_11_0_2/src/EGTagAndProbe/EGTagAndProbe/test/fitter
make clean; make
./fit.exe run/stage2_turnOnEG_fitter_test.par
```
Create plotting script based on test/fitter/results/plot_EG_example.py
```
cd results
python plot_EG_example.py
```
