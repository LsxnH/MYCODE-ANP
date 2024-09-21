
import os

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
                   'IndexRangeChild:type=VecInt']

    overlap_vars = ['ORHFJets_PassSelection:type=Short', 
                    'ORHFJets_IsRemoved:type=Short']

    mc_vtx_vars = ['Barcode:type=Int',
                   'NParents:type=Int',
                   'NChildren:type=Int',
                   'VtxX:type=Float',
                   'VtxY:type=Float',
                   'VtxZ:type=Float',
                   'IndexRangeParent:type=VecInt',
                   'IndexRangeChild:type=VecInt']
    
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
                 'IsGoodQuality:type=Short']
                 
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
                 'TrackPt:type=Float',
                 'IDTrackPt:type=Float',
                 'MSTrackPt:type=Float']

    tau_vars = ['Pt:type=Float',
                'Eta:type=Float',
                'Phi:type=Float',
                'Charge:type=Int',
                'NTrack:type=Int',
                'JetBDTSigVeryLoose:type=Short',
                'JetBDTSigLoose:type=Short',
                'JetBDTSigMedium:type=Short',
                'JetBDTSigTight:type=Short',
                'JetBDTScore:type=Float',
                'EleBDTLoose:type=Short',
                'EleBDTMedium:type=Short',
                'EleBDTTight:type=Short',
                'EleBDTScore:type=Float',
                'PassEleOLR:type=Short',
                'MuonVeto:type=Short']                

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
                     'isTightBad:type=Short']

    track_jet_vars = ['Pt:type=Float',
                      'Eta:type=Float',
                      'Phi:type=Float',
                      'MV2c10:type=Float',
                      'MV2c100:type=Float',
                      'MV2cl100:type=Float',
                      'MV2c10mu:type=Float',
                      'MV2c10rnn:type=Float',
                      'DL1:type=Float',
                      'DL1mu:type=Float',
                      'DL1rnn:type=Float',
                      'rnnip:type=Float',
                      'SV1:type=Float',
                      'IP2D:type=Float',
                      'IP3D:type=Float',
                      'JetF:type=Float',
                      'NTrack:type=Int',
                      'eta_abs_uCalib:type=Float',
                      'ip2_c:type=Float',
                      'ip2_cu:type=Float',
                      'ip3_c:type=Float',
                      'ip3_cu:type=Float',
                      'ip2:type=Float',
                      'ip3:type=Float',
                      'sv1_mass:type=Float',
                      'sv1_efrc:type=Float',
                      'sv1_Lxy:type=Float',
                      'sv1_L3d:type=Float',
                      'sv1_sig3:type=Float',
                      'sv1_dR:type=Float',
                      'sv1_ntkv:type=Int',
                      'sv1_n2t:type=Int',
                      'jf_mass:type=Float',
                      'jf_efrc:type=Float',
                      'jf_dR:type=Float',
                      'jf_sig3:type=Float',
                      'jf_n2tv:type=Int',
                      'jf_ntrkv:type=Int',
                      'jf_nvtx:type=Int',
                      'jf_nvtx1t:type=Int'] 

    evt_vars = ['Event:type=Long',
                'Run:type=Int',
                'LumiBlock:type=Int',
                'Year:type=Int',
                'bcid:type=Int',
                'backgroundFlags:type=UInt',
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
                'BeamPosSigmaZ:type=Float']

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

    #for evar in getMuonEffCorrTrigTools(None, None, option):
    #    muon_vars += ['%s:type=Float' %evar]

    if option.count('IS_DATA') == 0:
        reco_jet_vars += [#'JVTSF_Eff:type=Float',
                          #'JVTSF_Ineff:type=Float',
                          #'JVTSF_LooseEff:type=Float',
                          #'JVTSF_LooseIneff:type=Float',
                          #'MV2c10_70_Eff:type=Float',
                          #'MV2c10_77_Eff:type=Float',
                          #'MV2c10_85_Eff:type=Float',
                          #'MV2c10_70_SF:type=Float',
                          #'MV2c10_77_SF:type=Float',
                          #'MV2c10_85_SF:type=Float',                          
                          'TruthJetDR:type=Float',
                          'TruthJetPt:type=Float',
                          'TruthJetID:type=Int']

        evt_vars += ['MCChannel:type=Int',
                     'MCWeight:type=Float',
                     'PUWeight:type=Float',
                     'CorrectedMu:type=Float',
                     'RandomRunNumber:type=Int',
                     'RandomYear:type=Short']

        tau_vars += ['TauTruthType:type=Int',
                     'DecayMode:type=Int']

        #
        # Add scale factors for r21 when available
        #
        #for evar in getElecEffCorrTools(None):
        #    elec_vars += ['%s:type=Float' %evar]
            
        #for evar in getMuonEffCorrRecoTools(None):
        #    muon_vars += ['%s:type=Float' %evar]

    elec_vars      += getElecAuxVars(option)
    muon_vars      += getMuonAuxVars(option)
    tau_vars       += getTauAuxVars (option)
    reco_jet_vars  += getRJetAuxVars(option)
    track_jet_vars += getTJetAuxVars(option)

    write_tool = CfgMgr.Ath__WriteEvent(name)
    write_tool.stream     = stream
    write_tool.treename   = treename
    write_tool.keys_event = ','.join(evt_vars)

    write_tool.branches = ['m_jet_|%s'       %(','.join(reco_jet_vars)),
                           'm_track_jet_|%s' %(','.join(track_jet_vars)),
                           'm_elec_|%s'      %(','.join(elec_vars)), 
                           'm_muon_|%s'      %(','.join(muon_vars)),
                           'm_tau_|%s'       %(','.join(tau_vars)),
                           ]

    if option.count('IS_DATA') == 0:
        write_tool.branches += ['m_mc_part_|%s'   %(','.join(mc_prt_vars))]

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
        'FixedCutTight', #new for r21
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

    # To be updated with r21 when available
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
        asg_tool.CalibrationRelease = '170410_Moriond'

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
        asg_tool.CalibrationRelease = '170410_Moriond'

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

        isoTool = CfgMgr.CP__IsolationSelectionTool('IsolationSelectionTool_muon_%s' %ivar)
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

    # Updated to r21
    configPath = 'ElectronPhotonSelectorTools/offline/mc16_20170828/'
    
    configs = {
        'isLooseLH'       : 'ElectronLikelihoodLooseOfflineConfig2017_Smooth.conf',
        'isLooseLHWithBL' : 'ElectronLikelihoodLooseOfflineConfig2017_CutBL_Smooth.conf',
        'isMediumLH'      : 'ElectronLikelihoodMediumOfflineConfig2017_Smooth.conf',
        'isTightLH'       : 'ElectronLikelihoodTightOfflineConfig2017_Smooth.conf',
    }

    if key not in configs:
        raise Exception('getElecLHTool - unknown working point: %s' %key)
        
    elecLH  = CfgMgr.AsgElectronLikelihoodTool('ElectronLH_%s' %key)
    elecLH.ConfigFile = '%s/%s' %(configPath, configs[key])

    return elecLH

