'''
Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
'''

#================================================================================================
#  Definitions
#================================================================================================
name    = 'L1EG_TurnOn'
dirName = 'multicrab_'+name

dataset = {
    'SingleElectron_2017A_v2': '/SingleElectron/Run2017A-PromptReco-v2/MINIAOD',
    'SingleElectron_2017A_v3': '/SingleElectron/Run2017A-PromptReco-v3/MINIAOD',
    'SingleElectron_2017B_v1': '/SingleElectron/Run2017B-PromptReco-v1/MINIAOD',
    'SingleElectron_2017B_v2': '/SingleElectron/Run2017B-PromptReco-v2/MINIAOD',
    'SingleElectron_2017C_v1': '/SingleElectron/Run2017C-PromptReco-v1/MINIAOD',
    'SingleElectron_2017C_v2': '/SingleElectron/Run2017C-PromptReco-v2/MINIAOD',
    'SingleElectron_2017C_v3': '/SingleElectron/Run2017C-PromptReco-v3/MINIAOD',
    'SingleElectron_2017D_v1': '/SingleElectron/Run2017D-PromptReco-v1/MINIAOD',
    'SingleElectron_2017E_v1': '/SingleElectron/Run2017E-PromptReco-v1/MINIAOD',
    'SingleElectron_2017F_v1': '/SingleElectron/Run2017F-PromptReco-v1/MINIAOD',
}
eventsPerJob = {
    'SingleElectron_2017A_v2': 15000,
    'SingleElectron_2017A_v3': 15000,
    'SingleElectron_2017B_v1': 15000,
    'SingleElectron_2017B_v2': 15000,
    'SingleElectron_2017C_v1': 15000,
    'SingleElectron_2017C_v2': 15000,
    'SingleElectron_2017C_v3': 15000,
    'SingleElectron_2017D_v1': 15000,
    'SingleElectron_2017E_v1': 15000,
    'SingleElectron_2017F_v1': 15000,
    }
listOfSamples = [
    'SingleElectron_2017A_v2',
    'SingleElectron_2017A_v3',
    'SingleElectron_2017B_v1',
    'SingleElectron_2017B_v2',
    'SingleElectron_2017C_v1',
    'SingleElectron_2017C_v2',
    'SingleElectron_2017C_v3',
    'SingleElectron_2017D_v1',
    'SingleElectron_2017E_v1',
    'SingleElectron_2017F_v1',
   ]


if __name__ == '__main__':
    
    #============================================================================================
    #  Import Modules
    #============================================================================================
    from WMCore.Configuration import Configuration
    from CRABClient.UserUtilities import getUsernameFromSiteDB
    from CRABAPI.RawCommand import crabCommand
    from multiprocessing import Process
    
    config = Configuration()

    def submit(config):
        res = crabCommand('submit', config = config)
    
    #================================================================================================
    # General Section: The user specifies generic parameters about the request (e.g. request name).
    #================================================================================================ 
    config.section_("General")
    config.General.workArea        = dirName
    config.General.transferOutputs = True
    config.General.transferLogs    = True
    
    #================================================================================================
    # JobType Section: Contains all the parameters of the user job type and related configurables
    #================================================================================================
    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName   = 'test.py'    # Options = ['reEmulL1_new.py', 'test.py']
    
    #================================================================================================
    # Data Section: Contains all parameters related to the data to be analyzed (incl. splitting params)
    #================================================================================================
    config.section_("Data")
    config.Data.inputDBS      = 'global'
    config.Data.outLFNDirBase = '/store/user/%s/CRAB3_TransferData/L1EG' % (getUsernameFromSiteDB())
    config.Data.splitting     = 'EventAwareLumiBased'
    config.Data.publication   = False
    config.Data.totalUnits    = -1    
    config.Data.lumiMask      = 'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
    # Lumi Mask taken from:  '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
    
    #================================================================================================
    # Site Section: Contains the Grid site parameters (incl. stage out information)
    #================================================================================================
    config.section_("Site")
    config.Site.storageSite = 'T3_US_FNALLPC'
    
    listOfSamples.reverse()
    
    for sample in listOfSamples:
      config.General.requestName = sample
      config.Data.inputDataset   = dataset[sample]
#      config.Data.useParent      = True   # Needed for L1 Emulator (or grandparent?)
      config.Data.unitsPerJob    = eventsPerJob[sample]
      config.Data.outputDatasetTag = sample
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()
