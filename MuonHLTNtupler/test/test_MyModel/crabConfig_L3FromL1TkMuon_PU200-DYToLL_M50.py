from CRABClient.UserUtilities import config, getUsernameFromCRIC
from WMCore.Configuration import Configuration

#config = config()
config = Configuration()

config.section_('General')
config.General.requestName = 'PU200-DYToLL_M50_L3FromL1TkMuon_myModel_20220516'
config.General.workArea = 'crab_PhaseII_myModel_20220516'

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'HLT_Phase2_example_menu_Output.py'
config.JobType.maxMemoryMB = 4000
config.JobType.maxJobRuntimeMin = 2750
# config.JobType.inputFiles = ['L1TObjScaling.db']
# config.JobType.outputFiles = ['ntuple.root', 'DQMIO.root']

config.section_('Data')
config.Data.allowNonValidInputDataset = True
config.Data.inputDataset = '/DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/FEVT'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outLFNDirBase = '/store/user/sungwon/PhaseII_retry/My_model_20220516/PU200-DYToLL_M50'
config.Data.publication = False
# config.Data.useParent = True
# config.Data.ignoreLocality = True

config.section_('Site')
config.Site.storageSite = 'T3_KR_KNU'
# config.Site.whitelist = ['T2_CH_CERN','T2_FR_*']
    
