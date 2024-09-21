
#======================================================================================
def getWriteTool(ToolSvc, CfgMgr, name, stream='out', treename='nominal', option=''):

    mc_prt_vars = ['Status:type=Int',
                   'PDG:type=Int',
                   'TrueBarcode:type=Int',
                   'Mass:type=Float',
                   'Energy:type=Float',
                   'Pt:type=Float',
                   'Eta:type=Float',
                   'Phi:type=Float',
                   'ProdVtxBarcode:type=Int',
                   'DecayVtxBarcode:type=Int',
                   'IndexRangeParent:type=VecInt',
                   'IndexRangeChild:type=VecInt',
    ]

    mc_vtx_vars = ['VtxBarcode:type=Int',
                   'NParents:type=Int',
                   'NChildren:type=Int',
                   'VtxX:type=Float',
                   'VtxY:type=Float',
                   'VtxZ:type=Float',
                   'IndexRangeParent:type=VecInt',
                   'IndexRangeChild:type=VecInt',
                   ]
    
    elec_vars = ['Pt:type=Float',
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
             ]
                 
    muon_vars = ['Pt:type=Float',
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
                 'Loose:type=Short:nick=isLoose',
                 'Medium:type=Short:nick=isMedium',
                 'Tight:type=Short:nick=isTight',
                 'HighPt:type=Short:nick=isHighPt',
                 'PassedID:type=Short',
                 'Quality:type=Short',
                 ]

    reco_jet_vars = ['Pt:type=Float',
                     'Eta:type=Float',
                     'Phi:type=Float',
                     'Energy:type=Float',
                     'Mass:type=Float',
                     'MV2c00:type=Float',
                     'MV2c10:type=Float',
                     'MV2c20:type=Float',
                     'JVT:type=Float',
                     'JVTSF_Eff:type=Float',
                     'JVTSF_Ineff:type=Float',
                     'JVTSF_LooseEff:type=Float',
                     'JVTSF_LooseIneff:type=Float',
                     'JVTPass:type=Short',
                     'JVTPassLoose:type=Short',
                     'isLooseBad:type=Short',
                     'isTightBad:type=Short',
                     'MV2c10_70_Eff:type=Float',
                     'MV2c10_77_Eff:type=Float',
                     'MV2c10_85_Eff:type=Float',
                     'MV2c10_70_SF:type=Float',
                     'MV2c10_77_SF:type=Float',
                     'MV2c10_85_SF:type=Float',
                     'TruthJetDR:type=Float',
                     'TruthJetPt:type=Float',
                     'TruthJetID:type=Int',
                     ]

    evt_vars = ['Event:type=Long',
                'Run:type=Int',
                'LumiBlock:type=Int',
                'bcid:type=Int',
                'backgroundFlags:type=UInt',
                'MCChannel:type=Int',
                'MCWeight:type=Float',
                'PUWeight:type=Float',
                'CorrectedMu:type=Float',
                'RandomRunNumber:type=Int',
                'RandomYear:type=Short',
                'ActualInteractions:type=Float',
                'AverageInteractions:type=Float',
                'NRecoVtx:type=Short',
                'HasPriVtx:type=Short',
                'ErrorState_Core:type=Short',
                'ErrorState_Background:type=Short',
                'ErrorState_LAr:type=Short',
                'ErrorState_Tile:type=Short',
                'ErrorState_SCT:type=Short',
                'ErrorState_Pixel:type=Short',
                'ErrorState_TRT:type=Short',
                'ErrorState_Muon:type=Short',
    ]

    for trig in getTriggers('Elec'):
        evt_vars  += ['%s:type=Short'       %trig]
        elec_vars += ['match_%s:type=Short' %trig]

    for trig in getTriggers('Muon'):
        evt_vars  += ['%s:type=Short' %trig]
        muon_vars += ['match_%s:type=Short' %trig]

    for ivar in getIsoVars('Elec'):
        elec_vars += ['iso%s:type=Short' %ivar]

    for ivar in getIsoVars('Muon'):
        muon_vars += ['iso%s:type=Short' %ivar]

    for dvar in getDummyVars():
        evt_vars += ['%s:type=Float' %dvar]

    for evar in getElecEffCorrTools(None):
        elec_vars += ['%s:type=Float' %evar]

    for evar in getMuonEffCorrRecoTools(None) + getMuonEffCorrTrigTools(None, None):
        muon_vars += ['%s:type=Float' %evar]

    elec_vars     += getElecAuxVars('save')
    muon_vars     += getMuonAuxVars('save')
    reco_jet_vars += getRJetAuxVars('save')

    write_tool = CfgMgr.Ath__WriteEvent(name)
    write_tool.stream     = stream
    write_tool.treename   = treename
    write_tool.keys_event = ','.join(evt_vars)

    write_tool.branches = ['m_mc_part_|%s'   %(','.join(mc_prt_vars)),
                           'm_mc_vtx_|%s'    %(','.join(mc_vtx_vars)),
                           'm_jet_|%s'       %(','.join(reco_jet_vars)),
                           'm_electron_|%s'  %(','.join(elec_vars)), 
                           'm_muon_|%s'      %(','.join(muon_vars)),
                           ]

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
        'HLT_e60_lhmedium_nod0',
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
def getMuonEffCorrTrigTools(CfgMgr, year=None):

    out_list = []

    keys_id   = ['Loose', 'Medium', 'Tight', 'HighPt']
    keys_trig = {2015: 'HLT_mu20_iloose_L1MU15_OR_HLT_mu50',
                 2016: 'HLT_mu26_ivarmedium_OR_HLT_mu50'}

    for key_id in keys_id:
        skey = 'LepCorrSF_Trig1L_%s'  %(key_id)
        ekey = 'LepCorrEff_Trig1L_%s' %(key_id)
            
        if CfgMgr == None:
            out_list += [skey, ekey]
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
    alg.OutputLevel = 3
    alg.triggers    = getTriggers()
    alg.dummyVars   = getDummyVars()

    alg.trigDecision   = trig_decision
    alg.doTrigDecision = True

    alg.pileupTool     = putool
    alg.doPileup       = True

    return alg

