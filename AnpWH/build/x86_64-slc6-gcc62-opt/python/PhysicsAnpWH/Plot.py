import os
import sys
import re

import PhysicsAnpBase .PhysicsAnpBaseConfig as physicsBase
import PhysicsAnpWH   .Config               as config
import PhysicsAnpWH   .Common               as common

from PhysicsAnpBase.PhysicsAnpBaseConfig import CutItem
from PhysicsAnpBase.PhysicsAnpBaseConfig import addCuts
from PhysicsAnpBase.PhysicsAnpBaseConfig import getAlgName
from PhysicsAnpWH  .Config               import getCutValue

clog = physicsBase.getLog(os.path.basename(__file__))

#========================================================================================================
def prepareJobConfig(ROOT, options, files):

    clog.info('prepareJobConfig - prepare python configuration...')

    #-------------------------------------------------------------------------
    # Configure ntuple processing helper algorithms and candidate maker(s)
    #
    proc_algs = [common.getPrepReco('prepReco', options)]

    prep_algs = []
    plot_algs = [common.getPlotReco('plotReco', options)]

    if options.do_study:
        Regions = ['', '_PLNI', '_analysis', '_base']
    else:
        Regions = ['_base', '_base_tight']

    for cand in Regions:
        prep_cand = getPrepCand('prepCand%s' %cand, options)
        prep_tth  = getPrepttH ('prepttH%s'  %cand, prep_cand, options)

        prep_algs += [prep_cand, prep_tth]

        if cand == '_analysis':
            for flavour in ['', '_ee', '_em', '_mm']:
                plot_algs += [getStudyttH('studyttH_tight%s%s'            %(cand, flavour), prep_cand, options)]
                plot_algs += [getStudyttH('studyttH_tight%s%s_boosted'    %(cand, flavour), prep_cand, options)]

        if cand == '_PLNI':
            plot_algs += [getStudyttH('studyttH_loose%s'            %cand, prep_cand, options)]
            plot_algs += [getStudyttH('studyttH_loose%s_boosted'    %cand, prep_cand, options)]
            plot_algs += [getStudyttH('studyttH_loose%s_boosted_sr' %cand, prep_cand, options)]

            if options.mc_channel:
                for key in ['_hbb', '_hww']:
                    plot_algs += [getStudyttH('studyttH_loose%s%s_boosted'    %(cand, key), prep_cand, options)]
                    plot_algs += [getStudyttH('studyttH_loose%s%s_boosted_sr' %(cand, key), prep_cand, options)]

        if cand == '_base' or cand == '_base_tight':
            for pileup in ['', '_LowPU', '_HighPU']:
                for flavour in ['', '_ee', '_em', '_me', '_mm']:
                    plot_algs += [getPlotCand('cand%s%s_CR_ttbar_os%s'     %(cand, pileup, flavour), prep_cand, options)]
                    plot_algs += [getPlotCand('cand%s%s_CR_ttbar_ss%s'     %(cand, pileup, flavour), prep_cand, options)]
                    plot_algs += [getPlotCand('cand%s%s_SR_tth_ss%s'       %(cand, pileup, flavour), prep_cand, options)]
                    plot_algs += [getPlotCand('cand%s%s_SR_tth_ss_zveto%s' %(cand, pileup, flavour), prep_cand, options)]

                for flavour in ['ee', 'mm']:
                    plot_algs += [getPlotCand('cand%s%s_CR_Z_ss_%s'        %(cand, pileup, flavour), prep_cand, options)]
                    plot_algs += [getPlotCand('cand%s%s_CR_Z_os_%s'        %(cand, pileup, flavour), prep_cand, options)]
                    plot_algs += [getPlotCand('cand%s%s_CR_Zincl_os_%s'    %(cand, pileup, flavour), prep_cand, options)]
                    plot_algs += [getPlotCand('cand%s%s_CR_Zincl_ss_%s'    %(cand, pileup, flavour), prep_cand, options)]

    #-------------------------------------------------------------------------
    # Configure top level algorithms
    #
    top_algs  = proc_algs
    top_algs += prep_algs

    top_algs += [common.getRunNexus('runNexus', options, plot_algs)]
    
    common.addPrintEvent('printEvent', options, top_algs)

    #-------------------------------------------------------------------------
    # Prepare and configure top level C++ module
    #
    run = common.prepareReadModule(ROOT, options, files, top_algs)

    clog.info('prepareJobConfig - process up to %d events' %options.nevent)
    clog.info('prepareJobConfig - all done')

    return run

