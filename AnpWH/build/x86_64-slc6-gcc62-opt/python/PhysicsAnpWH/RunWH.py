import os

import PhysicsAnpBase.PhysicsAnpBaseConfig  as physicsBase
import PhysicsAnpWH  .Config                as config
import PhysicsAnpWH  .Common                as common

from   PhysicsAnpBase.PhysicsAnpBaseConfig   import CutItem
from   PhysicsAnpBase.PhysicsAnpBaseConfig   import getAlgName

clog = physicsBase.getLog(os.path.basename(__file__))

#============================================================================================
# Top level C++ module to read ntuples and configure and run algs
#============================================================================================
def prepareReadModule(ROOT, options, files, top_algs):

    run = config.prepareReadNtuple(ROOT, options, files, hist_config=['../source/PhysicsAnpWH/config/wh'])

    if options.trees != None:
        run.SetKey('TreeName', options.trees)
    else:
        run.SetKey('TreeName', 'nominal')
        
    evt_vars = []  
    var_vetos = []

    for f in files:
        run.StoreInputFile(f)

    if options.print_vars:
        ROOT.Anp.Var.PrintAllVars()   

    run.AddTopAlg('topAlg', top_algs)

    run.SetKey('PrefixJet',       'm_jet_')
    run.SetKey('PrefixElec',      'm_elec_')
    run.SetKey('PrefixMuon',      'm_muon_')  
    run.SetKey('PrefixTruthPart', 'm_mc_part_')
    run.SetKey('PrefixTruthVtx',  'm_mc_vtx_')
    run.SetKey('Lists',           'm_jet_, m_elec_, m_muon_, m_mc_part_, m_mc_vtx_')

    run.SetKey('VarNicks',    ','.join(evt_vars))
    run.SetKey('Vetos',       ','.join(var_vetos))
    
    run.SetKey('Print',          'yes')
    run.SetKey('NPrint',         1000)
    run.SetKey('Debug',          options.debug_run or options.debug)
    run.SetKey('FillTrueEvent',  'no')
    run.SetKey('FillTrueParts',  'yes')        

    return run

#============================================================================================
# Job configuration
#============================================================================================
def prepareJobConfig(ROOT, options, files):

    clog.info('Prepare python configuration...')
    
    proc_algs = [getPrepReco('prepReco', options)]
    
    prep_algs = []
    post_algs = []
    plot_algs = []
    
    #-------------------------------------------------------------------------
    # Configure candidates and corresponding plotting algs
    #
    prep_cand    = getPrepCand   ('prepCand',    options)
    prep_truthwh = getPrepTruthWH('prepTruthWH', options)
    prep_wh      = getPrepWH     ('prepWH',      options, prep_cand)
    prep_sf      = getPrepSF     ('prepSF',      options, prep_cand)

    prep_algs += [prep_cand]

    prep_algs += [prep_truthwh]

    prep_algs += [prep_wh]
    prep_algs += [prep_sf]

    plot_algs += [getPlotCand('%s_%s'%("cand", "total"),       prep_cand, options)]
    plot_algs += [getPlotCand('%s_%s'%("cand", "total_OR"),    prep_cand, options)]
    plot_algs += [getPlotCand('%s_%s'%("cand", "total_ORrev"), prep_cand, options)]

    if options.do_prompt_sr:
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SR_Zdominated"),             prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SR_Zdepleted"),              prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_Zdominated_ZplusFake"),   prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_Zdominated_ZplusmFake"),  prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_Zdominated_ZpluseFake"),  prep_cand, options)]

    if options.do_prompt_cr:
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_WZ"),                     prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_ZJet"),                   prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_ZgamJet"),                prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_Zgamma"),                 prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_ZZ"),                     prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_top_Zdom"),               prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_top_Zdep"),               prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_ttbar_os_df_lowbjetpT"),  prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_ttbar_os_df_highbjetpT"), prep_cand, options)]

    if options.do_fake_cr:
        if not options.do_prompt_sr:
            plot_algs += [getPlotCand('%s_%s'     %("cand", "SR_Zdominated"),             prep_cand, options)]
            plot_algs += [getPlotCand('%s_%s'     %("cand", "SR_Zdepleted"),              prep_cand, options)]
        
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_Zdominated_ZplusmFake"),           prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CR_Zdominated_ZpluseFake"),           prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_ZplusmFake"),        prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_ZplusmFake"),        prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_ZplusmmmFake"),      prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_ZplusmmmFake"),      prep_cand, options)]

        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_ZpluseemFake"),      prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_ZpluseemFake"),      prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_Zplus_MET_eemFake"), prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_Zplus_MET_eemFake"), prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_Zplus_ZMass_eemFake"),      prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_Zplus_ZMass_eemFake"),      prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_Zplus_ZMass_MET_eemFake"), prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_Zplus_ZMass_MET_eemFake"), prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_ZpluseFake"),        prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_ZpluseFake"),        prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_Zplus_MET_eFake"),   prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_Zplus_MET_eFake"),   prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_Zplus_ZMass_eFake"),        prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_Zplus_ZMass_eFake"),        prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "SRPri_Zdominated_Zplus_ZMass_MET_eFake"),   prep_cand, options)]
        plot_algs += [getPlotCand('%s_%s'     %("cand", "CRPri_Zdominated_Zplus_ZMass_MET_eFake"),   prep_cand, options)]

    if options.do_scan_sr:
        iso_wps = ['isoFCLoose',            'isoFCTight',
                   'isoFixedCutPflowLoose', 'isoFixedCutPflowTight',
                   'isoFCLoose_FixedRad',   'isoFCTight_FixedRad',
                   'isoFixedCutLoose',      'isoFixedCutTight',
                   'isoFixedCutTightTrackOnly', 
                   'isoFCTightTrackOnly_FixedRad',
                   'PromptLeptonVeto']

        for iso in iso_wps:
            prep_scan = getPrepCand('prepCand_%s' %iso, options)
            prep_algs += [prep_scan]
            
            prep_algs += [getPrepWH('prepWH_%s' %iso, options, prep_scan)]
            plot_algs += [getPlotCand('%s_%s_%s' %('cand', 'SR_Zdominated', iso), prep_scan, options)]
            plot_algs += [getPlotCand('%s_%s_%s' %('cand', 'SR_Zdepleted',  iso), prep_scan, options)]

    if options.do_2l_cr:
        for flavour in ['ee', 'mm']:
            plot_algs += [getPlotCand('cand_CR_Z_os_%s'        %(flavour), prep_cand, options)]
            plot_algs += [getPlotCand('cand_CR_Z_osnobveto_%s' %(flavour), prep_cand, options)]

        for flavour in ['ee', 'em', 'me', 'df', 'mm']:
            plot_algs += [getPlotCand('cand_CR_ttbar_os_%s'%(flavour), prep_cand, options)]
            plot_algs += [getPlotCand('cand_CR_ttbar_ss_%s'%(flavour), prep_cand, options)]

    #-------------------------------------------------------------------------
    # Configure top level algorithms
    #
    top_algs  = proc_algs + prep_algs
    top_algs += [common.getRunNexus('runNexus', options, plot_algs)]
    top_algs += post_algs

    common.addPrintEvent('printEvent', options, top_algs)

    #-------------------------------------------------------------------------
    # Prepare and configure top level C++ module
    #
    run = prepareReadModule(ROOT, options, files, top_algs)   

    clog.info('Finished python configuration: process up to %d event(s)' %options.nevent)

    return run