#======================================================================================
def getReadEvent(CfgMgr, ToolSvc, trig_decision):

    putool = CfgMgr.CP__PileupReweightingTool('MyPileupReweightingTool')
    
    putool.LumiCalcFiles = ['GoodRunsLists/data15_13TeV/20160720/physics_25ns_20.7.lumicalc.OflLumi-13TeV-005.root',
                            'GoodRunsLists/data16_13TeV/20170215/physics_25ns_20.7.lumicalc.OflLumi-13TeV-008.root'] 

    # Hacks for now - remove for grid submission
    #putool.UsePeriodConfig = 'MC16'
    #putool.ConfigFiles     = ['dev/PileupReweighting/mc16a_defaults_buggy.NotRecommended.prw.root']

    ToolSvc += putool

    alg = CfgMgr.Ath__ReadEvent('readEvent')
    alg.OutputLevel = 3
    alg.triggers    = getTriggers()
    alg.dummyVars   = getDummyVars()
    alg.debug       = False

    alg.trigDecision   = trig_decision
    alg.doTrigDecision = True

    alg.pileupTool     = putool
    alg.doPileup       = True

    return alg

#======================================================================================
def getReadPhysicsTruth(CfgMgr, name='readPhysicsTruth', option=''):

    alg = CfgMgr.Ath__ReadPhysicsTruth(name)

    alg.signalParticlePdgIds = [4, 5, 6, 7, 8, 15, 23, 24, 25, 32, 34, 35, 36, 37]
    alg.stableLeptonPdgIds   = [11, 12, 13, 14, 16]
    alg.minStableLeptonPt    = 5.0e3
    alg.outputStream         = 'out'
    alg.outputTruthPartName  = 'm_mc_part_'
    alg.outputTruthVtxName   = 'm_mc_vtx_'
    alg.fillHist             = True
    alg.saveTruthVertices    = True
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

    jet_cuts = ['Pt > 20.0e3']
    
    alg = CfgMgr.Ath__ReadJets('%s_readJets' %input_name)
    alg.inputContainerName  = input_name
    alg.outputContainerName = '%s_readJets' %(input_name)
    alg.truthContainerName  = 'AntiKt4TruthJets'
    alg.outputVectorName    = 'm_jet_'
    alg.saveExtraBtagInfo   = False
    alg.runOnPrimaryxAOD    = False
    alg.printAuxVars        = False
    alg.minPt               = 0.0e3
    alg.debug               = False
    alg.OutputLevel         = 3
    alg.auxVars             = getRJetAuxVars(option)
    alg.outputStream        = 'out'
    alg.configJetCuts       = jet_cuts

    #--------------------------------------------------------------------------------
    # Calibration and smearing tools - updated to rel 21
    #
    alg.jetCalibrationTool = CfgMgr.JetCalibrationTool('JESToolData')
    alg.jetCalibrationTool.ConfigFile    = 'JES_data2016_data2015_Recommendation_Dec2016_rel21.config'
    alg.jetCalibrationTool.JetCollection = 'AntiKt4EMTopo'
    alg.jetCalibrationTool.IsData        = (option.count('IS_DATA') > 0)

    #Pre recommendation r21
    if option.count('IS_DATA'):
        alg.jetCalibrationTool.CalibSequence = 'JetArea_Residual_EtaJES_GSC_Insitu' #JetArea_Residual_Origin_EtaJES_GSC_Insitu'
    else:
        alg.jetCalibrationTool.CalibSequence = 'JetArea_Residual_EtaJES_GSC' #'JetArea_Residual_Origin_EtaJES_GSC'

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
    for wp in ['70', '77', '85']:
        
        bjetEffTool = CfgMgr.BTaggingEfficiencyTool('bjetEffTool_%s' %wp)
        bjetEffTool.TaggerName          = 'MV2c10'
        bjetEffTool.OperatingPoint      = 'FixedCutBEff_%s' %wp
        bjetEffTool.JetAuthor           = input_name
        bjetEffTool.ScaleFactorFileName = '13TeV/2016-20_7-13TeV-MC15-CDI-2017-01-31_v1.root'

        bjetSelTool = CfgMgr.BTaggingSelectionTool('bjetSelTool_%s' %wp)
        bjetSelTool.TaggerName                   = 'MV2c10'
        bjetSelTool.OperatingPoint               = 'FixedCutBEff_%s' %wp
        bjetSelTool.JetAuthor                    = input_name
        bjetSelTool.FlvTagCutDefinitionsFileName = 'xAODBTaggingEfficiency/13TeV/2016-20_7-13TeV-MC15-CDI-2017-01-31_v1.root'
        
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
    alg.jvtUpdate = CfgMgr.JetVertexTaggerTool('UpdateJVT')
    alg.doJVT     = True

    jvtEffLoose = CfgMgr.CP__JetJvtEfficiency('JetJvtEff_Loose')
    jvtEffLoose.WorkingPoint = 'Loose'
    jvtEffLoose.SFFile       = 'JetJvtEfficiency/Moriond2017/JvtSFFile_EM.root'
    jvtEffLoose.TruthLabel   = ''
    
    jvtEffDefault = CfgMgr.CP__JetJvtEfficiency('JetJvtEff_Default')
    jvtEffLoose.WorkingPoint = 'Medium'
    jvtEffDefault.SFFile     = 'JetJvtEfficiency/Moriond2017/JvtSFFile_EM.root'
    jvtEffDefault.TruthLabel = ''
    
    alg.jvtEffDefault = jvtEffDefault
    alg.jvtEffLoose   = jvtEffLoose

    return alg