#========================================================================================================
def getPrepCand(name, options):
 
    event_cuts = []
    prep_cuts  = []
    elec_cuts  = getTightElecCuts()
    muon_cuts  = getTightMuonCuts()
    mobj_cuts  = getLooseMuonCuts()
    rjet_cuts  = getJetCuts      ()
    htau_cuts  = []
    truth_cuts = []


    remove_overlap = True

    if options.mc_channel:
        event_cuts += [CutItem('CutMC', 'MCChannel == %d' %options.mc_channel)]

    if options.btag_wp == None:
        WP = '60'
    else:
        WP = options.btag_wp

    bjet_cuts = getJetBTagCuts(WP)
    ljet_cuts = getJetBTagCuts(WP, reverse=True)

    if name.count('base'):
        elec_cuts = getElecCutsBase()
        muon_cuts = getMuonCutsBase()
        mobj_cuts = []

        remove_overlap = False

    elec_cuts += [CutItem('CutOR',     'passOR == 1')]
    muon_cuts += [CutItem('CutOR',     'passOR == 1')]
    rjet_cuts += [CutItem('CutOR',     'passOR == 1')]
    htau_cuts += [CutItem('CutOR',     'passOR == 1')]
    truth_cuts+= [CutItem('CutStatus', 'Status == 1')]

    alg = physicsBase.AlgConfig(name, 'PrepCand')

    alg.SetKey('Debug',                   'no')
    alg.SetKey('Print',                   'yes')
    alg.SetKey('PrintCutConf',            'yes')
    alg.SetKey('CopyVarsAll',             'yes')
    alg.SetKey('CountObj',                'yes')
    alg.SetKey('KeyHist',                 'PrepCand')
    alg.SetKey('DoLight',                 'no')
    alg.SetKey('DoFakeMuon',              'yes')
    alg.SetKey('SaveHist',                'yes')

    addCuts(alg, 'CutEvent',   event_cuts, save=options.print_cuts)
    addCuts(alg, 'CutPrep',    prep_cuts,  save=options.print_cuts)
    addCuts(alg, 'CutElec',    elec_cuts,  save=options.print_cuts)
    addCuts(alg, 'CutMuon',    muon_cuts,  save=options.print_cuts)
    addCuts(alg, 'CutMuonObj', mobj_cuts,  save=options.print_cuts)
    addCuts(alg, 'CutJet',     rjet_cuts,  save=options.print_cuts)
    addCuts(alg, 'CutJetBTag', bjet_cuts,  save=options.print_cuts)
    addCuts(alg, 'CutJetLTag', ljet_cuts,  save=options.print_cuts)
    addCuts(alg, 'CutTau',     htau_cuts,  save=options.print_cuts)

    if truth_cuts: addCuts(alg, 'CutTruth',      truth_cuts, save=options.print_cuts)

    if remove_overlap:
        alg.SetKey('OverlapCut_ElecElec', 0.1)
        alg.SetKey('OverlapCut_ElecJet',  0.4)
        alg.SetKey('OverlapCut_JetMuon',  0.4)
        alg.SetKey('OverlapCut_MObjElec', 0.1)
        alg.SetKey('OverlapCut_MuonMObj', 0.1)

    return alg

#========================================================================================================
def getPrepttH(name, cand, options):

    alg = physicsBase.AlgConfig(name, 'PrepttH')

    alg.SetKey('Debug',    options.debug)
    alg.SetKey('KeyHist',  'PrepttH')
    alg.SetKey('CandName', physicsBase.getAlgName(cand))

    physicsBase.addCuts(alg, 'CutElecCentral', [CutItem('CutEta', 'EtaBE2 < 1.37', abs=True)])

    physicsBase.addCuts(alg, 'CutElecTight',   getTightElecPLVCuts())
    physicsBase.addCuts(alg, 'CutMuonTight',   getTightMuonPLVCuts())
    
    physicsBase.addCuts(alg, 'CutTrigElec',    getTriggerMatchElecCuts(options))
    physicsBase.addCuts(alg, 'CutTrigMuon',    getTriggerMatchMuonCuts(options))

    physicsBase.addCuts(alg, 'CutTrigDileptonMMFirstLeg', getTriggerMatchDileptonCuts(options, 'mm', do_first=True))
    physicsBase.addCuts(alg, 'CutTrigDileptonEMFirstLeg', getTriggerMatchDileptonCuts(options, 'em', do_first=True))
    physicsBase.addCuts(alg, 'CutTrigDileptonEEFirstLeg', getTriggerMatchDileptonCuts(options, 'ee', do_first=True))

    physicsBase.addCuts(alg, 'CutTrigDileptonMMSecondLeg', getTriggerMatchDileptonCuts(options, 'mm', do_first=False))
    physicsBase.addCuts(alg, 'CutTrigDileptonEMSecondLeg', getTriggerMatchDileptonCuts(options, 'em', do_first=False))
    physicsBase.addCuts(alg, 'CutTrigDileptonEESecondLeg', getTriggerMatchDileptonCuts(options, 'ee', do_first=False))

    return alg

#========================================================================================================
def getStudyttH(name, cand, options):

    alg = physicsBase.AlgConfig(name, 'StudyttH')

    alg.SetKey('Debug',    options.debug)
    alg.SetKey('Print',    'no')
    alg.SetKey('KeyHist',  'StudyttH')
    alg.SetKey('CandName', physicsBase.getAlgName(cand))

    physicsBase.addCuts(alg, 'CutEvent', getEventCuts(name))

    return alg