#============================================================================================
def getPrepReco(name, options):

    alg = physicsBase.AlgConfig(name, 'PrepReco')

    alg.SetKey('Debug',         options.debug)
    alg.SetKey('DebugVars',     'no')
    alg.SetKey('Print',         'no')
    alg.SetKey('AddLeptonMass', 'yes')
    
    return alg

#============================================================================================
def getPrepCand(name, options):

    prep_cuts  = []
    event_cuts = []

    loose_elec_cuts  = getLooseElecCuts()
    loose_muon_cuts  = getLooseMuonCuts() 
    loose_rjet_cuts  = getLooseJetCuts ()
    rjet_cuts        = getJetCuts ()

    if options.mc_channel:
        event_cuts += [CutItem('CutMC', 'MCChannel == %d' %options.mc_channel)]

    if options.btag_wp == None:
        WP = '85'
    else:
        WP = options.btag_wp

    bjet_cuts = getJetBTagCuts(WP)
    ljet_cuts = getJetBTagCuts(WP, reverse=True)

    alg = physicsBase.AlgConfig(name, 'PrepCand')

    alg.SetKey('Debug',                 options.debug)
    alg.SetKey('DebugVars',             'no')
    alg.SetKey('Print',                 'no')
    alg.SetKey('CandName',              name)
    alg.SetKey('AddWeight',             'yes')
    alg.SetKey('AddPosMass',            'yes')    
    alg.SetKey('CopyVarsAll',           'yes')
    alg.SetKey('CountObj',              'yes')
    alg.SetKey('KeyHist',               'PrepCand')
    alg.SetKey('DoLight',               'no')
    alg.SetKey('SaveHist',              'yes')
    alg.SetKey('IgnoreTrivialCutFlows', 'yes')

    physicsBase.addCuts(alg, 'CutEvent',   event_cuts,       save=options.print_cuts)
    physicsBase.addCuts(alg, 'CutPrep',    prep_cuts,        save=options.print_cuts)
    physicsBase.addCuts(alg, 'CutElec',    loose_elec_cuts,  save=options.print_cuts)
    physicsBase.addCuts(alg, 'CutMuon',    loose_muon_cuts,  save=options.print_cuts)
    physicsBase.addCuts(alg, 'CutJet',     rjet_cuts,        save=options.print_cuts)
    physicsBase.addCuts(alg, 'CutJetBTag', bjet_cuts,        save=options.print_cuts)
    physicsBase.addCuts(alg, 'CutJetLTag', ljet_cuts,        save=options.print_cuts)

    return alg

#============================================================================================
def getPrepTruthWH(name, options):

    alg = physicsBase.AlgConfig(name, 'PrepTruthWH')
    alg.SetKey('Print',           'no')
    alg.SetKey('DoSherpa',        options.doSherpa)
    alg.SetKey('Debug',           options.debug)

    return alg

#============================================================================================
def getPrepSF(name, options, cand):

    alg = physicsBase.AlgConfig(name, 'PrepSF')
    
    alg.SetKey('DirName',   name)
    alg.SetKey('KeyHist',   'PrepSF')
    alg.SetKey('CandName',  getAlgName(cand))
    alg.SetKey('Print',     'no')
    alg.SetKey('Debug',     options.debug)    

    alg.SetKey('MuonSFNameTTVA',        'LepCorrSF_TTVA')
    alg.SetKey('MuonSFNamePIDLowPt',    'LepCorrSF_Medium')
    alg.SetKey('MuonSFNamePIDHighPt',   'LepCorrSF_Medium')
    alg.SetKey('MuonSFNameIso',         'LepCorrSF_isoFCTight')
    alg.SetKey('MuonTrigSFNameLowPt',   'LepCorrSF_Trig1L_Medium')
    alg.SetKey('MuonTrigSFNameHighPt',  'LepCorrSF_Trig1L_Medium')
    alg.SetKey('MuonTrigEffNameLowPt',  'LepCorrEff_Trig1L_Medium')
    alg.SetKey('MuonTrigEffNameHighPt', 'LepCorrEff_Trig1L_Medium')

    alg.SetKey('ElecSFNameReco',        'LepCorrSF_Reconstruction')
    alg.SetKey('ElecSFNameIsoLowPt',    'LepCorrSF_Tight_isoFCTight')
    alg.SetKey('ElecSFNameIsoHighPt',   'LepCorrSF_Medium_isoFCTight')
    alg.SetKey('ElecSFNamePIDLowPt',    'LepCorrSF_Tight')
    alg.SetKey('ElecSFNamePIDHighPt',   'LepCorrSF_Medium')
    alg.SetKey('ElecSFNameAntiPID',     'LepCorrSF_LooseBLayer')

    alg.SetKey('ElecTrigSFNameLowPt',     'LepCorrSF_Trig1L_Tight_isoFCTight')
    alg.SetKey('ElecTrigSFNameHighPt',    'LepCorrSF_Trig1L_Medium_isoFCTight')
    alg.SetKey('ElecTrigEffNameLowPt',    'LepCorrEff_Trig1L_Tight_isoFCTight')
    alg.SetKey('ElecTrigEffNameHighPt',   'LepCorrEff_Trig1L_Medium_isoFCTight')
    alg.SetKey('ElecTrigSFNameD4LowPt',   'LepCorrSF_Trig1L_Tight_isoFCTight')
    alg.SetKey('ElecTrigSFNameD4HighPt',  'LepCorrSF_Trig1L_Medium_isoFCTight')
    alg.SetKey('ElecTrigEffNameD4LowPt',  'LepCorrEff_Trig1L_Tight_isoFCTight')
    alg.SetKey('ElecTrigEffNameD4HighPt', 'LepCorrEff_Trig1L_Medium_isoFCTight')
    alg.SetKey('ElecTrigSFNameAntiID',    'LepCorrSF_Trig1L_LooseBLayer')
    alg.SetKey('ElecTrigEffNameAntiID',   'LepCorrEff_Trig1L_LooseBLayer')

    alg.SetKey('BtagSFName',      'MV2c10_85_SF')
    alg.SetKey('TrigReq',         'SingleLepOnly')

    cuts = [CutItem('CutPt',      'Pt > 25.0e3')]
    physicsBase.addCuts(alg, 'CutElecPt', cuts)
    physicsBase.addCuts(alg, 'CutMuonPt', cuts)

    physicsBase.addCuts(alg, 'CutMuonID', getMuonCuts(name))
    physicsBase.addCuts(alg, 'CutElecID', getElecCuts(name))

    event_cuts = []
    physicsBase.addCuts(alg, 'CutEvent', event_cuts)

    return alg

