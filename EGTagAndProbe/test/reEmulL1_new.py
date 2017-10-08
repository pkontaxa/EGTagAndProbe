import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

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
process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')


options = VarParsing.VarParsing ('analysis')
#options.register ('secondaryFilesList','',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "List of secondary input files")

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
options.maxEvents  = 1000

options.parseArguments()

# START ELECTRON CUT BASED ID SECTION
#
# Set up everything that is needed to compute electron IDs and
# add the ValueMaps with ID decisions into the event data stream
#

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
    process.GlobalTag.globaltag = '92X_dataRun2_Prompt_v8' #'90X_dataRun2_v0'  #'92X_dataRun2_Prompt_v8'

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
                 '/store/data/Run2017C/SingleElectron/MINIAOD/PromptReco-v3/000/300/777/00000/C499093F-BA7E-E711-9F4D-02163E013897.root'
                #'/store/data/Run2017B/SingleElectron/MINIAOD/PromptReco-v1/000/297/050/00000/166F7BB0-3C56-E711-BD8B-02163E0145C5.root'
                #'/store/data/Run2017B/SingleElectron/MINIAOD/PromptReco-v1/000/297/057/00000/94987913-A256-E711-A484-02163E01A391.root' 
                ),

            secondaryFileNames = cms.untracked.vstring('/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/06506BFA-FB7C-E711-B01B-02163E01A2A1.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/0CEB47FF-FB7C-E711-9BB5-02163E011E6F.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/24153D18-FC7C-E711-913C-02163E01A708.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/724E931C-FC7C-E711-8A9C-02163E012118.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/7AE81D09-FC7C-E711-B76A-02163E019B73.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/A42EC9FC-FB7C-E711-8935-02163E0133E0.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/B48FEC08-FC7C-E711-8344-02163E011C48.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/C67421FB-FB7C-E711-A22D-02163E019BC5.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/CA10D321-FC7C-E711-BB02-02163E0125F5.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/CA125336-FC7C-E711-ADFA-02163E013820.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/CC031C16-FC7C-E711-8E27-02163E0144EC.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/CE296BF9-FB7C-E711-88A1-02163E01341D.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/CE3E5B03-FC7C-E711-9171-02163E01A469.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/CE8E0824-FC7C-E711-8F04-02163E014330.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/D631951E-0B7D-E711-83D3-02163E0143E5.root',
'/store/data/Run2017C/SingleElectron/RAW/v1/000/300/777/00000/DE7D7A17-FC7C-E711-A5D0-02163E01A6F3.root',

)



            #secondaryFileNames = cms.untracked.vstring('file:AA918EB1-6E64-E611-9BE0-00259074AE54.root')
            #'/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/50000/302E52FC-8567-E611-B2AA-0CC47A703326.root',
            #),
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/6E300626-5E26-E611-980B-02163E0119A2.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/08F68A47-5D26-E611-B042-02163E012239.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/1011D344-5E26-E611-ABC4-02163E011CF0.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/1E3EFD43-5E26-E611-AE17-02163E0146FF.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/2EA6473B-5E26-E611-B82A-02163E011EAC.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/3CD7BB24-5D26-E611-88A3-02163E014736.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/3CE74444-5E26-E611-8CE6-02163E012545.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/488D1A44-5E26-E611-8057-02163E014285.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/5EECA846-5D26-E611-A99C-02163E01432B.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/7C7FB848-5E26-E611-8A06-02163E014167.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/86E8DC25-5D26-E611-9827-02163E014713.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/A4B22F44-5E26-E611-AFDA-02163E0141F3.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/BA326B3B-5E26-E611-A6E0-02163E0124FA.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/BADC0417-5D26-E611-872F-02163E012A7E.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/C813CA24-5E26-E611-B7A2-02163E011F93.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/E251C323-5E26-E611-825D-02163E011A0F.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/E8FD1844-5E26-E611-B99E-02163E0146CB.root',
            #            '/store/data/Run2016B/SingleMuon/RAW/v2/000/274/199/00000/F8B44816-5E26-E611-A87A-02163E011E74.root',
            #        ) 
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
    #process.GlobalTag.globaltag = 'auto:run2_mc' #MC 25 ns miniAODv2
    process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_v14'
    #process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2' #MC 25 ns miniAODv2
    # process.GlobalTag.globaltag = '76X_dataRun2_16Dec2015_v0'
    process.load('EGTagAndProbe.EGTagAndProbe.MCanalysis_cff')
    process.source = cms.Source("PoolSource",
            fileNames = cms.untracked.vstring(
                #'/store/mc/RunIISpring16DR80/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/40000/AA918EB1-6E64-E611-9BE0-00259074AE54.root'
                '/store/mc/RunIISpring16MiniAODv2/GluGluHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU20to70HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/50000/1A13CB76-9B67-E611-A143-0050560210EC.root'
                ),
            secondaryFileNames = cms.untracked.vstring(listSecondaryFiles)
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/00000/08D2C535-5458-E511-B0C0-FA163E83549A.root'
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/10000/8A2D3925-4658-E511-80B2-02163E014126.root',
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/10000/ECB7FC03-8058-E511-BE9D-02163E0141A2.root',
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/4473DFF5-9456-E511-9C4B-002590494C8A.root',
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/587A9A92-A956-E511-AC52-0025904B11CC.root',
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/7076052C-4A57-E511-B371-00259074AE9A.root',
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/7CD6A6C7-9C56-E511-87E5-003048C75840.root',
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/7E281C8E-4357-E511-8498-00259074AE80.root',
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/98884797-4957-E511-82C6-00259073E504.root',
            #'/store/mc/RunIISummer15GS/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM/MCRUN2_71_V1-v1/60000/BE274E99-4957-E511-88ED-0025907A1A2E.root',

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

process.load("L1Trigger.L1TCalorimeter.caloStage2Params_2017_v1_8_3_updateHFSF_v7MET_cfi")

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
       # process.patTriggerSeq        
        )
process.schedule = cms.Schedule(process.p) # do my sequence pls

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Adding ntuplizer
process.TFileService=cms.Service('TFileService',fileName=cms.string(options.outputFile))