#========================================================================================================
def getPlotCand(name, cand, options, do_print=False):
 
    plot_cand = physicsBase.AlgConfig('plotCand',  'PlotCand')
    plot_cand.SetKey('DirName',   '')
    plot_cand.SetKey('Plot2d',    'no')
    plot_cand.SetKey('PlotBCID',  'yes')
    plot_cand.SetKey('PrintVars', 'no')
    plot_cand.SetKey('KeyHist', 'run2_PlotCandFake2l')

    plot_lep  = physicsBase.AlgConfig('plotLep',   'PlotLep')
    plot_lep.SetKey('Debug',     options.debug)
    plot_lep.SetKey('Print',     'no')
    plot_lep.SetKey('PlotCand',  'yes')
    plot_lep.SetKey('CountLep',  'yes')
    plot_lep.SetKey('UseTopDir', 'yes')
    plot_lep.SetKey('UseWeight', 'yes')
    plot_lep.SetKey('DirName',   '')
    plot_lep.SetKey('KeyHist',   'run2_PlotLepFake')

    algs = [plot_cand, plot_lep]

    if options.do_Zincl and name.count('_Zincl_'):
        cuts = getZinclCuts(name)
    else:
        cuts = getNewEventCuts(name)

    chain = config.getRunChain(name, algs=algs, cuts=cuts, options=options)
    chain.SetKey('DirName',         name)
    chain.SetKey('Debug',           options.debug)
    chain.SetKey('Print',           do_print)
    chain.SetKey('NoWeight',        options.no_weight)
    chain.SetKey('PrintConfig',     'no')
    chain.SetKey('DoTimer',         options.do_timer)
    chain.SetKey('CandName',        physicsBase.getAlgName(cand))

    data_weights = []
    siml_weights = ['MCWeightOrg',
                    'PUWeight',
                    'MV2c10_70_EventWeight',
                    'JVTWeight',
                    'SherpaNJetWeight']
    # MV2c10_Continuous_EventWeight:  changed from Continuous to 70: in order to avoid effects of PCB very small at weight level

    #
    # Add different weights for loose and tight leptons
    #
    if name.count('_tight'):
        siml_weights += ['lepSFObjTight']
        if not options.noTrigSF:
           siml_weights += ['lepSFTrigTight']

    else:
        siml_weights += ['lepSFObjLoose']
        if not options.noTrigSF:
           siml_weights += ['lepSFTrigLoose']

    chain.SetKey('CandWeightsSiml', ','.join(siml_weights))
    chain.SetKey('CandWeightsData', ','.join(data_weights))

    return chain

#============================================================================================
# Event cuts
#============================================================================================
def getEventCuts(name):

    cuts = []
    
    cuts += [CutItem('CutNJetBTag', 'NJetBTag >= 2')]
    cuts += [CutItem('CutNJetLTag', 'NJetLTag >= 2')]
    cuts += [CutItem('CutSSCharge', 'LeptonChargeSum == 2', abs=True)]

    if name.count('tight'):
        cuts += [CutItem('CutNJet',     'NJet >= 4')]
        cuts += [CutItem('CutNLepton',  'NLepton  == 2')]
        cuts += [CutItem('CutNObjMuon', 'NObjMuon == 0')]

        if name.count('boosted'):
            cuts += [CutItem('CutSRNBJet',    'NJetBTag == 2')]
            cuts += [CutItem('CutBoostDRlu',  'LepBoost1st_DRlu2 < 1.0')]
            cuts += [CutItem('CutBoostDRlb',  'LepBoost1st_DRlb > 1.0')]

    elif name.count('loose'):
        cuts += [CutItem('CutNJet',     'NJet >= 5')]
        cuts += [CutItem('CutNLepton',  'NLepton == 2')]
        cuts += [CutItem('CutNObjMuon', 'NObjMuon == 1')]

        if name.count('boosted'):
            cuts += [CutItem('CutBoost', 'LepLoose0_DRlj2 < 1.0')]

        if name.count('_sr'):
            cuts += [CutItem('CutSRNBJet', 'NJetBTag == 2')]
            cuts += [CutItem('CutSR',      'LepLoose0_DRlb > 1.0')]

    else:
        raise Exception('getEventCuts - neither tight nor loose specified in name')

    cuts += getFlavourCuts(name)

    if   name.count('hbb'): cuts += [CutItem('CutHiggs', 'HiggsDecayMode == 0')]
    elif name.count('hww'): cuts += [CutItem('CutHiggs', 'HiggsDecayMode == 3')]

    return cuts

#============================================================================================
def getNewEventCuts(name):

  cuts  = []  
  cuts += [CutItem('CutEventClean',  'PassEventCleaning == 1')]
  cuts += getCandEventDiLepTrigCuts()

  cuts += [CutItem('CutTrigMatch',   'MatchTrigDilepton > 0')]  
  cuts += [CutItem('CutNLepton',     'dilep_type > 0')]
  cuts += [CutItem('CutLepPt',       'Lep0Pt > 25.0e3 && Lep1Pt > 25.0e3')]
  cuts += [CutItem('CutElecCentral', 'NElecForward == 0')]
  
  cuts += getFlavourCuts(name)
  cuts += getRegionCuts(name)

  return cuts

