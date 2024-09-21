
#======================================================================================
def getWriteTool(ToolSvc, CfgMgr, name, stream='out', treename='nominal', option=''):

    mc_prt_vars = ['Status:type=Int',
                   'PDG:type=Int',
                   'Barcode:type=Int',
                   'Mass:type=Float',
                   'Energy:type=Float',
                   'Pt:type=Float',
                   'Eta:type=Float',
                   'Phi:type=Float',
                   'IndexRangeParent:type=VecInt',
                   'IndexRangeChild:type=VecInt',
                   #'IndexRangeSignalParent:type=VecInt',                   
    ]

    mc_vtx_vars = ['Barcode:type=Int',
                   'NParents:type=Int',
                   'NChildren:type=Int',
                   'VtxX:type=Float',
                   'VtxY:type=Float',
                   'VtxZ:type=Float',
                   'IndexRangeParent:type=VecInt',
                   'IndexRangeChild:type=VecInt',
                   ]
 
    met_pass_vars = ['MET_PassSelection:type=Short']
   
    overlap_vars = ['ORHFJets_PassSelection:type=Short', 
                    'ORHFJets_IsRemoved:type=Short']

    elec_vars = ['Pt:type=Float',
                 'PtOrg:type=Float',
                 'Eta:type=Float',
                 'EtaBE2:type=Float',
                 'Phi:type=Float',
                 'Energy:type=Float',
                 'PDG:type=Int',
                 'D0:type=Float',
                 'D0Sig:type=Float',
                 'Z0:type=Float',
                 'Z0Sin:type=Float',
                 'PtVarCone20:type=Float',
                 'PtVarCone30:type=Float',
                 'PtVarCone40:type=Float',
                 'TopoEtCone20:type=Float',
                 'TopoEtCone30:type=Float',
                 'TopoEtCone40:type=Float',
                 'TrackPhi:type=Float',
                 'TrackTheta:type=Float',
                 'TrackPt:type=Float',
                 'ClEta:type=Float',
                 'ClPhi:type=Float',
                 'ClEt:type=Float',
                 'Author:type=Short',
                 'isLooseLH:type=Short',
                 'isLooseLHWithBL:type=Short',
                 'isMediumLH:type=Short',
                 'isTightLH:type=Short',
                 'IsGoodQuality:type=Short',
                 ] + overlap_vars + met_pass_vars
                 
    muon_vars = ['Pt:type=Float',
                 'PtOrg:type=Float',
                 'Eta:type=Float',
                 'Phi:type=Float',
                 'PDG:type=Int',
                 'D0:type=Float',
                 'D0Sig:type=Float',
                 'Z0:type=Float',
                 'Z0Sin:type=Float',
                 'PtVarCone20:type=Float',
                 'PtVarCone30:type=Float',
                 'PtVarCone40:type=Float',
                 'TopoEtCone20:type=Float',
                 'TopoEtCone30:type=Float',
                 'TopoEtCone40:type=Float',
                 'Loose:type=Short',
                 'Medium:type=Short',
                 'Tight:type=Short',
                 'HighPt:type=Short',
                 'PassedID:type=Short',
                 'Quality:type=Short',
                 'MuonType:type=Short',
                 ] + overlap_vars + met_pass_vars

    reco_jet_vars = ['Pt:type=Float',
                     'Eta:type=Float',
                     'Phi:type=Float',
                     'Energy:type=Float',
                     'Mass:type=Float',
                     'MV2c10:type=Float',
                     'JVT:type=Float', 
                     'JVTPass:type=Short',
                     'JVTPassLoose:type=Short',
                     'isLooseBad:type=Short',
                     'isTightBad:type=Short',
                     'ORHFJets_PassBJet:type=Short',
                     'MV2c10_60_Pass:type=Short',
                     'MV2c10_70_Pass:type=Short',
                     'MV2c10_77_Pass:type=Short',
                     'MV2c10_85_Pass:type=Short',
                     ] + overlap_vars

    true_jet_vars = ['Pt:type=Float',
                     'Eta:type=Float',
                     'Phi:type=Float',
                     'GhostPartons_barcode:type=VecInt',
                     'GhostPartons_pdgId:type=VecInt',                     
                     'constituentLinks_barcode:type=VecInt',
                     'constituentLinks_pdgId:type=VecInt']
    
    evt_vars = ['Event:type=Long',
                'Run:type=Int',
                'LumiBlock:type=Int',
                'Year:type=Int',
                'bcid:type=Int',
                'backgroundFlags:type=UInt',
                'MCChannel:type=Int',                
                'ActualInteractions:type=Float',
                'AverageInteractions:type=Float',
                'NRecoVtx:type=Short',
                'HasPriVtx:type=Short',
                'EventFlag_Core:type=Short',
                'ErrorState_Core:type=Short',
                'ErrorState_Background:type=Short',
                'ErrorState_LAr:type=Short',
                'ErrorState_Tile:type=Short',
                'ErrorState_SCT:type=Short',
                'ErrorState_Pixel:type=Short',
                'ErrorState_TRT:type=Short',
                'ErrorState_Muon:type=Short',
                'BeamPosX:type=Float',
                'BeamPosY:type=Float',
                'BeamPosZ:type=Float',
                'BeamPosSigmaX:type=Float',
                'BeamPosSigmaY:type=Float',
                'BeamPosSigmaZ:type=Float',
                ]

    evt_vars += getMETVars('')
    evt_vars += getEventAuxVars()
    
    for trig in getTriggers('Elec'):
        evt_vars  += ['%s:type=Short'       %trig]
        elec_vars += ['match_%s:type=Short' %trig]

    for trig in getTriggers('Muon'):
        evt_vars  += ['%s:type=Short'       %trig]
        muon_vars += ['match_%s:type=Short' %trig]

    for ivar in getIsoVars('Elec'):
        elec_vars += ['iso%s:type=Short' %ivar]

    for ivar in getIsoVars('Muon'):
        muon_vars += ['iso%s:type=Short' %ivar]

    for dvar in getDummyVars():
        evt_vars += ['%s:type=Float' %dvar]

    for evar in getMuonEffCorrTrigTools(None, None, option):
        muon_vars += ['%s:type=Float' %evar]

    if option.count('IS_DATA') == 0:
        reco_jet_vars += ['JVTSF_Eff:type=Float',
                          'JVTSF_Ineff:type=Float',
                          'JVTSF_LooseEff:type=Float',
                          'JVTSF_LooseIneff:type=Float',
                          'MV2c10_60_SF:type=Float',
                          'MV2c10_70_SF:type=Float',
                          'MV2c10_77_SF:type=Float',
                          'MV2c10_85_SF:type=Float',
                          'MV2c10_60_Eff:type=Float',
                          'MV2c10_70_Eff:type=Float',
                          'MV2c10_77_Eff:type=Float',
                          'MV2c10_85_Eff:type=Float',
                          'TruthJetDR:type=Float',
                          'TruthJetPt:type=Float',
                          'TruthJetID:type=Int']

        evt_vars += ['MCWeight:type=Float',
                     'PUWeight:type=Float',
                     'CorrectedMu:type=Float',
                     'RandomRunNumber:type=Int',
                     'RandomYear:type=Short']

        for evar in getElecEffCorrTools(None):
            elec_vars += ['%s:type=Float' %evar]
            
        for evar in getMuonEffCorrRecoTools(None):
            muon_vars += ['%s:type=Float' %evar]

    elec_vars     += getElecAuxVars(option)
    muon_vars     += getMuonAuxVars(option)
    reco_jet_vars += getRJetAuxVars(option)
    true_jet_vars += getTJetAuxVars(option)    

    write_tool = CfgMgr.Ath__WriteEvent(name)
    write_tool.stream     = stream
    write_tool.treename   = treename
    write_tool.keys_event = ','.join(evt_vars)

    write_tool.branches = ['m_jet_|%s'   %(','.join(reco_jet_vars)),
                           'm_elec_|%s'  %(','.join(elec_vars)), 
                           'm_muon_|%s'  %(','.join(muon_vars)),
                           ]

    if option.count('IS_DATA') == 0:
        write_tool.branches += ['m_mc_part_|%s'   %(','.join(mc_prt_vars)),
                                'm_truth_jet_|%s' %(','.join(true_jet_vars))]

        if option.count('mc_vtx'):
            write_tool.branches += ['m_mc_vtx_|%s'  %(','.join(mc_vtx_vars))]

    ToolSvc += write_tool
    
    return write_tool

