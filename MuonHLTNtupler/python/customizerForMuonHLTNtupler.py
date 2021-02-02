# -- custoimzer for ntupler that can be added to the HLT configuration for re-running HLT
# -- add two lines in the HLT config.:
# from MuonHLTTool.MuonHLTNtupler.customizerForMuonHLTNtupler import *
# process = customizerFuncForMuonHLTNtupler(process, "MYHLT")

import FWCore.ParameterSet.Config as cms
from HLTrigger.MuonHLTSeedMVAClassifier.mvaScale import *

def customizerFuncForMuonHLTNtupler(process, newProcessName = "MYHLT", doDYSkim = False):
    if hasattr(process, "DQMOutput"):
        del process.DQMOutput

    import SimTracker.TrackAssociatorProducers.quickTrackAssociatorByHits_cfi
    from SimTracker.TrackerHitAssociation.tpClusterProducer_cfi import tpClusterProducer as _tpClusterProducer

    process.hltTPClusterProducer = _tpClusterProducer.clone(
      # pixelClusterSrc = "hltSiPixelClusters",
      # stripClusterSrc = "hltSiStripRawToClustersFacility"
    )
    process.hltTPClusterProducer.pixelSimLinkSrc = cms.InputTag("simSiPixelDigis","Pixel")
    process.hltTrackAssociatorByHits = SimTracker.TrackAssociatorProducers.quickTrackAssociatorByHits_cfi.quickTrackAssociatorByHits.clone()
    process.hltTrackAssociatorByHits.cluster2TPSrc            = cms.InputTag("hltTPClusterProducer")
    process.hltTrackAssociatorByHits.UseGrouped               = cms.bool( False )
    process.hltTrackAssociatorByHits.UseSplitting             = cms.bool( False )
    process.hltTrackAssociatorByHits.ThreeHitTracksAreSpecial = cms.bool( False )

    # -- track - TP associations
    import SimMuon.MCTruth.MuonTrackProducer_cfi
    process.hltPhase2L3MuonsNoIDTracks = SimMuon.MCTruth.MuonTrackProducer_cfi.muonTrackProducer.clone()
    process.hltPhase2L3MuonsNoIDTracks.muonsTag                      = cms.InputTag("hltPhase2L3MuonsNoID")
    process.hltPhase2L3MuonsNoIDTracks.selectionTags                 = ('All',)
    process.hltPhase2L3MuonsNoIDTracks.trackType                     = "recomuonTrack"
    process.hltPhase2L3MuonsNoIDTracks.ignoreMissingMuonCollection   = True
    process.hltPhase2L3MuonsNoIDTracks.inputCSCSegmentCollection     = cms.InputTag("hltCscSegments")
    process.hltPhase2L3MuonsNoIDTracks.inputDTRecSegment4DCollection = cms.InputTag("hltDt4DSegments")

    process.hltPhase2L3MuonsTracks = SimMuon.MCTruth.MuonTrackProducer_cfi.muonTrackProducer.clone()
    process.hltPhase2L3MuonsTracks.muonsTag                          = cms.InputTag("hltPhase2L3Muons")
    process.hltPhase2L3MuonsTracks.selectionTags                     = ('All',)
    process.hltPhase2L3MuonsTracks.trackType                         = "recomuonTrack"
    process.hltPhase2L3MuonsTracks.ignoreMissingMuonCollection       = True
    process.hltPhase2L3MuonsTracks.inputCSCSegmentCollection         = cms.InputTag("hltCscSegments")
    process.hltPhase2L3MuonsTracks.inputDTRecSegment4DCollection     = cms.InputTag("hltDt4DSegments")

    from SimMuon.MCTruth.MuonAssociatorByHits_cfi import muonAssociatorByHits as _muonAssociatorByHits
    hltMuonAssociatorByHits = _muonAssociatorByHits.clone()
    hltMuonAssociatorByHits.PurityCut_track              = 0.75
    hltMuonAssociatorByHits.PurityCut_muon               = 0.75
    hltMuonAssociatorByHits.DTrechitTag                  = 'hltDt1DRecHits'
    hltMuonAssociatorByHits.ignoreMissingTrackCollection = True
    hltMuonAssociatorByHits.UseTracker                   = True
    hltMuonAssociatorByHits.UseMuon                      = True

    process.AhltPhase2L3OIMuonTrackSelectionHighPurity            = hltMuonAssociatorByHits.clone( tracksTag = 'hltPhase2L3OIMuonTrackSelectionHighPurity' )
    process.AhltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity = hltMuonAssociatorByHits.clone( tracksTag = 'hltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity' )
    process.AhltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity = hltMuonAssociatorByHits.clone( tracksTag = 'hltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity' )
    process.AhltIter2Phase2L3FromL1TkMuonMerged                   = hltMuonAssociatorByHits.clone( tracksTag = 'hltIter2Phase2L3FromL1TkMuonMerged' )
    process.AhltPhase2L3MuonsNoID                                 = hltMuonAssociatorByHits.clone( tracksTag = 'hltPhase2L3MuonsNoIDTracks' )
    process.AhltPhase2L3Muons                                     = hltMuonAssociatorByHits.clone( tracksTag = 'hltPhase2L3MuonsTracks' )

    trackNames = [
        'hltPhase2L3OI',
        'hltIter0Phase2L3FromL1TkMuon',
        'hltIter2Phase2L3FromL1TkMuon',
        'hltPhase2L3IOFromL1',
        'hltPhase2L3MuonsNoID',
        'hltPhase2L3Muons'
    ]

    trackLabels = [
        'hltPhase2L3OIMuonTrackSelectionHighPurity',
        'hltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity',
        'hltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity',
        'hltIter2Phase2L3FromL1TkMuonMerged',
        'hltPhase2L3MuonsNoIDTracks',
        'hltPhase2L3MuonsTracks'
    ]

    assoLabels = [
        'AhltPhase2L3OIMuonTrackSelectionHighPurity',
        'AhltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity',
        'AhltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity',
        'AhltIter2Phase2L3FromL1TkMuonMerged',
        'AhltPhase2L3MuonsNoID',
        'AhltPhase2L3Muons'
    ]

    process.trackAssoSeq = cms.Sequence(
        process.hltPhase2L3MuonsNoIDTracks +
        process.hltPhase2L3MuonsTracks +
        process.AhltPhase2L3OIMuonTrackSelectionHighPurity +
        process.AhltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity +
        process.AhltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity +
        process.AhltIter2Phase2L3FromL1TkMuonMerged +
        process.AhltPhase2L3MuonsNoID +
        process.AhltPhase2L3Muons
    )

    # -- Isolations
    trkIsoTags = []
    trkIsoLabels = []
    pfIsoTags = []
    pfIsoLabels = []

    from MuonHLTTool.MuonHLTNtupler.ntupler_cfi import ntuplerBase
    process.ntupler = ntuplerBase.clone()

    process.ntupler.trackCollectionNames  = cms.untracked.vstring(   trackNames )
    process.ntupler.trackCollectionLabels = cms.untracked.VInputTag( trackLabels )
    process.ntupler.associationLabels     = cms.untracked.VInputTag( assoLabels )

    process.ntupler.trkIsoTags   = cms.untracked.vstring(   trkIsoTags )
    process.ntupler.trkIsoLabels = cms.untracked.VInputTag( trkIsoLabels )
    process.ntupler.pfIsoTags    = cms.untracked.vstring(   pfIsoTags )
    process.ntupler.pfIsoLabels  = cms.untracked.VInputTag( pfIsoLabels )

    # -- set to the new process name
    process.ntupler.myTriggerResults = cms.untracked.InputTag("TriggerResults",          "",     newProcessName)
    process.ntupler.myTriggerEvent   = cms.untracked.InputTag("hltTriggerSummaryAOD",    "",     newProcessName)
    process.ntupler.lumiScaler       = cms.untracked.InputTag("hltScalersRawToDigi",     "",     newProcessName)

    # process.ntupler.L1Muon           = cms.untracked.InputTag("hltGtStage2Digis",        "Muon", newProcessName)
    # process.ntupler.L1Muon           = cms.untracked.InputTag("gmtStage2Digis",        "Muon", newProcessName) 
    # process.ntupler.L1Muon           = cms.untracked.InputTag("hltGtStage2Digis",        "Muon", "HLT") #for phaseII w/o emulation
    process.ntupler.L1Muon           = cms.untracked.InputTag("simGmtStage2Digis",       "",     newProcessName)  # Phase II sim emul
    process.ntupler.L2Muon           = cms.untracked.InputTag("hltL2MuonCandidates",     "",     newProcessName)
    process.ntupler.L3Muon           = cms.untracked.InputTag("hltPhase2L3MuonCandidates", "",     newProcessName)
    process.ntupler.TkMuon           = cms.untracked.InputTag("hltHighPtTkMuonCands",    "",     newProcessName)

    process.ntupler.iterL3OI         = cms.untracked.InputTag("hltL3MuonsIterL3OI",                   "", newProcessName)
    process.ntupler.iterL3IOFromL2   = cms.untracked.InputTag("hltL3MuonsIterL3IO",                   "", newProcessName)
    process.ntupler.iterL3FromL2     = cms.untracked.InputTag("hltIterL3MuonsFromL2LinksCombination", "", newProcessName)
    process.ntupler.iterL3IOFromL1   = cms.untracked.InputTag("hltIter3IterL3FromL1MuonMerged",       "", newProcessName)
    process.ntupler.iterL3MuonNoID   = cms.untracked.InputTag("hltIterL3MuonsNoID",                   "", newProcessName)
    process.ntupler.iterL3Muon       = cms.untracked.InputTag("hltIterL3Muons",                       "", newProcessName)

    process.ntupler.hltIterL3MuonTrimmedPixelVertices                 = cms.untracked.InputTag("hltIterL3MuonTrimmedPixelVertices",                   "", newProcessName)
    process.ntupler.hltIterL3FromL1MuonTrimmedPixelVertices           = cms.untracked.InputTag("hltIterL3FromL1MuonTrimmedPixelVertices",             "", newProcessName)

    process.ntupler.doMVA  = cms.bool(False)
    process.ntupler.doSeed = cms.bool(False)

    process.ntupler.hltIterL3OISeedsFromL2Muons                       = cms.untracked.InputTag("hltIterL3OISeedsFromL2Muons",                         "", newProcessName)
    process.ntupler.hltIter0IterL3MuonPixelSeedsFromPixelTracks       = cms.untracked.InputTag("hltIter0IterL3MuonPixelSeedsFromPixelTracks",         "", newProcessName)
    process.ntupler.hltIter2IterL3MuonPixelSeeds                      = cms.untracked.InputTag("hltIter2IterL3MuonPixelSeeds",                        "", newProcessName)
    process.ntupler.hltIter3IterL3MuonPixelSeeds                      = cms.untracked.InputTag("hltIter3IterL3MuonPixelSeeds",                        "", newProcessName)
    process.ntupler.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks = cms.untracked.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks",   "", newProcessName)
    process.ntupler.hltIter2IterL3FromL1MuonPixelSeeds                = cms.untracked.InputTag("hltIter2IterL3FromL1MuonPixelSeeds",                  "", newProcessName)
    process.ntupler.hltIter3IterL3FromL1MuonPixelSeeds                = cms.untracked.InputTag("hltIter3IterL3FromL1MuonPixelSeeds",                  "", newProcessName)

    process.ntupler.hltIterL3OIMuonTrack                              = cms.untracked.InputTag("hltIterL3OIMuonTrackSelectionHighPurity",             "", newProcessName)
    process.ntupler.hltIter0IterL3MuonTrack                           = cms.untracked.InputTag("hltIter0IterL3MuonTrackSelectionHighPurity",          "", newProcessName)
    process.ntupler.hltIter2IterL3MuonTrack                           = cms.untracked.InputTag("hltIter2IterL3MuonTrackSelectionHighPurity",          "", newProcessName)
    process.ntupler.hltIter3IterL3MuonTrack                           = cms.untracked.InputTag("hltIter3IterL3MuonTrackSelectionHighPurity",          "", newProcessName)
    process.ntupler.hltIter0IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter0IterL3FromL1MuonTrackSelectionHighPurity",    "", newProcessName)
    process.ntupler.hltIter2IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter2IterL3FromL1MuonTrackSelectionHighPurity",    "", newProcessName)
    process.ntupler.hltIter3IterL3FromL1MuonTrack                     = cms.untracked.InputTag("hltIter3IterL3FromL1MuonTrackSelectionHighPurity",    "", newProcessName)

    process.ntupler.associator = cms.untracked.InputTag("hltTrackAssociatorByHits")
    process.ntupler.trackingParticle = cms.untracked.InputTag("mix","MergedTrackTruth")

    # process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_B_0                       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIterL3OI_0.xml")
    # process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_B_1                       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIterL3OI_1.xml")
    # process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_B_2                       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIterL3OI_2.xml")
    # process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_B_3                       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIterL3OI_3.xml")
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_B_0       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter0_0.xml")
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_B_1       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter0_1.xml")
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_B_2       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter0_2.xml")
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_B_3       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter0_3.xml")
    # process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_B_0                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter2_0.xml")
    # process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_B_1                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter2_1.xml")
    # process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_B_2                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter2_2.xml")
    # process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_B_3                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter2_3.xml")
    # process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_B_0                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter3_0.xml")
    # process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_B_1                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter3_1.xml")
    # process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_B_2                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter3_2.xml")
    # process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_B_3                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter3_3.xml")
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B_0 = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter0FromL1_0.xml")
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B_1 = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter0FromL1_1.xml")
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B_2 = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter0FromL1_2.xml")
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B_3 = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter0FromL1_3.xml")
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_B_0                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/HLTTDR_v3_Barrel_hltIter2FromL1_0.xml")
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_B_1                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/HLTTDR_v3_Barrel_hltIter2FromL1_1.xml")
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_B_2                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/HLTTDR_v3_Barrel_hltIter2FromL1_2.xml")
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_B_3                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/HLTTDR_v3_Barrel_hltIter2FromL1_3.xml")
    # process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_B_0                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter3FromL1_0.xml")
    # process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_B_1                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter3FromL1_1.xml")
    # process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_B_2                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter3FromL1_2.xml")
    # process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_B_3                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Barrel_hltIter3FromL1_3.xml")
    # process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_E_0                       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIterL3OI_0.xml")
    # process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_E_1                       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIterL3OI_1.xml")
    # process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_E_2                       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIterL3OI_2.xml")
    # process.ntupler.mvaFileHltIterL3OISeedsFromL2Muons_E_3                       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIterL3OI_3.xml")
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_E_0       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter0_0.xml")
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_E_1       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter0_1.xml")
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_E_2       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter0_2.xml")
    # process.ntupler.mvaFileHltIter0IterL3MuonPixelSeedsFromPixelTracks_E_3       = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter0_3.xml")
    # process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_E_0                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter2_0.xml")
    # process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_E_1                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter2_1.xml")
    # process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_E_2                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter2_2.xml")
    # process.ntupler.mvaFileHltIter2IterL3MuonPixelSeeds_E_3                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter2_3.xml")
    # process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_E_0                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter3_0.xml")
    # process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_E_1                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter3_1.xml")
    # process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_E_2                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter3_2.xml")
    # process.ntupler.mvaFileHltIter3IterL3MuonPixelSeeds_E_3                      = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter3_3.xml")
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E_0 = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter0FromL1_0.xml")
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E_1 = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter0FromL1_1.xml")
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E_2 = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter0FromL1_2.xml")
    # process.ntupler.mvaFileHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E_3 = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter0FromL1_3.xml")
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_E_0                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/HLTTDR_v3_Endcap_hltIter2FromL1_0.xml")
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_E_1                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/HLTTDR_v3_Endcap_hltIter2FromL1_1.xml")
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_E_2                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/HLTTDR_v3_Endcap_hltIter2FromL1_2.xml")
    process.ntupler.mvaFileHltIter2IterL3FromL1MuonPixelSeeds_E_3                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/HLTTDR_v3_Endcap_hltIter2FromL1_3.xml")
    # process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_E_0                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter3FromL1_0.xml")
    # process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_E_1                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter3FromL1_1.xml")
    # process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_E_2                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter3FromL1_2.xml")
    # process.ntupler.mvaFileHltIter3IterL3FromL1MuonPixelSeeds_E_3                = cms.untracked.FileInPath("HLTrigger/MuonHLTSeedMVAClassifier/data/PU180to200Endcap_hltIter3FromL1_3.xml")

    # process.ntupler.mvaScaleMeanHltIterL3OISeedsFromL2Muons_B                       = cms.untracked.vdouble(PU180to200Barrel_hltIterL3OI_ScaleMean)
    # process.ntupler.mvaScaleStdHltIterL3OISeedsFromL2Muons_B                        = cms.untracked.vdouble(PU180to200Barrel_hltIterL3OI_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter0IterL3MuonPixelSeedsFromPixelTracks_B       = cms.untracked.vdouble(PU180to200Barrel_hltIter0_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter0IterL3MuonPixelSeedsFromPixelTracks_B        = cms.untracked.vdouble(PU180to200Barrel_hltIter0_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter2IterL3MuonPixelSeeds_B                      = cms.untracked.vdouble(PU180to200Barrel_hltIter2_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter2IterL3MuonPixelSeeds_B                       = cms.untracked.vdouble(PU180to200Barrel_hltIter2_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter3IterL3MuonPixelSeeds_B                      = cms.untracked.vdouble(PU180to200Barrel_hltIter3_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter3IterL3MuonPixelSeeds_B                       = cms.untracked.vdouble(PU180to200Barrel_hltIter3_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B = cms.untracked.vdouble(PU180to200Barrel_hltIter0FromL1_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_B  = cms.untracked.vdouble(PU180to200Barrel_hltIter0FromL1_ScaleStd)
    process.ntupler.mvaScaleMeanHltIter2IterL3FromL1MuonPixelSeeds_B                = cms.untracked.vdouble(HLTTDR_v3_Barrel_NThltIter2FromL1_ScaleMean)
    process.ntupler.mvaScaleStdHltIter2IterL3FromL1MuonPixelSeeds_B                 = cms.untracked.vdouble(HLTTDR_v3_Barrel_NThltIter2FromL1_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter3IterL3FromL1MuonPixelSeeds_B                = cms.untracked.vdouble(PU180to200Barrel_hltIter3FromL1_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter3IterL3FromL1MuonPixelSeeds_B                 = cms.untracked.vdouble(PU180to200Barrel_hltIter3FromL1_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIterL3OISeedsFromL2Muons_E                       = cms.untracked.vdouble(PU180to200Endcap_hltIterL3OI_ScaleMean)
    # process.ntupler.mvaScaleStdHltIterL3OISeedsFromL2Muons_E                        = cms.untracked.vdouble(PU180to200Endcap_hltIterL3OI_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter0IterL3MuonPixelSeedsFromPixelTracks_E       = cms.untracked.vdouble(PU180to200Endcap_hltIter0_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter0IterL3MuonPixelSeedsFromPixelTracks_E        = cms.untracked.vdouble(PU180to200Endcap_hltIter0_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter2IterL3MuonPixelSeeds_E                      = cms.untracked.vdouble(PU180to200Endcap_hltIter2_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter2IterL3MuonPixelSeeds_E                       = cms.untracked.vdouble(PU180to200Endcap_hltIter2_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter3IterL3MuonPixelSeeds_E                      = cms.untracked.vdouble(PU180to200Endcap_hltIter3_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter3IterL3MuonPixelSeeds_E                       = cms.untracked.vdouble(PU180to200Endcap_hltIter3_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E = cms.untracked.vdouble(PU180to200Endcap_hltIter0FromL1_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_E  = cms.untracked.vdouble(PU180to200Endcap_hltIter0FromL1_ScaleStd)
    process.ntupler.mvaScaleMeanHltIter2IterL3FromL1MuonPixelSeeds_E                = cms.untracked.vdouble(HLTTDR_v3_Endcap_NThltIter2FromL1_ScaleMean)
    process.ntupler.mvaScaleStdHltIter2IterL3FromL1MuonPixelSeeds_E                 = cms.untracked.vdouble(HLTTDR_v3_Endcap_NThltIter2FromL1_ScaleStd)
    # process.ntupler.mvaScaleMeanHltIter3IterL3FromL1MuonPixelSeeds_E                = cms.untracked.vdouble(PU180to200Endcap_hltIter3FromL1_ScaleMean)
    # process.ntupler.mvaScaleStdHltIter3IterL3FromL1MuonPixelSeeds_E                 = cms.untracked.vdouble(PU180to200Endcap_hltIter3FromL1_ScaleStd)

    process.TFileService = cms.Service("TFileService",
      fileName = cms.string("ntuple.root"),
      closeFileFast = cms.untracked.bool(False),
    )

    process.ntupler.DebugMode = cms.bool(False)
    process.ntupler.SaveAllTracks = cms.bool(True)
    # process.ntupler.SaveStubs = cms.bool(False)
    process.ntupler.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks") # TTTrack input 
    # process.ntupler.MCTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks")  ## MCTruth input
    # process.ntupler.L1StubInputTag = cms.InputTag("TTStubsFromPhase2TrackerDigis","StubAccepted")
    process.ntupler.TkMuonToken = cms.InputTag("L1TkMuons", "", newProcessName)
    process.ntupler.l1TkPrimaryVertex = cms.InputTag("L1TkPrimaryVertex","")

    # if doDYSkim:
    #     from MuonHLTTool.MuonHLTNtupler.DYmuSkimmer import DYmuSkimmer
    #     process.Skimmer = DYmuSkimmer.clone()
    #     process.mypath = cms.Path(process.Skimmer*process.hltTPClusterProducer*process.hltTrackAssociatorByHits*process.trackAssoSeq*process.ntupler)

    # else:
    #     process.mypath = cms.Path(process.hltTPClusterProducer*process.hltTrackAssociatorByHits*process.trackAssoSeq*process.ntupler)

    process.mypath    = cms.Path(process.hltTPClusterProducer*process.hltTrackAssociatorByHits*process.trackAssoSeq)
    process.myendpath = cms.EndPath(process.ntupler)

    return process