#============================================================================================
def getZinclCuts(name):

  cuts  = []  
  cuts += [CutItem('CutBlinded',       'IsBlinded == 0')]
  cuts += [CutItem('CutMll',           'Mll >= 40.0e3')]

  cuts += [CutItem('CutNLepton',       'dilep_type > 0')]
  cuts += [CutItem('CutEventClean',    'PassEventCleaning == 1')]
  if name.count('_os'):
      cuts += [CutItem('CutLepCharge', 'total_charge == 0')] 
  elif name.count('_ss'):
      cuts += [CutItem('CutLepCharge', 'total_charge != 0')] 

  cuts += getCandEventDiLepTrigCuts()
  cuts += [CutItem('CutLepTrig',       'lep_isTrigMatch_0 > 0 || lep_isTrigMatch_1 > 0||matchDLTll01 >0')]

  cuts += [CutItem('CutTrigMatch',     'MatchTrigNLep > 0 || MatchTrigDilepton > 0')]  
  cuts += [CutItem('CutLepPt',         'Lep0Pt > 25.0e3 && Lep1Pt > 10.0e3')]
  
  cuts += getFlavourCuts(name)


  return cuts


#============================================================================================
def getRegionCuts(name):
  '''
     define signal region or control region criteria 
  '''

  cuts = []

  # two lepton charge cuts
  if name.count('_os'):
      cuts += [CutItem('CutLepCharge', 'LeptonChargeSum == 0', abs=True)]      
  elif name.count('_ss'):
      cuts += [CutItem('CutLepCharge', 'LeptonChargeSum == 2', abs=True)] 

  # CR
  if name.count('_Z_'):
      cuts += [CutItem('CutMll', 'Mll > 81.2e3 && Mll < 101.2e3')]

  elif name.count('_ttbar_'):
      cuts += [CutItem('CutMll',   'Mll >= 40.0e3')]
      cuts += [CutItem('CutNJet',  'NJet < 5')]
      cuts += [CutItem('CutNBJet', 'NJetBTag >= 1')]

  # SR
  if name.count('_tth_'):
      cuts += [CutItem('CutNTau',  'NTau == 0')]
      cuts += [CutItem('CutNJet',  'NJet >= 4')]
      cuts += [CutItem('CutNBJet', 'NJetBTag >= 1')]

  # Z veto option
  if name.count('_zveto_'):
      cuts += [CutItem('CutZVeto', 'Mll < 81.2e3 || Mll > 101.2e3')]

  # pileup
  if name.count('_LowPU_'):
      cuts += [CutItem('CutPU',    '[NRecoPileUp]  < 30')]
  elif name.count('_HighPU_'):
      cuts += [CutItem('CutPU',    '[NRecoPileUp]  > 40')]

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

    if name.count('_ep'):
        cuts += [CutItem('CutNElec', 'NElecTight == 1')]

    if name.count('_mp'):
        cuts += [CutItem('CutNMuon', 'NMuonTight == 1')]

    if not name.count ('_tight_')==0:
        cuts += [CutItem('CutNLepTight', 'NLeptonTight2l == 2')]

    return cuts

#================================================================================
def getCandEventSingleTrigCuts():

    #    
    # 2015
    #    
    cut_trig_2015 = CutItem('CutSingleTrig2015')

    # single lepton 2015
    cut_trig_2015.AddCut(CutItem('Cut_2015_mu24',   'HLT_mu20_iloose_L1MU15    > 0'), 'OR')
    cut_trig_2015.AddCut(CutItem('Cut_2015_mu50',   'HLT_mu50                  > 0'), 'OR')
    cut_trig_2015.AddCut(CutItem('Cut_2015_e24_20', 'HLT_e24_lhmedium_L1EM18VH > 0 && MCChannel > 0'), 'OR')
    cut_trig_2015.AddCut(CutItem('Cut_2015_e24_18', 'HLT_e24_lhmedium_L1EM20VH > 0 && MCChannel < 1'), 'OR')
    cut_trig_2015.AddCut(CutItem('Cut_2015_e60',    'HLT_e60_lhmedium          > 0'), 'OR')
    cut_trig_2015.AddCut(CutItem('Cut_2015_e120',   'HLT_e120_lhloose          > 0'), 'OR')

    cut_pass_2015 = CutItem('CutSingleTrig2015Pass')
    cut_pass_2015.AddCut(CutItem('CutYear2015', 'RunYear == 2015'), 'AND')
    cut_pass_2015.AddCut(cut_trig_2015, 'AND')

    #    
    # 2016
    #    
    cut_trig_2016 = CutItem('CutSingleTrig2016')

    # single lepton 2016
    cut_trig_2016.AddCut(CutItem('Cut_2016_mu26', 'HLT_mu26_ivarmedium            > 0'), 'OR')
    cut_trig_2016.AddCut(CutItem('Cut_2016_mu50', 'HLT_mu50                       > 0'), 'OR')
    cut_trig_2016.AddCut(CutItem('Cut_2016_e26',  'HLT_e26_lhtight_nod0_ivarloose > 0'), 'OR')
    cut_trig_2016.AddCut(CutItem('Cut_2016_e60',  'HLT_e60_lhmedium_nod0          > 0'), 'OR')
    cut_trig_2016.AddCut(CutItem('Cut_2016_e140', 'HLT_e140_lhloose_nod0          > 0'), 'OR')

    cut_pass_2016 = CutItem('CutSingleTrig2016Pass')
    cut_pass_2016.AddCut(CutItem('CutYear2016', 'RunYear == 2016'), 'AND')
    cut_pass_2016.AddCut(cut_trig_2016, 'AND')


    #
    # 2017
    #
    cut_trig_2017 = CutItem('CutSingleTrig2017')

    # single lepton 2017
    cut_trig_2017.AddCut(CutItem('Cut_2017_mu26', 'HLT_mu26_ivarmedium            > 0'), 'OR')
    cut_trig_2017.AddCut(CutItem('Cut_2017_mu50', 'HLT_mu50                       > 0'), 'OR')
    cut_trig_2017.AddCut(CutItem('Cut_2017_e26',  'HLT_e26_lhtight_nod0_ivarloose > 0'), 'OR')
    cut_trig_2017.AddCut(CutItem('Cut_2017_e60',  'HLT_e60_lhmedium_nod0          > 0'), 'OR')
    cut_trig_2017.AddCut(CutItem('Cut_2017_e140', 'HLT_e140_lhloose_nod0          > 0'), 'OR')

    cut_pass_2017 = CutItem('CutSingleTrig2017Pass')
    cut_pass_2017.AddCut(CutItem('CutYear2017', 'RunYear == 2017'), 'AND')
    cut_pass_2017.AddCut(cut_trig_2017, 'AND')

    #
    # Add cuts
    #
    cut_trig = CutItem('CutSingleEventTrig')
    cut_trig.AddCut(cut_pass_2015, 'OR')
    cut_trig.AddCut(cut_pass_2016, 'OR')
    cut_trig.AddCut(cut_pass_2017, 'OR')

    return [cut_trig]


