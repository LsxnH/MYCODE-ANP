
import os
import PhysicsAnpProd.PhysicsAnpProdUtils as Utils

#======================================================================================
def getSaveAlg(ToolSvc, CfgMgr, alg_list, stream='out', treename='nominal', option='', name=''):

    keys_event = ''
    branches   = []

    for alg in alg_list:
        branches   += alg.GetAllBranchVarsAsList()
        keys_event += alg.GetEventVarsAsStr()

    write_tool = CfgMgr.Ath__WriteEvent('writeEvent%s' %name)
    write_tool.stream     = stream
    write_tool.treename   = treename
    write_tool.branches   = branches
    write_tool.keys_event = keys_event

    ToolSvc += write_tool

    save_event = CfgMgr.Ath__SaveEvent('saveEvent%s' %name)
    save_event.writeEvent    = write_tool
    save_event.printVarNames = False
    
    return save_event

#======================================================================================
def getTriggers(key=''):

    #
    # https://twiki.cern.ch/twiki/bin/view/Atlas/MuonTriggerPhysicsRecommendationsRel212017#Single_muon_triggers
    #
    muon_triggers_2015 = [
        'HLT_mu20_iloose_L1MU15',
        'HLT_mu50',
    ]
    muon_triggers_2016 = [
        'HLT_mu24_ivarmedium',
        'HLT_mu26_ivarmedium',
        'HLT_mu26_imedium',
        'HLT_mu50',
    ]
    #
    # https://gitlab.cern.ch/atlas-physics/higgs/hww/HWWPhysicsxAODMaker/blob/master/PhysicsxAODConfig/python/HWWCommonAnalysisFlags.py
    #
    muon_triggers_ext = [
        'HLT_mu24_imedium',                       # 2016
        'HLT_mu26_ivarmedium',                    # 2016 + 2017
        'HLT_mu50',                               # 2017
        'HLT_mu60_0eta105_msonly',
        'HLT_mu50_0eta105_msonly'                 #New R21 muon trigger
        'HLT_mu26_ivarmedium_OR_HLT_mu50'
    ]
    #
    # https://twiki.cern.ch/twiki/bin/view/Atlas/TrigEgammaRecommendedTriggers2015
    #
    elec_triggers_2015 = [      
        'HLT_e24_lhmedium_L1EM20VH',
        'HLT_e24_lhmedium_L1EM18VH',
        'HLT_e60_lhmedium',
        'HLT_e120_lhloose',
    ]

    #
    # https://twiki.cern.ch/twiki/bin/view/Atlas/TrigEgammaRecommendedTriggers2016
    #
    elec_triggers_2016 = [      
        'HLT_e24_lhtight_nod0_ivarloose',
        'HLT_e26_lhtight_nod0_ivarloose',
        'HLT_e60_lhmedium_nod0',
        'HLT_e140_lhloose_nod0',
        'HLT_e300_etcut',
    ]
    elec_triggers_ext = [
         'HLT_e17_lhloose',                        # Legs from the electron-muon triggers 2015
         'HLT_e7_lhmedium',
         'HLT_e17_lhloose_nod0',                   # Legs from the electron-muon triggers 2016
         'HLT_e7_lhmedium_nod0',
         'HLT_e28_lhtight_nod0_ivarloose',         # 2017
    ]
    diElectronTriggerList = [ 'HLT_2e12_lhloose_L12EM10VH',             # 2015
                              'HLT_2e17_lhvloose_nod0',                 # 2016 + 2017
                              'HLT_2e17_lhvloose_nod0_L12EM15VHI*',     # 2017
    ]
    diMuonTriggerList     = [ 'HLT_mu18_mu8noL1',                       # 2015
                              'HLT_2mu10',
                              'HLT_mu20_mu8noL1',                       # 2016
                              'HLT_mu22_mu8noL1',                       # 2016 + 2017
                              'HLT_2mu14',                              # 2017
                              'HLT_mu22_mu8noL1_calotag_0eta010'
    ]
    multiElectronTriggerList = [ 'HLT_e17_lhloose_2e9_lhloose',            # 2015
                                 'HLT_e17_lhloose_nod0_2e9_lhloose_nod0',  # 2016
                                 'HLT_e24_lhvloose_nod0_2e12_lhvloose_nod0_L1EM20VH_3EM10VH' # 2017
    ]
    multiMuonTriggerList     = [ 'HLT_3mu6',
                                 'HLT_3mu6_msonly',
                                 'HLT_mu20_2mu4noL1',
                                 'HLT_3mu4',
                                 'HLT_2mu14',                              #New R21 multi-muon triggers
                                 'HLT_mu22_mu8noL1'
    ]
    ## Additional electron-muon trigger chains
    electronMuonTriggerList      = [ 'HLT_e17_lhloose_mu14',                   # 2015
                                     'HLT_e7_lhmedium_mu24',
                                     'HLT_e17_lhloose_nod0_mu14',              # 2016 + 2017
                                     'HLT_e7_lhmedium_nod0_mu24',
                                     'HLT_e26_lhmedium_nod0_mu8noL1',          # 2017
                                   ] 
    multiElectronMuonTriggerList = [ 'HLT_2e12_lhloose_mu10',                  # 2015
                                     'HLT_e12_lhloose_2mu10',
                                     'HLT_2e12_lhloose_nod0_mu10',             # 2016 + 2017
                                     'HLT_e12_lhloose_nod0_2mu10',
                                   ]

    muon_triggers = sorted(list(set(muon_triggers_2015 + muon_triggers_2016)))
    elec_triggers = sorted(list(set(elec_triggers_2015 + elec_triggers_2016)))
    met_triggers  = [ 'HLT_xe70' ]

    if   key == 'Elec': return elec_triggers
    elif key == 'Muon': return muon_triggers

    singleLeptonTriggerList = sorted(list(set(muon_triggers + elec_triggers + muon_triggers_ext + elec_triggers_ext)))
    diLeptonTriggerList     = sorted(list(set(diMuonTriggerList + diElectronTriggerList + electronMuonTriggerList)))
    multiLeptonTriggerList  = sorted(list(set(multiMuonTriggerList + multiElectronTriggerList + multiElectronMuonTriggerList)))
    allLeptonTriggerList    = sorted(list(set(singleLeptonTriggerList + diLeptonTriggerList + multiLeptonTriggerList)))

    return sorted(list(set(allLeptonTriggerList + met_triggers)))

#======================================================================================
def getIsoElecTools(CfgMgr):

    elec_vars = [
        'LooseTrackOnly',
        'Loose',
        'Gradient',
        'GradientLoose',
        'FixedCutTight',
        'FixedCutTightTrackOnly',
        'FixedCutLoose',
        'FixedCutHighPtCaloOnly',
        'FixedCutTrackCone40',
        ]

    new_vars = [
        'FCLoose', 
        'FCLoose_FixedRad',
        'FCTight',
        'FCTight_FixedRad',
        'FCHighPtCaloOnly',
        'FCTightTrackOnly_FixedRad',
        'FixedCutPflowLoose',
        'FixedCutPflowTight',
        'Gradient_exp',
        'FCTightTrackOnly_new',
        ]

    iso_tools = []

    for ivar in elec_vars + new_vars:

        isoTool = CfgMgr.CP__IsolationSelectionTool( 'IsolationSelectionTool_elec_%s' %ivar)
        isoTool.ElectronWP = ivar

        athTool = CfgMgr.Ath__IsoTool('Ath_IsoTool_elec_%s' %ivar)
        athTool.isoTool = isoTool
        athTool.varName = 'iso%s' %ivar

        iso_tools += [athTool]
        
    return iso_tools

