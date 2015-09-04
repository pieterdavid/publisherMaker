## Intro
Are you tired of not being able to publish files not created by CRAB using CRAB? Of course you are.

## Setup
0. Check out this repository
1. `cmsrel CMSSW_7_4_1_patch1; cd CMSSW_7_4_1_patch1/src` or use your favorite release
2. `cmsenv; source /cvmfs/cms.cern.ch/crab3/crab.sh`
3. Edit filelist.txt to have one file per line (each crab job publishes one file)
4. Edit the `name` and `filelist` variables in `cfg.sh`
5. `crab submit cfg.sh`

## To do
* Change script so that we can publish arbitrary root files (non-EDM files)
