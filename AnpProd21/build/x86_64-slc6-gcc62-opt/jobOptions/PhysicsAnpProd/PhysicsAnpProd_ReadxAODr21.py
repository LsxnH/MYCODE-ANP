import os
import AthenaPoolCnvSvc.ReadAthenaPool

import PhysicsAnpProd.PhysicsAnpProdUtils   as Utils
import PhysicsAnpProd.PhysicsAnpProdxAODr21 as AthRead

clog = Utils.getLog(os.path.basename(__file__))

#======================================================================================
if 'EvtMax' in dir():
    theApp.EvtMax = EvtMax
else:
    theApp.EvtMax = -1

if 'inputDir' in dir():
    svcMgr.EventSelector.InputCollections += Utils.findInputFilesInDir(inputDir)
elif 'inputFile' in dir():
    if type(inputFile) == type([]):
        for ifile in inputFile:
            if os.path.isfile(ifile):
                svcMgr.EventSelector.InputCollections += [ifile]
    if type(inputFile) == type(''):
        if os.path.isfile(inputFile):
            svcMgr.EventSelector.InputCollections += [inputFile]
elif os.path.isdir('local_input'):
    svcMgr.EventSelector.InputCollections += Utils.findInputFilesInDir('local_input')

else:
    print 'Missing input files - OK for pathena'

if not hasattr(svcMgr, 'AthenaEventLoopMg'):
    from AthenaServices.AthenaServicesConf import AthenaEventLoopMgr
    svcMgr += AthenaEventLoopMgr()

svcMgr.AthenaEventLoopMgr.EventPrintoutInterval = 100

if 'dumpSG' in dir():
    StoreGateSvc = Service('StoreGateSvc')
    StoreGateSvc.Dump = dumpSG

svcMgr.MessageSvc.OutputLevel = INFO
svcMgr.MessageSvc.infoLimit = 0

#======================================================================================
if not hasattr(svcMgr, 'THistSvc'):
    from GaudiSvc.GaudiSvcConf import THistSvc
    svcMgr += THistSvc()

if 'outFile' not in dir():
    outFile = 'out.root'

svcMgr.THistSvc.Output += ["out DATAFILE='%s' OPT='RECREATE'" %outFile]

theAuditorSvc = svcMgr.AuditorSvc
theAuditorSvc.Auditors  += ["ChronoAuditor"]

svcMgr.ChronoStatSvc.PrintUserTime     = True
svcMgr.ChronoStatSvc.PrintSystemTime   = False
svcMgr.ChronoStatSvc.PrintEllapsedTime = False
theApp.AuditAlgorithms = True

#======================================================================================
#from RecExConfig.InputFilePeeker import inputFileSummary

stream_name = '' #Utils.getItemFromInputSummary(inputFileSummary, 'stream_names', 0)
evt_type    = '' #Utils.getItemFromInputSummary(inputFileSummary, 'evt_type',     0)    
option      = 'IS_SIMULATION'

if 'IS_DATA' in dir():
    option = 'IS_DATA'

if 'doDetails' in dir() and doDetails:
    option += 'doDetails'

if 'doConv' in dir() and doConv:
    option += 'doConv'

if 'mcSubCampaign' not in dir():
    mcSubCampaign = 'mc16a'

clog.info('stream_name: %s' %stream_name)
clog.info('evt_type: %s' %evt_type)

#======================================================================================
# Configure object and event tools
#
ToolSvc += CfgMgr.TrigConf__xAODConfigTool("TrigConfig", OutputLevel = WARNING) 
trig_decision_tool = CfgMgr.Trig__TrigDecisionTool('TrigDecisionTool', ConfigTool = ToolSvc.TrigConfig, TrigDecisionKey = 'xTrigDecision')
ToolSvc += trig_decision_tool

trig_match_muon_tool = CfgMgr.Ath__TrigMatch('trigMatch')
trig_match_muon_tool.TriggerTool = trig_decision_tool
ToolSvc += trig_match_muon_tool

algSeq = CfgMgr.AthSequencer('AthAlgSeq')

#======================================================================================
# Configure reader algorithms
#
alg_data_list = [AthRead.getReadEvent(CfgMgr, ToolSvc, option, trig_decision_tool, mcSubCampaign)]

if option.count('IS_DATA') == 0:
    if option.count('doDetails'): alg_data_list += [AthRead.getReadSimpleTruth (CfgMgr, 'readSimpleTruth',  'm_mc_part_', 'm_mc_vtx_', option)]
    else:                         alg_data_list += [AthRead.getReadPhysicsTruth(CfgMgr, 'readPhysicsTruth', 'm_mc_part_', '',          option)]

if option.count('doDetails'):
    alg_data_list += [AthRead.getReadIDTrack    (CfgMgr,          'InDetTrackParticles', 'm_id_track_',  option)]
    alg_data_list += [AthRead.getReadIDTrack    (CfgMgr,          'GSFTrackParticles',   'm_gsf_track_', option)]
    alg_data_list += [AthRead.getReadTrackJet   (CfgMgr, ToolSvc, 'AntiKt4PV0TrackJets', 'm_track_jet_', option)]
    alg_data_list += [AthRead.getReadCaloCluster(CfgMgr,          'CaloCalTopoClusters', 'm_clust_',     option)]

if option.count('doConv'):
    alg_data_list += [AthRead.getReadPhoton     (CfgMgr, ToolSvc, 'Photons',             'm_photon_',    option)]

alg_data_list += [AthRead.getReadElec(CfgMgr, ToolSvc, 'Electrons',           'm_elec_',      option)]
alg_data_list += [AthRead.getReadMuon(CfgMgr, ToolSvc, 'Muons',               'm_muon_',      option, trig_match_muon_tool)]
alg_data_list += [AthRead.getReadJet (CfgMgr, ToolSvc, 'AntiKt4EMTopo',       'm_jet_',       option)]

alg_data_list += [AthRead.getFillMET(CfgMgr, ToolSvc, prefix='MET',      input_elec='m_elec_', input_muon='m_muon_',                     option=option)]
alg_data_list += [AthRead.getFillOR (CfgMgr, ToolSvc, prefix='ORHFJets', input_elec='m_elec_', input_muon='m_muon_', input_jet='m_jet_', option=option)]

for alg_data in alg_data_list:
    algSeq += alg_data.athena_alg

#======================================================================================
# Configure writer algorithm
#
algSeq += AthRead.getSaveAlg(ToolSvc, CfgMgr, alg_data_list)

print algSeq
print ToolSvc