#======================================================================================
def getElecEffCorrTools(CfgMgr):

    #
    # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/LatestRecommendationsElectronIDRun2#Details
    # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XAODElectronEfficiencyCorrectionTool#List_of_keys
    #
    
    out_list = []
    
    keys_id   = ['LooseBLayer', 'Medium', 'Tight']
    keys_iso  = ['FCLoose', 'FCTight', 'FCHighPtCaloOnly', 'Gradient', '']
    keys_trig = {'LepCorrSF_'        : '',
                 'LepCorrSF_Trig1L_' :     'SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_2018_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0',
                 'LepCorrEff_Trig1L_': 'Eff_SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_2018_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0',
                 }

    for key_id in keys_id + ['Reconstruction']:
        ikey = 'LepCorrSF_%s' %(key_id)
        
        if CfgMgr == None:
            out_list += [ikey]
            continue

        asg_tool = CfgMgr.AsgElectronEfficiencyCorrectionTool('CP_ElecCorr_%s' %ikey)        
        asg_tool.CorrelationModel = 'TOTAL'

        if key_id == 'Reconstruction':
            asg_tool.RecoKey = 'Reconstruction'
        else:
            asg_tool.IdKey   = key_id            

        eff_tool = CfgMgr.Ath__ElecEffCorrTool('Ath_ElecCorr_%s' %ikey)
        eff_tool.varName     = ikey
        eff_tool.corrToolSF  = asg_tool

        out_list += [eff_tool]    

    for key_id in keys_id:
        for key_iso in keys_iso:
            for (var_pref, key_trig) in keys_trig.iteritems():
                if key_iso == '' and not var_pref.count('Trig1L'):
                    continue
                ikey = '%s%s_iso%s' %(var_pref, key_id, key_iso)
                if key_iso == '':
                    ikey = '%s%s' %(var_pref, key_id)

                if CfgMgr == None:
                    out_list += [ikey]
                    continue

                asg_tool = CfgMgr.AsgElectronEfficiencyCorrectionTool('CP_ElecCorr_%s' %ikey)
                asg_tool.IdKey            = key_id
                asg_tool.IsoKey           = key_iso
                asg_tool.TriggerKey       = key_trig
                asg_tool.CorrelationModel = 'TOTAL'
                #asg_tool.MapFilePath      = 'ElectronEfficiencyCorrection/2015_2017/rel21.2/Consolidation_September2018_v1/map0.txt'

                eff_tool = CfgMgr.Ath__ElecEffCorrTool('Ath_ElecCorr_%s' %ikey)
                eff_tool.varName     = ikey
                eff_tool.corrToolSF  = asg_tool

                out_list += [eff_tool]

    return out_list

#======================================================================================
def getMuonEffCorrRecoTools(CfgMgr):

    #
    # https://gitlab.cern.ch/atlas/athena/blob/21.2/PhysicsAnalysis/MuonID/MuonIDAnalysis/MuonEfficiencyCorrections/share/MuonEfficiencyCorrections_xAOD_Testing_jobOptions.py
    #  LowPt doesn't work
    #
    # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/IsolationSelectionTool#Leptons_PU_robust #doesn't work
    #
    out_list = []

    keys_pid = ['Loose', 'Medium', 'Tight', 'HighPt', 'TTVA']
    keys_iso = ['FixedCutLoose',      'FixedCutTight', 
                'FCLoose',            'FCTight',          'FCTightTrackOnly',
                'FCLoose_FixedRad',   'FCTight_FixedRad', 'FCTightTrackOnly_FixedRad',
                'FixedCutPflowLoose', 'FixedCutPflowTight',
               ]
   
    for key_pid in keys_pid:
        ikey = 'LepCorrSF_%s' %(key_pid)
            
        if CfgMgr == None:
            out_list += [ikey]
            continue

        asg_tool = CfgMgr.CP__MuonEfficiencyScaleFactors('CP_MuonCorr_%s' %ikey)
        asg_tool.WorkingPoint       = key_pid
        asg_tool.CalibrationRelease = '190220_Winter_r21'

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
        asg_tool.CalibrationRelease = '190220_Winter_r21'

        eff_tool = CfgMgr.Ath__MuonEffCorrRecoTool('Ath_MuonCorr_%s' %ikey)
        eff_tool.debug          = False
        eff_tool.varName        = ikey
        eff_tool.corrToolRecoSF = asg_tool
            
        out_list += [eff_tool]

    return out_list

#======================================================================================
def getMuonEffCorrTrigTools(CfgMgr, option=''):
    #
    # https://twiki.cern.ch/twiki/bin/view/Atlas/MuonTriggerPhysicsRecommendationsRel212017#Supported_triggers
    #
    
    out_list  = []
    keys_id   = ['Loose', 'Medium', 'Tight', 'HighPt']

    keys_trig = {2015:'HLT_mu20_iloose_L1MU15_OR_HLT_mu50',
                 2016:'HLT_mu26_ivarmedium_OR_HLT_mu50',
                 2017:'HLT_mu26_ivarmedium_OR_HLT_mu50',
                 2018:'HLT_mu26_ivarmedium_OR_HLT_mu50'
                }

    for key_id in keys_id:
        skey = 'LepCorrSF_Trig1L_%s'  %(key_id)
        ekey = 'LepCorrEff_Trig1L_%s' %(key_id)
            
        if CfgMgr == None:            
            if option.count('IS_DATA'): out_list += [ekey]
            else:                       out_list += [ekey, skey]
            continue
                
        for year, trigger in keys_trig.iteritems():
            trigkey = '%s_%d_%s' %(skey, year, trigger)

            asg_tool = CfgMgr.CP__MuonTriggerScaleFactors('CP_MuonTrigSF_%s' %trigkey)
            asg_tool.MuonQuality = key_id
            
            eff_tool = CfgMgr.Ath__MuonEffCorrTrigTool('Ath_MuonTrigSF_%s' %(trigkey))
            eff_tool.debug           = False
            eff_tool.varName         = skey
            eff_tool.effName         = ekey
            eff_tool.trigger         = trigger
            eff_tool.configEventCuts = getYearCuts(option, year)
            eff_tool.corrToolTrigSF  = asg_tool
        
            out_list += [eff_tool]
        
    return out_list

