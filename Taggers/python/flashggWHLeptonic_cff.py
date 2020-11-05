import FWCore.ParameterSet.Config as cms
from flashgg.MicroAOD.flashggJets_cfi import UnpackedJetCollectionVInputTag

flashggWHLeptonic = cms.EDProducer("FlashggWHLeptonicTagProducer",
                                    DiPhotonTag                 = cms.InputTag('flashggPreselectedDiPhotons'),
                                    SystLabel                   = cms.string(""),
                                    ElectronTag                 = cms.InputTag('flashggSelectedElectrons'),
                                    MuonTag                     = cms.InputTag('flashggSelectedMuons'),
                                    inputTagJets                = UnpackedJetCollectionVInputTag,
                                    METTag                      = cms.InputTag('flashggMets'),
                                    VertexTag                   = cms.InputTag('offlineSlimmedPrimaryVertices'),
                                    MVAResultTag                = cms.InputTag('flashggDiPhotonMVA'),
                                    leadPhoOverMassThreshold    = cms.double(0.25),
                                    subleadPhoOverMassThreshold = cms.double(0.2),
                                    PhoMVAThreshold             = cms.double(-0.4),
                                    electronPtThreshold         = cms.double(15),
                                    electronEtaThresholds       = cms.vdouble(1.4442, 1.566, 2.5),
                                    deltaRPhoElectronThreshold  = cms.double(0.2),
                                    DeltaRTrkElec               = cms.double(0.2),
                                    deltaMassElectronZThreshold = cms.double(10.),
                                    muonPtThreshold             = cms.double(15),
                                    muonEtaThreshold            = cms.double(2.4),
                                    muPFIsoSumRelThreshold      = cms.double(0.25),
                                    deltaRMuonPhoThreshold      = cms.double(0.2),
                                    METThreshold                = cms.double(30.)
                                    )
