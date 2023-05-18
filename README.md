# MuonHLT Ntupler

## Setup (13_0_6)
```
cmsrel CMSSW_13_0_6
cd CMSSW_13_0_6/src
cmsenv
git cms-init
```


## Seed classifier
```
git cms-addpkg HLTrigger/Configuration
git clone -b Phase2_won https://github.com/wonpoint4/MuonHLTSeedMVAClassifier.git HLTrigger/MuonHLTSeedMVAClassifier
```

## Ntupler
```
git clone -b Phase2_won https://github.com/wonpoint4/MuonHLTTool.git MuonHLTTool
scram b -j 8
```

## Get Phase-2 Menu
```
cmsDriver.py Phase2 -s HLT:75e33 --processName=MYHLT \
--conditions auto:phase2_realistic_T21 \
--geometry Extended2026D88 \
--era Phase2C17I13M9 \
--eventcontent FEVTDEBUGHLT \
--customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000 \
--filein=/store/mc/Phase2Fall22DRMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30000/0a5c8677-10c8-4cfe-a084-d45689504151.root \
-n 100 --nThreads 1 --no_exec
```


## Modify, and run the Menu
```
# comment-out FEVTDEBUGHLToutput
# Add Timing, Ntupler, DQM, EDMOutput parts

cmsRun Phase2_HLT.py
```