#================================================================================
def getCandEventDiLepTrigCuts():

    #    
    # 2015
    #    
    cut_trig_2015 = CutItem('CutDiLepTrig2015')

    # single lepton 2015
    cut_trig_2015.AddCut(CutItem('Cut_2015_2e12',      'HLT_2e12_lhloose_L12EM10VH    > 0'), 'OR')
    cut_trig_2015.AddCut(CutItem('Cut_2015_e17mu14',   'HLT_e17_lhloose_mu14    > 0'), 'OR')
    cut_trig_2015.AddCut(CutItem('Cut_2015_mu18mu8',   'HLT_mu18_mu8noL1   > 0'), 'OR')


    cut_pass_2015 = CutItem('CutDiLepTrig2015Pass')
    cut_pass_2015.AddCut(CutItem('CutYear2015', 'RunYear == 2015'), 'AND')
    cut_pass_2015.AddCut(cut_trig_2015, 'AND')

    #    
    # 2016
    #    
    cut_trig_2016 = CutItem('CutDiLepTrig2016')

    # single lepton 2016
    cut_trig_2016.AddCut(CutItem('Cut_2016_2e17',    'HLT_2e17_lhvloose_nod0            > 0'), 'OR')
    cut_trig_2016.AddCut(CutItem('Cut_2016_e17mu14', 'HLT_e17_lhloose_nod0_mu14            > 0'), 'OR')
    cut_trig_2016.AddCut(CutItem('Cut_2016_mu22mu8', 'HLT_mu22_mu8noL1            > 0'), 'OR')


    cut_pass_2016 = CutItem('CutDiLepTrig2016Pass')
    cut_pass_2016.AddCut(CutItem('CutYear2016', 'RunYear == 2016'), 'AND')
    cut_pass_2016.AddCut(cut_trig_2016, 'AND')


    #
    # 2017
    #
    cut_trig_2017 = CutItem('CutDiLepTrig2017')

    # single lepton 2017
    cut_trig_2017.AddCut(CutItem('Cut_2017_2e24',    'HLT_2e24_lhvloose_nod0            > 0'), 'OR')
    cut_trig_2017.AddCut(CutItem('Cut_2017_e17mu14', 'HLT_e17_lhloose_nod0_mu14            > 0'), 'OR')
    cut_trig_2017.AddCut(CutItem('Cut_2017_mu22mu8', 'HLT_mu22_mu8noL1            > 0'), 'OR')


    cut_pass_2017 = CutItem('CutDiLepTrig2017Pass')
    cut_pass_2017.AddCut(CutItem('CutYear2017', 'RunYear == 2017'), 'AND')
    cut_pass_2017.AddCut(cut_trig_2017, 'AND')

    #
    # Add cuts
    #
    cut_trig = CutItem('CutDiLepEventTrig')
    cut_trig.AddCut(cut_pass_2015, 'OR')
    cut_trig.AddCut(cut_pass_2016, 'OR')
    cut_trig.AddCut(cut_pass_2017, 'OR')

    return [cut_trig]



#============================================================================================
# Object cuts
#============================================================================================
def getElecCutsBase():

    cuts  = []

    cuts += [CutItem('CutPt',       'Pt > 10.0e3')]
    cuts += [CutItem('CutEtaCrack', 'EtaBE2 < 1.37 || EtaBE2 > 1.52', abs=True)]
    cuts += [CutItem('CutEtaFid',   'EtaBE2 < 2.47', abs=True)]
    cuts += [CutItem('CutPID',      'isTightLH == 1')]
    cuts += [CutItem('CutZ0Sin',    'Z0Sin < 0.5', abs=True)]
    cuts += [CutItem('CutD0Sig',    'D0Sig < 5.0', abs=True)]
    cuts += [CutItem('CutIso',      'isoLoose == 1')]

    return cuts