#======================================================================================
def getIsoMuonTools(CfgMgr, ToolSvc):

    muon_vars = [
        'LooseTrackOnly',
        'Loose',
        'Gradient',
        'GradientLoose',
        'FixedCutLoose',
        'FixedCutTightTrackOnly',
        'FixedCutTight',
        'FixedCutHighPtTrackOnly',
        ]

    new_vars = [
        'FCLoose', 
        'FCLoose_FixedRad',
        'FCTight',
        'FCTight_FixedRad',
        'FCTightTrackOnly',
        'FCTightTrackOnly_FixedRad',
        'FixedCutPflowTight',
        'FixedCutPflowLoose',
        'FixedCutHighMuTight',
        'FixedCutHighMuLoose',
        'FixedCutHighMuTrackOnly',
        ]

    iso_tools = []

    for ivar in muon_vars + new_vars:

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
def getReadEvent(CfgMgr, ToolSvc, option, trig_decision, mcSubCampaign=None):

    #----------------------------------------------------------------------------------
    # Configure output variables
    #
    outVars = ['Event                :type=Long',
               'Run                  :type=Int',
               'LumiBlock            :type=Int',
               'bcid                 :type=Int',
               'backgroundFlags      :type=UInt',
               'ActualInteractions   :type=Float',
               'AverageInteractions  :type=Float',
               'eventTriggerPass     :type=Short',
               'NRecoVtx             :type=Short',
               'HasPriVtx            :type=Short',
               'IsGRL                :type=Short',
               'EventFlag_Core       :type=Short',
               'IsEventFlagBitSet    :type=Short',
               'ErrorState_Core      :type=Short',
               'ErrorState_Background:type=Short',
               'ErrorState_LAr       :type=Short',
               'ErrorState_Tile      :type=Short',
               'ErrorState_SCT       :type=Short',
               'ErrorState_Pixel     :type=Short',
               'ErrorState_TRT       :type=Short',
               'ErrorState_Muon      :type=Short',
               'BeamPosX             :type=Float',
               'BeamPosY             :type=Float',
               'BeamPosZ             :type=Float',
               'BeamPosSigmaX        :type=Float',
               'BeamPosSigmaY        :type=Float',
               'BeamPosSigmaZ        :type=Float']
    
    auxVars = ['DFCommonJets_isBadBatman:         type=Int',
               'DFCommonJets_eventClean_LooseBad: type=Int']

    vtxVars = ['vx                    :type=Float',
               'vy                    :type=Float',
               'vz                    :type=Float',
               'type                  :type=Short',
               'NTrack                :type=Short',
               'IndexRangeTrack       :type=VecInt']

    svtxVars = ['x                              :type=Float',
                'y                              :type=Float',
                'z                              :type=Float',
                'chiSquared                     :type=Float',
                'numberDoF                      :type=Float',
                'SecondaryVertexIndex           :type=Int',
                'SecondaryVertexIndexVectorInput:type=VecInt',
                'distToPriVtx                   :type=Float',
                'normDistToPriVtx               :type=Float',
                'distToRefittedRmLepPriVtx      :type=Float',
                'normDistToRefittedRmLepPriVtx  :type=Float',
                'mass                           :type=Float']

    rvtxVars = ['x                              :type=Float',
                'y                              :type=Float',
                'z                              :type=Float',
                'chiSquared                     :type=Float',
                'numberDoF                      :type=Float',
                'normDistToPriVtx               :type=Float',
                'normDistToRefittedPriVtx       :type=Float',
                'distToPriVtx                   :type=Float',
                'distToRefittedPriVtx           :type=Float',
                'vertexType                     :type=Short',
                'refittedVertexType             :type=Short',
                ]

    cvtxVars = ['vertexType                     :type=Short',
                'x                              :type=Float',
                'y                              :type=Float',
                'z                              :type=Float',
                'chiSquared                     :type=Float',
                'numberDoF                      :type=Float',
                'px                             :type=Float',
                'py                             :type=Float',
                'pz                             :type=Float',
                'mass                           :type=Float',
                'DR1R2                          :type=Float',
                'deltaCotThetaTrk               :type=Float',
                'deltaInitRadius                :type=Float',
                'deltaPhiTracks                 :type=Float',
                'deltaPhiVtxTrk                 :type=Float',
                'etaAtCalo                      :type=Float',
                'minRfirstHit                   :type=Float',
                'minimumDistanceTrk             :type=Float',
                'phiAtCalo                      :type=Float',
                'pt1                            :type=Float',
                'pt2                            :type=Float',
                ]

    if option.count('IS_DATA') == 0:
        outVars += ['MCChannel      :type=Int',
                    'MCWeight       :type=Float',
                    'PUWeight       :type=Float',
                    'JVTWeight      :type=Float',
                    'FJVTWeight     :type=Float',
                    'CorrectedMu    :type=Float',
                    'RandomRunNumber:type=Int',
                    'PRWHash        :type=ULong',
                    'IsOverlap      :type=Short',
                    'PhotonPts      :type=VecFloat'
                    ]

        auxVars += ['mcEventNumber:type=ULong',
                    'GenFiltHT:    type=Float',
                    'GenFiltMET:   type=Float']

    if option.count('doDetails') > 0:
        outVars += ['EventDensityCentral:type=Float',
                    'EventDensityForward:type=Float']

    #----------------------------------------------------------------------------------
    # Pileup tool:
    #  https://gitlab.cern.ch/atlas/athena/blob/cf96bc809fc9ffcc388c09ec80434de3b14976f6/PhysicsAnalysis/AnalysisCommon/PileupReweighting/Root/PileupReweightingTool.cxx#L176
    # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/ExtendedPileupReweighting#Notes_for_users_of_MC16d
    #    

    #PRWConfigFilesFSmc16a   = [ 'PhysicsAnpProd/data/PRW/HWW_merged_prw_config_mc16a_FS_v1.root' ]
    #PRWConfigFilesAFIImc16a = [ 'PhysicsAnpProd/data/PRW/HWW_merged_prw_config_mc16a_AFII_v1.root' ]
    PRWConfigFilesFSmc16a   = [ '/lustre/AtlUser/liheng/WH/PRWConfigFiles/MergedConfigFiles/HWW_merged_prw_config_mc16a_FS_v1.root' ]
    PRWConfigFilesAFIImc16a = [ '/lustre/AtlUser/liheng/WH/PRWConfigFiles/MergedConfigFiles/HWW_merged_prw_config_mc16a_AFII_v1.root' ]
    LumiCalcFilesData1516   = [ 'GoodRunsLists/data15_13TeV/20170619/PHYS_StandardGRL_All_Good_25ns_276262-284484_OflLumi-13TeV-008.root',
                                'GoodRunsLists/data16_13TeV/20180129/PHYS_StandardGRL_All_Good_25ns_297730-311481_OflLumi-13TeV-009.root' ]

    PRWConfigFilesFSmc16d   = [ 'PhysicsAnpProd/data/PRW/HWW_merged_prw_config_mc16d_FS_v1.root' ]
    PRWConfigFilesAFIImc16d = [ 'PhysicsAnpProd/data/PRW/HWW_merged_prw_config_mc16d_AFII_v1.root' ]
    PRWActualMuData17       = [ 'GoodRunsLists/data17_13TeV/20180619/physics_25ns_Triggerno17e33prim.actualMu.OflLumi-13TeV-010.root' ]
    LumiCalcFilesData17     = [ 'GoodRunsLists/data17_13TeV/20180619/physics_25ns_Triggerno17e33prim.lumicalc.OflLumi-13TeV-010.root' ]

    PRWConfigFilesFSmc16e   = [ 'PhysicsAnpProd/data/PRW/HWW_merged_prw_config_mc16e_FS_v1.root' ]
    PRWConfigFilesAFIImc16e = [ 'PhysicsAnpProd/data/PRW/HWW_merged_prw_config_mc16e_AFII_v1.root' ]
    PRWActualMuData18       = [ 'GoodRunsLists/data18_13TeV/20181111/purw.actualMu.root' ]
    LumiCalcFilesData18     = [ 'GoodRunsLists/data18_13TeV/20181111/ilumicalc_histograms_None_348885-364292_OflLumi-13TeV-001.root' ]

    putool = CfgMgr.CP__PileupReweightingTool('MyPileupReweightingTool')

    if mcSubCampaign == 'mc16a':
        putool.ConfigFiles   = PRWConfigFilesFSmc16a
        putool.LumiCalcFiles = LumiCalcFilesData1516
    elif mcSubCampaign == 'mc16d':
        putool.ConfigFiles   = PRWConfigFilesFSmc16d + PRWActualMuData17
        putool.LumiCalcFiles = LumiCalcFilesData17
    elif mcSubCampaign == 'mc16e':
        putool.ConfigFiles   = PRWConfigFilesFSmc16e + PRWActualMuData18
        putool.LumiCalcFiles = LumiCalcFilesData18
    else:
        raise Exception('getReadEvent - unknown MC SubCampaign: %s' %mcSubCampaign)

    ToolSvc += putool

    #----------------------------------------------------------------------------------
    # Algorithm pre-select data events according to GoodRunsList
    #
    grlFileList = [ 'GoodRunsLists/data15_13TeV/20170619/data15_13TeV.periodAllYear_DetStatus-v89-pro21-02_Unknown_PHYS_StandardGRL_All_Good_25ns.xml',
                    'GoodRunsLists/data16_13TeV/20180129/data16_13TeV.periodAllYear_DetStatus-v89-pro21-01_DQDefects-00-02-04_PHYS_StandardGRL_All_Good_25ns.xml',
                    'GoodRunsLists/data17_13TeV/20180619/data17_13TeV.periodAllYear_DetStatus-v99-pro22-01_Unknown_PHYS_StandardGRL_All_Good_25ns_Triggerno17e33prim.xml',
                    'GoodRunsLists/data18_13TeV/20181111/data18_13TeV.periodAllYear_DetStatus-v102-pro22-04_Unknown_PHYS_StandardGRL_All_Good_25ns_Triggerno17e33prim.xml'
                  ]
    grltool = CfgMgr.GoodRunsListSelectionTool('MyGoodRunsListSelectionTool', GoodRunsListVec = grlFileList)
    ToolSvc += grltool

    #----------------------------------------------------------------------------------
    # Algorithm to decide Vjets/Vgamma overlap removal
    #
    #gamORtool = CfgMgr.CP__VGammaORTool('MyVGammaORTool')
    gamORtool = CfgMgr.VGammaORTool('MyVGammaORTool')
    #gamORtool.use_gamma_iso = False
    gamORtool.use_gamma_iso = True
    ToolSvc += gamORtool

    #----------------------------------------------------------------------------------
    # Algorithm to read event information
    #
    alg = CfgMgr.Ath__ReadEvent('readEvent')
    alg.OutputLevel       = 3
    alg.debug             = False
    alg.printAuxVars      = False
    alg.outputStream      = 'out'
    alg.triggers          = getTriggers()
    alg.auxVars           = auxVars

    alg.trigDecision   = trig_decision
    alg.doTrigDecision = True

    for trigger in alg.triggers:
        outVars += ['%s:type=Short' %trigger]

    data = Utils.AlgData(alg)
    data.AddEventVars(outVars+auxVars)

    if option.count('doDetails'):
        alg.outputRecoVtxName = 'm_primary_vtx_'
        data.AddBranchVars(alg.outputRecoVtxName, vtxVars)  

        alg.auxVarsSecondaryVertex    = svtxVars
        alg.doPileup                  = False
        alg.secondaryVertexContainers = ['SecVtxContainer_Electrons:m_secondary_vtx_elec_', 
                                         'SecVtxContainer_Muons:m_secondary_vtx_muon_']

        data.AddBranchVars('m_secondary_vtx_elec_', svtxVars + ['IndexRangeTrack:type=VecInt'])
        data.AddBranchVars('m_secondary_vtx_muon_', svtxVars + ['IndexRangeTrack:type=VecInt'])

        alg.auxVarsRefittedVertex  = rvtxVars
        alg.containerRefitVertices = 'RefittedPriVtx'
        alg.outputRefitVtxName     = 'm_refit_privtx_'

        if option.count('doConv'):
            alg.auxVarsConversionVertex     = cvtxVars
            alg.containerConversionVertices = 'GSFConversionVertices'
            alg.outputConversionVtxName     = 'm_gsf_conversion_vtx_'
            
            data.AddBranchVars(alg.outputRefitVtxName,      rvtxVars + ['Barcode:type=Int', 'IndexRangeTrack:type=VecInt'])
            data.AddBranchVars(alg.outputConversionVtxName, cvtxVars + ['Barcode:type=Int', 'IndexRangeTrack:type=VecInt', 'NTrack:type=Short'])
    else:
        alg.pileupTool = putool
        alg.doPileup   = True
        alg.GRLTool    = grltool
        alg.doGRL      = True
        alg.GamORTool  = gamORtool
        alg.doGamOR    = True

    return data

