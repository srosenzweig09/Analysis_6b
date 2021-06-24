import CRABClient
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.section_("JobType")
config.section_("Data")
config.section_("Site")
config.section_("User")
config.section_("Debug")

config.General.requestName     = '6jet_classifier_training'
config.General.workArea        = '6jet_classifier_training_202106XX'
config.General.transferOutputs = True
config.General.transferLogs    = False
# config.General.failureLimit    = <parameter-value>
config.General.instance        = 'prod' # Mandatory
# config.General.activity        = <parameter-value>

config.JobType.pluginName                       = 'PrivateMC' # Mandatory
# config.JobType.psetName                         = <parameter-value>
# config.JobType.generator                        = <parameter-value>
# config.JobType.pyCfgParams                      = <parameter-value>
config.JobType.inputFiles                       = ['scripts/scriptExe.sh, scripts/train_nn.py, signal/skimmed/NMSSM_XYH_YToHH_6b_MX_700_MY_400_training_set_skimmed.root']
# config.JobType.disableAutomaticOutputCollection = <parameter-value>
# config.JobType.outputFiles                      = <parameter-value>
# config.JobType.eventsPerLumi                    = <parameter-value>
# config.JobType.allowUndistributedCMSSW          = <parameter-value>
config.JobType.maxMemoryMB                      = 3500
# config.JobType.maxJobRuntimeMin                 = <parameter-value>
# config.JobType.numCores                         = <parameter-value>
# config.JobType.priority                         = <parameter-value>
config.JobType.scriptExe                        = 'crab/scriptExe.sh'
# config.JobType.scriptArgs                       = <parameter-value>
# config.JobType.sendPythonFolder                 = <parameter-value>
# config.JobType.sendExternalFolder               = <parameter-value>
# config.JobType.externalPluginFile               = <parameter-value>


# config.Data.inputDataset              = <parameter-value>
# config.Data.allowNonValidInputDataset = <parameter-value>
# config.Data.outputPrimaryDataset      = <parameter-value>
# config.Data.inputDBS                  = <parameter-value>
config.Data.splitting                 = 'FileBased'
config.Data.unitsPerJob               = 1
config.Data.totalUnits                = 2
# config.Data.useParent                 = <parameter-value>
# config.Data.secondaryInputDataset     = <parameter-value>
# config.Data.lumiMask                  = <parameter-value>
# config.Data.runRange                  = <parameter-value>
config.Data.outLFNDirBase             = '/eos/user/s/srosenzw/Projects/sixb/'
config.Data.publication               = False
# config.Data.publishDBS                = <parameter-value>
config.Data.outputDatasetTag          = '6jet_classifier_training'
# config.Data.publishWithGroupName      = <parameter-value>
# config.Data.ignoreLocality            = <parameter-value>
# config.Data.userInputFiles            = <parameter-value>

config.Site.storageSite           = 'T2_US_Florida' # Mandatory
# config.Site.whitelist             = <parameter-value>
# config.Site.blacklist             = <parameter-value>
# config.Site.ignoreGlobalBlackList = <parameter-value>

# config.User.voGroup = <parameter-value>
# config.User.voRole  = <parameter-value>

# config.Debug.oneEventMode = <parameter-value>
# config.Debug.asoConfig    = <parameter-value>
# config.Debug.scheddName   = <parameter-value>
# config.Debug.extraJDL     = <parameter-value>
# config.Debug.collector    = <parameter-value>
