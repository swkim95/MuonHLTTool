
from CRABClient.UserUtilities import config, getUsernameFromCRIC
from WMCore.Configuration import Configuration

config = Configuration()
# config = config()

config.section_('General')
config.General.requestName = 'PU200-MuonGun_L3FromL1TkMuon_20220926'
config.General.workArea = 'crab_PhaseII_CMSSW_12_4_9_20220926'

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'Phase2_HLT_D88Geo_MuonGun_ntupler.py'
config.JobType.maxMemoryMB = 4000
config.JobType.maxJobRuntimeMin = 2750
# config.JobType.inputFiles = ['L1TObjScaling.db']
# config.JobType.outputFiles = ['ntuple.root', 'DQMIO.root']

config.section_('Data')
config.Data.allowNonValidInputDataset = True
config.Data.inputDataset = '/DoubleMuon_FlatPt-1To100-gun/PhaseIISpring22DRMiniAOD-PU200_123X_mcRun4_realistic_v11-v1/GEN-SIM-DIGI-RAW-MINIAOD'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.outLFNDirBase = '/store/user/sungwon/PhaseII_CMSSW_12_4_9/20220926/D88Geo_MuonGun'
config.Data.publication = False
# config.Data.useParent = True
# config.Data.ignoreLocality = True

config.section_('Site')
config.Site.storageSite = 'T3_KR_KNU'
# config.Site.whitelist = ['T2_CH_CERN','T2_FR_*']