#======================================================================================
def getReadElec(CfgMgr, ToolSvc, input_name, option):

    elec_cuts = ['Pt > 5.0e3', 'isLooseLH > 0 || isLooseLHWithBL > 0 || DFCommonElectronsLHLoose > 0']
    
    alg = CfgMgr.Ath__ReadElec('%s_readElecs' %input_name)
    alg.inputContainerName = input_name
    alg.outputVectorName   = 'm_elec_'
    alg.printAuxVars       = False
    alg.outputStream       = 'out'
    alg.configElecCuts     = elec_cuts
    alg.minPt              = 5.0e3

    alg.trigMatchTool      = CfgMgr.Trig__MatchingTool('TrigMatchingTool', OutputLevel=3)
    alg.doTrigMatch        = True
    alg.triggers           = getTriggers('Elec')
    alg.isoTools           = getIsoElecTools(CfgMgr)

    # r21 pre-recommendation not in 2.6.4, update when available. No calibration until then
    alg.doEnergyCalibration = False
    alg.egammaCalibTool     = CfgMgr.CP__EgammaCalibrationAndSmearingTool('egammaCalibTool', 
                                                                          ESModel= 'es2016data_mc15c_summer', #'es2017_R21_PRE',
                                                                          decorrelationModel='1NP_v1')

    alg.elecLooseLHWithBL  = getElecLHTool(CfgMgr, 'isLooseLHWithBL')
    alg.elecLooseLH        = getElecLHTool(CfgMgr, 'isLooseLH')
    alg.elecMediumLH       = getElecLHTool(CfgMgr, 'isMediumLH')
    alg.elecTightLH        = getElecLHTool(CfgMgr, 'isTightLH')
    alg.doElecLikelihood   = True
    alg.auxVars            = getElecAuxVars(option)
    alg.debug              = False

    if option.count('IS_DATA') == 0: 
        alg.effCorrTools      = getElecEffCorrTools(CfgMgr)
        alg.doTruthClassifier = True

    for etool in alg.effCorrTools:
        etool.debug = alg.debug
    
    return alg