#======================================================================================
def getReadPhysicsTruth(CfgMgr, name, part_out, vtx_out='', option=''):

    alg = CfgMgr.Ath__ReadPhysicsTruth(name)

    alg.signalParticlePdgIds = [4, 5, 6, 7, 8, 15, 22, 23, 24, 25, 32, 34, 35, 36, 37]
    alg.stableLeptonPdgIds   = [11, 12, 13, 14, 16]
    alg.minStableLeptonPt    = 5.0e3
    alg.outputStream         = 'out'
    alg.outputTruthPartName  = part_out
    alg.outputTruthVtxName   = vtx_out
    alg.fillHist             = True
    alg.debug                = False

    data = Utils.AlgData(alg)
    data.AddBranchVars(part_out, getTruthPartVars())

    if len(vtx_out):
        alg.saveTruthVertices = False
        data.AddBranchVars(vtx_out,  getTruthVtxVars())

    return data

#======================================================================================
def getReadSimpleTruth(CfgMgr, name, part_out, vtx_out, option=''):

    alg = CfgMgr.Ath__ReadSimpleTruth(name)

    alg.outputStream               = 'out'
    alg.outputTruthPartName        = part_out
    alg.outputTruthVtxName         = vtx_out
    alg.fillHist                   = True
    alg.saveTruthVertices          = True
    alg.saveOnlyGeneratorParticles = False
    alg.debug                      = False
    
    data = Utils.AlgData(alg)
    data.AddBranchVars(part_out, getTruthPartVars())
    data.AddBranchVars(vtx_out,  getTruthVtxVars())

    return data

#======================================================================================
def getReadJet(CfgMgr, ToolSvc, input_name, output_name, option):

    #----------------------------------------------------------------------------------
    # Configure output variables
    #
    outVars = ['Pt                    :type=Float',
               'Eta                   :type=Float',
               'Phi                   :type=Float',
               'Energy                :type=Float',
               'Mass                  :type=Float',
               'JVTPass               :type=Short',
               'JVTPassLoose          :type=Short',
               'FJVTPass              :type=Short',
               'isLooseBad            :type=Short',
               'ORHFJets_PassBJet     :type=Short',
               'ORHFJets_PassSelection:type=Short',
               'ORHFJets_IsRemoved:    type=Short',
               'isTightBad:            type=Short',
               ]
    
    auxVars = ['Jvt:                            type=Float', 
               'EMFrac:                         type=Float',
               'DetectorEta:                    type=Float',
               'DFCommonJets_jetClean_LooseBad: type=Short',
               'DFCommonJets_jetClean_TightBad: type=Short']

    auxVarsBTagging = ['MV2c10_discriminant:type=Float']
    
    if option.count('IS_DATA') == 0:
        outVars += ['TruthJetDR:type=Float',
                    'TruthJetPt:type=Float',
                    'TruthJetID:type=Short']

        auxVars += ['PartonTruthLabelID:                type=Short',
                    'ConeTruthLabelID:                  type=Short',
                    'HadronConeExclExtendedTruthLabelID:type=Short',
                    'HadronConeExclTruthLabelID:        type=Short']

    #----------------------------------------------------------------------------------
    # Configure tools and algorithms
    #
    alg = CfgMgr.Ath__ReadJets('read%s' %input_name)
    alg.inputContainerName  = '%sJets' %input_name
    alg.outputContainerName = '%sJets_readJets' %(input_name)
    alg.truthContainerName  = 'AntiKt4TruthJets'
    alg.outputVectorName    = output_name
    alg.outputStream        = 'out'

    alg.saveExtraBtagInfo   = False
    alg.runOnPrimaryxAOD    = False
    alg.printAuxVars        = False
    alg.debug               = False
    alg.OutputLevel         = 3
    alg.doTileCorrection    = option.count('doDetails') == 0

    alg.auxVars             = auxVars
    alg.auxVarsBTagging     = auxVarsBTagging
    alg.configJetCuts       = ['[Pt] > 20.0e3']

    #--------------------------------------------------------------------------------
    # Calibration and smearing tools - updated to rel 21
    #
    alg.jetCalibrationTool = CfgMgr.JetCalibrationTool('JESToolData')

    if input_name == 'AntiKt4EMPFlow':
        alg.jetCalibrationTool.ConfigFile = 'JES_data2017_2016_2015_Consolidated_PFlow_2018_Rel21.config'
    elif input_name == 'AntiKt4EMTopo':
        alg.jetCalibrationTool.ConfigFile = 'JES_data2017_2016_2015_Consolidated_EMTopo_2018_Rel21.config'
    else:
        raise Exception('getReadJets - unknown jet collection %s' %input_name)
 
    alg.jetCalibrationTool.JetCollection = input_name
    alg.jetCalibrationTool.IsData        = (option.count('IS_DATA') > 0)
    alg.jetCalibrationTool.CalibArea     = '00-04-82'

    if option.count('IS_DATA'):
        alg.jetCalibrationTool.CalibSequence = 'JetArea_Residual_EtaJES_GSC_Insitu' 
    else:
        alg.jetCalibrationTool.CalibSequence = 'JetArea_Residual_EtaJES_GSC_Smear'

    alg.jetUncertaintyTool = CfgMgr.JetUncertaintiesTool('jetUncertaintiesTool')
    alg.jetUncertaintyTool.JetDefinition = input_name
    alg.jetUncertaintyTool.MCType        = 'MC16'
    alg.jetUncertaintyTool.ConfigFile    = 'rel21/Fall2018/R4_CategoryReduction_SimpleJER.config'
    alg.jetUncertaintyTool.CalibArea     = 'CalibArea-06'

    JERTool = CfgMgr.JERTool('jerTool')
    JERTool.PlotFileName   = 'JetResolution/Prerec2015_xCalib_2012JER_ReducedTo9NP_Plots_v2.root'
    JERTool.CollectionName = alg.inputContainerName

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
    # Jet vertex tools
    #
    alg.jvtUpdate = CfgMgr.JetVertexTaggerTool('UpdateJVT')
    alg.doJVT     = True

    jvtEffLoose = CfgMgr.CP__JetJvtEfficiency('JetJvtEff_Loose')
    jvtEffLoose.WorkingPoint = 'Loose'
    jvtEffLoose.SFFile       = 'JetJvtEfficiency/Moriond2018/JvtSFFile_EMTopoJets.root'
    jvtEffLoose.JetJvtMomentName = 'calibJvt'
    
    jvtEffDefault = CfgMgr.CP__JetJvtEfficiency('JetJvtEff_Default')
    jvtEffDefault.WorkingPoint = 'Medium'
    jvtEffDefault.SFFile       = 'JetJvtEfficiency/Moriond2018/JvtSFFile_EMTopoJets.root'
    jvtEffDefault.JetJvtMomentName = 'calibJvt'

    fjvtEffDefault = CfgMgr.CP__JetJvtEfficiency('JetFJvtEff_Default')
    fjvtEffDefault.SFFile           = 'JetJvtEfficiency/Moriond2018/fJvtSFFile.root'
    fjvtEffDefault.JetJvtMomentName = 'calibJvt'

    alg.jvtEffDefault  = jvtEffDefault
    alg.jvtEffLoose    = jvtEffLoose
    alg.fjvtEffDefault = fjvtEffDefault

    #-------------------------------------------------------------------------------
    # Forward Jet vertex tools
    # https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/ForwardJVT#Implementation
    fjvtTool = CfgMgr.JetForwardJvtTool('FJvtTool')
    fjvtTool.CentralMaxPt = 60.0e3
    fjvtTool.OutputDec    = 'passFJVT'
    fjvtTool.JvtMomentName = 'calibJvt'

    alg.fjvtTool = fjvtTool
    alg.doFJVT   = True
    
    #--------------------------------------------------------------------------------
    # JES and b-tagging calibration tools
    #
    for wp in ['70', '77', '85']:
        if input_name == 'AntiKt4EMPFlow':
            continue
        
        bjetEffTool = CfgMgr.BTaggingEfficiencyTool('bjetEffTool_%s' %wp)
        bjetEffTool.TaggerName          = 'MV2c10'
        bjetEffTool.OperatingPoint      = 'FixedCutBEff_%s' %wp
        bjetEffTool.JetAuthor           = alg.inputContainerName
        bjetEffTool.ScaleFactorFileName = 'xAODBTaggingEfficiency/13TeV/2017-21-13TeV-MC16-CDI-2018-06-29_v1.root'

        bjetSelTool = CfgMgr.BTaggingSelectionTool('bjetSelTool_%s' %wp)
        bjetSelTool.TaggerName                   = 'MV2c10'
        bjetSelTool.OperatingPoint               = 'FixedCutBEff_%s' %wp
        bjetSelTool.JetAuthor                    = alg.inputContainerName
        bjetSelTool.FlvTagCutDefinitionsFileName = 'xAODBTaggingEfficiency/13TeV/2017-21-13TeV-MC16-CDI-2018-06-29_v1.root'
        
        bjetTool = CfgMgr.Ath__BJetTool('bjetTool_%s' %wp)
        bjetTool.nameVarBTag = 'MV2c10_%s_Pass' %wp
        bjetTool.nameVarEff  = 'MV2c10_%s_Eff'  %wp
        bjetTool.nameVarSF   = 'MV2c10_%s_SF'   %wp
        bjetTool.effTool     = bjetEffTool
        bjetTool.selTool     = bjetSelTool
        bjetTool.debug       = False
        bjetTool.OutputLevel = 3

        alg.bjetTools += [bjetTool]

        outVars += ['%s:type=Float' %bjetTool.nameVarBTag, 
                    '%s:type=Float' %bjetTool.nameVarEff, 
                    '%s:type=Float' %bjetTool.nameVarSF]

    return Utils.AlgData(alg, outVars + auxVars + auxVarsBTagging)

