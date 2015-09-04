from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True

import os
index = 1
baseName = 'publishtestC'
filelist="filelist.txt"
# if it finds crab_UserScriptTest1/, it will use crab_UserScriptTest2/ automatically!
while os.path.isdir("crab_%s%s" % (baseName, index)):
    index += 1
config.General.requestName = baseName + str(index)

print config.General.requestName

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'pset.py'
config.JobType.inputFiles = ['filelist.txt']
config.JobType.outputFiles = ['output.root']
config.JobType.scriptExe = 'main.sh'

config.section_('Data')
config.Data.inputDataset = "/MinimumBias/Run2015B-PromptReco-v1/MINIAOD"
config.Data.publication = True
config.Data.publishDataName = 'publishtest4'
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
