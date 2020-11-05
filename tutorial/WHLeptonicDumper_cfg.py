import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import os
from flashgg.MetaData.MetaConditionsReader import *

# ========================================================================
# Standard configuration setting
process = cms.Process("FLASHggSyst")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.maxEvents   = cms.untracked.PSet( input  = cms.untracked.int32( 10 ) )
process.options     = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1 )

process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring(
'file:myMicroAODOutputFile_numEvent1000.root'
                             )
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("test.root"))


from flashgg.MetaData.JobConfig import customize

customize.options.register('ignoreNegR9',
                           True,
                           VarParsing.VarParsing.multiplicity.singleton,
                           VarParsing.VarParsing.varType.bool,
                           'ignoreNegR9'
                           )

# set default options if needed
customize.setDefault("maxEvents",300)
customize.setDefault("targetLumi",1.00e+3)
customize.parse()
customize.metaConditions = MetaConditionsReader(customize.metaConditions)

### Global Tag
from Configuration.AlCa.GlobalTag import GlobalTag
if customize.processId == "Data": process.GlobalTag.globaltag = str(customize.metaConditions['globalTags']['data'])
else: process.GlobalTag.globaltag = str(customize.metaConditions['globalTags']['MC'])


#========================================================================================
### Set WHLeptnic Producer
process.load('flashgg.Taggers.flashggWHLeptonicSequence_cfi')
from flashgg.Taggers.flashggWHLeptonicSequence_cfi import *
process.flashggWHLeptonicSequence = flashggPrepareWHLeptonicSequence( process, customize.metaConditions )
process.flashggWHLeptonic.leadPhoOverMassThreshold = cms.double(0.25)
process.flashggWHLeptonic.METThreshold             = cms.double(45)

### Systematics customize
from flashgg.Systematics.SystematicsCustomize import *
#jetSystematicsInputTags = createStandardSystematicsProducers(process,customize)
#modifyTagSequenceForSystematics(process,jetSystematicsInputTags,2)

process.load('flashgg.Systematics.flashggDiPhotonSystematics_cfi')
import flashgg.Systematics.flashggDiPhotonSystematics_cfi as diPhotons_syst
diPhotons_syst.setupDiPhotonSystematics( process, customize )
process.flashggPreselectedDiPhotons.src = cms.InputTag('flashggDiPhotonSystematics')

#Using standard tools
useEGMTools(process)

#==============================================================================================
### WHLeptonic Dumper setting
from   flashgg.Taggers.tagsDumpers_cfi   import createTagDumper
process.load('flashgg.Taggers.WHLeptonicDumper_cff')
process.WHLeptonicDumper.className = "CutBasedWHLeptonicTagDumper"
process.WHLeptonicDumper.dumpTrees     = True
process.WHLeptonicDumper.dumpHistos    = False
process.WHLeptonicDumper.dumpWorkspace = False
process.WHLeptonicDumper.src = "flashggWHLeptonic"
process.WHLeptonicDumper.nameTemplate = cms.untracked.string("$PROCESS_$SQRTS_$CLASSNAME_$SUBCAT_$LABEL")

# ===============================================================================================

# Set variables in N-tuples
wh_variables = [
    "dipho_mass             := diPhoton.mass",
    "dipho_leadPt           := diPhoton.leadingPhoton.pt",
    "dipho_leadEta          := diPhoton.leadingPhoton.eta",
    "dipho_leadPhi          := diPhoton.leadingPhoton.phi",
    "dipho_leadE            := diPhoton.leadingPhoton.energy",
    "dipho_leadIDMVA        := diPhoton.leadingView.phoIdMvaWrtChosenVtx",
    "dipho_subleadPt        := diPhoton.subLeadingPhoton.pt",
    "dipho_subleadEta       := diPhoton.subLeadingPhoton.eta",
    "dipho_subleadPhi       := diPhoton.subLeadingPhoton.phi",
    "dipho_subleadE         := diPhoton.subLeadingPhoton.energy",
    "dipho_subleadIDMVA     := diPhoton.subLeadingView.phoIdMvaWrtChosenVtx",

    "n_ele                  := electrons.size",
    "ele1_Pt                := ?(electrons.size>0)? electrons.at(0).pt               : -999",
    "ele1_Eta               := ?(electrons.size>0)? electrons.at(0).eta              : -999",
    "ele1_Phi               := ?(electrons.size>0)? electrons.at(0).phi              : -999",
    "ele1_E                 := ?(electrons.size>0)? electrons.at(0).energy           : -999",
    "ele2_Pt                := ?(electrons.size>1)? electrons.at(1).pt               : -999",
    "ele2_Eta               := ?(electrons.size>1)? electrons.at(1).eta              : -999",
    "ele2_Phi               := ?(electrons.size>1)? electrons.at(1).phi              : -999",
    "ele2_E                 := ?(electrons.size>1)? electrons.at(1).energy           : -999",

    "met_Pt                 := met.getCorPt()",
    "met_Phi                := met.getCorPhi()"

]

#wh_variables = [
#    "n_jets      := jets.size"
#]
#
#njet = 3
#for i in range(njet):
#    wh_variables.append( "jet%d_Pt  := ?(jets.size>%d)? jets.at(%d).pt      : -999" % (i+1, i, i))
#    wh_variables.append( "jet%d_Eta := ?(jets.size>%d)? jets.at(%d).eta     : -999" % (i+1, i, i))
#    wh_variables.append( "jet%d_Phi := ?(jets.size>%d)? jets.at(%d).phi     : -999" % (i+1, i, i))
#    wh_variables.append( "jet%d_E   := ?(jets.size>%d)? jets.at(%d).energy  : -999" % (i+1, i, i))
#    wh_variables.append( "jet%d_deepbtag   := ?(jets.size>%d)? jets.at(%d).bDiscriminator('pfDeepCSVJetTags:probb') + jets.at(%d).bDiscriminator('pfDeepCSVJetTags:probbb') : -999" % (i+1, i, i, i) )

# Set category
cats = [
    ("WHLeptonicTag","1",0)
]

import flashgg.Taggers.dumperConfigTools as cfgTools

cfgTools.addCategories(process.WHLeptonicDumper,
                       cats,
                       variables  = wh_variables,
                       histograms = []
)

### Final path
process.p = cms.Path(  process.flashggDifferentialPhoIdInputsCorrection
                     * process.flashggDiPhotonSystematics
                     * process.flashggUnpackedJets
                     * process.flashggWHLeptonicSequence
                     * process.WHLeptonicDumper
                     )


# call the customization
customize(process)