#======================================================================================
def getReadPhysicsTruth(CfgMgr, name='readPhysicsTruth', option=''):

    alg = CfgMgr.Ath__ReadPhysicsTruth(name)

    alg.saveParticleIndexes = True #always save children/parents

    alg.filterParticles     = True
    alg.selectPdgIdAll      = [6, 23, 24, 25, 15]
    alg.selectPdgIdStable   = [11, 12, 13, 14, 15, 16]
    alg.minStablePt         = 10.0e3
    alg.outputStream        = 'out'
    alg.outputTruthPartName = 'm_truth_'
    alg.fillHist            = True
    alg.printFilter         = False
    alg.debug               = False
    alg.OutputLevel         = 3

    if option.count('save_only_generator'):
        alg.saveOnlyGeneratorParticles = True
        alg.filterGenerator            = True

    return alg

#======================================================================================
def getReadSimpleTruth(CfgMgr, name='readSimpleTruth', option=''):

    alg = CfgMgr.Ath__ReadSimpleTruth(name)

    alg.outputStream               = 'out'
    alg.outputTruthPartName        = 'm_mc_part_'
    alg.outputTruthVtxName         = 'm_mc_vtx_'
    alg.fillHist                   = True
    alg.debug                      = False
    alg.saveOnlyGeneratorParticles = False
    alg.saveTruthVertices          = True

    return alg