#======================================================================================
def getReadElec(CfgMgr, ToolSvc, input_name, output_name, option):

    #----------------------------------------------------------------------------------
    # Configure output variables
    #
    outVars =  ['Pt             :type=Float',
                'PtRaw          :type=Float',
                'Eta            :type=Float',
                'EtaBE2         :type=Float',
                'Phi            :type=Float',
                'Energy         :type=Float',
                'PDG            :type=Int',
                'D0             :type=Float',
                'D0Sig          :type=Float',
                'Z0             :type=Float',
                'Z0Sin          :type=Float',
                'Z0Sig          :type=Float',
                'TrackPhi       :type=Float',
                'TrackTheta     :type=Float',
                'TrackPt        :type=Float',
                'ClEta          :type=Float',
                'ClPhi          :type=Float',
                'ClEt           :type=Float',
                'IsGoodQuality  :type=Short',
                'NTrack         :type=Short',
                'IndexRangeTrack:type=VecInt'] + getCommonLeptonOutVars()
    
    auxVars = ['author:                           type=Short',
               'OQ:                               type=UInt',
               'ambiguityType:                    type=Short',
               'DFCommonElectronsLHLoose:         type=Short', 
               'DFCommonElectronsLHLooseBL:       type=Short', 
               'DFCommonElectronsLHMedium:        type=Short', 
               'DFCommonElectronsLHTight:         type=Short',
               'DFCommonElectronsECIDS:           type=Short',
               'DFCommonElectronsECIDSResult:     type=Float',
               'ptvarcone20:                      type=Float',
               'ptvarcone20_TightTTVA_pt1000:     type=Float',
               'ptvarcone30:                      type=Float',
               'ptvarcone30_TightTTVA_pt500:      type=Float',
               'ptvarcone30_TightTTVA_pt1000:     type=Float',
               'ptvarcone40:                      type=Float',
               'topoetcone20:                     type=Float',
               'topoetcone30:                     type=Float',
               'topoetcone40:                     type=Float'] + getCommonLeptonAuxVars(option)

    if option.count('IS_DATA') == 0:
        auxVars += ['firstEgMotherPdgId:                type=Int',
                    'firstEgMotherTruthOrigin:          type=Int',
                    'firstEgMotherTruthType:            type=Int',
                    'lastEgMotherPdgId:                 type=Int',
                    'lastEgMotherTruthOrigin:           type=Int',
                    'lastEgMotherTruthType:             type=Int',
                    'truthOrigin:                       type=Int',
                    'truthPdgId:                        type=Int',
                    'truthType:                         type=Int']

        outVars += ['firstEgMotherTruthParticleBarcode: type=Int',
                    'lastEgMotherTruthParticleBarcode:  type=Int',
                    'truthParticleBarcode:              type=Int']
                    
    if option.count('doDetails'):
        auxVars += ['deltaEta1:                        type=Float',
                    'deltaPhi1:                        type=Float',
                    'deltaPhi2:                        type=Float',
                    'deltaPhiFromLastMeasurement:      type=Float',
                    'deltaPhiRescaled2:                type=Float',
                    'wtots1:                           type=Float',
                    'Eratio:                           type=Float']

    #----------------------------------------------------------------------------------
    # Configure algorithm and tools
    #
    alg = CfgMgr.Ath__ReadElec('read%s' %input_name)
    alg.inputContainerName  = input_name
    alg.outputVectorName    = output_name
    alg.outputStream        = 'out'
    alg.configElecCuts      = ['[DFCommonElectronsLHLoose] > 0 || [DFCommonElectronsLHLooseBL] > 0', '[Pt] > 4.0e3']
    alg.minPtRaw            = 4.0e3

    alg.egammaCalibTool     = CfgMgr.CP__EgammaCalibrationAndSmearingTool('egammaCalibTool', 
                                                                          ESModel= 'es2017_R21_v1',
                                                                          decorrelationModel='1NP_v1')

    alg.trigMatchTool       = CfgMgr.Trig__MatchingTool('TrigMatchingTool', OutputLevel=3)
    alg.doTrigMatch         = True
    alg.triggers            = getTriggers('Elec')
    alg.isoTools            = getIsoElecTools(CfgMgr)

    alg.doEnergyCalibration = True
    alg.auxVars             = auxVars
    alg.printAuxVars        = False
    alg.debug               = False

    if option.count('IS_DATA') == 0 and option.count('doDetails') == 0: 
        #
        # Efficiency scale factors are NOT implemented yet
        #            
        alg.effCorrTools      = getElecEffCorrTools(CfgMgr)
        alg.doTruthClassifier = True

    #
    # Add output variables for saving
    #
    for itool in alg.isoTools:
        outVars += ['%s:type=Short' %itool.varName]

    for etool in alg.effCorrTools:
        etool.debug = alg.debug
        outVars += ['%s:type=Float' %etool.varName]

    for trig in alg.triggers:
        outVars += ['match_%s:type=Short' %trig]

    return Utils.AlgData(alg, auxVars+outVars)