#======================================================================================
def getTriggers(key=''):

    muon_triggers = [
        'HLT_mu20_iloose_L1MU15',
        'HLT_mu24_imedium',
        'HLT_mu24_ivarmedium',
        'HLT_mu26_imedium',
        'HLT_mu26_ivarmedium',
        'HLT_mu40',
        'HLT_mu50',
    ]

    elec_triggers = [        
        'HLT_e24_lhtight_nod0_ivarloose',
        'HLT_e26_lhmedium_nod0_ivarloose',
        'HLT_e26_lhtight_nod0_ivarloose',
        'HLT_e60_lhmedium_nod0',
        'HLT_e60_medium',
        'HLT_e140_lhloose_nod0',
        'HLT_e24_lhmedium_L1EM18VH',
        'HLT_e24_lhmedium_L1EM20VH',
        'HLT_e60_lhmedium',
        'HLT_e120_lhloose',
    ]

    if   key == 'Elec': return elec_triggers
    elif key == 'Muon': return muon_triggers

    return muon_triggers + elec_triggers

#======================================================================================
def getDummyVars():

    dummy_vars = []
    
    return dummy_vars
    
#======================================================================================
def getIsoVars(key):

    muon_vars = [
        'LooseTrackOnly',
        'Loose',
        'Gradient',
        'GradientLoose',
        'FixedCutTightTrackOnly',
        'FixedCutLoose',
    ]

    elec_vars = [
        'LooseTrackOnly',
        'Loose',
        'Gradient',
        'GradientLoose',
        'FixedCutTight',
        'FixedCutTightTrackOnly',
        'FixedCutLoose',
    ]

    if   key == 'Elec': return elec_vars
    elif key == 'Muon': return muon_vars

    raise Exception('getIsoVars - unknown key: %s' %key)

