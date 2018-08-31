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
isMC = False
isMINIAOD = True
process = cms.Process("TagAndProbe", eras.Run2_2018)  # Marina
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')


options = VarParsing.VarParsing ('analysis')
#options.register ('secondaryFilesList','',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "List of secondary input files")

options.register ('skipEvents',
        -1,                                            # Defaul  = -1
        VarParsing.VarParsing.multiplicity.singleton,  # Options = [singleton, list]
        VarParsing.VarParsing.varType.int,             # Options = [string, int, float]
        "Number of events to skip")
options.register ('JSONfile',
        "",                                            # Default = -1
        VarParsing.VarParsing.multiplicity.singleton,  # Options = [singleton, list]
        VarParsing.VarParsing.varType.string,          # Options = [string, int, float]
        "JSON file (empty for no JSON)")
options.outputFile = 'NTuple.root'
options.inputFiles = []
options.maxEvents  = -999

options.parseArguments()


#========================================
# START ELECTRON CUT BASED ID SECTION
#========================================
# Set up everything that is needed to compute electron IDs and
# add the ValueMaps with ID decisions into the event data stream

# Load tools and function definitions
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

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

# Marina
# Define which IDs we want to produce
# Each of these two example IDs contains all four standard 
my_id_modules =[
#'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
#'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                 # recommended for both 50 and 25 ns
#'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns, triggering still to come
#'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',    # 25 ns trig
#'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',    # 50 ns trig
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',   #Spring16
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',   #Spring16 HZZ
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',     # Fall17
]


#Add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)


egmMod = 'egmGsfElectronIDs'
mvaMod = 'electronMVAValueMapProducer'
regMod = 'electronRegressionValueMapProducer'
egmSeq = 'egmGsfElectronIDSequence'
setattr(process,egmMod,process.egmGsfElectronIDs.clone())
setattr(process,mvaMod,process.electronMVAValueMapProducer.clone())
setattr(process,regMod,process.electronRegressionValueMapProducer.clone())
setattr(process,egmSeq,cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod)))
process.electrons = cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod))

#process.load('EGTagAndProbe.EGTagAndProbe.triggerProducer_cfi')

import FWCore.Utilities.FileUtils as FileUtils
#listSecondaryFiles = FileUtils.loadListFromFile (options.secondaryFilesList)

# Marina
if not isMC: # will use 80X
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = '101X_dataRun2_Prompt_v9'

#Martin's addition (not necessary for me)

    #process.GlobalTag.toGet = cms.VPSet(
     #       cms.PSet(record = cms.string("EcalTPGLinearizationConstRcd"),
      #          tag = cms.string("EcalTPGLinearizationConst_IOV_280026_beginning_at_1"),
       #         connect =cms.string('sqlite_file:/home/llr/cms/novoa/PedestalCond/EcalTPG_280026_moved_to_1_Ped_161310.db')),
        #    cms.PSet(record = cms.string("EcalTPGPedestalsRcd"),
         #       tag = cms.string("EcalTPGPedestals_280026_beginning_at_1"),
          #      connect =cms.string('sqlite_file:/home/llr/cms/novoa/PedestalCond/EcalTPG_280026_moved_to_1_Ped_161310.db')))

    # Marina
    process.load('EGTagAndProbe.EGTagAndProbe.tagAndProbe_cff')
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
            '/store/data/Run2018A/EGamma/MINIAOD/PromptReco-v1/000/315/255/00000/2C278415-5B4B-E811-9447-FA163E62E0F4.root',
            ),
                                secondaryFileNames = cms.untracked.vstring(
            '/store/data/Run2018A/EGamma/RAW/v1/000/315/255/00000/32C5B2BE-9549-E811-AE24-02163E019FC7.root',
            '/store/data/Run2018A/EGamma/RAW/v1/000/315/255/00000/7651A54B-9649-E811-9404-FA163E0417AC.root',
            '/store/data/Run2018A/EGamma/RAW/v1/000/315/255/00000/AE346DEC-9449-E811-844F-FA163E048F61.root',
            '/store/data/Run2018A/EGamma/RAW/v1/000/315/255/00000/B24FCA9D-9449-E811-B8A1-FA163E94857D.root',
            '/store/data/Run2018A/EGamma/RAW/v1/000/315/255/00000/C87B6B65-9449-E811-A252-FA163E92F260.root',
            ),
                                )
    #process.source.eventsToProcess = cms.untracked.VEventRange('281613:108:12854629')
    #process.source.eventsToProcess = cms.untracked.VEventRange('274199:353:670607108')

########################################## Addition for Ntuples ###################################### 
if isMINIAOD:
       process.Ntuplizer.electrons = cms.InputTag("slimmedElectrons")
       process.Ntuplizer.genParticles = cms.InputTag("prunedGenParticles")
       process.Ntuplizer.Vertices = cms.InputTag("offlineSlimmedPrimaryVertices")      
      # process.Ntuplizer.triggerSet = cms.InputTag("slimmedPatTrigger","","RECO")
######################################################################################################

else:
    process.GlobalTag.globaltag = '101X_mcRun2_asymptotic_v5'
    process.load('EGTagAndProbe.EGTagAndProbe.MCanalysis_cff')
    process.source = cms.Source("PoolSource",
            fileNames = cms.untracked.vstring(
                '/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/50000/1A13CB76-9B67-E611-A143-0050560210EC.root'
                ),
            )

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

# Marina
process.load("L1Trigger.L1TCalorimeter.caloParams_2018_v1_2_cfi")

#### handling of cms line options for tier3 submission
#### the following are dummy defaults, so that one can normally use the config changing file list by hand etc.



if options.JSONfile:
    print "Using JSON: " , options.JSONfile
    process.source.lumisToProcess = LumiList.LumiList(filename = options.JSONfile).getVLuminosityBlockRange()

if options.inputFiles:
    process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(-1)
        )

if options.maxEvents >= -1:
    process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if options.skipEvents >= 0:
    process.source.skipEvents = cms.untracked.uint32(options.skipEvents)

process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(True)
        )

 
process.p = cms.Path (
        process.electrons +
        process.RawToDigi +
        process.L1TReEmul +
        process.NtupleSeq #+
        #process.patTriggerSeq        
        )


'''
## Pantelis
process.p = cms.Path(process.electrons)
print("after process.electrons")
process.p = cms.Path(process.RawToDigi)
print("after process.RawToDigi")
process.p = cms.Path(process.L1TReEmul)
print("after process.L1TReEmul")
process.p = cms.Path(process.NtupleSeq)
print("after process.NtupleSeq")
'''


process.schedule = cms.Schedule(process.p) # do my sequence pls

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))
