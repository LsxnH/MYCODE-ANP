import os
import sys
import re

import PhysicsAnpBase.PhysicsAnpBaseConfig  as physicsBase
import PhysicsAnpWH.  Config                as config

from PhysicsAnpBase.PhysicsAnpBaseConfig import CutItem
from PhysicsAnpBase.PhysicsAnpBaseConfig import addCuts
from PhysicsAnpBase.PhysicsAnpBaseConfig import getAlgName
from PhysicsAnpWH  .Config               import getCutValue

clog = physicsBase.getLog(os.path.basename(__file__))

#========================================================================================================
# Top level C++ module to read ntuples and configure and run algs
#========================================================================================================
def prepareReadModule(ROOT, options, files, top_algs):

    run = config.prepareReadNtuple(ROOT, options, files, hist_config=['PhysicsAnpWH/config'])

    if options.trees != None:
        run.SetKey('TreeName', options.trees)
    else:
        run.SetKey('TreeName', 'event')

    var_nicks = []
    var_vetos = []
    vec_vetos = []

    run.SetKey('VarNicks',    ','.join(var_nicks))
    run.SetKey('VetoVars',    ','.join(var_vetos))
    run.SetKey('VetoVecs',    ','.join(vec_vetos))

    run.SetKey('Print',            'yes')
    run.SetKey('NPrint',           10000)
    run.SetKey('NEventPerFile',    0)
    run.SetKey('Debug',            options.debug_run or options.debug)
    run.SetKey('FillTrueParts',    'yes')
    run.SetKey('FillAllTrueParts', 'yes')

    run.SetKey('PrefixJet',        'jet_')
    run.SetKey('PrefixElec',       'electron_')
    run.SetKey('PrefixMuon',       'muon_')
    run.SetKey('PrefixTruthPart',  'm_truth_')

    run.SetKey('Lists', 'jet_, electron_, muon_, m_truth_')
    
    for f in files:
        run.StoreInputFile(f)

    if options.print_vars:
        ROOT.Anp.Var.PrintAllVars()   

    run.AddTopAlg('topAlg', top_algs)

    if options.debug_all:
        run.SetGlobalPar('Debug', 'yes')

    return run

#========================================================================================================
def getRunNexus(name, options, algs=None):
	
    chain = config.getRunChain(name, algs=algs, cuts=None)

    chain.SetKey('DirName',         '')
    chain.SetKey('Debug',           options.debug)
    chain.SetKey('Print',           options.debug)
	
    alg = physicsBase.AlgConfig(name, 'RunNexus')   

    alg.SetKey('Print',    options.debug)
    alg.SetKey('Debug',    options.debug)
    alg.SetKey('AlgName',   chain.GetAlgName())
    alg.SetKey('DirData',  'data')
    alg.SetKey('VarName',  'MCChannel')

    alg.AddAlg(chain)
	   
    return alg

#========================================================================================================
def getPlotReco(name, options):

    plot_reco  = physicsBase.AlgConfig('plotReco',     'PlotReco')
    plot_jet   = physicsBase.AlgConfig('plotJet',      'PlotJet')
    plot_elec  = physicsBase.AlgConfig('plotElec',     'PlotElec')
    plot_muon  = physicsBase.AlgConfig('plotMuon',     'PlotMuon')
    plot_truth = physicsBase.AlgConfig('plotTruth',    'PlotTruth')

    plot_reco.SetKey('DirName',   '')  
    plot_reco.SetKey('UseWeight', 'no')

    plot_jet.SetKey('DoEachJet', 'no')

    algs = [plot_jet,
            plot_elec,
            plot_muon,
            plot_truth,
            plot_reco]

    for plot in algs:
        plot.SetKey('PlotCand', 'no')
        plot.SetKey('Debug',    options.debug)
        plot.SetKey('KeyHist',  'run2_%s' %plot.GetAlgType())

    chain = config.getRunChain(name, algs=algs)
    chain.SetKey('DirName',     name)
    chain.SetKey('Debug',       options.debug)
    chain.SetKey('Print',       options.debug)
    chain.SetKey('DoTimer',     options.do_timer)

    return chain

#========================================================================================================
def addPrintEvent(name, options, top_algs):

    if not options.print_reco_event and not options.print_cand_event:
        return

    alg = physicsBase.AlgConfig(name, 'PrintEvent')
    alg.SetKey('PrintRecoEvent',    options.print_reco_event)
    alg.SetKey('PrintCandEvent',    options.print_cand_event)
    alg.SetKey('PrintCandReco',     'no')
    alg.SetKey('PrintExtraTruth',   'yes')
    alg.SetKey('MatchEvents',       'yes')

    top_algs += [alg]

#========================================================================================================
def getPrepReco(name, options, key=None):

    alg = physicsBase.AlgConfig(name, 'PrepReco')

    alg.SetKey('Debug',         options.debug)
    alg.SetKey('DebugVars',     'no')
    alg.SetKey('Print',         'yes')
    alg.SetKey('AddLeptonMass', 'yes')
    
    return alg