#======================================================================================
def getIsoElecTools(CfgMgr):

    iso_tools = []

    for ivar in getIsoVars('Elec'):

        isoTool = CfgMgr.CP__IsolationSelectionTool( 'IsolationSelectionTool_elec_%s' %ivar)
        isoTool.ElectronWP = ivar

        athTool = CfgMgr.Ath__IsoTool('Ath_IsoTool_elec_%s' %ivar)
        athTool.isoTool = isoTool
        athTool.varName = 'iso%s' %ivar

        iso_tools += [athTool]
        
    return iso_tools

#======================================================================================
def getElecEffCorrTools(CfgMgr):

    out_list = []

    keys_id   = ['LooseBLayer', 'Medium', 'Tight']
    keys_iso  = ['FixedCutLoose', 'FixedCutTight', 'Gradient', 'Loose']
    keys_trig = {'LepCorrSF_'        : '',
                 'LepCorrSF_Trig1L_' :     'SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0',
                 'LepCorrEff_Trig1L_': 'Eff_SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0',
                 }

    for key_id in keys_id + ['Reconstruction']:
        ikey = 'LepCorrSF_%s' %(key_id)
        
        if CfgMgr == None:
            out_list += [ikey]
            continue

        asg_tool = CfgMgr.AsgElectronEfficiencyCorrectionTool('CP_ElecCorr_%s' %ikey)
        asg_tool.MapFilePath      = 'ElectronEfficiencyCorrection/2015_2016/rel20.7/Moriond_February2017_v1/map0.txt'
        asg_tool.CorrelationModel = 'TOTAL'

        if key_id == 'Reconstruction':
            asg_tool.RecoKey = 'Reconstruction'
        else:
            asg_tool.IdKey   = key_id            

        eff_tool = CfgMgr.Ath__ElecEffCorrTool('Ath_ElecCorr_%s' %ikey)
        eff_tool.VarName     = ikey
        eff_tool.corrToolSF  = asg_tool

        out_list += [eff_tool]    

    for key_id in keys_id:
        for key_iso in keys_iso:
            for (var_pref, key_trig) in keys_trig.iteritems():
                ikey = '%s%s_iso%s' %(var_pref, key_id, key_iso)

                if CfgMgr == None:
                    out_list += [ikey]
                    continue

                asg_tool = CfgMgr.AsgElectronEfficiencyCorrectionTool('CP_ElecCorr_%s' %ikey)
                asg_tool.IdKey            = key_id
                asg_tool.IsoKey           = key_iso
                asg_tool.TriggerKey       = key_trig
                asg_tool.MapFilePath      = 'ElectronEfficiencyCorrection/2015_2016/rel20.7/Moriond_February2017_v1/map0.txt'
                asg_tool.CorrelationModel = 'TOTAL'

                eff_tool = CfgMgr.Ath__ElecEffCorrTool('Ath_ElecCorr_%s' %ikey)
                eff_tool.VarName     = ikey
                eff_tool.corrToolSF  = asg_tool

                out_list += [eff_tool]

    return out_list

#======================================================================================
def getMuonEffCorrRecoTools(CfgMgr):

    out_list = []

    keys_pid = ['Loose', 'Medium', 'Tight', 'HighPt', 'TTVA']
    keys_iso = ['FixedCutLoose', 'FixedCutTightTrackOnly', 'Gradient', 'Loose']
        
    for key_pid in keys_pid:
        ikey = 'LepCorrSF_%s' %(key_pid)
            
        if CfgMgr == None:
            out_list += [ikey]
            continue

        asg_tool = CfgMgr.CP__MuonEfficiencyScaleFactors('CP_MuonCorr_%s' %ikey)
        asg_tool.WorkingPoint       = key_pid
        asg_tool.CalibrationRelease = '170303_Moriond'

        eff_tool = CfgMgr.Ath__MuonEffCorrRecoTool('Ath_MuonCorr_%s' %ikey)
        eff_tool.debug          = False
        eff_tool.varName        = ikey
        eff_tool.corrToolRecoSF = asg_tool
            
        out_list += [eff_tool]

    for key_iso in keys_iso:
        ikey = 'LepCorrSF_iso%s' %(key_iso)
            
        if CfgMgr == None:
            out_list += [ikey]
            continue

        asg_tool = CfgMgr.CP__MuonEfficiencyScaleFactors('CP_MuonCorr_%s' %ikey)
        asg_tool.WorkingPoint       = '%sIso' %key_iso
        asg_tool.CalibrationRelease = '170303_Moriond'

        eff_tool = CfgMgr.Ath__MuonEffCorrRecoTool('Ath_MuonCorr_%s' %ikey)
        eff_tool.debug          = False
        eff_tool.varName        = ikey
        eff_tool.corrToolRecoSF = asg_tool
            
        out_list += [eff_tool]

    return out_list

