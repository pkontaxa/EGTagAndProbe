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
process = cms.Process("TagAndProbe",eras.Run2_2017)
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

# Define which IDs we want to produce
# Each of these two example IDs contains all four standard 
my_id_modules =[
'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                 # recommended for both 50 and 25 ns
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns, triggering still to come
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',    # 25 ns trig
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',    # 50 ns trig
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',   #Spring16
'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',   #Spring16 HZZ

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

if not isMC: # will use 80X
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = '100X_dataRun2_v1'  #'94X_dataRun2_v2' #'90X_dataRun2_v0'  #'92X_dataRun2_Prompt_v8'

#Martin's addition (not necessary for me)

    #process.GlobalTag.toGet = cms.VPSet(
     #       cms.PSet(record = cms.string("EcalTPGLinearizationConstRcd"),
      #          tag = cms.string("EcalTPGLinearizationConst_IOV_280026_beginning_at_1"),
       #         connect =cms.string('sqlite_file:/home/llr/cms/novoa/PedestalCond/EcalTPG_280026_moved_to_1_Ped_161310.db')),
        #    cms.PSet(record = cms.string("EcalTPGPedestalsRcd"),
         #       tag = cms.string("EcalTPGPedestals_280026_beginning_at_1"),
          #      connect =cms.string('sqlite_file:/home/llr/cms/novoa/PedestalCond/EcalTPG_280026_moved_to_1_Ped_161310.db')))

    process.load('EGTagAndProbe.EGTagAndProbe.tagAndProbe_cff')
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
            '/store/data/Run2017F/SingleElectron/MINIAOD/17Nov2017-v1/50000/0014F790-FDE0-E711-A3E0-FA163E1B87FE.root',
            ),
                                secondaryFileNames = cms.untracked.vstring(
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/306/454/00000/A013486D-5BC5-E711-9D85-02163E01A2D4.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/306/125/00000/6E0E1CEB-16C2-E711-B6D0-02163E01A463.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/862/00000/909C68D2-7DBD-E711-9CC4-02163E011C76.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/862/00000/8C61620D-7EBD-E711-8632-02163E01A760.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/814/00000/FA30763E-E9BB-E711-9690-02163E0138BE.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/814/00000/EECE8647-EDBB-E711-BEC4-02163E011FBF.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/814/00000/ACA0D835-E1BB-E711-9B65-02163E01467B.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/814/00000/A64F648A-FDBB-E711-9135-02163E013765.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/814/00000/9C8BD8F8-01BC-E711-B285-02163E011884.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/814/00000/6C599230-E1BB-E711-90AB-02163E019BE1.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/814/00000/486CB205-02BC-E711-BD97-02163E019BB5.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/814/00000/369E27C9-E0BB-E711-8E35-02163E01442D.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/814/00000/182B4730-E1BB-E711-93C0-02163E014251.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/766/00000/969EAA15-DABA-E711-A3FB-02163E013399.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/636/00001/981452C1-0FBA-E711-9BC5-02163E019B3B.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/636/00001/64754484-0FBA-E711-8C69-02163E019BC0.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/636/00001/42C31672-0FBA-E711-8F1C-02163E013473.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/636/00001/2E83F474-0FBA-E711-96E4-02163E019E02.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/636/00001/1036B781-0FBA-E711-AE0A-02163E01A70A.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/636/00001/0881ED67-0FBA-E711-91C6-02163E014737.root',
            '/store/data/Run2017F/SingleElectron/RAW/v1/000/305/636/00000/625FF10E-0EBA-E711-96C8-02163E019C94.root',
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
    process.GlobalTag.globaltag = '100X_mcRun2_asymptotic_v2'
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

process.load("L1Trigger.L1TCalorimeter.caloStage2Params_2017_v1_8_4_cfi")

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
