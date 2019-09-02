// -- ntuple maker for Muon HLT study
// -- author: Kyeongpil Lee (Seoul National University, kplee@cern.ch)

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/L1Trigger/interface/Muon.h"
#include "DataFormats/Luminosity/interface/LumiDetails.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/MuonReco/interface/MuonTrackLinks.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositFwd.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidateFwd.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidateIsolation.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Scalers/interface/LumiScalers.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "HLTrigger/HLTcore/interface/HLTEventAnalyzerAOD.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

#include "DataFormats/TrajectorySeed/interface/TrajectorySeed.h"
#include "DataFormats/TrajectorySeed/interface/TrajectorySeedCollection.h"
#include "DataFormats/TrajectorySeed/interface/PropagationDirection.h"
#include "DataFormats/TrajectoryState/interface/PTrajectoryStateOnDet.h"
#include "DataFormats/TrajectoryState/interface/LocalTrajectoryParameters.h"

#include "TTree.h"

using namespace std;
using namespace reco;
using namespace edm;

class MuonHLTNtupler : public edm::EDAnalyzer
{
public:
  MuonHLTNtupler(const edm::ParameterSet &iConfig);
  virtual ~MuonHLTNtupler() {};

  virtual void analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup);
  virtual void beginJob();
  virtual void endJob();
  virtual void beginRun(const edm::Run &iRun, const edm::EventSetup &iSetup);
  virtual void endRun(const edm::Run &iRun, const edm::EventSetup &iSetup);