#======================================================================================
def getMuonEffCorrTrigTools(CfgMgr, year=None, option=''):

    out_list = []

    keys_id   = ['Loose', 'Medium', 'Tight', 'HighPt']
    keys_trig = {2015: 'HLT_mu20_iloose_L1MU15_OR_HLT_mu50',
                 2016: 'HLT_mu26_ivarmedium_OR_HLT_mu50'}

    for key_id in keys_id:
        skey = 'LepCorrSF_Trig1L_%s'  %(key_id)
        ekey = 'LepCorrEff_Trig1L_%s' %(key_id)
            
        if CfgMgr == None:            
            if option.count('IS_DATA'): out_list += [ekey]
            else:                       out_list += [ekey, skey]
            continue

        for iyear, itrig in keys_trig.iteritems():
            if year != iyear:
                continue
            
            asg_tool = CfgMgr.CP__MuonTriggerScaleFactors('CP_MuonTrigSF_%s_%d' %(skey, iyear))
            asg_tool.MuonQuality = key_id
            asg_tool.Year        = '%s' %iyear
            
            eff_tool = CfgMgr.Ath__MuonEffCorrTrigTool('Ath_MuonTrigSF_%s_%d' %(skey, iyear))
            eff_tool.debug          = False
            eff_tool.varName        = skey
            eff_tool.effName        = ekey
            eff_tool.trigger        = itrig
            eff_tool.corrToolTrigSF = asg_tool
        
            out_list += [eff_tool]
        
    return out_list

#======================================================================================
def getIsoMuonTools(CfgMgr, ToolSvc):

    iso_tools = []

    for ivar in getIsoVars('Muon'):

        isoTool = CfgMgr.CP__IsolationSelectionTool( 'IsolationSelectionTool_muon_%s' %ivar)
        isoTool.MuonWP = ivar

        ToolSvc += isoTool

        athTool = CfgMgr.Ath__IsoTool('Ath_IsoTool_muon_%s' %ivar)
        athTool.isoTool = isoTool
        athTool.varName = 'iso%s' %ivar

        ToolSvc += athTool

        iso_tools += [athTool]
        
    return iso_tools

#======================================================================================
def getElecLHTool(CfgMgr, key):

    configPath = 'ElectronPhotonSelectorTools/offline/mc15_20160512/'
    
    configs = {
        'isLooseLH'       : 'ElectronLikelihoodLooseOfflineConfig2016_Smooth.conf',
        'isLooseLHWithBL' : 'ElectronLikelihoodLooseOfflineConfig2016_CutBL_Smooth.conf',
        'isMediumLH'      : 'ElectronLikelihoodMediumOfflineConfig2016_Smooth.conf',
        'isTightLH'       : 'ElectronLikelihoodTightOfflineConfig2016_Smooth.conf',
    }

    if key not in configs:
        raise Exception('getElecLHTool - unknown working point: %s' %key)
        
    elecLH  = CfgMgr.AsgElectronLikelihoodTool('ElectronLH_%s' %key)
    elecLH.ConfigFile = '%s/%s' %(configPath, configs[key])

    return elecLH

#======================================================================================
def getReadEvent(CfgMgr, ToolSvc, trig_decision):

    putool = CfgMgr.CP__PileupReweightingTool('MyPileupReweightingTool')
    putool.LumiCalcFiles =  ['GoodRunsLists/data15_13TeV/20160720/physics_25ns_20.7.lumicalc.OflLumi-13TeV-005.root',
                             'GoodRunsLists/data16_13TeV/20161101/physics_25ns_20.7.lumicalc.OflLumi-13TeV-005.root'] 

    ToolSvc += putool

    alg = CfgMgr.Ath__ReadEvent('readEvent')
    alg.OutputLevel  = 3
    alg.triggers     = getTriggers()
    alg.dummyVars    = getDummyVars()
    alg.auxVars      = getEventAuxVars()
    alg.printAuxVars = False
    alg.debug        = False

    alg.trigDecision   = trig_decision
    alg.doTrigDecision = True

    alg.pileupTool     = putool
    alg.doPileup       = True

    return alg

#======================================================================================
def getReadPhysicsTruth(CfgMgr, name='readPhysicsTruth', option=''):

    alg = CfgMgr.Ath__ReadPhysicsTruth(name)

    alg.signalParticlePdgIds = [6, 7, 8, 15, 23, 24, 25, 32, 34, 35, 36, 37]
    alg.stableLeptonPdgIds   = [11, 12, 13, 14, 16]
    alg.minStableLeptonPt    = 5.0e3
    alg.outputStream         = 'out'
    alg.outputTruthPartName  = 'm_mc_part_'
    alg.outputTruthVtxName   = 'm_mc_vtx_'
    alg.fillHist             = True
    alg.debug                = False

    return alg

#======================================================================================
def getReadSimpleTruth(CfgMgr, name='readSimpleTruth', option=''):

    alg = CfgMgr.Ath__ReadSimpleTruth(name)

    alg.outputStream               = 'out'
    alg.outputTruthPartName        = 'm_mc_part_'
    alg.outputTruthVtxName         = 'm_mc_vtx_'
    alg.fillHist                   = True
    alg.saveTruthVertices          = True
    alg.saveOnlyGeneratorParticles = True
    alg.debug                      = False

    return alg