#============================================================================================
def getPrepWH(name, options, cand):

    alg = physicsBase.AlgConfig(name, 'PrepWH')
    
    alg.SetKey('DirName',         name)
    alg.SetKey('KeyHist',         'PrepWH')
    alg.SetKey('CandName',        getAlgName(cand))
    alg.SetKey('Print',           'no')
    alg.SetKey('Debug',           options.debug)

    physicsBase.addCuts(alg, 'CutTrigEvent',       getTriggerEventCuts(options))
    physicsBase.addCuts(alg, 'CutIDElecTight',     getTightElecCuts(options, name, False))
    physicsBase.addCuts(alg, 'CutAntiIDElecTight', getTightElecCuts(options, name, True))
    physicsBase.addCuts(alg, 'CutIDMuonTight',     getTightMuonCuts(options, name, False))
    physicsBase.addCuts(alg, 'CutAntiIDMuonTight', getTightMuonCuts(options, name, True))
    physicsBase.addCuts(alg, 'CutTrigElec',        getTriggerMatchElecCuts(options))
    physicsBase.addCuts(alg, 'CutTrigMuon',        getTriggerMatchMuonCuts(options))

    return alg

#============================================================================================
def getPlotCand(name, cand, options, do_print=False):
    
    plot_cand = physicsBase.AlgConfig('plotCand',  'PlotCand')
    plot_cand.SetKey('DirName',   '')
    plot_cand.SetKey('Plot2d',    'yes')
    plot_cand.SetKey('PlotBCID',  'yes')
    plot_cand.SetKey('PrintVars', 'no')

    if   name.count('_Zgamma'): plot_cand.SetKey('KeyHist',   'PlotCandWHZgam')
    elif name.count('_Z'):      plot_cand.SetKey('KeyHist',   'PlotCandWHZ')
    elif name.count('_WZ'):     plot_cand.SetKey('KeyHist',   'PlotCandWHWZ')
    elif name.count('_ttbar'):  plot_cand.SetKey('KeyHist',   'PlotCandWHttbar')
    elif name.count('total'):   plot_cand.SetKey('KeyHist',   'PlotCandWHTotal')
    else:                       plot_cand.SetKey('KeyHist',   'PlotCandWH')

    if options.do_scan_sr and name.count('_iso'):
        plot_cand.SetKey('KeyHist', 'PlotCandWHScanSR')        

    plot_lep  = physicsBase.AlgConfig('plotLep',   'PlotLep')
    plot_lep.SetKey('Debug',     options.debug)
    plot_lep.SetKey('Print',     'no')
    plot_lep.SetKey('PlotCand',  'yes')
    plot_lep.SetKey('CountLep',  'yes')
    plot_lep.SetKey('UseTopDir', 'yes')
    plot_lep.SetKey('UseWeight', 'yes')
    plot_lep.SetKey('DirName',   '')

    if name.count('_Z'): plot_lep.SetKey('KeyHist',   'PlotLepWHZ')
    else:                plot_lep.SetKey('KeyHist',   'PlotLepWH')

    if options.do_scan_sr:
        algs = [plot_cand]
    else:
        algs = [plot_cand, plot_lep]

    cuts = getNewEventCuts(name, options)

    chain = config.getRunChain(name, algs=algs, cuts=cuts, options=options)
    chain.SetKey('DirName',         name)
    chain.SetKey('Debug',           options.debug)
    chain.SetKey('Print',           do_print)
    chain.SetKey('NoWeight',        options.no_weight)
    chain.SetKey('PrintConfig',     'no')
    chain.SetKey('DoTimer',         options.do_timer)
    chain.SetKey('CandName',        physicsBase.getAlgName(cand))

    data_weights = []
    siml_weights = ['MCWeight',
                    'PUWeight',
                    'MuonPidSF',
                    'ElecRecSF',
                    #'MuonIsoSF',
                    'MuonTTVASF',
                    'ElecPidSF',
                    #'ElecIsoSF',
                    'JVTWeight',
                    'FJVTWeight',
                    'LepTriggerSF',
                    'bJetReconstructionSF',
                   ]

    if name.count('total'):
        siml_weights = ['MCWeight',
                        'PUWeight',]

    if options.do_scan_sr and name.count('_iso'):
        siml_weights = ['MCWeight',
                        'PUWeight',
                        'MuonPidSF',
                        'ElecRecSF',
                        'MuonTTVASF',
                        'ElecPidSF',
                        'JVTWeight',
                        'FJVTWeight',
                        'bJetReconstructionSF',]

    chain.SetKey('CandWeightsSiml', ','.join(siml_weights))
    chain.SetKey('CandWeightsData', ','.join(data_weights))

    return chain