#======================================================================================
def getReadMuon(CfgMgr, ToolSvc, input_name, option, match_tool):

    ''' Process muons - MuonSelectionTool requires variables not stored with EGAM1 so it is disabled '''

    muon_cuts = ['Pt > 5.0e3', 'Loose > 0']
    
    select_muon  = CfgMgr.CP__MuonSelectionTool('muonSelectionTool_MCP', OutputLevel = 5)

    calibrate_muon  = CfgMgr.CP__MuonCalibrationAndSmearingTool('muonCalibrationTool_MCP', OutputLevel = 3)
    # Pre recommendation r21
    calibrate_muon.StatComb    = False #new change
    calibrate_muon.SagittaCorr = False #True

    ToolSvc += select_muon
    ToolSvc += calibrate_muon

    alg = CfgMgr.Ath__ReadMuon('%s_readMuons' %input_name)
    alg.inputContainerName = input_name
    alg.outputVectorName   = 'm_muon_'
    alg.printAuxVars       = False
    alg.debug              = False
    alg.OutputLevel        = 3
    alg.outputStream       = 'out'
    alg.configMuonCuts     = muon_cuts
    alg.minPt              = 5.0e3

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
def getReadTau(CfgMgr, ToolSvc, input_name, option):

    tau_cuts = ['Pt > 15.0e3', 'NTrack == 1 || NTrack == 3', 'Abs[Charge] == 1']

    alg = CfgMgr.Ath__ReadTaus('%s_readTaus' %input_name)

    alg.inputContainerName = input_name
    alg.outputVectorName   = 'm_tau_'
    alg.printAuxVars       = False
    alg.debug              = False
    alg.OutputLevel        = 3
    alg.outputStream       = 'out'
    alg.minPt              = 15.0e3
    alg.configTauCuts      = tau_cuts
    alg.auxVars            = getTauAuxVars(option)

    if option.count('IS_DATA') == 0:
        tau_smearing_tool = CfgMgr.TauAnalysisTools__TauSmearingTool('tauSmearingTool', OutputLevel = 3)
        tau_smearing_tool.RecommendationTag = '2017-moriond'
        tau_smearing_tool.ApplyMVATES       = True

        tau_truth_matching_tool = CfgMgr.TauAnalysisTools__TauTruthMatchingTool('tauTruthMatchingTool', OutputLevel = 5)
        tau_truth_matching_tool.WriteTruthTaus = True

        alg.doTruth              = True
        alg.tauSmearingTool      = tau_smearing_tool
        alg.tauTruthMatchingTool = tau_truth_matching_tool        

    return alg

#======================================================================================
def getReadTrackJet(CfgMgr, ToolSvc, input_name, option):

    alg = CfgMgr.Ath__ReadTrackJet('%s_readTrackJets' %input_name)

    alg.inputContainerName = input_name
    alg.outputVectorName   = 'm_track_jet_'
    alg.release21          = True
    alg.checkSimulation    = (input_name.count('Truth') > 0) 
    alg.OutputLevel        = 3
    alg.outputStream       = 'out'
    alg.debug              = False
    alg.auxVars            = getTJetAuxVars(option)
    alg.printAuxVars       = False    

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
    alg.configCutsBJet = ['MV2c10 > 0.1758475']
    
    alg.toolOR = recommended_tools('ORTool',
                                   #OutputLevel = VERBOSE,
                                   #inputLabel  = "",
                                   #RequireExpectedPointers = False,
                                   bJetLabel  = alg.varNamePassBJet,
                                   doEleEleOR = True,
                                   doTaus     = False,
                                   doPhotons  = False )

    alg.toolOR.MuJetORT.MuJetPtRatio    = 1e20
    alg.toolOR.MuJetORT.MuJetTrkPtRatio = 1e20

    return alg