#======================================================================================
def getReadJets(CfgMgr, ToolSvc, input_name, option):

    alg = CfgMgr.Ath__ReadJets('%s_readJets' %input_name)
    alg.inputContainerName        = input_name
    alg.outputContainerName       = '%s_readJets' %(input_name)
    alg.truthContainerName        = 'AntiKt4TruthJets'
    alg.outputVectorName          = 'm_jet_'
    alg.outputVectorNameTruthJets = 'm_truth_jet_'
    alg.saveExtraBtagInfo         = False
    alg.runOnPrimaryxAOD          = False
    alg.printAuxVars              = False
    alg.printAuxVarsTruthJet      = False
    alg.debug                     = False
    alg.OutputLevel               = 3
    alg.auxVars                   = getRJetAuxVars(option)
    alg.auxVarsTruthJet           = getTJetAuxVars(option)
    alg.outputStream              = 'out'
    alg.configJetCuts             = []

    #--------------------------------------------------------------------------------
    # Calibration and smearing tools
    #
    alg.jetCalibrationTool = CfgMgr.JetCalibrationTool('JESToolData')
    alg.jetCalibrationTool.ConfigFile    = 'JES_data2016_data2015_Recommendation_Dec2016.config'
    alg.jetCalibrationTool.JetCollection = 'AntiKt4EMTopo'

    if option.count('IS_DATA'):
        alg.jetCalibrationTool.IsData        = True
        alg.jetCalibrationTool.CalibSequence = 'JetArea_Residual_Origin_EtaJES_GSC_Insitu'
    else:
        alg.jetCalibrationTool.IsData        = False
        alg.jetCalibrationTool.CalibSequence = 'JetArea_Residual_Origin_EtaJES_GSC'

    alg.jetUncertaintyTool = CfgMgr.JetUncertaintiesTool('jetUncertaintiesTool')
    alg.jetUncertaintyTool.JetDefinition = 'AntiKt4EMTopo'
    alg.jetUncertaintyTool.MCType        = 'MC15'
    alg.jetUncertaintyTool.ConfigFile    = 'JES_2016/Moriond2017/JES2016_21NP.config'

    JERTool = CfgMgr.JERTool('jerTool')
    JERTool.PlotFileName   = 'JetResolution/Prerec2015_xCalib_2012JER_ReducedTo9NP_Plots_v2.root'
    JERTool.CollectionName = 'AntiKt4EMTopoJets'

    ToolSvc += JERTool
    alg.jerTool = JERTool

    alg.jerSmearingTool = CfgMgr.JERSmearingTool('jetSmearingTool')
    alg.jerSmearingTool.ApplyNominalSmearing = False
    alg.jerSmearingTool.SystematicMode       = 'Full'
    alg.jerSmearingTool.isMC                 = (option.count('IS_DATA') == 0)
    alg.jerSmearingTool.JERTool              = JERTool

    #--------------------------------------------------------------------------------
    # Cleaning tools
    #
    jetCleanLoose = CfgMgr.JetCleaningTool('JetCleaningTool_Loose')
    jetCleanLoose.CutLevel = 'LooseBad'
    jetCleanLoose.DoUgly   = False

    jetCleanTight = CfgMgr.JetCleaningTool('JetCleaningTool_Tight')
    jetCleanTight.CutLevel = 'TightBad'
    jetCleanTight.DoUgly   = False

    alg.jetCleanLoose = jetCleanLoose
    alg.jetCleanTight = jetCleanTight
    alg.doCleaning    = True

    alg.tileCorrectionTool = CfgMgr.CP__JetTileCorrectionTool('tileCorrectionTool')
    alg.tileCorrectionTool.CorrectionFileName = 'JetTileCorrection/JetTile_pFile_010216.root'

    #--------------------------------------------------------------------------------
    # JES and b-tagging calibration tools
    #
    for wp in ['60', '70', '77', '85']:
        
        bjetEffTool = CfgMgr.BTaggingEfficiencyTool('bjetEffTool_%s' %wp)
        bjetEffTool.TaggerName          = 'MV2c10'
        bjetEffTool.OperatingPoint      = 'FixedCutBEff_%s' %wp
        bjetEffTool.JetAuthor           = input_name
        bjetEffTool.ScaleFactorFileName = 'xAODBTaggingEfficiency/13TeV/2016-20_7-13TeV-MC15-CDI-2017-06-07_v2.root'

        bjetSelTool = CfgMgr.BTaggingSelectionTool('bjetSelTool_%s' %wp)
        bjetSelTool.TaggerName                   = 'MV2c10'
        bjetSelTool.OperatingPoint               = 'FixedCutBEff_%s' %wp
        bjetSelTool.JetAuthor                    = input_name
        bjetSelTool.FlvTagCutDefinitionsFileName = 'xAODBTaggingEfficiency/13TeV/2016-20_7-13TeV-MC15-CDI-2017-06-07_v2.root'
        
        bjetTool = CfgMgr.Ath__BJetTool('bjetTool_%s' %wp)
        bjetTool.nameVarBTag = 'MV2c10_%s_Pass' %wp
        bjetTool.nameVarEff  = 'MV2c10_%s_Eff'  %wp
        bjetTool.nameVarSF   = 'MV2c10_%s_SF'   %wp
        bjetTool.effTool     = bjetEffTool
        bjetTool.selTool     = bjetSelTool
        bjetTool.debug       = False
        bjetTool.OutputLevel = 3
        
        alg.bjetTools += [bjetTool]

    #--------------------------------------------------------------------------------
    # Jet vertex tools
    #
    alg.jvtUpdate     = CfgMgr.JetVertexTaggerTool('UpdateJVT')
    alg.doJVT         = True

    jvtEffLoose = CfgMgr.CP__JetJvtEfficiency('JetJvtEff_Loose')
    jvtEffLoose.WorkingPoint = 'Loose'
    jvtEffLoose.SFFile       = 'JetJvtEfficiency/Moriond2017/JvtSFFile_EM.root'
    jvtEffLoose.TruthLabel   = ''
    
    jvtEffDefault = CfgMgr.CP__JetJvtEfficiency('JetJvtEff_Default')
    jvtEffDefault.WorkingPoint = 'Medium'
    jvtEffDefault.SFFile       = 'JetJvtEfficiency/Moriond2017/JvtSFFile_EM.root'
    jvtEffDefault.TruthLabel   = ''

    alg.jvtEffDefault = jvtEffDefault
    alg.jvtEffLoose   = jvtEffLoose

    return alg

