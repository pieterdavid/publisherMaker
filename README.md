## Intro
Are you tired of not being able to publish files not created by CRAB using CRAB? Of course you are.

## NEW!!!
Old, but working instructions are below, but if you want to quickly publish files to an *arbitrary* dataset,
then do this:
1. Check out this repository
2. `cmsrel CMSSW_7_4_1_patch1; cd CMSSW_7_4_1_patch1/src`
3. `cmsenv; source /cvmfs/cms.cern.ch/crab3/crab.sh`
4. `source  /cvmfs/cms.cern.ch/common/crab-setup.sh`
5. Inside of the `v2` folder, edit `config.py` and `InsertFiles.py` with the appropriate parameters (denoted by "change this" or similar)
6. Do `python InsertFiles.py`
7. Check that the dataset was published properly by pasting the name into DAS.


##### ATTENTION! 
Please make sure before you start you have a valid proxy with: `voms-proxy-init -voms cms`

## To do
* Change script so that we can publish arbitrary root files (non-EDM files)
