'''
Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
'''

#================================================================================================
#  Definitions
#================================================================================================
name    = 'L1EG_Unpacked'
dirName = 'multicrab_'+name

dataset = {
    'SingleElectron_2017B': '/SingleElectron/Run2017B-17Nov2017-v1/MINIAOD',
    'SingleElectron_2017C': '/SingleElectron/Run2017C-17Nov2017-v1/MINIAOD',
    'SingleElectron_2017D': '/SingleElectron/Run2017D-17Nov2017-v1/MINIAOD',
    'SingleElectron_2017E': '/SingleElectron/Run2017E-17Nov2017-v1/MINIAOD',
    'SingleElectron_2017F': '/SingleElectron/Run2017F-17Nov2017-v1/MINIAOD',
}
eventsPerJob = {
    'SingleElectron_2017B': 15000,
    'SingleElectron_2017C': 15000,
    'SingleElectron_2017D': 15000,
    'SingleElectron_2017E': 15000,
    'SingleElectron_2017F': 15000,
    }
listOfSamples = [
#    'SingleElectron_2017B',
#    'SingleElectron_2017C',
#    'SingleElectron_2017D',
    'SingleElectron_2017E',
    'SingleElectron_2017F',
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
    config.Data.lumiMask      = 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
    # Lumi Mask taken from:  '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
    
    #================================================================================================
    # Site Section: Contains the Grid site parameters (incl. stage out information)
    #================================================================================================
    config.section_("Site")
    config.Site.storageSite = 'T3_US_FNALLPC'
    
    listOfSamples.reverse()
    
    for sample in listOfSamples:
      config.General.requestName   = sample
      config.Data.inputDataset     = dataset[sample]
#      config.Data.useParent       = True   # Needed for L1 Emulator (or grandparent?)
      config.Data.unitsPerJob      = eventsPerJob[sample]
      config.Data.outputDatasetTag = sample
      p = Process(target=submit, args=(config,))
      p.start()
      p.join()