#======================================================================================
def getReadElec(CfgMgr, ToolSvc, input_name, option):

    elec_cuts = ['[Pt] > 5.0e3',
                 '[isLooseLH] > 0 || [isLooseLHWithBL] > 0 || [DFCommonElectronsLHLoose] > 0']
    
    alg = CfgMgr.Ath__ReadElec('%s_readElecs' %input_name)
    alg.inputContainerName = input_name
    alg.outputVectorName    = 'm_elec_'
    alg.printAuxVars        = False
    alg.outputStream        = 'out'
    alg.configElecCuts      = []
    alg.debug               = False
    alg.auxVars             = getElecAuxVars(option)

    alg.doTrigMatch         = True
    alg.trigMatchTool       = CfgMgr.Trig__MatchingTool('TrigMatchingTool', OutputLevel=3)

    alg.triggers            = getTriggers('Elec')
    alg.isoTools            = getIsoElecTools(CfgMgr)

    alg.doEnergyCalibration = True
    alg.egammaCalibTool     = CfgMgr.CP__EgammaCalibrationAndSmearingTool('egammaCalibTool', 
                                                                         ESModel='es2016data_mc15c_final', 
                                                                         decorrelationModel='1NP_v1')

    alg.doElecLikelihood    = True
    alg.elecLooseLHWithBL   = getElecLHTool(CfgMgr, 'isLooseLHWithBL')
    alg.elecLooseLH         = getElecLHTool(CfgMgr, 'isLooseLH')
    alg.elecMediumLH        = getElecLHTool(CfgMgr, 'isMediumLH')
    alg.elecTightLH         = getElecLHTool(CfgMgr, 'isTightLH')

    if option.count('IS_DATA') == 0: 
        alg.effCorrTools = getElecEffCorrTools(CfgMgr)

    for etool in alg.effCorrTools:
        etool.debug = alg.debug
    
    return alg

#======================================================================================
def getReadMuon(CfgMgr, ToolSvc, input_name, option, match_tool):

    ''' Process muons - MuonSelectionTool requires variables not stored with EGAM1 so it is disabled '''

    muon_cuts = ['[Pt] > 5.0e3', '[Loose] > 0']
    
    select_muon  = CfgMgr.CP__MuonSelectionTool('muonSelectionTool_MCP', OutputLevel = 5)

    calibrate_muon  = CfgMgr.CP__MuonCalibrationAndSmearingTool('muonCalibrationTool_MCP', OutputLevel = 3)
    calibrate_muon.SagittaCorr = True

    ToolSvc += select_muon
    ToolSvc += calibrate_muon

    alg = CfgMgr.Ath__ReadMuon('%s_readMuons' %input_name)
    alg.inputContainerName = input_name
    alg.outputVectorName   = 'm_muon_'
    alg.printAuxVars       = False
    alg.debug              = False
    alg.OutputLevel        = 3
    alg.outputStream       = 'out'
    alg.configMuonCuts     = []

    alg.doMuonCalibration  = True
    alg.doMuonSelection    = True
    alg.selectMuon         = select_muon
    alg.calibMuon          = calibrate_muon
    alg.isoTools           = getIsoMuonTools(CfgMgr, ToolSvc)

    alg.triggersHLT        = getTriggers('Muon')
    alg.trigMatch          = match_tool
    alg.doTrigMatch        = True
    alg.auxVars            = getMuonAuxVars(option)

    alg.trigEff2015Tools   = getMuonEffCorrTrigTools(CfgMgr, 2015, option)
    alg.trigEff2016Tools   = getMuonEffCorrTrigTools(CfgMgr, 2016, option)

    if option.count('IS_DATA') == 0: 
        alg.recoEffCorrTools = getMuonEffCorrRecoTools(CfgMgr)

    return alg