#============================================================================================
def getTightElecCuts():

    cuts  = []

    cuts += [CutItem('CutPt',       'Pt > 20.0e3')]

    cuts += [CutItem('CutEtaCrack', 'EtaBE2 < 1.37 || EtaBE2 > 1.52', abs=True)]
    cuts += [CutItem('CutEtaFid',   'Eta < 2.47', abs=True)] 
    cuts += [CutItem('CutTightPID', 'isTightLH == 1')]
    cuts += [CutItem('CutZ0Sin',    'Z0Sin < 0.5', abs=True)]
    cuts += [CutItem('CutD0Sig',    'D0Sig < 5.0', abs=True)] 

    cuts += [CutItem('CutIso',      'isoFixedCutTight == 1')]

    return cuts


#============================================================================================
def getTightElecPLVCuts():

    cuts  = []

    cuts += [CutItem('CutPt',    'Pt > 10.0e3')]

    cuts += [CutItem('CutEtaCrack', 'EtaBE2 < 1.37 || EtaBE2 > 1.52', abs=True)]
    cuts += [CutItem('CutEtaFid',   'Eta < 2.47', abs=True)]
    cuts += [CutItem('CutTightPID', 'isTightLH == 1')]
    cuts += [CutItem('CutZ0Sin',    'Z0Sin < 0.5', abs=True)]
    cuts += [CutItem('CutD0Sig',    'D0Sig < 5.0', abs=True)] 

    #new tight lepton definition
    cuts += [CutItem('CutAmType',   'ambiguityType == 0')]
    cuts += [CutItem('CutPLV',      'isoFixedCutLoose == 1 && PromptLeptonVeto_TagWeight < -0.7')]
    cuts += [CutItem('CutQmisID',   'ChargeIDBDT > 0.7')]

    return cuts

#============================================================================================
def getMuonCutsBase():

    cuts  = []

    cuts += [CutItem('CutPt',      'Pt > 10.0e3')]
    cuts += [CutItem('CutEta',     'Eta < 2.5', abs=True)]
    cuts += [CutItem('CutPID',     'isLoose == 1')]
    cuts += [CutItem('CutZ0Sin',   'Z0Sin < 0.5', abs=True)]
    cuts += [CutItem('CutD0Sig',   'D0Sig < 3.0', abs=True)]
    cuts += [CutItem('CutIsoVeto', 'isoLoose == 1')]

    return cuts


#============================================================================================
def getLooseMuonCuts(PLNI=False):

    cuts  = []

    cuts += [CutItem('CutPt',      'Pt > 20.0e3')]
    cuts += [CutItem('CutEta',     'Eta < 2.5', abs=True)]
    cuts += [CutItem('CutPID',     'isLoose == 1')]
    cuts += [CutItem('CutZ0Sin',   'Z0Sin < 0.5', abs=True)]
    cuts += [CutItem('CutD0Sig',   'D0Sig < 3.0', abs=True)]
    cuts += [CutItem('CutIsoVeto', 'isoFixedCutTightTrackOnly == 0')]

    return cuts

#============================================================================================
def getTightMuonCuts():

    cuts  = []

    cuts += [CutItem('CutPt',    'Pt > 20.0e3')]
    
    cuts += [CutItem('CutEta',   'Eta < 2.5', abs=True)]
    cuts += [CutItem('CutPID',   'isLoose == 1')]
    cuts += [CutItem('CutZ0Sin', 'Z0Sin < 0.5', abs=True)]
    cuts += [CutItem('CutD0Sig', 'D0Sig < 3.0', abs=True)]

    cuts += [CutItem('CutIso',   'isoFixedCutTightTrackOnly == 1')]

    return cuts


#============================================================================================
def getTightMuonPLVCuts():

    cuts  = []

    cuts += [CutItem('CutPt',    'Pt > 10.0e3')]

    cuts += [CutItem('CutEta',   'Eta < 2.5', abs=True)]
    cuts += [CutItem('CutPID',   'isLoose == 1')]
    cuts += [CutItem('CutZ0Sin', 'Z0Sin < 0.5', abs=True)]
    cuts += [CutItem('CutD0Sig', 'D0Sig < 3.0', abs=True)]

    #new tight lepton definition
    cuts += [CutItem('CutPLV',   'isoFixedCutLoose == 1 && PromptLeptonVeto_TagWeight < -0.5')]

    return cuts

#============================================================================================
def getJetCuts():

    cuts  = []
    cuts += [CutItem('CutPt',  'Pt > 25.0e3')]
    cuts += [CutItem('CutEta', 'Eta < 2.5', abs=True)]
    cuts += [CutItem('CutJVT', 'Pt > 60e3 || Eta > 2.4 || JVT > 0.59',abs=True)]

    return cuts

