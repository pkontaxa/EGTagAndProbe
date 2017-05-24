# TauTagAndProbe
Set of tools to evaluate tau trigger performance on T&amp;P

### Install instructions
```
cmsrel CMSSW_9_1_0_pre3
cd CMSSW_9_1_0_pre3/src
cmsenv
git clone https://github.com/tstreble/EGTagAndProbe
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
cd CMSSW_9_1_0_pre3/src/EGTagAndProbe/EGTagAndProbe/test
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init -voms cms
crab submit -c crab3_config.py
```

### Producing turn-on plots
Create configuration file base on test/fitter/run/stage2_turnOnEG_fitter_test.par
```
cd CMSSW_9_1_0_pre3/src/EGTagAndProbe/EGTagAndProbe/test/fitter
make clean; make
./fit.exe run/stage2_turnOnEG_fitter_test.par
```
Create plotting script based on test/fitter/results/plot_EG_example.py
```
cd results
python plot_EG_example.py
```