#======================================================================================
def getFillOR(CfgMgr, ToolSvc, alg_name, option):

    from AssociationUtils.config import recommended_tools

    alg = CfgMgr.Ath__FillOR('%s_fillOR' %alg_name)
    alg.outputStream         = 'out'
    alg.inputVecElec         = 'm_elec_'
    alg.inputVecMuon         = 'm_muon_'
    alg.inputVecJet          = 'm_jet_'
    alg.varNamePassSelection = 'ORHFJets_PassSelection'
    alg.varNamePassBJet      = 'ORHFJets_PassBJet'
    alg.varNameIsRemoved     = 'ORHFJets_IsRemoved'
    alg.debug                = False

    alg.configCutsElec = getPreSelectionCuts_Elec()
    alg.configCutsMuon = getPreSelectionCuts_Muon()
    alg.configCutsJet  = getPreSelectionCuts_Jet ()
    alg.configCutsBJet = ['[MV2c10_85_Pass] > 0']
    
    alg.toolOR = recommended_tools('ORTool',
                                   #OutputLevel = VERBOSE,
                                   #inputLabel  = '',
                                   bJetLabel   = alg.varNamePassBJet,
                                   doElectrons = True, 
                                   doMuons     = True, 
                                   doJets      = True,
                                   doEleEleOR  = True,
                                   doTaus      = False,
                                   doPhotons   = False,
                                   doFatJets   = False)

    return alg

#======================================================================================
def getFillORLepLepOnly(CfgMgr, ToolSvc, alg_name, option):

    from AssociationUtils.config import recommended_tools

    alg = CfgMgr.Ath__FillOR('%s_fillOR' %alg_name)
    alg.outputStream            = 'out'
    alg.inputVecElec            = 'm_elec_'
    alg.inputVecMuon            = 'm_muon_'
    alg.inputVecJet             = 'm_jet_'
    alg.varNamePassSelection    = 'ORLL_PassSelection'
    alg.varNamePassBJet         = 'ORLL_PassBJet'
    alg.varNameIsRemoved        = 'ORLL_IsRemoved'
    alg.debug                   = False

    alg.configCutsElec = getPreSelectionCuts_Elec()
    alg.configCutsMuon = getPreSelectionCuts_Muon()
    alg.configCutsJet  = getPreSelectionCuts_Jet ()
    alg.configCutsBJet = ['[MV2c10_85_Pass] > 0']
    
    alg.toolOR = recommended_tools('ORToolLepLepOnly',
                                   #OutputLevel = VERBOSE,
                                   #inputLabel  = '',
                                   bJetLabel   = alg.varNamePassBJet,
                                   doElectrons = True, 
                                   doMuons     = True, 
                                   doJets      = False,
                                   doEleEleOR  = False,
                                   doTaus      = False,
                                   doPhotons   = False,
                                   doFatJets   = False)

    return alg

#======================================================================================
def getFillMET(CfgMgr, ToolSvc, alg_name, option):

    alg = CfgMgr.Ath__FillMET('%s_fillMET' %alg_name)
    alg.outputStream         = 'out'
    alg.inputVecElec         = 'm_elec_'
    alg.inputVecMuon         = 'm_muon_'
    alg.debug                = False

    alg.inputContMETMap      = 'METAssoc_AntiKt4EMTopo'
    alg.inputContMETCore     = 'MET_Core_AntiKt4EMTopo'
    alg.inputContCalibJets   = 'AntiKt4EMTopoJets_readJets'
    alg.inputContFullMuons   = 'Muons'
    alg.inputContTau         = ''
    alg.inputContPhoton      = ''

    alg.outputContElec       = '%s_Elec' %alg_name
    alg.outputContMuon       = '%s_Muon' %alg_name
    alg.outputContMET        = '%s_MET'  %alg_name

    alg.varNamePassSelection = 'MET_PassSelection'
    alg.varPrefixMET         = ''

    alg.rebuildJetMET_softClustKey = 'SoftClus'
    alg.rebuildJetMET_softTrackKey = 'PVSoftTrk'
    alg.doMET_LCTopo               = False
    alg.doMET_EMTopo               = True
    alg.doMET_Track                = True

    #
    # MET tool wants selected leptons but "the entire calibrated jet collection"
    #
    alg.configCutsElec = getPreSelectionCuts_Elec()
    alg.configCutsMuon = getPreSelectionCuts_Muon()

    alg.toolMETMaker = CfgMgr.met__METMaker          ('METMaker_%s'           %alg_name)
    alg.toolMETSyst  = CfgMgr.met__METSystematicsTool('METSystematicsTool_%s' %alg_name)

    alg.toolMETMaker.OutputLevel = 3
    alg.toolMETSyst .OutputLevel = 3

    return alg

