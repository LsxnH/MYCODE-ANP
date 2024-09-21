import AthenaPoolCnvSvc.ReadAthenaPool
import os

if 'EvtMax' in dir():
    theApp.EvtMax = EvtMax
else:
    theApp.EvtMax = -1
    

if 'inputDir' in dir():
    for f in os.listdir(inputDir):
        svcMgr.EventSelector.InputCollections += ['%s/%s' %(inputDir, f)]

elif 'inputFile' in dir() and os.path.isfile(inputFile):
    svcMgr.EventSelector.InputCollections += [inputFile]

else:
    print 'Missing input files - OK for pathena'

if not hasattr(svcMgr, 'AthenaEventLoopMg'):
    from AthenaServices.AthenaServicesConf import AthenaEventLoopMgr
    svcMgr += AthenaEventLoopMgr()

svcMgr.AthenaEventLoopMgr.EventPrintoutInterval = 100

if 'dumpSG' in dir():
    StoreGateSvc = Service('StoreGateSvc')
    StoreGateSvc.Dump = dumpSG

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
import PhysicsAth.PhysicsAthReadFxAOD as AthRead

trig_decision_tool = CfgMgr.Trig__TrigDecisionTool('TrigDecisionTool', TrigDecisionKey = 'xTrigDecision')
ToolSvc += trig_decision_tool

trig_match_muon_tool = CfgMgr.Ath__TrigMatch('trigMatch')
trig_match_muon_tool.TriggerTool = trig_decision_tool
ToolSvc += trig_match_muon_tool

algSeq = CfgMgr.AthSequencer('AthAlgSeq')

algSeq += AthRead.getReadEvent       (CfgMgr, ToolSvc, trig_decision_tool)
algSeq += AthRead.getReadJets        (CfgMgr, ToolSvc, 'AntiKt4EMTopoJets',   'm_jet_')
algSeq += AthRead.getReadElec        (CfgMgr, ToolSvc, 'Electrons',           'm_electron_')
algSeq += AthRead.getReadMuon        (CfgMgr, ToolSvc, 'Muons',               'm_muon_',     trig_match_muon_tool)
algSeq += AthRead.getReadSimpleTruth (CfgMgr, option='')

write_tool = AthRead.getWriteTool(ToolSvc, CfgMgr, 'writeEvent', option='')
save_event = CfgMgr.Ath__SaveEvent()
save_event.writeEvent = write_tool

algSeq += save_event

print ToolSvc