#======================================================================================
def getReadMuon(CfgMgr, ToolSvc, input_name, output_name, option, match_tool):

    #----------------------------------------------------------------------------------
    # Configure output variables
    #
    outVars = ['Pt             :type=Float',
               'PtRaw          :type=Float',
               'Eta            :type=Float',
               'Phi            :type=Float',
               'PDG            :type=Int',
               'D0             :type=Float',
               'D0Sig          :type=Float',
               'Z0             :type=Float',
               'Z0Sin          :type=Float',
               'Z0Sig          :type=Float',
               'Loose          :type=Short',
               'Medium         :type=Short',
               'Tight          :type=Short',
               'HighPt         :type=Short',
               'PassedID       :type=Short',
               'isBadMuon      :type=Short',
               'Quality        :type=Short',
               'MuonType       :type=Short',
               'TrackPt        :type=Float',
               'IDTrackPt      :type=Float',
               'IDTrackBarcode :type=Int',
               'MSTrackPt      :type=Float',
               'IndexRangeTrack:type=VecInt'] + getCommonLeptonOutVars()

    auxVars = ['author:                      type=Short',
               'InnerDetectorPt:             type=Float',
               'MuonSpectrometerPt:          type=Float',
               'ptvarcone20:                 type=Float',
               'ptvarcone30:                 type=Float',
               'ptvarcone40:                 type=Float',
               'ptvarcone30_TightTTVA_pt500: type=Float',
               'ptvarcone30_TightTTVA_pt1000:type=Float',
               'topoetcone20:                type=Float',
               'topoetcone30:                type=Float',
               'topoetcone40:                type=Float',
               'momentumBalanceSignificance: type=Short',
               'numberOfPrecisionLayers:     type=Short',
               'DFCommonGoodMuon:            type=Short'] + getCommonLeptonAuxVars(option)

    auxVarsCluster = ['calE:              type=Float',
                      'calEta:            type=Float',
                      'calPhi:            type=Float',
                      'e_sampl:           type=VecFloat:nick=cal_e_sampl']

    if option.count('IS_DATA') == 0:
        auxVars += ['truthOrigin:type=Int',
                    'truthType:  type=Int']

        outVars += ['truthParticleBarcode:type=Int']

    if option.count('doDetails') > 0:
        outVars += ['calClusterBarcodes:  type=VecInt',
                    'calIsoTopo20Barcodes:type=VecInt',
                    'caloExt_eta:         type=Float',
                    'caloExt_phi:         type=Float',
                    'calPt:               type=Float']

        auxVars += ['neflowisol20:                type=Float',
                    'neflowisol30:                type=Float',
                    'ptvarcone20_TightTTVA_pt500: type=Float',
                    'ptvarcone20_TightTTVA_pt1000:type=Float',
                    'ET_Core:                     type=Float',
                    'ET_EMCore:                   type=Float',
                    'ET_HECCore:                  type=Float',
                    'ET_TileCore:                 type=Float',
                    'EnergyLoss:                  type=Float',
                    'EnergyLossSigma:             type=Float',
                    'MeasEnergyLoss:              type=Float',
                    'MeasEnergyLossSigma:         type=Float',
                    'ParamEnergyLoss:             type=Float',
                    'ParamEnergyLossSigmaMinus:   type=Float',
                    'ParamEnergyLossSigmaPlus:    type=Float',
                    ]

    #----------------------------------------------------------------------------------
    # Configure algorithm and tools
    #
    select_muon  = CfgMgr.CP__MuonSelectionTool('muonSelectionTool_MCP', OutputLevel = 5)
    select_muon.MaxEta = 2.5

    calibrate_muon  = CfgMgr.CP__MuonCalibrationAndSmearingTool('muonCalibrationTool_MCP', OutputLevel = 3)
    calibrate_muon.SagittaCorr = True

    ToolSvc += select_muon
    ToolSvc += calibrate_muon

    alg = CfgMgr.Ath__ReadMuon('%s_readMuons' %input_name)
    alg.inputContainerName = input_name
    alg.outputVectorName   = output_name
    alg.printAuxVars       = False
    alg.debug              = False
    alg.OutputLevel        = 3
    alg.outputStream       = 'out'
    alg.configMuonCuts     = ['[Loose] > 0']
    alg.auxVars            = auxVars
    alg.auxVarsCluster     = auxVarsCluster

    alg.doMuonCalibration  = True
    alg.doMuonSelection    = True
    alg.selectMuon         = select_muon
    alg.calibMuon          = calibrate_muon
    alg.isoTools           = getIsoMuonTools(CfgMgr, ToolSvc)

    alg.triggers           = getTriggers('Muon')
    alg.trigMatchTool      = CfgMgr.Trig__MatchingTool('TrigMatchingTool', OutputLevel=3)
    alg.doTrigMatch        = True

    dataVars = auxVars+outVars

    if option.count('doDetails') == 0:
        alg.recoEffCorrTools = getMuonEffCorrRecoTools(CfgMgr)
        alg.trigEffCorrTools = getMuonEffCorrTrigTools(CfgMgr, option)
    else:
        alg.doCaloCluster   = True
        alg.vertexLinkNames = ['RefittedPriVtxLink',
                               'RefittedPriVtxWithoutLeptonLink']

        dataVars += auxVarsCluster
        dataVars += ['RefittedPriVtxLinkBarcode:type=Int',
                     'RefittedPriVtxWithoutLeptonLinkBarcode:type=Int']
        
    #
    # Add output variables for saving
    #
    for itool in alg.isoTools:
        dataVars += ['%s:type=Short' %itool.varName]

    for etool in alg.recoEffCorrTools:
        dataVars += ['%s:type=Float' %etool.varName]

    for trig in alg.triggers:
        dataVars += ['match_%s:type=Short' %trig]

    for ttool in alg.trigEffCorrTools:
        dataVars += ['%s:type=Float' %ttool.varName]
        dataVars += ['%s:type=Float' %ttool.effName]

    return Utils.AlgData(alg, list(set(dataVars)))

#======================================================================================
def getReadTrackJet(CfgMgr, ToolSvc, input_name, output_name, option):    
       
    outVars = ['Pt                 :type=Float',
               'Eta                :type=Float',
               'Phi                :type=Float',
               'NTrack             :type=Short',
               'NTrackBTag         :type=Short',
               'IndexRangeTrack    :type=VecInt',
               'IndexRangeBTagTrack:type=VecInt',
               ]

    auxVars          = []
    auxVarsBTagging  = ['MV2c100_discriminant  :type=Float',
                        'MV2c10_discriminant   :type=Float',
                        'MV2cl100_discriminant :type=Float',
                        'MV2c10mu_discriminant :type=Float',

                        'IP2D_pb:type=Float',
                        'IP2D_pc:type=Float',
                        'IP2D_pu:type=Float',
                        'IP3D_pb:type=Float',
                        'IP3D_pc:type=Float',
                        'IP3D_pu:type=Float',

                        'JetFitter_N2Tpair            :type=Short',
                        'JetFitter_chi2               :type=Float',                                                         
                        'JetFitter_dRFlightDir        :type=Float',                                                         
                        'JetFitter_deltaeta           :type=Float',                                                         
                        'JetFitter_deltaphi           :type=Float',                                                         
                        'JetFitter_energyFraction     :type=Float',                                                         
                        'JetFitter_mass               :type=Float',                                                         
                        'JetFitter_massUncorr         :type=Float',                                                         
                        'JetFitter_nSingleTracks      :type=Short',                                                           
                        'JetFitter_nTracksAtVtx       :type=Short',                                                           
                        'JetFitter_nVTX               :type=Short',                                                           
                        'JetFitter_ndof               :type=Short',                                                           
                        'JetFitter_pb                 :type=Float',                                                        
                        'JetFitter_pc                 :type=Float',                                                        
                        'JetFitter_pu                 :type=Float',                                                        
                        'JetFitter_significance3d     :type=Float', 

                        'DL1_pb   :type=Float',
                        'DL1_pc   :type=Float',
                        'DL1_pu   :type=Float',
                        'DL1mu_pb :type=Float',
                        'DL1mu_pc :type=Float',
                        'DL1mu_pu :type=Float',
                        'DL1rnn_pb:type=Float',
                        'DL1rnn_pc:type=Float',
                        'DL1rnn_pu:type=Float',

                        'rnnip_pb       :type=Float',
                        'rnnip_pc       :type=Float',
                        'rnnip_pu       :type=Float',
                        'rnnip_pbIsValid:type=Short',
                        'rnnip_pcIsValid:type=Short',
                        'rnnip_puIsValid:type=Short',

                        'SMT_ID_qOverP          :type=Float',
                        'SMT_dR                 :type=Float',
                        'SMT_discriminant       :type=Float',
                        'SMT_discriminantIsValid:type=Float',
                        'SMT_mombalsignif       :type=Float',
                        'SMT_mu_d0              :type=Float',
                        'SMT_mu_pt              :type=Float',
                        'SMT_mu_z0              :type=Float',
                        'SMT_pTrel              :type=Float',
                        'SMT_scatneighsignif    :type=Float',

                        'SV1_L3d           :type=Float',
                        'SV1_Lxy           :type=Float',
                        'SV1_N2Tpair       :type=Short',
                        'SV1_NGTinSvx      :type=Short',                        
                        'SV1_deltaR        :type=Float',
                        'SV1_dstToMatLay   :type=Float',
                        'SV1_efracsvx      :type=Float',
                        'SV1_energyTrkInJet:type=Float',
                        'SV1_masssvx       :type=Float',
                        'SV1_normdist      :type=Float',
                        'SV1_pb            :type=Float',
                        'SV1_pc            :type=Float',
                        'SV1_pu            :type=Float',
                        'SV1_significance3d:type=Float',
                        
                        'trkSum_SPt :type=Float',
                        'trkSum_VPt :type=Float',
                        'trkSum_ntrk:type=Short',
                        ]
    
    if option.count('IS_DATA') == 0:
        auxVars += ['PartonTruthLabelID        :type=Short',
                    'ConeTruthLabelID          :type=Short',
                    'HadronConeExclTruthLabelID:type=Short']

    alg = CfgMgr.Ath__ReadTrackJet('%s_readTrackJets' %input_name)
    alg.inputContainerName = input_name
    alg.outputVectorName   = output_name
    alg.checkSimulation    = False
    alg.OutputLevel        = 3
    alg.outputStream       = 'out'
    alg.debug              = False
    alg.printAuxVars       = False
    alg.auxVars            = auxVars
    alg.auxVarsBTagging    = auxVarsBTagging

    return Utils.AlgData(alg, alg.auxVars + alg.auxVarsBTagging + outVars)