#======================================================================================
def getElecAuxVars(option):

    auxVars = [('DFCommonElectronsLHLoose',       'Short'), 
               ('DFCommonElectronsLHMedium',      'Short'), 
               ('DFCommonElectronsLHTight',       'Short'),
               ('PromptLeptonIso_TagWeight',      'Float'), 
               ('PromptLeptonIso_TrackJetNTrack', 'Short'),
               ('PromptLeptonIso_sv1_jf_ntrkv',   'Short'),
               ('PromptLeptonIso_ip2',            'Float'),
               ('PromptLeptonIso_ip3',            'Float'),
               ('PromptLeptonIso_LepJetPtFrac',   'Float'),
               ('PromptLeptonIso_DRlj',           'Float')]

    if option.count('IS_DATA') == 0:
        auxVars += [ ('firstEgMotherPdgId',             'Int'),
                     ('firstEgMotherTruthOrigin',       'Int'),
                     ('firstEgMotherTruthType',         'Int'),
                     ('truthOrigin',                    'Int'),
                     ('truthPdgId',                     'Int'),
                     ('truthType',                      'Int'),
                     ('bkgMotherPdgId',                 'Int'),
                     ('bkgTruthOrigin',                 'Int'),
                     ('bkgTruthType',                   'Int'),
                     ]
 
    outVars = []

    for v in auxVars:
        outVars += ['%s:type=%s' %(v[0], v[1])]

    return outVars

#======================================================================================
def getMuonAuxVars(option):

    auxVars = [('PromptLeptonIso_TagWeight',      'Float'), 
               ('PromptLeptonIso_TrackJetNTrack', 'Short'),
               ('PromptLeptonIso_sv1_jf_ntrkv',   'Short'),
               ('PromptLeptonIso_ip2',            'Float'),
               ('PromptLeptonIso_ip3',            'Float'),
               ('PromptLeptonIso_LepJetPtFrac',   'Float'),
               ('PromptLeptonIso_DRlj',           'Float'),
               ('InnerDetectorPt',                'Float'),
               ('MuonSpectrometerPt',             'Float'),
               ]

    if option.count('IS_DATA') == 0:
        auxVars += [ ('truthOrigin',                    'Int'),
                     ('truthPdgId',                     'Int'),
                     ('truthType',                      'Int'),
                     ]

    outVars = []
    
    for v in auxVars:
        outVars += ['%s:type=%s' %(v[0], v[1])]

    return outVars

#======================================================================================
def getRJetAuxVars(option):

    auxVars = [('EMFrac',                     'Float'),
               ('DetectorEta',                'Float'),
               ('TileStatus',                 'Int')]

    if option.count('IS_DATA') == 0:
        auxVars += [('PartonTruthLabelID',         'Short'),
                    ('ConeTruthLabelID',           'Short'),
                    ('HadronConeExclTruthLabelID', 'Short')]

    outVars = []

    for v in auxVars:
        outVars += ['%s:type=%s' %(v[0], v[1])]

    return outVars

#======================================================================================
def getTJetAuxVars(option):

    if option.count('IS_DATA') == 0:
        auxVars = [('PartonTruthLabelID',         'Short'),
                   ('ConeTruthLabelID',           'Short'),
                   ('HadronConeExclTruthLabelID', 'Short')]

    outVars = []

    for v in auxVars:
        outVars += ['%s:type=%s' %(v[0], v[1])]

    return outVars

#======================================================================================
def getEventAuxVars():

    auxVars = [('DFCommonJets_isBadBatman',   'Int')]
    outVars = []

    for v in auxVars:
        outVars += ['%s:type=%s' %(v[0], v[1])]

    return outVars

#======================================================================================
def getMETVars(prefix):

   met_names = ['FinalTrack', 
                'FinalEMTopo', 
                'RefEle', 
                'Muons', 
                'MuonEloss', 
                'RefJet', 
                #'SoftClus', 
                'PVSoftTrk']

   met_vars = []

   for met in met_names:
       met_vars += ['%s%s_MET:type=Float'   %(prefix, met)]
       met_vars += ['%s%s_Phi:type=Float'   %(prefix, met)]
       met_vars += ['%s%s_SumEt:type=Float' %(prefix, met)]

   return met_vars

#======================================================================================
# Object pre-selection cuts
#======================================================================================
def getPreSelectionCuts_Elec():
    
    cuts = ['[Pt] > 6.0e3',
            'fabs([EtaBE2]) < 2.47',
            'fabs([Eta]) < 2.5',
            '[isLooseLHWithBL] > 0',
            'fabs([Z0Sin]) < 0.5',
            'fabs([D0Sig]) < 5.0']
    
    return cuts
   
#======================================================================================
def getPreSelectionCuts_Muon():
    
    cuts = ['[Pt] > 6.0e3',
            'fabs([Eta]) < 2.7',
            '[PassedID] > 0',
            '[Loose] > 0',
            '[MuonType] == 1 || fabs([Z0Sin]) < 0.5',
            '[MuonType] == 1 || fabs([D0Sig]) < 10.0']

    return cuts

#======================================================================================
def getPreSelectionCuts_Jet():
    
    cuts = ['fabs([Eta]) < 4.5',
            '[Pt] > 25.0e3',            
            'fabs([Eta]) < 2.4 || [Pt] > 30.0e3']

    return cuts