#======================================================================================
def getFillMET(CfgMgr, ToolSvc, alg_name, option):

    alg = CfgMgr.Ath__FillMET('%s_fillMET' %alg_name)
    alg.outputStream         = 'out'
    alg.inputVecElec         = 'm_elec_'
    alg.inputVecMuon         = 'm_muon_'
    alg.inputVecJet          = 'm_jet_'

    alg.inputContMETMap      = 'METAssoc_AntiKt4LCTopo'
    alg.inputContMETCore     = 'MET_Core_AntiKt4LCTopo'
    alg.inputContTau         = ''
    alg.inputContPhoton      = ''

    alg.outputContElec       = 'Elec_%s' %alg_name
    alg.outputContMuon       = 'Muon_%s' %alg_name
    alg.outputContJet        = 'Jet_%s'  %alg_name
    alg.outputContMET        = 'MET_%s'  %alg_name

    alg.varNamePassSelection = 'MET_PassSelection'
    alg.varNameMET_LCTopo    = 'MET_LCTopo'
    alg.varNameMET_Track     = 'MET_Track'
    alg.debug                = False

    alg.configCutsElec       = getPreSelectionCuts_Elec()
    alg.configCutsMuon       = getPreSelectionCuts_Muon()
    alg.configCutsJet        = getPreSelectionCuts_Jet ()

    alg.toolMET = CfgMgr.met__METMaker('METMaker_%s' %alg_name,
                                       OutputLevel      = 3,
                                       JetSelection     = 'Tight',
                                       #JetRejectionDec  = "passFJVT",
                                       JetJvtMomentName = 'JVT' )

    return alg

#======================================================================================
def getElecAuxVars(option):

    auxVars = [('DFCommonElectronsLHLoose',  'Short'), 
               ('DFCommonElectronsLHMedium', 'Short'), 
               ('DFCommonElectronsLHTight',  'Short')]

    if option.count('IS_DATA') == 0:
        auxVars += [ ('firstEgMotherPdgId',       'Int'),
                     ('firstEgMotherTruthOrigin', 'Int'),
                     ('firstEgMotherTruthType',   'Int'),
                     ('truthOrigin',              'Int'),
                     ('truthPdgId',               'Int'),
                     ('truthType',                'Int')]
 
    outVars = []

    for v in auxVars:
        outVars += ['%s:type=%s' %(v[0], v[1])]

    return outVars

#======================================================================================
def getMuonAuxVars(option):

    auxVars = [('InnerDetectorPt',    'Float'),
               ('MuonSpectrometerPt', 'Float')]

    if option.count('IS_DATA') == 0:
        auxVars += [('truthOrigin',   'Int'),
                    ('truthType',     'Int')]

    outVars = []

    for v in auxVars:
        outVars += ['%s:type=%s' %(v[0], v[1])]

    return outVars

#======================================================================================
def getTauAuxVars(option):

    auxVars = [('EleMatchLikelihoodScore', 'Float')]

    if option.count('IS_DATA') == 0:
        auxVars += [('truthOrigin',        'Int'),
                    ('truthType',          'Int')]

    outVars = []

    for v in auxVars:
        outVars += ['%s:type=%s' %(v[0], v[1])]

    return outVars

#======================================================================================
def getRJetAuxVars(option):

    auxVars = [('EMFrac',      'Float'),
               ('DetectorEta', 'Float')]

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
def getPreSelectionCuts_Elec():
    
    cuts = ['Pt > 10.0e3',
            'Abs[EtaBE2] < 2.47',
            'Abs[EtaBE2] < 1.37 || Abs[EtaBE2] > 1.52',
            'isLooseLH > 0',
            'Abs[Z0Sin] < 0.5',
            'Abs[D0Sig] < 5.0']
    
    return cuts
   
#======================================================================================
def getPreSelectionCuts_Muon():
    
    cuts = ['Pt > 10.0e3',
            'Abs[Eta] < 2.5',
            'Loose > 0',
            'Abs[Z0Sin] < 0.5',
            'Abs[D0Sig] < 3.0']

    return cuts

#======================================================================================
def getPreSelectionCuts_Jet():
    
    cuts = ['Pt > 20.0e3', 
            'Abs[Eta] < 4.5']

    return cuts
