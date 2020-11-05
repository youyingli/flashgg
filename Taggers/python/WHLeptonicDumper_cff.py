import FWCore.ParameterSet.Config as cms

from flashgg.Taggers.tagsDumpConfig_cff import tagsDumpConfig

WHLeptonicDumper = cms.EDAnalyzer('CutBasedWHLeptonicTagDumper',
                 **tagsDumpConfig.parameters_())