#============================================================================================
# Event cuts
#============================================================================================
def getNewEventCuts(name, options):

  cuts  = []

  cuts += [CutItem('CutGRL', '[IsMC] == 1 || [IsGRL] > 0')]

  if options.ZjetsOR and not name.count('total'):
      cuts += [CutItem('CutZjetsGammaOR',  '[IsOverlap] != 1')]
  elif options.ZjetsORreverse and not name.count('total'):
      cuts += [CutItem('CutZjetsGammaOR',  '[IsOverlap] == 1')]
  elif not name.count('total'):
      cuts += [CutItem('CutZjetsGammaOR',  '[IsMC] == 1 || [IsGRL] > 0')]

  cuts += [CutItem('CutEventQuality',  '([IsMC] == 1) || ([ErrorState_LAr] < 1 && [ErrorState_Tile] < 1 && [ErrorState_SCT] < 1 && [IsEventFlagBitSet] < 1)')]
  cuts += [CutItem('CutJetCleaning',   '[DFCommonJets_eventClean_LooseBad] > 0')]
  cuts += [CutItem('CutPriVtx',        '[HasPriVtx] > 0')]
  cuts += [CutItem('CutTrigSelection', '[eventTriggerPass] > 0')]
  cuts += [CutItem('CutTrigEvent',     '[TrigEventPass] > 0')]
  cuts += [CutItem('CutTrigMatch',     '[MatchTrigNLep] > 0')]
 
  if name.count('total_ORrev'): 
      cuts += [CutItem('CutZjetsGammaOR',  '[IsOverlap] == 1')]
      return cuts
  if name.count('total_OR'): 
      cuts += [CutItem('CutZjetsGammaOR',  '[IsOverlap] != 1')]
      return cuts
  if name.count('total'): 
      return cuts

  if name.count('CR_Z_os') or name.count('CR_ttbar'): 
      cuts += [CutItem('CutLep0ID',        '[Lep0id] == 1')]
      cuts += [CutItem('CutLep1ID',        '[Lep1id] == 1')]
      cuts += getFlavourCuts(name)
      cuts += getRegionCuts(name)
      return cuts
  if name.count('CR_Zdominated_Zplus') or name.count('CRPri_Zdominated_Zplus'):
      cuts += [CutItem('CutNLepton',       '[NLepton] == 3')]
      cuts += [CutItem('CutLepCharge',     'abs([LeptonChargeSum]) == 1')]
      cuts += [CutItem('CutLepPt',         '[Lep0Pt] > 15.0e3 && [Lep1Pt] > 15.0e3 && [Lep2Pt] > 15.0e3')]
      cuts += [CutItem('CutLep0ID',        '[Lep0ID] == 1')]
      cuts += getFlavourCuts(name)
      cuts += getRegionCuts(name)
      return cuts

  cuts += [CutItem('CutNLepton',       '[NLepton] == 3')]
  cuts += [CutItem('CutLepCharge',     'abs([LeptonChargeSum]) == 1')]
  cuts += [CutItem('CutLepPt',         '[Lep0Pt] > 15.0e3 && [Lep1Pt] > 15.0e3 && [Lep2Pt] > 15.0e3')]
  cuts += [CutItem('CutLep0ID',        '[Lep0ID] == 1')]
  cuts += [CutItem('CutLep1ID',        '[Lep1ID] == 1')]
  cuts += [CutItem('CutLep2ID',        '[Lep2ID] == 1')]
  cuts += getFlavourCuts(name)
  cuts += getRegionCuts(name)

  return cuts

