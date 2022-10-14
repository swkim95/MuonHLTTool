
from CRABClient.UserUtilities import config, getUsernameFromCRIC
from WMCore.Configuration import Configuration

config = Configuration()
# config = config()

config.section_('General')
config.General.requestName = 'PU200-DYToLL_M-50_L3FromL1TkMuon_seedNtupler_20221010'
config.General.workArea = 'crab_PhaseII_CMSSW_12_4_9_20221010'

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'Phase2_HLT_D88Geo_DYToLL_seedNtupler.py'
config.JobType.maxMemoryMB = 4000
config.JobType.maxJobRuntimeMin = 2750
# config.JobType.inputFiles = ['L1TObjScaling.db']
# config.JobType.outputFiles = ['ntuple.root', 'DQMIO.root']

config.section_('Data')
config.Data.allowNonValidInputDataset = True
config.Data.inputDataset = '/DYToLL_M-50_TuneCP5_14TeV-pythia8/PhaseIISpring22DRMiniAOD-PU200_BSzpz35_123X_mcRun4_realistic_v11_ext1-v1/GEN-SIM-RECO'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outLFNDirBase = '/store/user/sungwon/PhaseII_CMSSW_12_4_9/20221010/D88Geo_DYToLL_seedNtuple_for_Binary_train'
config.Data.publication = False
# config.Data.useParent = True
# config.Data.ignoreLocality = True

config.section_('Site')
config.Site.storageSite = 'T3_KR_KNU'
# config.Site.whitelist = ['T2_CH_CERN','T2_FR_*']