#======================================================================================
def getReadIDTrack(CfgMgr, input_name, output_name, option):

    auxVars = ['numberOfPrecisionHoleLayers:                  type=Short',
               'numberOfPrecisionLayers:                      type=Short',
               'expectInnermostPixelLayerHit:                 type=Short',
               'expectNextToInnermostPixelLayerHit:           type=Short',
               'numberOfInnermostPixelLayerHits:              type=Short',
               'numberOfInnermostPixelLayerSharedHits:        type=Short',
               'numberOfNextToInnermostPixelLayerHits:        type=Short',
               'numberOfNextToInnermostPixelLayerSharedHits:  type=Short',
               'numberOfPixelHits:                            type=Short',
               'numberOfPixelSharedHits:                      type=Short',
               'numberOfPixelHoles:                           type=Short',
               'numberOfSCTHits:                              type=Short',
               'numberOfSCTSharedHits:                        type=Short',
               'numberOfSCTHoles:                             type=Short',
               'DFCommonTightPrimary:                         type=Short',
               'numberDoF:                                    type=Float',               
               'qOverP:                                       type=Float',
               'chiSquared:                                   type=Float',
               'd0:                                           type=Float',
               'theta:                                        type=Float',
               'z0:                                           type=Float',
               'radiusOfFirstHit:                             type=Float',
               ]

    outVars = ['Pt:         type=Float',
               'Eta:        type=Float',
               'Phi:        type=Float',
               'Barcode:    type=Int',
               'D0:         type=Float',
               'D0Sig:      type=Float',
               'Z0:         type=Float',
               'Z0Sin:      type=Float',
               'Z0Sig:      type=Float',
               'MatchPriVtx:type=Short',
               ]
    
    if option.count('IS_DATA') == 0:
        outVars += ['truthParticleBarcode:type=Int']

        auxVars += ['truthOrigin:          type=Int',
                    'truthType:            type=Int',
                    'truthMatchProbability:type=Float']

    alg = CfgMgr.Ath__ReadTrack('%s_readIDTrack' %input_name)


    alg.inputContainerName = input_name
    alg.outputVectorName   = output_name
    alg.OutputLevel        = 3
    alg.outputStream       = 'out'
    alg.printAuxVars       = False or option.count('printAuxVars')
    alg.auxVars            = auxVars

    if input_name.count('GSF'):
        alg.originalLinkName = 'originalTrackParticle'
        outVars += ['originalTrackParticleBarcode:type=Short']

    return Utils.AlgData(alg, auxVars+outVars)

#======================================================================================
def getReadCaloCluster(CfgMgr, input_name, output_name, option):

    auxVars = ['AVG_LAR_Q:                                      type=Float',
               'AVG_TILE_Q:                                     type=Float',
               'BADLARQ_FRAC:                                   type=Float',
               'CENTER_LAMBDA:                                  type=Float',
               'CENTER_MAG:                                     type=Float',
               'EM_PROBABILITY:                                 type=Float',
               'ENG_BAD_CELLS:                                  type=Float',
               'ENG_POS:                                        type=Float',
               'ISOLATION:                                      type=Float',
               'N_BAD_CELLS:                                    type=Float',
               'SECOND_LAMBDA:                                  type=Float',
               'SECOND_R:                                       type=Float',
               'time:                                           type=Float',
               'calE:                                           type=Float',
               'calEta:                                         type=Float',
               'calPhi:                                         type=Float',
               'rawE:                                           type=Float',
               'rawEta:                                         type=Float',
               'rawPhi:                                         type=Float',
               'e_sampl:                                        type=VecFloat:nick=cal_e_sampl'
               ]

    outVars = ['Barcode        :type=Int',
               'InBarrel       :type=Short',
               'SamplingPattern:type=UInt',
               'Energy         :type=Float',
               'Pt             :type=Float',
               'Eta            :type=Float',
               'Phi            :type=Float',
               'uncalibEt:      type=Float',
               'uncalibEta:     type=Float',
               'ESampleTileGap3:type=Float',
               ]

    alg = CfgMgr.Ath__ReadCluster('%s_readCluster' %input_name)

    alg.inputContainerName = input_name
    alg.outputVectorName   = output_name
    alg.OutputLevel        = 3
    alg.auxVars            = auxVars
    alg.outputStream       = 'out'
    alg.printAuxVars       = False

    return Utils.AlgData(alg, auxVars+outVars)

#======================================================================================
def getFillOR(CfgMgr, ToolSvc, prefix, input_elec, input_muon, input_jet, option):

    alg = CfgMgr.Ath__FillOR('%s_fillOR' %prefix)
    alg.outputStream         = 'out'
    alg.inputVecElec         = input_elec
    alg.inputVecMuon         = input_muon
    alg.inputVecJet          = input_jet
    alg.varNamePassBJet      = '%s_PassBJet'      %prefix
    alg.varNameIsRemoved     = '%s_IsRemoved'     %prefix
    alg.varNamePassSelection = '%s_PassSelection' %prefix
    alg.debug                = False

    alg.configCutsElec = getPreSelectionCuts_Elec()
    alg.configCutsMuon = getPreSelectionCuts_Muon()
    alg.configCutsJet  = getPreSelectionCuts_Jet ()
    alg.configCutsBJet = getPreSelectionCuts_BJet()
    
    from AssociationUtils.config import recommended_tools

    alg.toolOR = recommended_tools('ORTool',
                                   bJetLabel  = alg.varNamePassBJet,
                                   doEleEleOR = True,
                                   doTaus     = False,
                                   doPhotons  = False )

    return Utils.AlgData(alg)