#============================================================================================
def getRegionCuts(name):
  '''
     define signal region or control region criteria 
  '''

  cuts = []

  # two lepton charge cuts
  if name.count('_os'):
      cuts += [CutItem('CutNLepton',   '[NLepton] == 2')]
      cuts += [CutItem('CutLepCharge', '[DiLeptonChargeSum] == 0', abs=True)]
  elif name.count('_ss'):
      cuts += [CutItem('CutNLepton',   '[NLepton] == 2')]
      cuts += [CutItem('CutLepCharge', '[DiLeptonChargeSum] == 2', abs=True)]

  # CR
  if name.count('CR_Z_os_'):
      cuts += [CutItem('CutMll',   'fabs([Mll] - 91.2e3) < 10.0e3')]
      cuts += [CutItem('CutNBJet', '[NJetBTag] == 0')]
  if name.count('CR_Z_osnobveto'):
      cuts += [CutItem('CutMll',   'fabs([Mll] - 91.2e3) < 10.0e3')]

  elif name.count('CR_ttbar_'):
      cuts += [CutItem('CutNBJet', '[NJetBTag] >= 1')]
      if name.count('_ee') or name.count('_mm'):
          cuts += [CutItem('CutMll',   'fabs([Mll] - 91.2e3) > 10.0e3')]
      if name.count('_lowbjetpT'):
          cuts += [CutItem('CutbjetpT',  '[bjet0Pt] < 250e3')]
      if name.count('_highbjetpT'):
          cuts += [CutItem('CutbjetpT',  '[bjet0Pt] > 250e3')]

  if name.count('_WZ'):
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.2e3) < 25.0e3')]    # Z-veto cut inverted
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 30.0e3')]        # MET > 50 GeV

  if name.count('_ZJet'):
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1')] # exact 1 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.2e3) < 25.0e3')]    # Z-veto cut inverted
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET > 50 GeV

  if name.count('_ZgamJet'):
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1')] # exact 1 SFOS pair
      cuts += [CutItem('CutEventTopo',  '[NMuonTight] == 2 && [NElecTight] == 1')]   #3 ID lepton
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.2e3) < 25.0e3')]    # Z-veto cut inverted
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET > 50 GeV

  if name.count('_Zgamma'):
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1')] # exact 1 SFOS pair
      cuts += [CutItem('CutEventTopo',  '[NMuonTight] == 2 && [NElecTight] == 1')]   #3 ID lepton
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllSFOS',    '[Mlll] > 75.0e3 && [Mlll] < 100.0e3')]    # Z-veto cut inverted
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET > 50 GeV

  if name.count('_ZZ'):
      cuts += [CutItem('CutNMuon',      '[NMuonTight] == 3')] # to correct
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMlll',       'fabs([Mlll] - 91.2e3) < 15.0e3')]
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET > 50 GeV

  if name.count('_top_Zdom'):
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] > 0')]
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 1')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.2e3) > 25.0e3')]      # Z-veto
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 50.0e3')]        # MET > 50 GeV

  if name.count('_top_Zdep'):
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 0')] 
      cuts += [CutItem('CutNJet',       '[NJet] > 0')]
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 1')] 

  # SR
  if name.count('SR_Zdominated'):
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.2e3) > 25.0e3')]      # Z-veto
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 30.0e3')]        # MET > 30 GeV
      # BDT cuts ?

  if name.count('SR_Zdepleted'):
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 0')] # to add 0 SFOS pair
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]        # top veto
      # BDT cuts ?

  # for Z plus fake
  if name.count('CR_Zdominated_ZplusFake'):
      cuts += [CutItem('CutEventTopo',  '([Lep1ID] == 1 && [Lep2AntiID] == 1) || ([Lep2ID] == 1 && [Lep1AntiID] == 1)')]   # 2 ID lepton plus 1 Anti-ID muon
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.2e3) > 25.0e3')]      # Z-veto
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 30.0e3')]        # MET > 30 GeV

  if name.count('CR_Zdominated_ZplusmFake'):
      #cuts += [CutItem('CutEventTopo',  '([Lep1ID] == 1 && [Lep2AntiID] == 1) || ([Lep2ID] == 1 && [Lep1AntiID] == 1)')]   # 2 ID lepton plus 1 Anti-ID muon
      cuts += [CutItem('CutMuonFake',   '[IsFakeMuon] > 0')] 
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.2e3) > 25.0e3')]      # Z-veto
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 30.0e3')]        # MET > 30 GeV

  if name.count('CR_Zdominated_ZpluseFake'):
      #cuts += [CutItem('CutEventTopo',  '([Lep1ID] == 1 && [Lep2AntiID] == 1) || ([Lep2ID] == 1 && [Lep1AntiID] == 1)')]   # 2 ID lepton plus 1 Anti-ID muon
      cuts += [CutItem('CutElecFake',   '[IsFakeElec] > 0')] 
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.2e3) > 25.0e3')]      # Z-veto
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 30.0e3')]        # MET > 30 GeV

  if name.count('SRPri_Zdominated_ZplusmFake'):
      cuts += [CutItem('CutEventTopo',  '([NElecTight] == 2 && [NMuonTight] == 1) || [NMuonTight] == 3')]   # 3 ID lepton
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.0e3) < 15.0e3')]  # Z-window within 15GeV
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET < 30 GeV

  if name.count('CRPri_Zdominated_ZplusmFake'):
      #cuts += [CutItem('CutEventTopo',  '[eeAntiIDm] == 1 || [mmAntiIDm] == 1')]   # 2 ID lepton plus 1 Anti-ID muon
      cuts += [CutItem('CutEventTopo',  'eeAntiIDm == 1 || mmAntiIDm == 1')]   # 2 ID lepton plus 1 Anti-ID muon
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.0e3) < 15.0e3')]  # Z-window within 15GeV
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET < 30 GeV

  if name.count('SRPri_Zdominated_ZplusmmmFake'):
      cuts += [CutItem('CutEventTopo',  '[NMuonTight] == 3')]   # 3 ID muon
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.0e3) < 15.0e3')]  # Z-window within 15GeV
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET < 30 GeV

  if name.count('CRPri_Zdominated_ZplusmmmFake'):
      cuts += [CutItem('CutEventTopo',  '[mmAntiIDm] == 1')]   # 2 ID muon plus 1 Anti-ID muon
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.0e3) < 15.0e3')]  # Z-window within 15GeV
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET < 30 GeV

  if name.count('SRPri_Zdominated_Zplus') and name.count('eemFake'):
      cuts += [CutItem('CutEventTopo',  '[NElecTight] == 2 && [NMuonTight] == 1')]   # 2 ID electron plus 1 ID muon
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      if name.count('ZMass'):
          cuts += [CutItem('CutMllSFOS',    '[MllSFOS] > 40.0e3 && [MllSFOS] < 100.0e3')]  # to check Z mass region 
      else:
          cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.0e3) < 15.0e3')]  # Z-window within 15GeV
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      if name.count('MET'):
          cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 30.0e3')]
      else:
          cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET < 30 GeV

  if name.count('CRPri_Zdominated_Zplus') and name.count('eemFake'):
      cuts += [CutItem('CutEventTopo',  '[eeAntiIDm] == 1')]   # 2 ID electron plus 1 Anti-ID muon
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      if name.count('ZMass'):
          cuts += [CutItem('CutMllSFOS',    '[MllSFOS] > 40.0e3 && [MllSFOS] < 100.0e3')]  # to check Z mass region 
      else:
          cuts += [CutItem('CutMllSFOS',    'fabs([MllSFOS] - 91.0e3) < 15.0e3')]  # Z-window within 15GeV
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      if name.count('MET'):
          cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 30.0e3')]
      else:
          cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET < 30 GeV

  if name.count('SRPri_Zdominated_Zplus') and name.count('eFake'):
      cuts += [CutItem('CutEventTopo',  '[NMuonTight] == 2 && [NElecTight] == 1')]   #3 ID lepton
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      if name.count('ZMass'):
          cuts += [CutItem('CutMllSFOS',    '[MllSFOS] > 40.0e3 && [MllSFOS] < 100.0e3')]  # to check Z mass region 
      else:
          cuts += [CutItem('CutMllSFOS',    '[MllSFOS] > 40.0e3 && [MllSFOS] < 85.0e3')]  # shift due to losing the FSR gamma
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      if name.count('MET'):
          cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 30.0e3')]
      else:
          cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET < 30 GeV

  if name.count('CRPri_Zdominated_Zplus') and name.count('eFake'):
      cuts += [CutItem('CutEventTopo',  '[mmAntiIDe] == 1')]   # 2 ID lepton plus 1 Anti-ID electron
      cuts += [CutItem('CutNSFOSPairs', '[NSFOSPairs] == 1 || [NSFOSPairs] == 2')] # 1 or 2 SFOS pair
      cuts += [CutItem('CutNJet',       '[NJet] < 2')]
      if name.count('ZMass'):
          cuts += [CutItem('CutMllSFOS',    '[MllSFOS] > 40.0e3 && [MllSFOS] < 100.0e3')]  # to check Z mass region 
      else:
          cuts += [CutItem('CutMllSFOS',    '[MllSFOS] > 40.0e3 && [MllSFOS] < 85.0e3')]  # shift due to losing the FSR gamma
      cuts += [CutItem('CutNBJet',      '[NJetBTag] == 0')]                      # top veto
      cuts += [CutItem('CutMllOSMin',   '[MllOSMin] > 12.0e3')]                  # minimum OS inv mass > 12GeV
      if name.count('MET'):
          cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] > 30.0e3')]
      else:
          cuts += [CutItem('CutMET',        '[METFinalEMTopo_MET] < 30.0e3')]        # MET < 30 GeV

  return cuts

