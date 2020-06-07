#=====================================
# User Imports
#=====================================
import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

#=====================================
# Options
#=====================================
isMC          = False
isMINIAOD     = True
year          = "2018"
globalTagMC   = "110X_mcRun2_asymptotic_v6"
globalTagData = "110X_dataRun2_v12" 
caloParams    = "caloParams_2018_v1_2"

if year == "2016":
    process = cms.Process("TagAndProbe", eras.Run2_2016)
elif year == "2017":
    process = cms.Process("TagAndProbe", eras.Run2_2017)
else:
    process = cms.Process("TagAndProbe", eras.Run2_2018)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
if year == "2016":
    process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
else:
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')


options = VarParsing.VarParsing ('analysis')
options.register ('secondaryFilesList','',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,  "List of secondary input files")

options.register ('skipEvents',
                  -1, # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Number of events to skip")
options.register ('JSONfile',
                  "", # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "JSON file (empty for no JSON)")
options.outputFile = 'NTuple.root'
options.inputFiles = []
options.maxEvents  = -999

options.parseArguments()

#import FWCore.Utilities.FileUtils as FileUtils
#listSecondaryFiles = FileUtils.loadListFromFile (options.secondaryFilesList)
 
# START ELECTRON CUT BASED ID SECTION
#
# Set up everything that is needed to compute electron IDs and
# add the ValueMaps with ID decisions into the event data stream
#

# Load tools and function definitions
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

from RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi import *
from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry

process.load("RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi")

#**********************
dataFormat = DataFormat.AOD
if isMINIAOD:
    dataFormat = DataFormat.MiniAOD
switchOnVIDElectronIdProducer(process, dataFormat)
#**********************

process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
# overwrite a default parameter: for miniAOD, the collection name is a slimmed one
if isMINIAOD:
    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('slimmedElectrons')

from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)

# Define which IDs we want to produce
# Each of these two example IDs contains all four standard 
my_id_modules =[
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff'
] 


#Add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

from RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi import *

egmGsfElectronIDTask = cms.Task(
    #electronMVAVariableHelper,
    electronMVAValueMapProducer,
    egmGsfElectronIDs
)
egmGsfElectronIDSequence = cms.Sequence(egmGsfElectronIDTask)

if not isMC:
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = globalTagData
    process.load('EGTagAndProbe.EGTagAndProbe.tagAndProbe_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            '/store/data/Run2018D/EGamma/MINIAOD/22Jan2019-v2/110000/10A4CCCC-3FB2-7F4B-841C-926A03DFBC61.root'
        ),

        secondaryFileNames = cms.untracked.vstring(
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/233/00000/7A7B417B-969F-E811-9CC0-FA163EC80159.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/233/00000/9012D37D-969F-E811-913B-FA163EAF7E70.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/414/00000/004596BD-BBA2-E811-A445-FA163EB5B1F7.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/414/00000/C603AEE4-BBA2-E811-AE3E-FA163EFF1C10.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/887/00000/4210A02C-83AA-E811-A2FC-FA163E6CD89F.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/887/00000/18A5473E-82AA-E811-816D-02163E014BB9.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/887/00000/102E6C7D-7FAA-E811-892E-FA163ED1C998.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/414/00000/F21A0D70-BBA2-E811-A608-FA163EAEFBE1.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/414/00000/E675C0A9-BBA2-E811-810D-FA163E5ACC8E.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/233/00000/A8C98583-969F-E811-B653-FA163E8E54FF.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/887/00000/50D37695-81AA-E811-8B09-FA163E3116C8.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/887/00000/5E4E4A7C-7FAA-E811-B494-FA163E8A6FB6.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/887/00000/F404327D-81AA-E811-B1EF-FA163E818EF8.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/887/00000/F847F781-7FAA-E811-BF05-FA163EC968BB.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/325/057/00000/66BBB3F2-EB2F-7746-A8FE-3C865C2E652E.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/325/057/00000/4A0AB096-D0D7-524C-A5C1-69A429C5F609.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/233/00000/1C47877C-969F-E811-830E-FA163E346E5B.root',
	'/store/data/Run2018D/EGamma/RAW/v1/000/321/887/00000/4618ECCB-81AA-E811-8EAF-FA163E22EC2E.root'
	)
    )

