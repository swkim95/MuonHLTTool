# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Phase2 -s HLT:75e33 --processName=HLTX --conditions auto:phase2_realistic_T21 --geometry Extended2026D88 --era Phase2C17I13M9 --eventcontent FEVTDEBUGHLT --filein=/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-RECO/123X_mcRun4_realistic_v11_2026D88noPU-v1/2580000/4cb86d46-f780-4ce7-94df-9e0039e1953b.root -n 100 --nThreads 1 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2C17I13M9_cff import Phase2C17I13M9

process = cms.Process('MYHLT',Phase2C17I13M9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D88Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('HLTrigger.Configuration.HLT_75e33_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/mc/PhaseIISpring22DRMiniAOD/DoubleMuon_FlatPt-1To100-gun/GEN-SIM-DIGI-RAW-MINIAOD/PU200_123X_mcRun4_realistic_v11-v1/40000/00f9cc24-8f1a-4d68-8e4b-99134af74460.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Phase2 nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

#process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
#    dataset = cms.untracked.PSet(
#        dataTier = cms.untracked.string(''),
#        filterName = cms.untracked.string('')
#    ),
#    fileName = cms.untracked.string('Phase2_HLT.root'),
#    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
#    splitLevel = cms.untracked.int32(0)
#)

# Additional output definition

# Other statements
from HLTrigger.Configuration.CustomConfigs import ProcessName
process = ProcessName(process)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T21', '')

# Path and EndPath definitions
process.hltTriggerSummaryAOD.moduleLabelPatternsToMatch = cms.vstring( 'hlt*', 'L1Tk*')


# -- Timing -- #
doTiming = False
if doTiming:
    # configure the FastTimerService
    process.load( "HLTrigger.Timer.FastTimerService_cfi" )
    # print a text summary at the end of the job
    process.FastTimerService.printEventSummary         = False
    process.FastTimerService.printRunSummary           = False
    process.FastTimerService.printJobSummary           = True

    # enable DQM plots
    process.FastTimerService.enableDQM                 = True

    # enable per-path DQM plots (starting with CMSSW 9.2.3-patch2)
    process.FastTimerService.enableDQMbyPath           = True

    # enable per-module DQM plots
    process.FastTimerService.enableDQMbyModule         = True

    # enable per-event DQM plots vs lumisection
    process.FastTimerService.enableDQMbyLumiSection    = False
    process.FastTimerService.dqmLumiSectionsRange      = 2500

    # set the time resolution of the DQM plots
    process.FastTimerService.dqmTimeRange              = 50000.
    process.FastTimerService.dqmTimeResolution         =    10.
    process.FastTimerService.dqmPathTimeRange          = 50000.
    process.FastTimerService.dqmPathTimeResolution     =     5.
    process.FastTimerService.dqmModuleTimeRange        = 50000.
    process.FastTimerService.dqmModuleTimeResolution   =     1.

    # set the base DQM folder for the plots
    process.FastTimerService.dqmPath                   = 'HLT/TimerService'
    process.FastTimerService.enableDQMbyProcesses      = False
# -- #

# -- Ntuple, DQMOutput, and EDMOutput -- #
doNtuple = True
if doNtuple:
    from MuonHLTTool.MuonHLTNtupler.customizerForMuonHLTNtupler import *
    process = customizerFuncForMuonHLTNtupler(process, "MYHLT", False)

    process.ntupler.offlineMuon                   = cms.untracked.InputTag("slimmedMuons")
    process.ntupler.L2Muon                        = cms.untracked.InputTag("hltL2MuonFromL1TkMuonCandidates","","MYHLT")
    process.ntupler.iterL3OI                      = cms.untracked.InputTag("hltL3MuonsPhase2L3OI", "", "MYHLT")
    process.ntupler.iterL3IOFromL1                = cms.untracked.InputTag("hltIter2Phase2L3FromL1TkMuonMerged", "", "MYHLT")
    process.ntupler.hltIter0IterL3FromL1MuonTrack = cms.untracked.InputTag("hltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity", "", "MYHLT")
    process.ntupler.hltIter2IterL3FromL1MuonTrack = cms.untracked.InputTag("hltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity", "", "MYHLT")
    process.ntupler.iterL3MuonNoID                = cms.untracked.InputTag("hltPhase2L3MuonsNoID", "", "MYHLT")
    process.ntupler.iterL3Muon                    = cms.untracked.InputTag("hltPhase2L3Muons",     "", "MYHLT")
    process.ntupler.L3Muon                        = cms.untracked.InputTag("hltPhase2L3MuonCandidates", "", "MYHLT")
    process.ntupler.TkMuonToken                   = cms.InputTag("L1TkMuons", "", "HLT")
    process.ntupler.doMVA                         = cms.bool(True)
    # Isolation study
    # process.ntupler.trkIsoTags                    = cms.untracked.vstring(   trkIsoTags )
    # process.ntupler.trkIsoLabels                  = cms.untracked.VInputTag( trkIsoLabels )
    # process.ntupler.pfIsoTags                     = cms.untracked.vstring(   pfIsoTags )
    # process.ntupler.pfIsoLabels                   = cms.untracked.VInputTag( pfIsoLabels )

    #from MuonHLTTool.MuonHLTNtupler.customizerForMuonHLTSeedNtupler import *
    #process = customizerFuncForMuonHLTSeedNtupler(process, "MYHLT", True)
#
    ##process.seedNtupler.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "", "MYHLT")
    #process.seedNtupler.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks", "RECO")
#
    #process.seedNtupler.L2Muon                        = cms.untracked.InputTag("hltL2MuonFromL1TkMuonCandidates", "", "MYHLT")
#
    #process.seedNtupler.hltIterL3OISeedsFromL2Muons                       = cms.untracked.InputTag("hltPhase2L3OISeedsFromL2Muons", "", "MYHLT")
    #process.seedNtupler.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks = cms.untracked.InputTag("hltIter0Phase2L3FromL1TkMuonPixelSeedsFromPixelTracks", "", "MYHLT")
    #process.seedNtupler.hltIter2IterL3FromL1MuonPixelSeeds                = cms.untracked.InputTag("hltIter2Phase2L3FromL1TkMuonPixelSeeds", "", "MYHLT")
#
    #process.seedNtupler.hltIterL3OIMuonTrack                              = cms.untracked.InputTag("hltPhase2L3OIMuonTrackSelectionHighPurity", "", "MYHLT")
    #process.seedNtupler.hltIter0IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity", "", "MYHLT")
    #process.seedNtupler.hltIter2IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity", "", "MYHLT")

    process.TFileService.fileName = cms.string("ntuple_D88Geo_MuonGun.root")
    
    #from HLTrigger.MuonHLTSeedMVAClassifier.customizerForMuonHLTSeeding import *
    #WPNAME = 'noMVAcut_noSeedMax'
    #doSort = False
    #nSeedMax_B = (-1,)
    #nSeedMax_E = (-1,)
    #mvaCuts_B = (0,)
    #mvaCuts_E = (0,)
    #process = customizerFuncForMuonHLTSeeding(process, "MYHLT", WPNAME, doSort, nSeedMax_B, nSeedMax_E, mvaCuts_B, mvaCuts_E )

doDQMOut = False
if doDQMOut:
    process.dqmOutput = cms.OutputModule("DQMRootOutputModule",
        dataset = cms.untracked.PSet(
            dataTier = cms.untracked.string('DQMIO'),
            filterName = cms.untracked.string('')
        ),
        fileName = cms.untracked.string("DQMIO.root"),
        outputCommands = process.DQMEventContent.outputCommands,
        splitLevel = cms.untracked.int32(0)
    )
    process.DQMOutput = cms.EndPath( process.dqmOutput )

doEDMOut = False
if doEDMOut:
    process.writeDataset = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string('edmOutput.root'),
        outputCommands = cms.untracked.vstring(
            'drop *',
            'keep *_*_*_MYHLT'
        )
    )
    process.EDMOutput = cms.EndPath(process.writeDataset)
# -- #





process.L1T_DoubleNNTau52 = cms.Path(process.HLTL1Sequence+process.hltL1DoubleNNTau52)
process.L1T_SingleNNTau150 = cms.Path(process.HLTL1Sequence+process.hltL1SingleNNTau150)
process.endjob_step = cms.EndPath(process.endOfProcess)
#process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
# process.schedule imported from cff in HLTrigger.Configuration
#process.schedule.extend([process.endjob_step,process.FEVTDEBUGHLToutput_step])
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)