#============================================================================================
def getFlavourCuts(name):

    cuts = []

    if name.count('_ee'):
        cuts += [CutItem('CutNElec', 'NElecTight == 2')]

    if name.count('_mm'):
        cuts += [CutItem('CutNMuon', 'NMuonTight == 2')]

    if name.count('_em'):
        cuts += [CutItem('CutLep0Flav', 'abs([Lep0PDG]) == 11')]
        cuts += [CutItem('CutLep1Flav', 'abs([Lep1PDG]) == 13')]

    if name.count('_me'):
        cuts += [CutItem('CutLep0Flav', 'abs([Lep0PDG]) == 13')]
        cuts += [CutItem('CutLep1Flav', 'abs([Lep1PDG]) == 11')]

    if name.count('_df'):
        cuts += [CutItem('CutDiffFlav', '(abs([Lep0PDG]) == 11 && abs([Lep1PDG]) == 13) || (abs([Lep0PDG]) == 13 && abs([Lep1PDG]) == 11)')]

    if name.count('_ep'):
        cuts += [CutItem('CutNElec', 'NElecTight == 1')]

    if name.count('_mp'):
        cuts += [CutItem('CutNMuon', 'NMuonTight == 1')]

    if not name.count ('_tight_')==0:
        cuts += [CutItem('CutNLepTight', 'NLeptonTight2l == 2')]

    return cuts

#============================================================================================
# Object cuts
#============================================================================================
def getElecCuts(key):

    cuts  = []
    cuts += [CutItem('CutAuthor',   '[author] == 1')]
    cuts += [CutItem('CutPt',       '[Pt] > 15.0e3')]
    cuts += [CutItem('CutPIDHighPt','[DFCommonElectronsLHMedium] == 1')]
    cuts += [CutItem('CutPIDLowPt', '[Pt] > 25.0e3 || [DFCommonElectronsLHTight] == 1')]
    cuts += [CutItem('CutOR',       '[ORHFJets_IsRemoved] == 0')]
    cuts += [CutItem('CutZ0Sin',    'fabs([Z0Sin]) < 0.5')]
    cuts += [CutItem('CutD0Sig',    'fabs([D0Sig]) < 5.0')]

    if key.count('PromptLeptonVeto'):
        cuts += [CutItem('CutIsoID',     '[ambiguityType] == 0')]
        cuts += [CutItem('CutIsoQMisID', '[DFCommonElectronsECIDSResult] > 0.7')]
        cuts += [CutItem('CutIsoIso',    '[isoFixedCutLoose] == 1')]
        cuts += [CutItem('CutIsoPlv',    '[PromptLeptonVeto] < -0.7')]
    elif key.count('_iso'):
        iso_wp = key.partition('_iso')[2]
        cuts += [CutItem('CutIso', '[iso%s] == 1' %iso_wp)]
    else:
        #cuts += [CutItem('CutIso', '[isoFCTight] == 1')]
        cuts += [CutItem('CutIso', '[isoFixedCutTightTrackOnly] == 1')]

    return cuts

#============================================================================================
def getMuonCuts(key):

    cuts  = []
    cuts += [CutItem('CutPt',       '[Pt]  > 15.0e3')]
    cuts += [CutItem('CutEta',      'fabs([Eta]) < 2.5')]
    cuts += [CutItem('CutPID',      '[Medium] == 1')]
    cuts += [CutItem('CutPassedID', '[PassedID] == 1')]
    cuts += [CutItem('CutOR',       '[ORHFJets_IsRemoved] == 0')]
    cuts += [CutItem('CutZ0Sin',    'fabs([Z0Sin]) < 0.5')]
    cuts += [CutItem('CutD0Sig',    'fabs([D0Sig]) < 3.0')]

    if key.count('PromptLeptonVeto'):
        cuts += [CutItem('CutIsoIso', '[isoFixedCutLoose] == 1')]
        cuts += [CutItem('CutIsoPlv', '[PromptLeptonVeto] < -0.5')]
    elif key.count('_iso'): 
        iso_wp = key.partition('_iso')[2]
        cuts += [CutItem('CutIso', '[iso%s] == 1' %iso_wp)]
    else:
        #cuts += [CutItem('CutIso', '[isoFCTight] == 1')]
        cuts += [CutItem('CutIso', '[isoFixedCutTightTrackOnly] == 1')]

    return cuts

#============================================================================================
def getAntiIDElecCuts():

    cuts  = []
    cuts += [CutItem('CutAuthor',   '[author] == 1')]
    cuts += [CutItem('CutPt',       '[Pt] > 15.0e3')]
    cuts += [CutItem('CutPID',      '[DFCommonElectronsLHLooseBL] == 1')]
    cuts += [CutItem('CutOR',       '[ORHFJets_IsRemoved] == 0')]
    cuts += [CutItem('CutZ0Sin',    'fabs([Z0Sin]) < 0.5')]
    cuts += [CutItem('CutD0Sig',    'fabs([D0Sig]) < 5.0')]

    return cuts

#============================================================================================
def getAntiIDMuonCuts():

    cuts  = []
    cuts += [CutItem('CutPt',       '[Pt]  > 15.0e3')]
    cuts += [CutItem('CutEta',      'fabs([Eta]) < 2.5')]
    cuts += [CutItem('CutPID',      '[Medium] == 1')]
    cuts += [CutItem('CutPassedID', '[PassedID] == 1')]
    cuts += [CutItem('CutOR',       '[ORHFJets_IsRemoved] == 0')]
    cuts += [CutItem('CutZ0Sin',    'fabs([Z0Sin]) < 0.5')]
    cuts += [CutItem('CutD0Sig',    'fabs([D0Sig]) < 15.0')]

    return cuts