private:
  void Init();
  void Make_Branch();
  void Fill_HLT(const edm::Event &iEvent, bool isMYHLT);
  void Fill_Muon(const edm::Event &iEvent);
  void Fill_HLTMuon(const edm::Event &iEvent);
  void Fill_L1Muon(const edm::Event &iEvent);
  void Fill_GenParticle(const edm::Event &iEvent);

  //For Rerun (Fill_IterL3*)
  void Fill_IterL3(const edm::Event &iEvent);
  void Fill_Seed(const edm::Event &iEvent);

  bool SavedTriggerCondition( std::string& pathName );
  bool SavedFilterCondition( std::string& filterName );

  bool isNewHighPtMuon(const reco::Muon& muon, const reco::Vertex& vtx);

  edm::EDGetTokenT< std::vector<reco::Muon> >                t_offlineMuon_;
  edm::EDGetTokenT< reco::VertexCollection >                 t_offlineVertex_;
  edm::EDGetTokenT< edm::TriggerResults >                    t_triggerResults_;
  edm::EDGetTokenT< trigger::TriggerEvent >                  t_triggerEvent_;
  edm::EDGetTokenT< edm::TriggerResults >                    t_myTriggerResults_;
  edm::EDGetTokenT< trigger::TriggerEvent >                  t_myTriggerEvent_;

  edm::EDGetTokenT< reco::RecoChargedCandidateCollection >   t_L3Muon_;
  edm::EDGetTokenT< reco::RecoChargedCandidateCollection >   t_L2Muon_;
  edm::EDGetTokenT< l1t::MuonBxCollection >                  t_L1Muon_;
  edm::EDGetTokenT< reco::RecoChargedCandidateCollection >   t_TkMuon_;

  edm::EDGetTokenT< std::vector<reco::MuonTrackLinks> >      t_iterL3OI_;
  edm::EDGetTokenT< std::vector<reco::MuonTrackLinks> >      t_iterL3IOFromL2_;
  edm::EDGetTokenT< std::vector<reco::MuonTrackLinks> >      t_iterL3FromL2_;
  edm::EDGetTokenT< std::vector<reco::Track> >               t_iterL3IOFromL1_;
  edm::EDGetTokenT< std::vector<reco::Muon> >                t_iterL3MuonNoID_;
  edm::EDGetTokenT< std::vector<reco::Muon> >                t_iterL3Muon_;

  edm::EDGetTokenT< TrajectorySeedCollection >               t_hltIterL3OISeedsFromL2Muons_;
  edm::EDGetTokenT< TrajectorySeedCollection >               t_hltIter0IterL3MuonPixelSeedsFromPixelTracks_;
  edm::EDGetTokenT< TrajectorySeedCollection >               t_hltIter2IterL3MuonPixelSeeds_;
  edm::EDGetTokenT< TrajectorySeedCollection >               t_hltIter3IterL3MuonPixelSeeds_;
  edm::EDGetTokenT< TrajectorySeedCollection >               t_hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_;
  edm::EDGetTokenT< TrajectorySeedCollection >               t_hltIter2IterL3FromL1MuonPixelSeeds_;
  edm::EDGetTokenT< TrajectorySeedCollection >               t_hltIter3IterL3FromL1MuonPixelSeeds_;

  edm::EDGetTokenT< std::vector<reco::Track> >               t_hltIterL3OIMuonTrack_;
  edm::EDGetTokenT< std::vector<reco::Track> >               t_hltIter0IterL3MuonTrack_;
  edm::EDGetTokenT< std::vector<reco::Track> >               t_hltIter2IterL3MuonTrack_;
  edm::EDGetTokenT< std::vector<reco::Track> >               t_hltIter3IterL3MuonTrack_;
  edm::EDGetTokenT< std::vector<reco::Track> >               t_hltIter0IterL3FromL1MuonTrack_;
  edm::EDGetTokenT< std::vector<reco::Track> >               t_hltIter2IterL3FromL1MuonTrack_;
  edm::EDGetTokenT< std::vector<reco::Track> >               t_hltIter3IterL3FromL1MuonTrack_;

  edm::EDGetTokenT< LumiScalersCollection >                  t_lumiScaler_;
  edm::EDGetTokenT< LumiScalersCollection >                  t_offlineLumiScaler_;
  edm::EDGetTokenT< std::vector<PileupSummaryInfo> >         t_PUSummaryInfo_;
  edm::EDGetTokenT< GenEventInfoProduct >                    t_genEventInfo_;
  edm::EDGetTokenT< reco::GenParticleCollection >            t_genParticle_;

  TTree *ntuple_;
  static const int arrSize_ = 2000;

  // -- general event information
  bool isRealData_;
  int runNum_;
  int lumiBlockNum_;
  unsigned long long eventNum_;

  int nVertex_;

  double bunchID_;
  double instLumi_;
  double dataPU_;
  double dataPURMS_;
  double bunchLumi_;
  double offlineInstLumi_;
  double offlineDataPU_;
  double offlineDataPURMS_;
  double offlineBunchLumi_;
  int truePU_;
  double genEventWeight_;

  // -- generator level particles (only MC)
  int nGenParticle_;
  int genParticle_ID_[arrSize_];
  int genParticle_status_[arrSize_];
  int genParticle_mother_[arrSize_];

  double genParticle_pt_[arrSize_];
  double genParticle_eta_[arrSize_];
  double genParticle_phi_[arrSize_];
  double genParticle_px_[arrSize_];
  double genParticle_py_[arrSize_];
  double genParticle_pz_[arrSize_];
  double genParticle_energy_[arrSize_];
  double genParticle_charge_[arrSize_];

  int genParticle_isPrompt_[arrSize_];
  int genParticle_isPromptFinalState_[arrSize_];
  int genParticle_isTauDecayProduct_[arrSize_];
  int genParticle_isPromptTauDecayProduct_[arrSize_];
  int genParticle_isDirectPromptTauDecayProductFinalState_[arrSize_];
  int genParticle_isHardProcess_[arrSize_];
  int genParticle_isLastCopy_[arrSize_];
  int genParticle_isLastCopyBeforeFSR_[arrSize_];
  int genParticle_isPromptDecayed_[arrSize_];
  int genParticle_isDecayedLeptonHadron_[arrSize_];
  int genParticle_fromHardProcessBeforeFSR_[arrSize_];
  int genParticle_fromHardProcessDecayed_[arrSize_];
  int genParticle_fromHardProcessFinalState_[arrSize_];
  int genParticle_isMostlyLikePythia6Status3_[arrSize_];

  // -- trigger info.
  vector< std::string > vec_firedTrigger_;
  vector< std::string > vec_filterName_;
  vector< double > vec_HLTObj_pt_;
  vector< double > vec_HLTObj_eta_;
  vector< double > vec_HLTObj_phi_;

  vector< std::string > vec_myFiredTrigger_;
  vector< std::string > vec_myFilterName_;
  vector< double > vec_myHLTObj_pt_;
  vector< double > vec_myHLTObj_eta_;
  vector< double > vec_myHLTObj_phi_;

  class tmpTSOD {
  private:
    uint32_t TSODDetId;
    float TSODPt;
    float TSODX;
    float TSODY;
    float TSODDxdz;
    float TSODDydz;
    float TSODPx;
    float TSODPy;
    float TSODPz;
    float TSODqbp;
    int TSODCharge;
  public:
    void SetTmpTSOD(const PTrajectoryStateOnDet TSODIn) {
      TSODDetId = TSODIn.detId();
      TSODPt = TSODIn.pt();
      TSODX = TSODIn.parameters().position().x();
      TSODY = TSODIn.parameters().position().y();
      TSODDxdz = TSODIn.parameters().dxdz();
      TSODDydz = TSODIn.parameters().dydz();
      TSODPx = TSODIn.parameters().momentum().x();
      TSODPy = TSODIn.parameters().momentum().y();
      TSODPz = TSODIn.parameters().momentum().z();
      TSODqbp = TSODIn.parameters().qbp();
      TSODCharge = TSODIn.parameters().charge();
    }

    tmpTSOD(const PTrajectoryStateOnDet TSODIn) { SetTmpTSOD(TSODIn); }

    bool operator==(const tmpTSOD& other) const {
      return (
        this->TSODDetId == other.TSODDetId &&
        this->TSODPt == other.TSODPt &&
        this->TSODX == other.TSODX &&
        this->TSODY == other.TSODX &&
        this->TSODDxdz == other.TSODDxdz &&
        this->TSODDydz == other.TSODDydz &&
        this->TSODPx == other.TSODPx &&
        this->TSODPy == other.TSODPy &&
        this->TSODPz == other.TSODPz &&
        this->TSODqbp == other.TSODqbp &&
        this->TSODCharge == other.TSODCharge
      );
    }

    bool operator<(const tmpTSOD& other) const {
      return (this->TSODPt!=other.TSODPt) ? (this->TSODPt < other.TSODPt) : (this->TSODDetId < other.TSODDetId);
    }
  };

  // -- offline muon
  int nMuon_;

  double muon_pt_[arrSize_];
  double muon_eta_[arrSize_];
  double muon_phi_[arrSize_];
  double muon_px_[arrSize_];
  double muon_py_[arrSize_];
  double muon_pz_[arrSize_];
  double muon_dB_[arrSize_];
  double muon_charge_[arrSize_];
  int muon_isGLB_[arrSize_];
  int muon_isSTA_[arrSize_];
  int muon_isTRK_[arrSize_];
  int muon_isPF_[arrSize_];
  int muon_isTight_[arrSize_];
  int muon_isMedium_[arrSize_];
  int muon_isLoose_[arrSize_];
  int muon_isHighPt_[arrSize_];
  int muon_isHighPtNew_[arrSize_];
  int muon_isSoft_[arrSize_];

  double muon_iso03_sumPt_[arrSize_];
  double muon_iso03_hadEt_[arrSize_];
  double muon_iso03_emEt_[arrSize_];

  double muon_PFIso03_charged_[arrSize_];
  double muon_PFIso03_neutral_[arrSize_];
  double muon_PFIso03_photon_[arrSize_];
  double muon_PFIso03_sumPU_[arrSize_];

  double muon_PFIso04_charged_[arrSize_];
  double muon_PFIso04_neutral_[arrSize_];
  double muon_PFIso04_photon_[arrSize_];
  double muon_PFIso04_sumPU_[arrSize_];

  double muon_PFCluster03_ECAL_[arrSize_];
  double muon_PFCluster03_HCAL_[arrSize_];

  double muon_PFCluster04_ECAL_[arrSize_];
  double muon_PFCluster04_HCAL_[arrSize_];

  double muon_normChi2_global_[arrSize_];
  int muon_nTrackerHit_global_[arrSize_];
  int muon_nTrackerLayer_global_[arrSize_];
  int muon_nPixelHit_global_[arrSize_];
  int muon_nMuonHit_global_[arrSize_];

  double muon_normChi2_inner_[arrSize_];
  int muon_nTrackerHit_inner_[arrSize_];
  int muon_nTrackerLayer_inner_[arrSize_];
  int muon_nPixelHit_inner_[arrSize_];

  double muon_pt_tuneP_[arrSize_];
  double muon_ptError_tuneP_[arrSize_];

  double muon_dxyVTX_best_[arrSize_];
  double muon_dzVTX_best_[arrSize_];

  int muon_nMatchedStation_[arrSize_];
  int muon_nMatchedRPCLayer_[arrSize_];
  int muon_stationMask_[arrSize_];

  std::map<tmpTSOD,unsigned int> MuonIterSeedMap;

  // -- L3 muon
  int nL3Muon_;
  double L3Muon_pt_[arrSize_];
  double L3Muon_eta_[arrSize_];
  double L3Muon_phi_[arrSize_];
  double L3Muon_charge_[arrSize_];
  double L3Muon_trkPt_[arrSize_];

  // -- L2 muon
  int nL2Muon_;
  double L2Muon_pt_[arrSize_];
  double L2Muon_eta_[arrSize_];
  double L2Muon_phi_[arrSize_];
  double L2Muon_charge_[arrSize_];
  double L2Muon_trkPt_[arrSize_];

  // -- L1 muon
  int nL1Muon_;
  double L1Muon_pt_[arrSize_];
  double L1Muon_eta_[arrSize_];
  double L1Muon_phi_[arrSize_];
  double L1Muon_charge_[arrSize_];
  double L1Muon_quality_[arrSize_];

  // -- Tracker muon
  int nTkMuon_;
  double TkMuon_pt_[arrSize_];
  double TkMuon_eta_[arrSize_];
  double TkMuon_phi_[arrSize_];
  double TkMuon_charge_[arrSize_];
  double TkMuon_trkPt_[arrSize_];

  // -- iterL3 object from outside-in step
  int    nhltIterL3OIMuonTrack_;
  double hltIterL3OIMuonTrack_pt_[arrSize_];
  double hltIterL3OIMuonTrack_eta_[arrSize_];
  double hltIterL3OIMuonTrack_phi_[arrSize_];
  double hltIterL3OIMuonTrack_charge_[arrSize_];

  int    nIterL3OI_;
  double iterL3OI_inner_pt_[arrSize_];
  double iterL3OI_inner_eta_[arrSize_];
  double iterL3OI_inner_phi_[arrSize_];
  double iterL3OI_inner_charge_[arrSize_];
  double iterL3OI_outer_pt_[arrSize_];
  double iterL3OI_outer_eta_[arrSize_];
  double iterL3OI_outer_phi_[arrSize_];
  double iterL3OI_outer_charge_[arrSize_];
  double iterL3OI_global_pt_[arrSize_];
  double iterL3OI_global_eta_[arrSize_];
  double iterL3OI_global_phi_[arrSize_];
  double iterL3OI_global_charge_[arrSize_];

  // -- iterL3 object from inside-out step (from L2)
  int    nhltIter0IterL3MuonTrack_;
  double hltIter0IterL3MuonTrack_pt_[arrSize_];
  double hltIter0IterL3MuonTrack_eta_[arrSize_];
  double hltIter0IterL3MuonTrack_phi_[arrSize_];
  double hltIter0IterL3MuonTrack_charge_[arrSize_];
  int    nhltIter2IterL3MuonTrack_;
  double hltIter2IterL3MuonTrack_pt_[arrSize_];
  double hltIter2IterL3MuonTrack_eta_[arrSize_];
  double hltIter2IterL3MuonTrack_phi_[arrSize_];
  double hltIter2IterL3MuonTrack_charge_[arrSize_];
  int    nhltIter3IterL3MuonTrack_;
  double hltIter3IterL3MuonTrack_pt_[arrSize_];
  double hltIter3IterL3MuonTrack_eta_[arrSize_];
  double hltIter3IterL3MuonTrack_phi_[arrSize_];
  double hltIter3IterL3MuonTrack_charge_[arrSize_];

  int    nIterL3IOFromL2_;
  double iterL3IOFromL2_inner_pt_[arrSize_];
  double iterL3IOFromL2_inner_eta_[arrSize_];
  double iterL3IOFromL2_inner_phi_[arrSize_];
  double iterL3IOFromL2_inner_charge_[arrSize_];
  double iterL3IOFromL2_outer_pt_[arrSize_];
  double iterL3IOFromL2_outer_eta_[arrSize_];
  double iterL3IOFromL2_outer_phi_[arrSize_];
  double iterL3IOFromL2_outer_charge_[arrSize_];
  double iterL3IOFromL2_global_pt_[arrSize_];
  double iterL3IOFromL2_global_eta_[arrSize_];
  double iterL3IOFromL2_global_phi_[arrSize_];
  double iterL3IOFromL2_global_charge_[arrSize_];

  // -- iterL3 object from outside-in + inside-out step (from L2)
  int    nIterL3FromL2_;
  double iterL3FromL2_inner_pt_[arrSize_];
  double iterL3FromL2_inner_eta_[arrSize_];
  double iterL3FromL2_inner_phi_[arrSize_];
  double iterL3FromL2_inner_charge_[arrSize_];
  double iterL3FromL2_outer_pt_[arrSize_];
  double iterL3FromL2_outer_eta_[arrSize_];
  double iterL3FromL2_outer_phi_[arrSize_];
  double iterL3FromL2_outer_charge_[arrSize_];
  double iterL3FromL2_global_pt_[arrSize_];
  double iterL3FromL2_global_eta_[arrSize_];
  double iterL3FromL2_global_phi_[arrSize_];
  double iterL3FromL2_global_charge_[arrSize_];

  // -- iterL3 object from inside-out step (from L1)
  int    nhltIter0IterL3FromL1MuonTrack_;
  double hltIter0IterL3FromL1MuonTrack_pt_[arrSize_];
  double hltIter0IterL3FromL1MuonTrack_eta_[arrSize_];
  double hltIter0IterL3FromL1MuonTrack_phi_[arrSize_];
  double hltIter0IterL3FromL1MuonTrack_charge_[arrSize_];
  int    nhltIter2IterL3FromL1MuonTrack_;
  double hltIter2IterL3FromL1MuonTrack_pt_[arrSize_];
  double hltIter2IterL3FromL1MuonTrack_eta_[arrSize_];
  double hltIter2IterL3FromL1MuonTrack_phi_[arrSize_];
  double hltIter2IterL3FromL1MuonTrack_charge_[arrSize_];
  int    nhltIter3IterL3FromL1MuonTrack_;
  double hltIter3IterL3FromL1MuonTrack_pt_[arrSize_];
  double hltIter3IterL3FromL1MuonTrack_eta_[arrSize_];
  double hltIter3IterL3FromL1MuonTrack_phi_[arrSize_];
  double hltIter3IterL3FromL1MuonTrack_charge_[arrSize_];

  int    nIterL3IOFromL1_;
  double iterL3IOFromL1_pt_[arrSize_];
  double iterL3IOFromL1_eta_[arrSize_];
  double iterL3IOFromL1_phi_[arrSize_];
  double iterL3IOFromL1_charge_[arrSize_];

  // -- iterL3 object before applying ID @ HLT
  int nIterL3MuonNoID_;
  double iterL3MuonNoID_pt_[arrSize_];
  double iterL3MuonNoID_eta_[arrSize_];
  double iterL3MuonNoID_phi_[arrSize_];
  double iterL3MuonNoID_charge_[arrSize_];
  int iterL3MuonNoID_isGLB_[arrSize_];
  int iterL3MuonNoID_isSTA_[arrSize_];
  int iterL3MuonNoID_isTRK_[arrSize_];

  // -- iterL3 object after applying ID @ HLT
  int nIterL3Muon_;
  double iterL3Muon_pt_[arrSize_];
  double iterL3Muon_eta_[arrSize_];
  double iterL3Muon_phi_[arrSize_];
  double iterL3Muon_charge_[arrSize_];
  int iterL3Muon_isGLB_[arrSize_];
  int iterL3Muon_isSTA_[arrSize_];
  int iterL3Muon_isTRK_[arrSize_];

  // -- local reco and seeding information
  int      nhltIterL3OISeedsFromL2Muons_;
  int      hltIterL3OISeedsFromL2Muons_dir_[arrSize_];
  uint32_t hltIterL3OISeedsFromL2Muons_tsos_detId_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_pt_[arrSize_];
  int      hltIterL3OISeedsFromL2Muons_tsos_hasErr_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err0_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err1_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err2_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err3_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err4_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err5_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err6_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err7_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err8_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err9_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err10_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err11_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err12_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err13_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_err14_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_x_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_y_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_dxdz_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_dydz_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_px_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_py_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_pz_[arrSize_];
  float   hltIterL3OISeedsFromL2Muons_tsos_qbp_[arrSize_];
  int      hltIterL3OISeedsFromL2Muons_tsos_charge_[arrSize_];
  int hltIterL3OISeedsFromL2Muons_iterL3GlobalRef_[arrSize_];
  int hltIterL3OISeedsFromL2Muons_iterL3InnerRef_[arrSize_];
  int hltIterL3OISeedsFromL2Muons_iterL3OuterRef_[arrSize_];

  int      nhltIter0IterL3MuonPixelSeedsFromPixelTracks_;
  int      hltIter0IterL3MuonPixelSeedsFromPixelTracks_dir_[arrSize_];
  uint32_t hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_detId_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_pt_[arrSize_];
  int      hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_hasErr_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err0_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err1_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err2_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err3_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err4_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err5_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err6_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err7_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err8_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err9_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err10_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err11_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err12_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err13_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_err14_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_x_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_y_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_dxdz_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_dydz_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_px_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_py_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_pz_[arrSize_];
  float   hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_qbp_[arrSize_];
  int      hltIter0IterL3MuonPixelSeedsFromPixelTracks_tsos_charge_[arrSize_];
  int hltIter0IterL3MuonPixelSeedsFromPixelTracks_iterL3GlobalRef_[arrSize_];
  int hltIter0IterL3MuonPixelSeedsFromPixelTracks_iterL3InnerRef_[arrSize_];
  int hltIter0IterL3MuonPixelSeedsFromPixelTracks_iterL3OuterRef_[arrSize_];

  int      nhltIter2IterL3MuonPixelSeeds_;
  int      hltIter2IterL3MuonPixelSeeds_dir_[arrSize_];
  uint32_t hltIter2IterL3MuonPixelSeeds_tsos_detId_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_pt_[arrSize_];
  int      hltIter2IterL3MuonPixelSeeds_tsos_hasErr_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err0_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err1_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err2_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err3_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err4_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err5_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err6_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err7_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err8_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err9_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err10_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err11_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err12_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err13_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_err14_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_x_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_y_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_dxdz_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_dydz_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_px_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_py_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_pz_[arrSize_];
  float   hltIter2IterL3MuonPixelSeeds_tsos_qbp_[arrSize_];
  int      hltIter2IterL3MuonPixelSeeds_tsos_charge_[arrSize_];
  int hltIter2IterL3MuonPixelSeeds_iterL3GlobalRef_[arrSize_];
  int hltIter2IterL3MuonPixelSeeds_iterL3InnerRef_[arrSize_];
  int hltIter2IterL3MuonPixelSeeds_iterL3OuterRef_[arrSize_];

  int      nhltIter3IterL3MuonPixelSeeds_;
  int      hltIter3IterL3MuonPixelSeeds_dir_[arrSize_];
  uint32_t hltIter3IterL3MuonPixelSeeds_tsos_detId_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_pt_[arrSize_];
  int      hltIter3IterL3MuonPixelSeeds_tsos_hasErr_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err0_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err1_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err2_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err3_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err4_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err5_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err6_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err7_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err8_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err9_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err10_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err11_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err12_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err13_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_err14_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_x_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_y_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_dxdz_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_dydz_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_px_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_py_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_pz_[arrSize_];
  float   hltIter3IterL3MuonPixelSeeds_tsos_qbp_[arrSize_];
  int      hltIter3IterL3MuonPixelSeeds_tsos_charge_[arrSize_];
  int hltIter3IterL3MuonPixelSeeds_iterL3GlobalRef_[arrSize_];
  int hltIter3IterL3MuonPixelSeeds_iterL3InnerRef_[arrSize_];
  int hltIter3IterL3MuonPixelSeeds_iterL3OuterRef_[arrSize_];

  int      nhltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_;
  int      hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_dir_[arrSize_];
  uint32_t hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_detId_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_pt_[arrSize_];
  int      hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_hasErr_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err0_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err1_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err2_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err3_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err4_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err5_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err6_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err7_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err8_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err9_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err10_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err11_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err12_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err13_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_err14_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_x_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_y_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_dxdz_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_dydz_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_px_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_py_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_pz_[arrSize_];
  float   hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_qbp_[arrSize_];
  int      hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_tsos_charge_[arrSize_];
  int hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_iterL3GlobalRef_[arrSize_];
  int hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_iterL3InnerRef_[arrSize_];
  int hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks_iterL3OuterRef_[arrSize_];

  int      nhltIter2IterL3FromL1MuonPixelSeeds_;
  int      hltIter2IterL3FromL1MuonPixelSeeds_dir_[arrSize_];
  uint32_t hltIter2IterL3FromL1MuonPixelSeeds_tsos_detId_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_pt_[arrSize_];
  int      hltIter2IterL3FromL1MuonPixelSeeds_tsos_hasErr_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err0_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err1_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err2_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err3_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err4_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err5_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err6_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err7_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err8_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err9_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err10_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err11_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err12_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err13_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_err14_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_x_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_y_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_dxdz_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_dydz_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_px_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_py_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_pz_[arrSize_];
  float   hltIter2IterL3FromL1MuonPixelSeeds_tsos_qbp_[arrSize_];
  int      hltIter2IterL3FromL1MuonPixelSeeds_tsos_charge_[arrSize_];
  int hltIter2IterL3FromL1MuonPixelSeeds_iterL3GlobalRef_[arrSize_];
  int hltIter2IterL3FromL1MuonPixelSeeds_iterL3InnerRef_[arrSize_];
  int hltIter2IterL3FromL1MuonPixelSeeds_iterL3OuterRef_[arrSize_];

  int      nhltIter3IterL3FromL1MuonPixelSeeds_;
  int      hltIter3IterL3FromL1MuonPixelSeeds_dir_[arrSize_];
  uint32_t hltIter3IterL3FromL1MuonPixelSeeds_tsos_detId_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_pt_[arrSize_];
  int      hltIter3IterL3FromL1MuonPixelSeeds_tsos_hasErr_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err0_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err1_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err2_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err3_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err4_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err5_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err6_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err7_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err8_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err9_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err10_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err11_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err12_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err13_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_err14_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_x_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_y_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_dxdz_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_dydz_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_px_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_py_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_pz_[arrSize_];
  float   hltIter3IterL3FromL1MuonPixelSeeds_tsos_qbp_[arrSize_];
  int      hltIter3IterL3FromL1MuonPixelSeeds_tsos_charge_[arrSize_];
  int hltIter3IterL3FromL1MuonPixelSeeds_iterL3GlobalRef_[arrSize_];
  int hltIter3IterL3FromL1MuonPixelSeeds_iterL3InnerRef_[arrSize_];
  int hltIter3IterL3FromL1MuonPixelSeeds_iterL3OuterRef_[arrSize_];
};
