## Intro
Are you tired of not being able to publish files not created by CRAB using CRAB? Of course you are.

## NEW!!!
Old, but working instructions are below, but if you want to quickly publish files to an *arbitrary* dataset,
then do this:
1. Check out this repository
2. `cmsrel CMSSW_7_4_1_patch1; cd CMSSW_7_4_1_patch1/src`
3. `cmsenv; source /cvmfs/cms.cern.ch/crab3/crab.sh`
4. `. /cvmfs/cms.cern.ch/crab3/crab-env-bootstrap.sh >& /dev/null`
5. Inside of the `v2` folder, edit `config.py` with the appropriate parameters (denoted by "change this")
6. Do `python InsertFiles.py`
7. Check that the dataset was published properly by pasting the name into DAS.


## Setup
*  Check out this repository
*  `cmsrel CMSSW_7_4_1_patch1; cd CMSSW_7_4_1_patch1/src` or use your favorite release
*  `cmsenv; source /cvmfs/cms.cern.ch/crab3/crab.sh`
*  Edit filelist.txt to have one file to publish per line (each crab job publishes one file).
*  Note that `/hadoop/cms/store/user/namin/asdf` must be input as `/store/user/namin/asdf` as this is what xrootd expects.
*  Edit the `name` and `filelist` variables in `cfg.sh`
*  `crab submit cfg.sh`

## To do
* Change script so that we can publish arbitrary root files (non-EDM files)