#============================================================================================
def getLooseElecCuts(PLNI=False):

    cuts  = []

    cuts += [CutItem('CutOR',       '[ORHFJets_IsRemoved] == 0')]
    cuts += [CutItem('CutOQ',       '[IsGoodQuality] > 0')]
    cuts += [CutItem('CutPt',       '[Pt] > 10.0e3')]
    cuts += [CutItem('CutEtaCrack', 'fabs([ClEta]) < 1.37 || fabs([ClEta]) > 1.52')]
    cuts += [CutItem('CutEtaFid',   'fabs([ClEta]) < 2.47')]
    cuts += [CutItem('CutPID',      '[DFCommonElectronsLHLoose] == 1')]
    cuts += [CutItem('CutZ0Sin',    'fabs([Z0Sin]) < 0.5')]
    cuts += [CutItem('CutD0Sig',    'fabs([D0Sig]) < 5.0')]

    return cuts

#============================================================================================
def getLooseMuonCuts():

    cuts  = []

    cuts += [CutItem('CutOR',       '[ORHFJets_IsRemoved] == 0')]
    cuts += [CutItem('CutPt',       '[Pt] > 10.0e3')]
    cuts += [CutItem('CutEta',      'fabs([Eta]) < 2.5')]
    cuts += [CutItem('CutPID',      '[Medium] == 1')]
    cuts += [CutItem('CutPassedID', '[PassedID] == 1')]
    cuts += [CutItem('CutZ0Sin',    'fabs([Z0Sin]) < 0.5')]
    cuts += [CutItem('CutD0Sig',    'fabs([D0Sig]) < 15.0')]

    return cuts

#============================================================================================
def getLooseJetCuts():

    cuts  = []
    cuts += [CutItem('CutOR',  '[ORHFJets_IsRemoved] == 0')]
    cuts += [CutItem('CutPt',  '[Pt] > 25.0e3')]
    cuts += [CutItem('CutEta', 'fabs([Eta]) < 4.5')]

    return cuts

#============================================================================================
def getJetCuts():

    cuts  = []
    cuts += [CutItem('CutOR',  '[ORHFJets_IsRemoved] == 0')]
    cuts += [CutItem('CutPt',  '[Pt] > 25.0e3')]
    cuts += [CutItem('CutEta', 'fabs([Eta]) < 4.5')]
    cuts += [CutItem('CutFR',  'fabs([Eta]) < 2.5 || [Pt] > 30.0e3')]
    cuts += [CutItem('CutJVT', 'Pt > 60e3 || Eta > 2.4 || JVT > 0.59', abs=True)]

    return cuts

#================================================================================
def getJetBTagCuts(WP='70', reverse=False):

    WP_dict = {'70': 'MV2c10_70_Pass',
               '77': 'MV2c10_77_Pass',
               '85': 'MV2c10_85_Pass'}

    try:
        cut_value = WP_dict[WP]

    except KeyError:
        raise ValueError('getJetBTagCuts - unknown btag working point %s' %WP)

    if reverse:
        cut = [CutItem('CutJetBTag', '%s == 0' %cut_value)]
    else:
        cut = [CutItem('CutJetBTag', '%s == 1' %cut_value)]

    return cut

#================================================================================
def getTightElecCuts(options, key, AntiID=False):

    if AntiID:
        return getAntiIDElecCuts()

    else:
        return getElecCuts(key)

#================================================================================
def getTightMuonCuts(options, key, AntiID=False):

    if AntiID:
        return getAntiIDMuonCuts()

    else:
        return getMuonCuts(key)

#================================================================================
def getTriggerEventCuts(options):

    cut_year15 = CutItem('CutTrigYear15')
    cut_trig15 = CutItem('CutTrigs15')

    for trigger in getTriggers(options, 'All', 2015):
        cut_trig15.AddCut(CutItem('Cut%s' %trigger, '%s == 1' %trigger), 'OR')

    cut_year15.AddCut(CutItem('CutYear',  'RunYear == 2015'), 'AND')
    cut_year15.AddCut(cut_trig15,                             'AND')

    cut_year16 = CutItem('CutTrigYear16')
    cut_trig16 = CutItem('CutTrigs16')

    for trigger in getTriggers(options, 'All', 2016):
        cut_trig16.AddCut(CutItem('Cut%s' %trigger, '%s == 1' %trigger), 'OR')

    cut_year16.AddCut(CutItem('CutYear',  'RunYear == 2016'), 'AND')
    cut_year16.AddCut(cut_trig16,                             'AND')

    cut_year16D = CutItem('CutTrigYear16D')
    cut_trig16D = CutItem('CutTrigs16D')

    for trigger in getTriggers(options, 'All', 20164):
        cut_trig16D.AddCut(CutItem('Cut%s' %trigger, '%s == 1' %trigger), 'OR')

    cut_year16D.AddCut(CutItem('CutYear',  'RunYear == 20164'), 'AND')
    cut_year16D.AddCut(cut_trig16D,                             'AND')

    cut_year17 = CutItem('CutTrigYear17')
    cut_trig17 = CutItem('CutTrigs17')

    for trigger in getTriggers(options, 'All', 2017):
        cut_trig17.AddCut(CutItem('Cut%s' %trigger, '%s == 1' %trigger), 'OR')

    cut_year17.AddCut(CutItem('CutYear',  'RunYear == 2017'), 'AND')
    cut_year17.AddCut(cut_trig17,                             'AND')


    cut_trigs = CutItem('CutTrigMatch')
    cut_trigs.AddCut(cut_year15,  'OR')
    cut_trigs.AddCut(cut_year16,  'OR')
    cut_trigs.AddCut(cut_year16D, 'OR')
    cut_trigs.AddCut(cut_year17,  'OR')

    return [cut_trigs]

