
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
process = cms.Process("MYHLT", eras.Phase2C9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input  = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(''),
    secondaryFileNames = cms.untracked.vstring()
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T15', '')

# -- L1 emulation -- #
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.L1TkMuons.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks", "RECO")
process.L1TkMuons.applyQualityCuts = cms.bool(True)
# -- #

# -- HLTriggerFinalPath -- #
process.hltTriggerSummaryAOD = cms.EDProducer( "TriggerSummaryProducerAOD",
    moduleLabelPatternsToSkip = cms.vstring(  ),
    processName = cms.string( "@" ),
    moduleLabelPatternsToMatch = cms.vstring( 'hlt*', 'L1Tk*' ),
    throw = cms.bool( False )
)
process.hltTriggerSummaryRAW = cms.EDProducer( "TriggerSummaryProducerRAW",
    processName = cms.string( "@" )
)
process.hltBoolFalse = cms.EDFilter( "HLTBool",
    result = cms.bool( False )
)
process.HLTriggerFinalPath = cms.Path(
    process.hltTriggerSummaryAOD+
    process.hltTriggerSummaryRAW+
    process.hltBoolFalse
)
# -- #

# -- HLT paths -- #
from HLTrigger.PhaseII.Muon.Customizers.loadPhase2MuonHLTPaths_cfi import loadPhase2MuonHLTPaths
process = loadPhase2MuonHLTPaths(process)

# from HLTrigger.PhaseII.Muon.Customizers.customizerForPhase2MuonHLT import customizePhase2MuonHLTIsolationForOpt
# process, _pfIso, _trkIso = customizePhase2MuonHLTIsolationForOpt(process)

# pfIsoTags = _pfIso[0]
# pfIsoLabels = _pfIso[1]
# trkIsoTags = _trkIso[0]
# trkIsoLabels = _trkIso[1]
# -- #

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

# -- Validation -- #
doValidation = False
if doValidation:
    from SimTracker.TrackAssociatorProducers.trackAssociatorByHits_cfi import *
    process.LhcParametersDefinerForTP = cms.ESProducer("ParametersDefinerForTPESProducer",
       ComponentName = cms.string('LhcParametersDefinerForTP'),
       beamSpot      = cms.untracked.InputTag('offlineBeamSpot', '', 'MYHLT')
    )

    from Validation.RecoMuon.associators_cff import *
    from Validation.RecoMuon.muonValidationHLT_cff import *
    from Validation.RecoMuon.selectors_cff import muonTPSet
    muonTPSetPt22 = muonTPSet.clone()
    muonTPSetPt22.ptMin = cms.double(22.0)
    muonTPSetPt22.minRapidity = cms.double(-2.4)
    muonTPSetPt22.maxRapidity = cms.double(2.4)

    process.load("Validation.RecoMuon.muonValidationHLT_cff")
    process.tpToL3FromL1TkMuonAssociation.tracksTag                = cms.InputTag("hltIter2Phase2L3FromL1TkMuonMerged")
    process.l3IOFromL1TkMuonMuTrackV.label                         = cms.VInputTag("hltIter2Phase2L3FromL1TkMuonMerged:")
    process.l3IOFromL1TkMuonMuTrackV.beamSpot                      = cms.InputTag('offlineBeamSpot', '', 'MYHLT')
    process.l3IOFromL1TkMuonMuTrackV.muonTPSelector                = muonTPSetPt22

    process.hltIterL3MuonsNoIDTracks.muonsTag                      = cms.InputTag("hltPhase2L3MuonsNoID")
    process.hltIterL3MuonsNoIDTracks.inputCSCSegmentCollection     = cms.InputTag("hltCscSegments")
    process.hltIterL3MuonsNoIDTracks.inputDTRecSegment4DCollection = cms.InputTag("hltDt4DSegments")
    # process.tpToL3NoIDMuonAssociation
    process.l3NoIDMuonMuTrackV.beamSpot                            = cms.InputTag('offlineBeamSpot', '', 'MYHLT')
    process.l3NoIDMuonMuTrackV.muonTPSelector                      = muonTPSetPt22

    process.hltIterL3MuonsTracks.muonsTag                          = cms.InputTag("hltPhase2L3Muons")
    process.hltIterL3MuonsTracks.inputCSCSegmentCollection         = cms.InputTag("hltCscSegments")
    process.hltIterL3MuonsTracks.inputDTRecSegment4DCollection     = cms.InputTag("hltDt4DSegments")
    # process.tpToL3MuonAssociation
    process.l3MuonMuTrackV.beamSpot                                = cms.InputTag('offlineBeamSpot', '', 'MYHLT')
    process.l3MuonMuTrackV.muonTPSelector                          = muonTPSetPt22

    process.valpath = cms.Path(
        process.tpToL3FromL1TkMuonAssociation+
        process.l3IOFromL1TkMuonMuTrackV+

        process.hltIterL3MuonsNoIDTracks+
        process.tpToL3NoIDMuonAssociation+
        process.l3NoIDMuonMuTrackV+

        process.hltIterL3MuonsTracks+
        process.tpToL3MuonAssociation+
        process.l3MuonMuTrackV
    )
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
    process.ntupler.doMVA                         = cms.bool(True)
    # Isolation study
    # process.ntupler.trkIsoTags                    = cms.untracked.vstring(   trkIsoTags )
    # process.ntupler.trkIsoLabels                  = cms.untracked.VInputTag( trkIsoLabels )
    # process.ntupler.pfIsoTags                     = cms.untracked.vstring(   pfIsoTags )
    # process.ntupler.pfIsoLabels                   = cms.untracked.VInputTag( pfIsoLabels )

    from MuonHLTTool.MuonHLTNtupler.customizerForMuonHLTSeedNtupler import *
    process = customizerFuncForMuonHLTSeedNtupler(process, "MYHLT", True)

    #process.seedNtupler.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "", "MYHLT")
    process.seedNtupler.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks", "RECO")

    process.seedNtupler.L2Muon                        = cms.untracked.InputTag("hltL2MuonFromL1TkMuonCandidates", "", "MYHLT")

    process.seedNtupler.hltIterL3OISeedsFromL2Muons                       = cms.untracked.InputTag("hltPhase2L3OISeedsFromL2Muons", "", "MYHLT")
    process.seedNtupler.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks = cms.untracked.InputTag("hltIter0Phase2L3FromL1TkMuonPixelSeedsFromPixelTracks", "", "MYHLT")
    process.seedNtupler.hltIter2IterL3FromL1MuonPixelSeeds                = cms.untracked.InputTag("hltIter2Phase2L3FromL1TkMuonPixelSeeds", "", "MYHLT")

    process.seedNtupler.hltIterL3OIMuonTrack                              = cms.untracked.InputTag("hltPhase2L3OIMuonTrackSelectionHighPurity", "", "MYHLT")
    process.seedNtupler.hltIter0IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity", "", "MYHLT")
    process.seedNtupler.hltIter2IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity", "", "MYHLT")

    process.TFileService.fileName = cms.string("Ntuple_SeedNtuple.root")
    
    from HLTrigger.MuonHLTSeedMVAClassifier.customizerForMuonHLTSeeding import *
    WPNAME = 'NoMVACut_with_ntuple'
    doSort = False
    nSeedMax_B = (-1,)
    nSeedMax_E = (-1,)
    mvaCuts_B = (0,)
    mvaCuts_E = (0,)
    process = customizerFuncForMuonHLTSeeding(process, "MYHLT", WPNAME, doSort, nSeedMax_B, nSeedMax_E, mvaCuts_B, mvaCuts_E )

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

# -- Simple gen matching analyzer -- #
process.GenMuAnalyzerFromFileIn = cms.EDAnalyzer("GenMuAnalyzer",
    genParticle_src = cms.InputTag("genParticles"),
    L1TT_src = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks", "RECO"),
    L1TkMuon_src = cms.InputTag("L1TkMuons", "", "RECO"),
    pt_min = cms.double(10.0)
)

process.GenMuAnalyzerReEmu = cms.EDAnalyzer("GenMuAnalyzer",
    genParticle_src = cms.InputTag("genParticles"),
    L1TT_src = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks", "RECO"),
    L1TkMuon_src = cms.InputTag("L1TkMuons", "", "MYHLT"),
    pt_min = cms.double(10.0)
)

process.myana = cms.Path(
    process.GenMuAnalyzerFromFileIn+
    process.GenMuAnalyzerReEmu
)

# process.HLT_IsoStudy = cms.Path(
#     process.HLTBeginSequence+

#     # L1TkMuon filter
#     cms.ignore( process.hltL1TkSingleMuFiltered22 )+

#     process.HLTMuonLocalRecoSequence+
#     process.HLTDoLocalPixelSequence+
#     process.HLTDoLocalStripSequence+

#     # L2 reco
#     process.HLTL2muonrecoSequence+

#     # L3 reco
#     process.HLTPhase2L3MuonRecoSequence+
#     cms.ignore( process.hltL3fL1TkSingleMu22L3Filtered24Q )+

#     # Isolation
#     process.HLTPhase2L3MuonBaseIsoSequence+
#     process.IsolationStudySequence+

#     # cms.ignore( process.hltL3crIsoL1TkSingleMu22L3f24QL3pfecalIsoFiltered0p39 ) +

#     # cms.ignore( process.hltL3crIsoL1TkSingleMu22L3f24QL3pfhcalIsoFiltered0p40 ) +

#     # cms.ignore( process.hltL3crIsoL1TkSingleMu22L3f24QL3pfhgcalIsoFiltered0p06 ) +

#     # process.hltPhase2L3MuonsTrkIsoRegionaldR0p3dRVeto0p005dz0p25dr0p20ChisqInfPtMin0p0Cut0p06 +
#     # cms.ignore( process.hltL3crIsoL1TkSingleMu22L3f24QL3trkIsoRegionalOldFiltered0p07EcalHcalHgcalTrk ) +

#     # process.hltPhase2L3MuonsTrkIsoRegionalNewdR0p3dRVeto0p005dz0p25dr0p20ChisqInfPtMin0p0Cut0p07 +
#     # cms.ignore( process.hltL3crIsoL1TkSingleMu22L3f24QL3trkIsoRegionalNewFiltered0p07EcalHcalHgcalTrk ) +

#     process.HLTEndSequence
# )
# -- #

# -- Gen filters -- #
process.load('HLTrigger.PhaseII.EGamma.Paths.Gen_QCDBCToEFilter_cff')
process.load('HLTrigger.PhaseII.EGamma.Paths.Gen_QCDEmEnrichingFilter_cff')
process.load('HLTrigger.PhaseII.EGamma.Paths.Gen_QCDEmEnrichingNoBCToEFilter_cff')
process.load('HLTrigger.PhaseII.EGamma.Paths.Gen_QCDMuGenFilter_cff')

process.Gen_QCDMuNoEmGenFilter = cms.Path(
   ~process.emEnrichingFilter +
   process.muGenFilter
)

process.Gen_QCDEmNoMuGenFilter = cms.Path(
   ~process.muGenFilter +
   process.emEnrichingFilter
)
# -- #

process.schedule = cms.Schedule(
    process.L1simulation_step,
    process.L1_SingleTkMuon_22,
    process.L1_DoubleTkMuon_15_7,
    process.L1_TripleTkMuon_5_3_3,
    process.HLT_Mu50_FromL1TkMuon_Open,
    process.HLT_Mu50_FromL1TkMuon,
    process.HLT_IsoMu24_FromL1TkMuon,
    process.HLT_Mu37_Mu27_FromL1TkMuon,
    process.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_FromL1TkMuon,
    process.HLT_TriMu_10_5_5_DZ_FromL1TkMuon,
    # process.HLT_IsoStudy,
    process.HLTriggerFinalPath,
    process.Gen_QCDBCToEFilter,
    process.Gen_QCDEmEnrichingFilter,
    process.Gen_QCDEmEnrichingNoBCToEFilter,
    process.Gen_QCDMuGenFilter,
    process.Gen_QCDMuNoEmGenFilter,
    process.Gen_QCDEmNoMuGenFilter,
    process.myana,
    process.mypath,
    # process.valpath,
    process.myendpath,
    process.myseedpath
    # process.DQMOutput
    # process.EDMOutput
)
# -- #

# -- Test Setup -- #
process.load( "DQMServices.Core.DQMStore_cfi" )
process.DQMStore.enableMultiThread = True

process.GlobalTag.globaltag = "111X_mcRun4_realistic_T15_v5"

process.source.fileNames = cms.untracked.vstring(
    "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/100000/00695E54-EAD4-3444-A833-3FE1C2BC8880.root"
   #  "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/FlatPU0To200_pilot_111X_mcRun4_realistic_T15_v1-v2/30026/83959981-E532-9E46-9C60-6C464C4E9D8F.root"

    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DoubleMuon_gun_FlatPt-1To100/FEVT/NoPU_111X_mcRun4_realistic_T15_v1-v1/100000/183F7FEF-A746-B740-840A-62A504300C63.root"

    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYJetsToLL_M-10to50_TuneCP5_14TeV-madgraphMLM-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_111X_mcRun4_realistic_T15_v1-v1/120000/5821E269-9E33-AE49-9133-67A03F2527EC.root",

    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F7512F92-AA6C-F642-BBA5-8BAED84CF4C9.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F786C6BD-D600-A845-B12B-D2A499B05D2B.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F7CBE904-DE8D-ED4D-A5C3-EACE571910BE.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F8C8FBAC-2360-E649-B7C9-A1F5C8F2A788.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F9371A50-AC2F-1649-9949-11D1C169E6A5.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FAB40CB7-0647-F344-8470-2E0BAB68C7AF.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FAF35BE0-D62E-9E41-AA4E-6EFA98032795.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FB635D0A-F1D3-5D4E-90AD-6C396681FC87.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FC9170CA-633F-EB4C-8CE5-4E2D29969EBB.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FCB6CEBD-0248-1C4E-9C95-D45A3F3F5902.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FDE7E62F-A277-B145-9FC7-8078B21C0913.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FE7B45F1-3D6D-7643-999E-CEA976B2CDC1.root",

    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FC1C5501-17FF-AD4E-B0C2-78B114D94AD6.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FD2DCC3C-9732-854B-AD23-A010899DB902.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FD35A9AA-051D-B94B-A971-901867BFED51.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FD8D88D6-E791-6B4F-B067-AAFEA3F852D3.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FDA9AEB8-5A1F-AF49-B919-5C7A64194B0A.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FDB296D7-F051-9645-BC27-9D222B962B3A.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FDBE16F6-13A5-FF48-A316-83D9B8FB3CB2.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FE0F2AF9-BDD9-AF4A-88F1-D426E89F788E.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FE352801-A32A-304E-8EF2-FEB62D8A4036.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FEA94BB5-2837-A14F-9F65-24D5103522D2.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF3C16DF-5B11-8B4A-9B67-DF3CEF790F2F.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF7BF0E2-1380-2D48-BB19-F79E6907CD5D.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/87C80516-CB14-0346-9579-1CCCE4607148.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/0058F613-AE76-4840-82C3-7F6F3224BBF3.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/0064CF05-E335-5440-BDA1-4DDA696F3CBD.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/008A2993-1370-424A-ABA1-B2D163F8AEED.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/012D4B65-425E-8A49-B961-A289D0447E1E.root",
    # "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/014A3F26-43E6-AA41-B605-AA4861CE6351.root",
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( -1 )
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool( True ),
    numberOfThreads = cms.untracked.uint32( 1 ),
    numberOfStreams = cms.untracked.uint32( 0 ),
    sizeOfStackForThreadsInKB = cms.untracked.uint32( 10*1024 )
)

if 'MessageLogger' in process.__dict__:
    process.MessageLogger.categories.append('TriggerSummaryProducerAOD')
    process.MessageLogger.categories.append('L1GtTrigReport')
    process.MessageLogger.categories.append('L1TGlobalSummary')
    process.MessageLogger.categories.append('HLTrigReport')
    process.MessageLogger.categories.append('FastReport')
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000
# -- #


from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000
process = customise_aging_1000(process)

from L1Trigger.Configuration.customisePhase2TTNoMC import customisePhase2TTNoMC
process = customisePhase2TTNoMC(process)

from HLTrigger.Configuration.Eras import modifyHLTforEras
modifyHLTforEras(process)


# process.Timing = cms.Service("Timing",
#     summaryOnly = cms.untracked.bool(True),
#     useJobReport = cms.untracked.bool(True)
# )

# process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
#     ignoreTotal = cms.untracked.int32(1)
# )

# print process.dumpPython()

