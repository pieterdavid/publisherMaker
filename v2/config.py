
# dataset will become /[primary_ds]/[processed_ds]/[tier]
dataset_info = {
    'primary_ds'    : 'Nick', # change this
    'processed_ds'  : 'InjectionTest-v4', # change this
    'tier'          : 'RAW',
    'group'         : 'GEN',
    'campaign_name' : 'Spring2014',
    'application'   : 'Madgraph',
    'app_version'   : 'Mad_20_20_20',
}

# take the [/hadoop/cms/store/...] dir and drop the /hadoop/cms/ part
common_lfn_prefix = '/store/user/namin/' # change this

directory_path='foo/test/' # change this: must have at least two directories

filelist = ["ntuple1.root","ntuple2.root"] # change this: must end with .root (just rename your files)