#================================================================================
def getTriggerMatchMuonCuts(options):

    cut_year15 = CutItem('CutTrigYear15')
    cut_trig15 = CutItem('CutTrigs15')

    for trigger in getTriggers(options, 'Muon', 2015):
        cut_trig15.AddCut(CutItem('Cut%s' %trigger, 'Pt > 21.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year15.AddCut(CutItem('CutYear',  'RunYear == 2015'), 'AND')
    cut_year15.AddCut(cut_trig15,                             'AND')

    cut_year16 = CutItem('CutTrigYear16')
    cut_trig16 = CutItem('CutTrigs16')

    for trigger in getTriggers(options, 'Muon', 2016):
        cut_trig16.AddCut(CutItem('Cut%s' %trigger, 'Pt > 27.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year16.AddCut(CutItem('CutYear',  'RunYear == 2016'), 'AND')
    cut_year16.AddCut(cut_trig16,                             'AND')

    cut_year16D = CutItem('CutTrigYear16D')
    cut_trig16D = CutItem('CutTrigs16D')

    for trigger in getTriggers(options, 'Muon', 20164):
        cut_trig16D.AddCut(CutItem('Cut%s' %trigger, 'Pt > 27.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year16D.AddCut(CutItem('CutYear',  'RunYear == 20164'), 'AND')
    cut_year16D.AddCut(cut_trig16D,                             'AND')

    cut_year17 = CutItem('CutTrigYear17')
    cut_trig17 = CutItem('CutTrigs17')

    for trigger in getTriggers(options, 'Muon', 2017):
        cut_trig17.AddCut(CutItem('Cut%s' %trigger, 'Pt > 27.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year17.AddCut(CutItem('CutYear',  'RunYear == 2017'), 'AND')
    cut_year17.AddCut(cut_trig17,                             'AND')


    cut_trigs = CutItem('CutTrigMatch')
    cut_trigs.AddCut(cut_year15,  'OR')
    cut_trigs.AddCut(cut_year16,  'OR')
    cut_trigs.AddCut(cut_year16D, 'OR')
    cut_trigs.AddCut(cut_year17,  'OR')

    return [cut_trigs]

#================================================================================
def getTriggerMatchElecCuts(options):

    cut_year15 = CutItem('CutTrigYear15')
    cut_trig15 = CutItem('CutTrigs15')

    for trigger in getTriggers(options, 'Elec', 2015):
        cut_trig15.AddCut(CutItem('Cut%s' %trigger, 'Pt > 25.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year15.AddCut(CutItem('CutYear',  'RunYear == 2015'), 'AND')
    cut_year15.AddCut(cut_trig15,                             'AND')

    cut_year16 = CutItem('CutTrigYear16')
    cut_trig16 = CutItem('CutTrigs16')

    for trigger in getTriggers(options, 'Elec', 2016):
        cut_trig16.AddCut(CutItem('Cut%s' %trigger, 'Pt > 27.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year16.AddCut(CutItem('CutYear',  'RunYear == 2016'), 'AND')
    cut_year16.AddCut(cut_trig16,                             'AND')

    cut_year16D = CutItem('CutTrigYear16D')
    cut_trig16D = CutItem('CutTrigs16D')

    for trigger in getTriggers(options, 'Elec', 20164):
        cut_trig16D.AddCut(CutItem('Cut%s' %trigger, 'Pt > 27.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year16D.AddCut(CutItem('CutYear',  'RunYear == 20164'), 'AND')
    cut_year16D.AddCut(cut_trig16D,                             'AND')

    cut_year17 = CutItem('CutTrigYear17')
    cut_trig17 = CutItem('CutTrigs17')

    for trigger in getTriggers(options, 'Elec', 2017):
        cut_trig17.AddCut(CutItem('Cut%s' %trigger, 'Pt > 27.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year17.AddCut(CutItem('CutYear',  'RunYear == 2017'), 'AND')
    cut_year17.AddCut(cut_trig17,                             'AND')

    cut_trigs = CutItem('CutTrigMatch')
    cut_trigs.AddCut(cut_year15,  'OR')
    cut_trigs.AddCut(cut_year16,  'OR')
    cut_trigs.AddCut(cut_year16D, 'OR')
    cut_trigs.AddCut(cut_year17,  'OR')

    return [cut_trigs]

#================================================================================
def getTriggers(options, key='All', year=2015):

    trigger_muon_2015 = ['HLT_mu20_iloose_L1MU15',
                         'HLT_mu50']

    trigger_elec_2015 = ['HLT_e24_lhmedium_L1EM20VH', # change to HLT_e24_lhmedium_L1EM18VH for MC
                         'HLT_e60_lhmedium',
                         'HLT_e120_lhloose']

    trigger_muon_2016 = ['HLT_mu26_ivarmedium',
                         'HLT_mu50']

    #trigger_elec_2016 = ['HLT_e24_lhtight_nod0_ivarloose',
    trigger_elec_2016 = ['HLT_e26_lhtight_nod0_ivarloose',
                         'HLT_e60_lhmedium_nod0',
                         'HLT_e140_lhloose_nod0']

    trigger_muon_2016D = ['HLT_mu26_ivarmedium',
                          'HLT_mu50']

    trigger_elec_2016D = ['HLT_e26_lhtight_nod0_ivarloose',
                          'HLT_e60_lhmedium_nod0',
                          'HLT_e140_lhloose_nod0']

    trigger_muon_2017 = ['HLT_mu26_ivarmedium',
                         'HLT_mu50']

    trigger_elec_2017 = ['HLT_e26_lhtight_nod0_ivarloose',
                         'HLT_e60_lhmedium_nod0',
                         'HLT_e140_lhloose_nod0']

    if year == 2015:
        if   key == 'All':  return trigger_muon_2015 + trigger_elec_2015
        elif key == 'Elec': return trigger_elec_2015
        elif key == 'Muon': return trigger_muon_2015

    if year == 2016:
        if   key == 'All':  return trigger_muon_2016 + trigger_elec_2016
        elif key == 'Elec': return trigger_elec_2016
        elif key == 'Muon': return trigger_muon_2016

    if year == 20164:
        if   key == 'All':  return trigger_muon_2016D + trigger_elec_2016D
        elif key == 'Elec': return trigger_elec_2016D
        elif key == 'Muon': return trigger_muon_2016D

    if year == 2017:
        if   key == 'All':  return trigger_muon_2017 + trigger_elec_2017
        elif key == 'Elec': return trigger_elec_2017
        elif key == 'Muon': return trigger_muon_2017


    raise Exception('getTriggers - failed to find triggers for: %s, %s' %(key, year))