#======================================================================================
def getReadPhoton(CfgMgr, ToolSvc, input_name, output_name, option):

    #----------------------------------------------------------------------------------
    # Configure output variables
    #
    outVars =  ['Pt                     :type=Float',
                'Eta                     :type=Float',
                'EtaBE2                  :type=Float',
                'Phi                     :type=Float',
                'Energy                  :type=Float',
                'ClEta                   :type=Float',
                'ClPhi                   :type=Float',
                'ClEt                    :type=Float',
                'IsGoodQuality           :type=Short',
                'NConvVtx                :type=Short',
                'momentumAtVertex        :type=Float',
                'conversionType          :type=Short',
                'conversionRadius        :type=Float',
                'conversionVertexBarcodes:type=VecInt',
                ]
    
    auxVars = ['author:                           type=Short',
               'm:                                type=Float',
               'OQ:                               type=UInt',
               'DFCommonPhotonsIsEMLoose:         type=Short', 
               'DFCommonPhotonsIsEMTight:         type=Short',
               'DFCommonPhotonsCleaning:          type=Short',
               'DFCommonPhotonsCleaningNoTime:    type=Float',
               'ptcone20:                         type=Float',
               'topoetcone20:                     type=Float',
               'topoetcone20ptCorrection:         type=Float',
               'topoetcone40:                     type=Float',
               'topoetcone40ptCorrection:         type=Float',
               ]

    if option.count('IS_DATA') == 0:
        auxVars += ['truthOrigin:                       type=Int',
                    'truthType:                         type=Int']

        outVars += ['truthParticleBarcode:              type=Int']        

    #----------------------------------------------------------------------------------
    # Configure algorithm and tools
    #
    alg = CfgMgr.Ath__ReadPhoton('read%s' %input_name)
    alg.inputContainerName  = input_name
    alg.outputVectorName    = output_name
    alg.outputStream        = 'out'
    alg.configPhotonCuts    = ['[Pt] > 1.0e3']
    alg.minPtRaw            = 0.0
    alg.auxVars             = auxVars
    alg.printAuxVars        = False
    alg.debug               = False

    return Utils.AlgData(alg, auxVars+outVars)

#======================================================================================
def getFillMET(CfgMgr, ToolSvc, prefix, input_elec, input_muon, option):

    alg = CfgMgr.Ath__FillMET('%s_fillMET' %prefix)
    alg.debug                = False
    alg.outputStream         = 'out'
    alg.inputVecElec         = input_elec
    alg.inputVecMuon         = input_muon

    alg.inputContMETMap      = 'METAssoc_AntiKt4EMTopo'
    alg.inputContMETCore     = 'MET_Core_AntiKt4EMTopo'
    alg.inputContCalibJets   = 'AntiKt4EMTopoJets_readJets'
    alg.inputContFullMuons   = 'Muons'
    alg.inputContTau         = ''
    alg.inputContPhoton      = ''

    alg.outputContElec       = 'ContainerElec_%s' %prefix
    alg.outputContMuon       = 'ContainerMuon_%s' %prefix
    alg.outputContMET        = 'Container_%s'     %prefix

    alg.varNamePassSelection = '%s_PassSelection' %prefix
    alg.varPrefixMET         = prefix

    alg.configCutsElec       = getPreSelectionCuts_Elec()
    alg.configCutsMuon       = getPreSelectionCuts_Muon()

    alg.rebuildJetMET_softClustKey = 'SoftClus'
    alg.rebuildJetMET_softTrackKey = 'PVSoftTrk'
    alg.doMET_LCTopo               = False
    alg.doMET_EMTopo               = True
    alg.doMET_Track                = True

    alg.toolMETMaker = CfgMgr.met__METMaker          ('METMaker_%s'           %prefix)
    alg.toolMETSyst  = CfgMgr.met__METSystematicsTool('METSystematicsTool_%s' %prefix)

    alg.toolMETMaker.OutputLevel = 3
    alg.toolMETSyst .OutputLevel = 3

    data = Utils.AlgData(alg)
    data.AddEventVars(getMETVars(prefix))

    return data

#======================================================================================
def getCommonLeptonAuxVars(option):

    auxVars = ['PromptLeptonInput_DL1mu:                     type=Float',
               'PromptLeptonInput_DRlj:                      type=Float',                                                         
               'PromptLeptonInput_LepJetPtFrac:              type=Float',
               'PromptLeptonInput_PtFrac:                    type=Float',
               'PromptLeptonInput_PtRel:                     type=Float',                                                        
               'PromptLeptonInput_TrackJetNTrack:            type=Short',
               'PromptLeptonInput_ip2:                       type=Float',
               'PromptLeptonInput_ip3:                       type=Float',                                                         
               'PromptLeptonInput_rnnip:                     type=Float',
               'PromptLeptonInput_sv1_jf_ntrkv:              type=Short',
               'PromptLeptonIso:                             type=Float',
               'PromptLeptonVeto:                            type=Float']

    if option.count('doDetails'):
        auxVars += ['PromptLeptonInput_SecondaryVertexIndexVector:     type=VecInt',
                    'PromptLeptonInput_SecondaryVertexIndexVectorInDet:type=VecInt',
                    'PromptLeptonInput_SecondaryVertexIndexVectorMerge:type=VecInt']

    return auxVars


#======================================================================================
def getCommonLeptonOutVars():

    auxVars = ['MET_PassSelection:                type=Short',
               'ORHFJets_PassSelection:           type=Short',
               'ORHFJets_IsRemoved:               type=Short']

    return auxVars
#======================================================================================
def getTruthPartVars():

    return ['Status          :type=Int',
            'PDG             :type=Int',
            'Barcode         :type=Int',
            'Mass            :type=Float',
            'Energy          :type=Float',
            'Pt              :type=Float',
            'Eta             :type=Float',
            'Phi             :type=Float',
            'IndexRangeParent:type=VecInt',
            'IndexRangeChild :type=VecInt']

#======================================================================================
def getTruthVtxVars():

    return ['Barcode         :type=Int',
            'VtxX            :type=Float',
            'VtxY            :type=Float',
            'VtxZ            :type=Float',
            'IndexRangeParent:type=VecInt',
            'IndexRangeChild :type=VecInt']

#======================================================================================
def getMETVars(prefix):

   met_names = ['FinalTrack', 
                'FinalEMTopo', 
                'RefEle', 
                'Muons', 
                'MuonEloss', 
                'RefJet', 
                'PVSoftTrk']

   met_vars = []

   for met in met_names:
       met_vars += ['%s%s_MET  :type=Float' %(prefix, met)]
       met_vars += ['%s%s_Phi  :type=Float' %(prefix, met)]
       met_vars += ['%s%s_SumEt:type=Float' %(prefix, met)]

   return met_vars

#======================================================================================
def getPreSelectionCuts_Elec():
    
    cuts = ['[IsGoodQuality] > 0',
            '[Pt] > 10.0e3',
            'fabs([ClEta]) < 2.47',
            '[DFCommonElectronsLHLoose] > 0',
            'fabs([Z0Sin]) < 0.5',
            'fabs([D0Sig]) < 5.0']
    
    return cuts
   
#======================================================================================
def getPreSelectionCuts_Muon():
    
    cuts = ['[Pt] > 10.0e3',
            'fabs([Eta]) < 2.7',
            '[Loose] > 0',
            '[PassedID] > 0 && [MuonType] != 1',
            'fabs([Z0Sin]) < 0.5',
            #'fabs([D0Sig]) < 3.0']
            'fabs([D0Sig]) < 15.0']

    return cuts

#======================================================================================
def getPreSelectionCuts_Jet():
    
    cuts = ['[Pt] > 20.0e3', 
            'fabs([Eta]) < 4.5',
            '[FJVTPass] > 0',
            '[JVTPass] > 0']

    return cuts

#======================================================================================
def getPreSelectionCuts_BJet():
    
    cuts = ['[MV2c10_discriminant] > 0.11 && [Pt] > 20.0e3']

    return cuts

#======================================================================================
def getYearCuts(option, year=2015):

    cuts = []

    if option.count('IS_DATA'):
        if year == 2015:
            cuts = ['[Run] > 276261 && [Run] < 284485']
        elif year == 2016:
            cuts = ['[Run] > 297729 && [Run] < 311482']
        elif year == 2017:
            cuts = ['[Run] > 325712 && [Run] < 340454']
        elif year == 2018:
            cuts = ['[Run] > 348884 && [Run] < 364293']
        else:
            raise Exception('getYearCuts - unknown year: %s' %year)
    else:
        if year == 2015:
            cuts = ['[RandomRunNumber] > 276261 && [RandomRunNumber] < 284485']
        elif year == 2016:
            cuts = ['[RandomRunNumber] > 297729 && [RandomRunNumber] < 311482']
        elif year == 2017:
            cuts = ['[RandomRunNumber] > 325712 && [RandomRunNumber] < 340454']
        elif year == 2018:
            cuts = ['[RandomRunNumber] > 348884 && [RandomRunNumber] < 364293']
        else:
            raise Exception('getYearCuts - unknown year: %s' %year)

    return cuts
