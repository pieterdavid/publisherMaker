
# dataset will become /[primary_ds]/[processed_ds]/[tier]

dataset_info = {
    'primary_ds'    : 'TopDMJets_scalar_tWChan_Mchi_1_Mphi_100_TuneCP5_13TeV_madgraphMLM_pythia8_RunIIFall17_MINIAODSIM', # change this 
        #!!! no minus "-" in primary_ds name change to "_", not longer than 99 characters 
    'processed_ds'  : 'nstefano-TopDMJets_scalar_tWChan_Mchi_1_Mphi_100_TuneCP5_13TeV_madgraphMLM_pythia8_RunIIFall17_MINIAODSIM-18ccc6f0af3851e1390ed52d244f3857', # change this !!! structure to be obeyed: username-primary_ds-md5sumInvention
#    'acquisition_era_name':'CRAB',                                                                                                                                                                                                                         
     'tier'          : 'USER',
    #'dataset_access_type' : 'VALID',                                                                                                                                                                                                                       
    #'datatype' : 'mc',                                                                                                                                                                                                                                     
    'group'         : 'CRAB3',
    'campaign_name' : 'Fall17', #dummy values, no need to change
    'application'   : 'Madgraph', #dummy values, no need to change
    'app_version'   : 'Mad_20_20_20',#dummy values, no need to change
}


# take the [/pnfs/desy.de/cms/tier2/store/...] dir and drop the /pnfs/desy.de/cms/tier2 part
# hard coded path /pnfs/desy.de/cms/tier2/ in InsertFiles, thus change as needed

common_lfn_prefix = '/store/user/nstefano/' # change this                                                                                                                                                                                                   

directory_path='TopDMJets_scalar_tWChan_Mchi_1_Mphi_100_TuneCP5_13TeV_madgraphMLM_pythia8_RunIIFall17_MINIAODSIM/201704_155333/0000/' # change this: must have at least main directory + two fake directories like crab is producing                        

filelist = ["TopDMJets_scalar_tWChan_Mchi-1_Mphi-100_TuneCP5_13TeV-madgraphMLM-pythia8-MINIAODSIM_100_EXO-RunIIFall17MiniAODv2-00053.root",
"TopDMJets_scalar_tWChan_Mchi-1_Mphi-100_TuneCP5_13TeV-madgraphMLM-pythia8-MINIAODSIM_10_EXO-RunIIFall17MiniAODv2-00053.root",
"TopDMJets_scalar_tWChan_Mchi-1_Mphi-100_TuneCP5_13TeV-madgraphMLM-pythia8-MINIAODSIM_11_EXO-RunIIFall17MiniAODv2-00053.root",
"TopDMJets_scalar_tWChan_Mchi-1_Mphi-100_TuneCP5_13TeV-madgraphMLM-pythia8-MINIAODSIM_12_EXO-RunIIFall17MiniAODv2-00053.root",
"TopDMJets_scalar_tWChan_Mchi-1_Mphi-100_TuneCP5_13TeV-madgraphMLM-pythia8-MINIAODSIM_99_EXO-RunIIFall17MiniAODv2-00053.root",
"TopDMJets_scalar_tWChan_Mchi-1_Mphi-100_TuneCP5_13TeV-madgraphMLM-pythia8-MINIAODSIM_9_EXO-RunIIFall17MiniAODv2-00053.root",
]# change this: must end with .root (just rename your files)                                                                                                                                                                                                