#======================================================================================
def getReadJets(CfgMgr, ToolSvc, input_name, output_name):

    alg = CfgMgr.Ath__ReadJets('%s_readJets' %input_name)
    alg.inputContainerName = input_name
    alg.truthContainerName = 'AntiKt4TruthJets'
    alg.outputVectorName   = output_name
    alg.saveExtraBtagInfo  = False
    alg.runOnPrimaryxAOD   = False
    alg.printAuxVars       = False
    alg.minPt              = 9.0e3
    alg.debug              = False
    alg.OutputLevel        = 3
    alg.auxVars            = getRJetAuxVars('read')

    jesToolData = CfgMgr.JetCalibrationTool('JESToolData')
    jesToolData.IsData        = True
    jesToolData.ConfigFile    = 'JES_data2016_data2015_Recommendation_Dec2016.config'
    jesToolData.CalibSequence = 'JetArea_Residual_Origin_EtaJES_GSC_Insitu'
    jesToolData.JetCollection = 'AntiKt4EMTopo'

    jesToolSiml = CfgMgr.JetCalibrationTool('JESToolSiml')
    jesToolSiml.IsData        = False
    jesToolSiml.ConfigFile    = 'JES_data2016_data2015_Recommendation_Dec2016.config'
    jesToolSiml.CalibSequence = 'JetArea_Residual_Origin_EtaJES_GSC'
    jesToolSiml.JetCollection = 'AntiKt4EMTopo'

    alg.doCalibration      = True
    alg.jetCalibrationData = jesToolData
    alg.jetCalibrationSiml = jesToolSiml

    for wp in ['70', '77', '85']:

        bjetEffTool = CfgMgr.BTaggingEfficiencyTool('bjetEffTool_%s' %wp)
        bjetEffTool.TaggerName          = 'MV2c10'
        bjetEffTool.OperatingPoint      = 'FixedCutBEff_%s' %wp
        bjetEffTool.JetAuthor           = input_name
        bjetEffTool.ScaleFactorFileName = '13TeV/2016-20_7-13TeV-MC15-CDI-2017-01-31_v1.root'

        bjetTool = CfgMgr.Ath__BJetTool('bjetTool_%s' %wp)
        bjetTool.nameVarEff  = 'MV2c10_%s_Eff' %wp
        bjetTool.nameVarSF   = 'MV2c10_%s_SF'  %wp
        bjetTool.effTool     = bjetEffTool
        bjetTool.debug       = False
        bjetTool.OutputLevel = 3

        alg.bjetEffTools += [bjetTool]

    jetCleanLoose = CfgMgr.JetCleaningTool('JetCleaningTool_Loose')
    jetCleanLoose.CutLevel = 'LooseBad'
    jetCleanLoose.DoUgly   = False

    jetCleanTight = CfgMgr.JetCleaningTool('JetCleaningTool_Tight')
    jetCleanTight.CutLevel = 'TightBad'
    jetCleanTight.DoUgly   = False

    alg.jetCleanLoose = jetCleanLoose
    alg.jetCleanTight = jetCleanTight
    alg.doCleaning    = True

    jvtEffLoose = CfgMgr.CP__JetJvtEfficiency('JetJvtEff_Loose')
    jvtEffLoose.WorkingPoint = 'Loose'
    jvtEffLoose.SFFile       = 'JetJvtEfficiency/Moriond2017/JvtSFFile_EM.root'
    jvtEffLoose.TruthLabel   = ''

    jvtEffDefault = CfgMgr.CP__JetJvtEfficiency('JetJvtEff_Default')
    jvtEffLoose.WorkingPoint = 'Medium'
    jvtEffDefault.SFFile       = 'JetJvtEfficiency/Moriond2017/JvtSFFile_EM.root'
    jvtEffDefault.TruthLabel   = ''

    alg.jvtEffDefault = jvtEffDefault
    alg.jvtEffLoose   = jvtEffLoose
    alg.jvtUpdate     = CfgMgr.JetVertexTaggerTool('UpdateJVT')
    alg.doJVT         = True

    return alg

#======================================================================================
def getReadElec(CfgMgr, ToolSvc, input_name, output_name):

    alg = CfgMgr.Ath__ReadElec('%s_readElecs' %input_name)
    alg.inputContainerName = input_name
    alg.outputVectorName   = output_name
    alg.printAuxVars       = False
    alg.minPt              = 9.0e3
    alg.doTruthClassifier  = True
    alg.OutputLevel        = 3

    alg.trigMatchTool      = CfgMgr.Trig__MatchingTool('TrigMatchingTool', OutputLevel=3)
    alg.doTrigMatch        = True
    alg.triggers           = getTriggers('Elec')
    alg.isoTools           = getIsoElecTools(CfgMgr)

    alg.egammaCalibTool    = CfgMgr.CP__EgammaCalibrationAndSmearingTool('egammaCalibTool', 
                                                                         ESModel='es2016data_mc15c', 
                                                                         decorrelationModel='1NP_v1')

    alg.elecLooseLHWithBL  = getElecLHTool(CfgMgr, 'isLooseLHWithBL')
    alg.elecLooseLH        = getElecLHTool(CfgMgr, 'isLooseLH')
    alg.elecMediumLH       = getElecLHTool(CfgMgr, 'isMediumLH')
    alg.elecTightLH        = getElecLHTool(CfgMgr, 'isTightLH')
    alg.doElecLikelihood   = True

    alg.effCorrTools       = getElecEffCorrTools(CfgMgr)
    alg.auxVars            = getElecAuxVars('read')
    alg.debug              = False

    for etool in alg.effCorrTools:
        etool.debug = False
    
    return alg

