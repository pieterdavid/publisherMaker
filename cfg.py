from WMCore.Configuration import Configuration

name = 'publishtestC'
filelist="filelist.txt"

config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = name

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'pset.py'
config.JobType.inputFiles = ['filelist.txt']
config.JobType.outputFiles = ['output.root']
config.JobType.scriptExe = 'main.sh'

config.section_('Data')
config.Data.inputDataset = "/MinimumBias/Run2015B-PromptReco-v1/MINIAOD"
config.Data.publication = True
config.Data.publishDataName = name
njobs = len(open(filelist,"r").readlines())
config.Data.totalUnits = njobs
config.Data.unitsPerJob = 1
config.Data.splitting = 'FileBased'
config.Data.ignoreLocality = True

config.section_('User')

config.section_('Site')
config.Site.storageSite = 'T2_US_UCSD'
config.Site.whitelist = ['T2_US_Caltech','T2_US_Florida', 'T2_US_MIT', 'T2_US_Nebraska', 'T2_US_Purdue', 'T2_US_UCSD', 'T2_US_Vanderbilt', 'T2_US_Wisconsin']

config.section_('Debug')
config.Debug.oneEventMode = True