#================================================================================
def getJetBTagCuts(WP='60', reverse=False):
	
    WP_dict = {'60': 0.92,
               '70': 0.79,
               '77': 0.58,
               '85': 0.05}
	
    try:
        cut_value = WP_dict[WP]
	
    except KeyError:
        raise ValueError('getJetBTagCuts - unknown btag working point %s' %WP)
	
    if reverse:
        cut = [CutItem('CutJetBTag', 'MV2c10 < %f' %cut_value)]
    else:
        cut = [CutItem('CutJetBTag', 'MV2c10 > %f' %cut_value)]
	
    return cut

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

    cut_year17 = CutItem('CutTrigYear17')
    cut_trig17 = CutItem('CutTrigs17')

    for trigger in getTriggers(options, 'Muon', 2017):
        cut_trig17.AddCut(CutItem('Cut%s' %trigger, 'Pt > 27.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year17.AddCut(CutItem('CutYear',  'RunYear == 2017'), 'AND')
    cut_year17.AddCut(cut_trig17,                             'AND')


    cut_trigs = CutItem('CutTrigMatch')
    cut_trigs.AddCut(cut_year15, 'OR')
    cut_trigs.AddCut(cut_year16, 'OR')
    cut_trigs.AddCut(cut_year17, 'OR')

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

    cut_year17 = CutItem('CutTrigYear17')
    cut_trig17 = CutItem('CutTrigs17')

    for trigger in getTriggers(options, 'Elec', 2017):
        cut_trig17.AddCut(CutItem('Cut%s' %trigger, 'Pt > 27.0e3 && match_%s == 1' %trigger), 'OR')

    cut_year17.AddCut(CutItem('CutYear',  'RunYear == 2017'), 'AND')
    cut_year17.AddCut(cut_trig17,                             'AND')

    cut_trigs = CutItem('CutTrigMatch')
    cut_trigs.AddCut(cut_year15, 'OR')
    cut_trigs.AddCut(cut_year16, 'OR')
    cut_trigs.AddCut(cut_year17, 'OR')

    return [cut_trigs]

#================================================================================
def getTriggers(options, key='All', year=2015):

    trigger_muon_2015 = ['HLT_mu20_iloose_L1MU15',
                         'HLT_mu50']

    trigger_elec_2015 = ['HLT_e24_lhmedium_L1EM18VH',
                         'HLT_e24_lhmedium_L1EM20VH',
                         'HLT_e60_lhmedium',
                         'HLT_e120_lhloose']

    trigger_muon_2016 = ['HLT_mu26_ivarmedium',
                         'HLT_mu50']

    trigger_elec_2016 = ['HLT_e26_lhtight_nod0_ivarloose',
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

    if year == 2017:
        if   key == 'All':  return trigger_muon_2017 + trigger_elec_2017
        elif key == 'Elec': return trigger_elec_2017
        elif key == 'Muon': return trigger_muon_2017


    raise Exception('getTriggers - failed to find triggers for: %s, %s' %(key, year))

#================================================================================
def getTriggerMatchDileptonCuts(options, comb, do_first=True):

    #
    # This function assumes there is only one dilepton trigger
    # for each of ee, em and mm
    #

    cut_year15 = CutItem('CutDilepTrigYear15')
    cut_trig15 = CutItem('CutDilepTrigs15')

    for trigger in getDileptonTriggers(options, comb, 2015):
        first, second = getDileptonTriggerInfo(trigger)
        pid1, pt1 = first
        pid2, pt2 = second

        if do_first:
            cut_trig15.AddCut(CutItem('Cut%s_FirstLegPID'  %trigger, 'PDG == %i' %pid1, abs=True), 'AND')
            cut_trig15.AddCut(CutItem('Cut%s_FirstLeg'     %trigger, 'Pt > %.1fe3 && match_%s == 1' %(pt1, trigger)), 'AND')
        else:
            cut_trig15.AddCut(CutItem('Cut%s_SecondLegPID' %trigger, 'PDG == %i' %pid2, abs=True), 'AND')
            cut_trig15.AddCut(CutItem('Cut%s_SecondLeg'    %trigger, 'Pt > %.1fe3 && match_%s == 1' %(pt2, trigger)), 'AND')

    cut_year15.AddCut(CutItem('CutYear', 'RunYear == 2015'), 'AND')
    cut_year15.AddCut(cut_trig15,                            'AND')

    cut_year16 = CutItem('CutDilepTrigYear16')
    cut_trig16 = CutItem('CutDilepTrigs16')

    for trigger in getDileptonTriggers(options, comb, 2016):
        first, second = getDileptonTriggerInfo(trigger)
        pid1, pt1 = first
        pid2, pt2 = second

        if do_first:
            cut_trig16.AddCut(CutItem('Cut%s_FirstLegPID'  %trigger, 'PDG == %i' %pid1, abs=True), 'AND')
            cut_trig16.AddCut(CutItem('Cut%s_FirstLeg'     %trigger, 'Pt > %.1fe3 && match_%s == 1' %(pt1, trigger)), 'AND')
        else:
            cut_trig16.AddCut(CutItem('Cut%s_SecondLegPID' %trigger, 'PDG == %i' %pid2, abs=True), 'AND')
            cut_trig16.AddCut(CutItem('Cut%s_SecondLeg'    %trigger, 'Pt > %.1fe3 && match_%s == 1' %(pt2, trigger)), 'AND')

    cut_year16.AddCut(CutItem('CutYear', 'RunYear == 2016'), 'AND')
    cut_year16.AddCut(cut_trig16,                            'AND')

    cut_year17 = CutItem('CutDilepTrigYear17')
    cut_trig17 = CutItem('CutDilepTrigs17')

    for trigger in getDileptonTriggers(options, comb, 2017):
        first, second = getDileptonTriggerInfo(trigger)
        pid1, pt1 = first
        pid2, pt2 = second

        if do_first:
            cut_trig17.AddCut(CutItem('Cut%s_FirstLegPID'  %trigger, 'PDG == %i' %pid1, abs=True), 'AND')
            cut_trig17.AddCut(CutItem('Cut%s_FirstLeg'     %trigger, 'Pt > %.1fe3 && match_%s == 1' %(pt1, trigger)), 'AND')
        else:
            cut_trig17.AddCut(CutItem('Cut%s_SecondLegPID' %trigger, 'PDG == %i' %pid2, abs=True), 'AND')
            cut_trig17.AddCut(CutItem('Cut%s_SecondLeg'    %trigger, 'Pt > %.1fe3 && match_%s == 1' %(pt2, trigger)), 'AND')

    cut_year17.AddCut(CutItem('CutYear', 'RunYear == 2017'), 'AND')
    cut_year17.AddCut(cut_trig17,                            'AND')


    cut_trigs = CutItem('CutDilepTrigMatch')
    cut_trigs.AddCut(cut_year15, 'OR')
    cut_trigs.AddCut(cut_year16, 'OR')
    cut_trigs.AddCut(cut_year17, 'OR')

    return [cut_trigs]

#================================================================================
def getDileptonTriggerInfo(trigger):

    #
    # Function to return (pid, pt threshold) for first and second legs of 
    # dilepton trigger
    #

    parts = trigger.split('_')
    first_leg = parts[1]

    if trigger.count('mu18_mu8') or trigger.count('mu22_mu8'):
        pid = 13
        first_pt  = 1.05*float(first_leg.lstrip('mu'))
        second_pt = 1.05*8.0
        first  = (pid, first_pt)
        second = (pid, second_pt)

    elif trigger.count('2e'):
        pid = 11
        first_pt = 1.05*float(first_leg.lstrip('2e'))
        second_pt = first_pt
        first  = (pid, first_pt)
        second = (pid, second_pt)

    elif first_leg.count('e'):
        first_pt  = 1.05*float(first_leg.lstrip('e'))
        for part in parts:
            if part.count('mu'): second_pt = 1.05*float(part.lstrip('mu'))
        first  = (11, first_pt)
        second = (13, second_pt)

    return first, second

#================================================================================
def getDileptonTriggers(options, key, year=2015):

    trigger_dilepton_2015 = ['HLT_2e12_lhloose_L12EM10VH',
                             'HLT_e17_lhloose_mu14',
                             'HLT_mu18_mu8noL1']

    trigger_dilepton_2016 = ['HLT_2e17_lhvloose_nod0',
                             'HLT_e17_lhloose_nod0_mu14',
                             'HLT_mu22_mu8noL1']

    trigger_dilepton_2017 = ['HLT_2e24_lhvloose_nod0',
                             'HLT_e17_lhloose_nod0_mu14',
                             'HLT_mu22_mu8noL1']

    if year == 2015:
        if key == 'All': return trigger_dilepton_2015
        if key == 'ee':  return ['HLT_2e12_lhloose_L12EM10VH']
        if key == 'em':  return ['HLT_e17_lhloose_mu14']
        if key == 'mm':  return ['HLT_mu18_mu8noL1']

    if year == 2016:
        if key == 'All': return trigger_dilepton_2016
        if key == 'ee':  return ['HLT_2e17_lhvloose_nod0']
        if key == 'em':  return ['HLT_e17_lhloose_nod0_mu14']
        if key == 'mm':  return ['HLT_mu22_mu8noL1']

    if year == 2017:
        if key == 'All': return trigger_dilepton_2017
        if key == 'ee':  return ['HLT_2e24_lhvloose_nod0']
        if key == 'em':  return ['HLT_e17_lhloose_nod0_mu14']
        if key == 'mm':  return ['HLT_mu22_mu8noL1']

    raise Exception('getDileptonTriggers - failed to find triggers for: %s' %(year))


#================================================================================
def getDileptonTriggerInfo(trigger):

    #
    # Function to return (pid, pt threshold) for first and second legs of 
    # dilepton trigger
    #

    parts = trigger.split('_')
    first_leg = parts[1]

    if trigger.count('mu18_mu8') or trigger.count('mu22_mu8'):
        pid = 13
        first_pt  = 1.05*float(first_leg.lstrip('mu'))
        second_pt = 1.05*8.0
        first  = (pid, first_pt)
        second = (pid, second_pt)

    elif trigger.count('2e'):
        pid = 11
        first_pt = 1.05*float(first_leg.lstrip('2e'))
        second_pt = first_pt
        first  = (pid, first_pt)
        second = (pid, second_pt)

    elif first_leg.count('e'):
        first_pt  = 1.05*float(first_leg.lstrip('e'))
        for part in parts:
            if part.count('mu'): second_pt = 1.05*float(part.lstrip('mu'))
            0
        first  = (11, first_pt)
        second = (13, second_pt)

    return first, second