#======================================================================================
def getReadMuon(CfgMgr, ToolSvc, input_name, output_name, match_tool):

    ''' Process muons - MuonSelectionTool requires variables not stored with EGAM1 so it is disabled '''

    select_muon  = CfgMgr.CP__MuonSelectionTool('muonSelectionTool_MCP', OutputLevel = 5)
    ToolSvc += select_muon

    calibrate_muon  = CfgMgr.CP__MuonCalibrationAndSmearingTool('muonCalibrationTool_MCP', OutputLevel = 3)
    ToolSvc += calibrate_muon

    alg = CfgMgr.Ath__ReadMuon('%s_readMuons' %input_name)
    alg.inputContainerName = input_name
    alg.outputVectorName   = output_name
    alg.printAuxVars       = False
    alg.debug              = False
    alg.OutputLevel        = 3

    alg.doMuonCalibration  = True
    alg.doMuonSelection    = True
    alg.selectMuon         = select_muon
    alg.calibMuon          = calibrate_muon
    alg.isoTools           = getIsoMuonTools(CfgMgr, ToolSvc)

    alg.triggersHLT        = getTriggers('Muon')
    alg.trigMatch          = match_tool
    alg.doTrigMatch        = True

    alg.recoEffCorrTools   = getMuonEffCorrRecoTools(CfgMgr)
    alg.trigEff2015Tools   = getMuonEffCorrTrigTools(CfgMgr, 2015)
    alg.trigEff2016Tools   = getMuonEffCorrTrigTools(CfgMgr, 2016)

    alg.auxVars            = getMuonAuxVars('read')

    return alg

#======================================================================================
def getElecAuxVars(opt):

    outVars = []

    auxVars = [('firstEgMotherPdgId',             'Int'),
               ('firstEgMotherTruthOrigin',       'Int'),
               ('firstEgMotherTruthType',         'Int'),
               ('truthOrigin',                    'Int'),
               ('truthPdgId',                     'Int'),
               ('truthType',                      'Int'),
               ]

    if opt == 'read':
        for v in auxVars:
            outVars += [v[0]]
    elif opt == 'save':
        for v in auxVars:
            outVars += ['%s:type=%s' %(v[0], v[1])]
    else:
        raise Exception('getMuonAuxVars - unknown opt=%s' %opt)

    return outVars

#======================================================================================
def getMuonAuxVars(opt):

    auxVars = []

    outVars = []

    if opt == 'read':
        for v in auxVars:
            outVars += [v[0]]
    elif opt == 'save':
        for v in auxVars:
            outVars += ['%s:type=%s' %(v[0], v[1])]
    else:
        raise Exception('getMuonAuxVars - unknown opt=%s' %opt)

    return outVars

#======================================================================================
def getRJetAuxVars(opt):

    auxVars = [('EMFrac',                     'Float'),
               ('DetectorEta',                'Float'),
               ('PartonTruthLabelID',         'Short'),
               ('ConeTruthLabelID',           'Short'),
               ('HadronConeExclTruthLabelID', 'Short'),
               ]

    outVars = []

    if opt == 'read':
        for v in auxVars:
            outVars += [v[0]]
    elif opt == 'save':
        for v in auxVars:
            outVars += ['%s:type=%s' %(v[0], v[1])]
    else:
        raise Exception('getMuonAuxVars - unknown opt=%s' %opt)

    return outVars