else:
    process.GlobalTag.globaltag = globalTagMC  #'106X_mcRun2_asymptotic_preVFP_v5'
    process.load('EGTagAndProbe.EGTagAndProbe.MCanalysis_cff')
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            	#'/store/relval/CMSSW_10_6_8/RelValZEE_13/MINIAODSIM/PU25ns_106X_mcRun2_asymptotic_preVFP_v3_UL16_CP5_preVFP-v1/20000/FEF96392-3307-3B4F-9A4A-3571A8C54F26.root'
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/MINIAODSIM/PU25ns_106X_mcRun2_asymptotic_preVFP_v5_UL16hltval_preVFP_v5-v1/10000/CCB6A88B-A1DE-4044-910A-B548D565AFC4.root'
		#'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/MINIAODSIM/PU25ns_106X_mcRun2_asymptotic_preVFP_v5_UL16hltval_preVFP_v5-v1/10000/8943C7FE-7326-D64E-9D54-B4FB6EE9229D.root',
		#'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/MINIAODSIM/PU25ns_106X_mcRun2_asymptotic_preVFP_v5_UL16hltval_preVFP_v5-v1/10000/362B166F-348C-1948-B1BB-F26AEABED9FB.root'
        ),
       secondaryFileNames = cms.untracked.vstring(
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/A255DD0A-714F-EA11-BCEB-0CC47A4D75EC.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/00FDEC5B-4C4F-EA11-8B31-0025905B85D6.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/10EBA3B3-444F-EA11-9328-AC1F6BAC7D10.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/366241A5-454F-EA11-B7C6-0CC47A4D75F2.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/3EB877C6-494F-EA11-BF42-0CC47A4D7600.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/40E0EA66-484F-EA11-B6E5-0025905A612E.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/4436D4C2-494F-EA11-A1C9-0CC47A4C8F18.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/4A55CE2B-764F-EA11-A940-0CC47A4D76C6.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/F041AF46-4C4F-EA11-A210-0CC47A7452DA.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/D0413658-514F-EA11-A0DA-0025905B85F6.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/EADA2848-614F-EA11-AF89-0025905B8598.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/8CD19F06-664F-EA11-9280-0CC47A4D7628.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/8CD7B387-4D4F-EA11-839A-0025905B85D6.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/BC9CA916-6A4F-EA11-BD3D-AC1F6BAC7C2A.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/EE735DDC-464F-EA11-A8CE-0CC47A7C3408.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/CEF45DE6-7B4F-EA11-B9EF-0CC47A7C354C.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/BC234A3D-494F-EA11-A2D2-0CC47A4C8E28.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/4ABB1E6C-484F-EA11-9F80-0025905A48FC.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/7CA13DCE-864F-EA11-A60C-AC1F6BAC7D14.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/50A5D0F3-644F-EA11-91DC-AC1F6BAC807A.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/5698404B-904F-EA11-89F5-0CC47A4D7646.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/7ADA49E9-414F-EA11-B0E3-AC1F6BAC7C78.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/7E787757-634F-EA11-91F1-0CC47A4D7690.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/8E11FA7C-624F-EA11-9696-0CC47A7C35D8.root',
		'/store/relval/CMSSW_10_6_8/RelValZEE_13UP16/GEN-SIM-RAW/PU25ns_80X_mcRun2_asymptotic_v20_UL16hltval_preVFP_v5-v1/10000/B4732519-6D4F-EA11-867E-0025905B85AE.root'
	)
    )
    process.Ntuplizer.useHLTMatch = cms.bool(False) #In case no HLT object in MC sample considered or you're fed up with trying to find the right HLT collections

if isMINIAOD:
    process.Ntuplizer.electrons = cms.InputTag("slimmedElectrons")
    process.Ntuplizer.genParticles = cms.InputTag("prunedGenParticles")
    process.Ntuplizer.Vertices = cms.InputTag("offlineSlimmedPrimaryVertices")

process.schedule = cms.Schedule()

## L1 emulation stuff

if not isMC:
    from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW 
    process = L1TReEmulFromRAW(process)
else:
    from L1Trigger.Configuration.customiseReEmul import L1TReEmulMCFromRAW
    process = L1TReEmulMCFromRAW(process) 
    from L1Trigger.Configuration.customiseUtils import L1TTurnOffUnpackStage2GtGmtAndCalo 
    process = L1TTurnOffUnpackStage2GtGmtAndCalo(process)


#process.load("L1Trigger.L1TCalorimeter.caloStage2Params_2016_v2_2_cfi")
#process.load("L1Trigger.L1TCalorimeter.caloStage2Params_2016_v3_3_1_2018_EcalSF_cfi")
#process.load("L1Trigger.L1TCalorimeter.caloStage2Params_2016_v3_3_1_2018_EcalSF_EGcalib_cfi")
process.load("L1Trigger.L1TCalorimeter.%s_cfi" % (caloParams))


#### handling of cms line options for tier3 submission
#### the following are dummy defaults, so that one can normally use the config changing file list by hand etc.

if options.JSONfile:
    print "Using JSON: " , options.JSONfile
    process.source.lumisToProcess = LumiList.LumiList(filename = options.JSONfile).getVLuminosityBlockRange()

if options.inputFiles:
    process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

if options.maxEvents >= -1:
    process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if options.skipEvents >= 0:
    process.source.skipEvents = cms.untracked.uint32(options.skipEvents)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.p = cms.Path (
    process.egmGsfElectronIDSequence +
    process.RawToDigi +
    process.L1TReEmul +
    process.NtupleSeq
)
process.schedule = cms.Schedule(process.p) # do my sequence pls

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))