process.HLT_Mu50_FromL1TkMuon_Open = cms.Path(
    process.HLTBeginSequence+
    cms.ignore(process.hltL1TkSingleMuFiltered22)+
    cms.ignore(process.hltL3fL1TkSingleMu22L3Filtered50Q)+
    process.HLTEndSequence, 
    cms.Task(process.MeasurementTrackerEvent, process.hltCsc2DRecHits, process.hltCscSegments, process.hltDt1DRecHits, process.hltDt4DSegments, process.hltGemRecHits, process.hltGemSegments, process.hltIter0Phase2L3FromL1TkMuonCkfTrackCandidates, process.hltIter0Phase2L3FromL1TkMuonCtfWithMaterialTracks, process.hltIter0Phase2L3FromL1TkMuonPixelSeedsFromPixelTracks, process.hltIter0Phase2L3FromL1TkMuonTrackCutClassifier, process.hltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity, process.hltIter2Phase2L3FromL1TkMuonCkfTrackCandidates, process.hltIter2Phase2L3FromL1TkMuonClustersRefRemoval, process.hltIter2Phase2L3FromL1TkMuonCtfWithMaterialTracks, process.hltIter2Phase2L3FromL1TkMuonMaskedMeasurementTrackerEvent, process.hltIter2Phase2L3FromL1TkMuonMerged, process.hltIter2Phase2L3FromL1TkMuonPixelClusterCheck, process.hltIter2Phase2L3FromL1TkMuonPixelHitDoublets, process.hltIter2Phase2L3FromL1TkMuonPixelHitTriplets, process.hltIter2Phase2L3FromL1TkMuonPixelLayerTriplets, process.hltIter2Phase2L3FromL1TkMuonPixelSeeds, process.hltIter2Phase2L3FromL1TkMuonTrackCutClassifier, process.hltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity, process.hltL1TkMuons, process.hltL2MuonFromL1TkMuonCandidates, process.hltL2MuonSeedsFromL1TkMuon, process.hltL2MuonsFromL1TkMuon, process.hltL2OfflineMuonSeeds, process.hltL3MuonsPhase2L3Links, process.hltL3MuonsPhase2L3OI, process.hltMe0RecHits, process.hltMe0Segments, process.hltPhase2L3FromL1TkMuonPixelLayerQuadruplets, process.hltPhase2L3FromL1TkMuonPixelTracks, process.hltPhase2L3FromL1TkMuonPixelTracksHitDoublets, process.hltPhase2L3FromL1TkMuonPixelTracksHitQuadruplets, process.hltPhase2L3FromL1TkMuonPixelTracksTrackingRegions, process.hltPhase2L3FromL1TkMuonPixelVertices, process.hltPhase2L3FromL1TkMuonTrimmedPixelVertices, process.hltPhase2L3GlbMuon, process.hltPhase2L3MuonCandidates, process.hltPhase2L3MuonMerged, process.hltPhase2L3MuonPixelTracksFilter, process.hltPhase2L3MuonPixelTracksFitter, process.hltPhase2L3MuonTracks, process.hltPhase2L3Muons, process.hltPhase2L3MuonsNoID, process.hltPhase2L3OIL3MuonCandidates, process.hltPhase2L3OIL3Muons, process.hltPhase2L3OIL3MuonsLinksCombination, process.hltPhase2L3OIMuCtfWithMaterialTracks, process.hltPhase2L3OIMuonTrackCutClassifier, process.hltPhase2L3OIMuonTrackSelectionHighPurity, process.hltPhase2L3OISeedsFromL2Muons, process.hltPhase2L3OITrackCandidates, process.hltRpcRecHits, process.siPhase2Clusters, process.siPixelClusterShapeCache, process.siPixelClusters, process.siPixelRecHits))

