import AthenaPoolCnvSvc.ReadAthenaPool
import PhysicsAnpProd.PhysicsAnpProdUtils as utils
import os

if 'EvtMax' in dir():
    theApp.EvtMax = EvtMax
else:
    theApp.EvtMax = -1

clog = utils.getLog(os.path.basename(__file__))

if 'inputDir' in dir():
    for f in os.listdir(inputDir):
        svcMgr.EventSelector.InputCollections += ['%s/%s' %(inputDir, f)]

elif 'inputFile' in dir() and os.path.isfile(inputFile):
    svcMgr.EventSelector.InputCollections += [inputFile]

elif os.path.isdir('local_input'):
    svcMgr.EventSelector.InputCollections += utils.findInputFilesInDir('local_input')
    
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
theAuditorSvc.Auditors  += [ "ChronoAuditor"]

svcMgr.ChronoStatSvc.PrintUserTime     = True
svcMgr.ChronoStatSvc.PrintSystemTime   = False
svcMgr.ChronoStatSvc.PrintEllapsedTime = False
theApp.AuditAlgorithms = True

#======================================================================================
from RecExConfig.InputFilePeeker import inputFileSummary

stream_name = utils.getItemFromInputSummary(inputFileSummary, 'stream_names', 0)
evt_type    = utils.getItemFromInputSummary(inputFileSummary, 'evt_type',     0)    
option      = '%s' %evt_type

print 'stream_name: ', stream_name
print 'evt_type: ', evt_type

#======================================================================================
import PhysicsAnpProd.PhysicsAnpProdxAODHIGG3 as AthRead

trig_decision_tool = CfgMgr.Trig__TrigDecisionTool('TrigDecisionTool', TrigDecisionKey = 'xTrigDecision')
ToolSvc += trig_decision_tool

trig_match_muon_tool = CfgMgr.Ath__TrigMatch('trigMatch')
trig_match_muon_tool.TriggerTool = trig_decision_tool
ToolSvc += trig_match_muon_tool

algSeq = CfgMgr.AthSequencer('AthAlgSeq')

algSeq += AthRead.getReadEvent(CfgMgr, ToolSvc, trig_decision_tool)
algSeq += AthRead.getReadJets (CfgMgr, ToolSvc, 'AntiKt4EMTopoJets',  option)
algSeq += AthRead.getReadElec (CfgMgr, ToolSvc, 'Electrons',          option)
algSeq += AthRead.getReadMuon (CfgMgr, ToolSvc, 'Muons',              option, trig_match_muon_tool)
algSeq += AthRead.getFillOR   (CfgMgr, ToolSvc, 'HFJets',             option)
algSeq += AthRead.getFillMET  (CfgMgr, ToolSvc, 'MET',                option)

if evt_type != 'IS_DATA':
    if 'simpleTruth' in dir(): algSeq += AthRead.getReadSimpleTruth (CfgMgr, option='')
    else:                      algSeq += AthRead.getReadPhysicsTruth(CfgMgr, option='')

write_tool = AthRead.getWriteTool(ToolSvc, CfgMgr, 'writeEvent', option='mc_vtx %s' %evt_type)
save_event = CfgMgr.Ath__SaveEvent()
save_event.writeEvent = write_tool

algSeq += save_event

print ToolSvc
print algSeq
