from CRABClient.UserUtilities import config, getUsernameFromCRIC
import sys, os
import gc
import datetime
now = datetime.datetime.now()
date = now.strftime('%Y%m%d')

submitVersion = 'PhaseII'
mainOutputDir = '/store/user/%s/%s/%s' % (getUsernameFromCRIC(), submitVersion, date)



# 'MultiCRAB' part
if __name__ == '__main__':
    # from CRABAPI.RawCommand import crabCommand

    crab_cfg = """
from CRABClient.UserUtilities import config, getUsernameFromCRIC

config = config()

config.General.requestName = '%(datasetTag)s_%(name)s_%(date)s'
config.General.workArea = 'crab_%(submitVersion)s_%(date)s'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '%(menu)s'
config.JobType.maxMemoryMB = 4000
config.JobType.maxJobRuntimeMin = 2750
# config.JobType.inputFiles = ['L1TObjScaling.db']
# config.JobType.outputFiles = ['ntuple.root', 'DQMIO.root']

config.Data.allowNonValidInputDataset = True
config.Data.inputDataset = '%(datasetPath)s'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outLFNDirBase = '%(mainOutputDir)s'
config.Data.publication = False
# config.Data.useParent = True
# config.Data.ignoreLocality = True

config.Site.storageSite = 'T3_KR_KNU'
# config.Site.whitelist = ['T2_CH_CERN','T2_FR_*']
    """

    datasets = [
        # for BDT training
        ("PU200-DYToLL_M50",     "/DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        ("PU0To200-DYToLL_M50",     "/DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-FlatPU0To200_pilot_111X_mcRun4_realistic_T15_v1-v2/FEVT"),

        # -- PU 200
        # ("PU200-DYToLL_M50",     "/DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # ("PU200-DYToLL_M10to50", "/DYJetsToLL_M-10to50_TuneCP5_14TeV-madgraphMLM-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # ("PU200-WToLNu",               "/WJetsToLNu_TuneCP5_14TeV-amcatnloFXFX-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),

        # ("PU200-TTToSemiLep",          "/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # ("PU200-TTTo2L2Nu",            "/TTTo2L2Nu_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # ("PU200-TT",                   "/TT_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v2/FEVT"),

        # -- PU 140
        # ("PU140-DYToLL_M50",     "/DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_pilot_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # ("PU140-DYToLL_M10to50", "/DYToLL_M-10To50_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_pilot_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # ("PU140-WToLNu",         "/WJetsToLNu_TuneCP5_14TeV-amcatnloFXFX-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),

        # ("PU140-TTToSemiLep",          "/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # ("PU140-TTTo2L2Nu",            "/TTTo2L2Nu_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # ("PU140-TT",                   "/TT_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/FEVT"),

        # -- QCDs
        # # (               "PU140-MinBias", "/MinBias_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # (         "PU140-MinBias-NewMB", "/MinBias_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v2/FEVT"),
        # # (               "PU200-MinBias", "/MinBias_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # (         "PU200-MinBias-NewMB", "/MinBias_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v2/FEVT"),

        # (   "PU140-QCD_Pt120to170_MuEn", "/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (   "PU200-QCD_Pt120to170_MuEn", "/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU140-QCD_Pt15to20_MuEn", "/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU200-QCD_Pt15to20_MuEn", "/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (   "PU140-QCD_Pt170to300_MuEn", "/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (   "PU200-QCD_Pt170to300_MuEn", "/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU140-QCD_Pt20to30_MuEn", "/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU200-QCD_Pt20to30_MuEn", "/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (   "PU140-QCD_Pt300toInf_MuEn", "/QCD_Pt-300toInf_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (   "PU200-QCD_Pt300toInf_MuEn", "/QCD_Pt-300toInf_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU140-QCD_Pt30to50_MuEn", "/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU200-QCD_Pt30to50_MuEn", "/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU140-QCD_Pt50to80_MuEn", "/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU200-QCD_Pt50to80_MuEn", "/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU140-QCD_Pt80to120_MuEn", "/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU200-QCD_Pt80to120_MuEn", "/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),

        # (        "PU140-QCD_Pt120to170", "/QCD_Pt_120to170_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (        "PU200-QCD_Pt120to170", "/QCD_Pt_120to170_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (        "PU140-QCD_Pt170to300", "/QCD_Pt_170to300_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (        "PU200-QCD_Pt170to300", "/QCD_Pt_170to300_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU140-QCD_Pt20to30-NewMB", "/QCD_Pt_20to30_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_withNewMB_111X_mcRun4_realistic_T15_v1-v2/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU200-QCD_Pt20to30-NewMB", "/QCD_Pt_20to30_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1-v2/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (        "PU140-QCD_Pt300to470", "/QCD_Pt_300to470_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (        "PU200-QCD_Pt300to470", "/QCD_Pt_300to470_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (          "PU140-QCD_Pt30to50", "/QCD_Pt_30to50_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU140-QCD_Pt30to50-NewMB", "/QCD_Pt_30to50_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v2/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (          "PU200-QCD_Pt30to50", "/QCD_Pt_30to50_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU200-QCD_Pt30to50-NewMB", "/QCD_Pt_30to50_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v2/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (        "PU140-QCD_Pt470to600", "/QCD_Pt_470to600_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (        "PU200-QCD_Pt470to600", "/QCD_Pt_470to600_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (          "PU140-QCD_Pt50to80", "/QCD_Pt_50to80_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU140-QCD_Pt50to80-NewMB", "/QCD_Pt_50to80_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v2/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (          "PU200-QCD_Pt50to80", "/QCD_Pt_50to80_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU200-QCD_Pt50to80-NewMB", "/QCD_Pt_50to80_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v3/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (         "PU140-QCD_Pt600oInf", "/QCD_Pt_600oInf_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (         "PU200-QCD_Pt600oInf", "/QCD_Pt_600oInf_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (         "PU140-QCD_Pt80to120", "/QCD_Pt_80to120_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (         "PU200-QCD_Pt80to120", "/QCD_Pt_80to120_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),

        # (   "PU140-QCD_Pt120to170_EMEn", "/QCD_Pt-120to170_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (   "PU200-QCD_Pt120to170_EMEn", "/QCD_Pt-120to170_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU140-QCD_Pt15to20_EMEn", "/QCD_Pt-15to20_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU200-QCD_Pt15to20_EMEn", "/QCD_Pt-15to20_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (   "PU140-QCD_Pt170to300_EMEn", "/QCD_Pt-170to300_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (   "PU200-QCD_Pt170to300_EMEn", "/QCD_Pt-170to300_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU140-QCD_Pt20to30_EMEn", "/QCD_Pt-20to30_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU200-QCD_Pt20to30_EMEn", "/QCD_Pt-20to30_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (   "PU140-QCD_Pt300toInf_EMEn", "/QCD_Pt-300toInf_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # # (   "PU200-QCD_Pt300toInf_EMEn", "/QCD_Pt-300toInf_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU140-QCD_Pt30to50_EMEn", "/QCD_Pt-30to50_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU200-QCD_Pt30to50_EMEn", "/QCD_Pt-30to50_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU140-QCD_Pt50to80_EMEn", "/QCD_Pt-50to80_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (     "PU200-QCD_Pt50to80_EMEn", "/QCD_Pt-50to80_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU140-QCD_Pt80to120_EMEn", "/QCD_Pt-80to120_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # (    "PU200-QCD_Pt80to120_EMEn", "/QCD_Pt-80to120_EMEnriched_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),

        # Others
        # ("PU140-Zprime_M6000", "/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # ("PU200-Zprime_M6000", "/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # ("PU140-MuonGun",      "/DoubleMuon_gun_FlatPt-1To100/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # ("PU200-MuonGun",      "/DoubleMuon_gun_FlatPt-1To100/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT"),
        # ("PU140-JPsi",         "/JPsiToMuMu_Pt0to100-pythia8_TuneCP5-gun/Phase2HLTTDRSummer20ReRECOMiniAOD-PU140_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD"),
        # ("PU200-JPsi",         "/JPsiToMuMu_Pt0to100-pythia8_TuneCP5-gun/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1_ext1-v3/GEN-SIM-DIGI-RAW-MINIAOD"),
    ]

    HLT_menus = [
        "HLT_Phase2_example_menu_Output.py",
    ]

    proxy = '"/tmp/x509up_u41164"'  # UPDATE

    for menu in HLT_menus:
        name = "L3FromL1TkMuon"  # menu.replace(".py", "").replace("HLT_Phase2_", "").replace("_Output", "")

        for datasetTag, datasetPath in datasets:

            Crab_Config = 'crabConfig_'+name+ '_' + datasetTag +'.py'

            crab_cfg_out = crab_cfg % locals()

            if 'PU0To200-DYToLL_M50' in datasetTag:
                crab_cfg_out = crab_cfg_out.replace('config.Data.unitsPerJob = 5', 'config.Data.unitsPerJob = 20')
                crab_cfg_out = crab_cfg_out.replace("config.Data.outLFNDirBase = '/store/user/sungwon/PhaseII/20210929'", "config.Data.outLFNDirBase = '/store/user/sungwon/PhaseII/20210929/PU0To200-DYToLL_M50'")
            else:
                crab_cfg_out = crab_cfg_out.replace("config.Data.outLFNDirBase = '/store/user/sungwon/PhaseII/20210929'", "config.Data.outLFNDirBase = '/store/user/sungwon/PhaseII/20210929/PU200-DYToLL_M50'")


            print "\n\n", crab_cfg_out
            sys.stdout.flush()
            gc.collect()

            open(Crab_Config, 'wt').write(crab_cfg_out)

            cmd = 'crab submit -c '+Crab_Config+' --proxy='+proxy

            print cmd
            sys.stdout.flush()
            gc.collect()

            os.system(cmd)