process.schedule = cms.Schedule(
    # process.L1simulation_step,
    process.L1T_SingleTkMuon_22,
    process.L1T_DoubleTkMuon_15_7,
    process.L1T_TripleTkMuon_5_3_3,
    process.HLT_Mu50_FromL1TkMuon_Open,
    process.HLT_Mu50_FromL1TkMuon,
    process.HLT_IsoMu24_FromL1TkMuon,
    process.HLT_Mu37_Mu27_FromL1TkMuon,
    process.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_FromL1TkMuon,
    process.HLT_TriMu_10_5_5_DZ_FromL1TkMuon,
    # process.HLT_IsoStudy,
    process.HLTriggerFinalPath,
    # process.Gen_QCDBCToEFilter,
    # process.Gen_QCDEmEnrichingFilter,
    # process.Gen_QCDEmEnrichingNoBCToEFilter,
    # process.Gen_QCDMuGenFilter,
    # process.Gen_QCDMuNoEmGenFilter,
    # process.Gen_QCDEmNoMuGenFilter,
    # process.myana,
    process.mypath,
    # process.valpath,
    process.myendpath,
    # process.myseedpath
    # process.DQMOutput
    # process.EDMOutput
)
# -- #

process.options.wantSummary = cms.untracked.bool( True )
if 'MessageLogger' in process.__dict__:
	process.MessageLogger.TriggerSummaryProducerAOD = cms.untracked.PSet()
	process.MessageLogger.L1GtTrigReport = cms.untracked.PSet()
	process.MessageLogger.L1TGlobalSummary = cms.untracked.PSet()
	process.MessageLogger.HLTrigReport = cms.untracked.PSet()
	process.MessageLogger.FastReport = cms.untracked.PSet()
	process.MessageLogger.ThroughputService = cms.untracked.PSet()
	process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion



