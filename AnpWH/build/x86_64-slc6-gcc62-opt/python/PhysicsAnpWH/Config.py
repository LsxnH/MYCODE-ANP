
import logging
import os
import re
import sys

import PhysicsAnpBase.PhysicsAnpBaseConfig as physicsBase

#========================================================================================================
def prepareOptionParser():
    
    from optparse import OptionParser
    
    p = OptionParser()

    p.add_option('--dirs-key',          type='string', default=None,               dest='dirskey')
    p.add_option('--file-key',          type='string', default='.root',           dest='filekey')
    p.add_option('--data-key',          type='string', default='data_[0-9]+.root', dest='datakey')    
    p.add_option('--output', '-o',      type='string', default=None,               dest='output')
    p.add_option('--trees',             type='string', default=None,               dest='trees')
    p.add_option('--save-input-files',  type='string', default=None)
    p.add_option('--run-xml',           type='string', default='run.xml',          help='xml job file')
    p.add_option('--debug-alg',         type='string', default=False)

    p.add_option('--nevent', '-n',      type='int',    default=0,              dest='nevent')
    p.add_option('--nprint',            type='int',    default=10000,          dest='nprint')
    p.add_option('--mc-channel',        type='int',    default=None,           dest='mc_channel')
    p.add_option('--lumi',              type='float',  default=20280.2,        dest='lumi')

    p.add_option('--batch', '-b',        action='store_true',  default=False, dest='batch')
    p.add_option('--debug', '-d',        action='store_true',  default=False, dest='debug')
    p.add_option('--debug-all',          action='store_true',  default=False, dest='debug_all')
    p.add_option('--debug-run',          action='store_true',  default=False, dest='debug_run')
    p.add_option('--debug-prep',         action='store_true',  default=False, dest='debug_prep')
    p.add_option('--debug-reco',         action='store_true',  default=False, dest='debug_reco')    
    p.add_option('--print-vars',         action='store_true',  default=False, dest='print_vars')
    p.add_option('--print-cuts',         action='store_true',  default=False, dest='print_cuts')    
    p.add_option('--print-true',         action='store_true',  default=False, dest='print_true')
    p.add_option('--print-reco-event',   action='store_true',  default=False, dest='print_reco_event')
    p.add_option('--print-cand-event',   action='store_true',  default=False, dest='print_cand_event')
    p.add_option('--test', '-t',         action='store_true',  default=False, dest='test')    
    p.add_option('--dry-run',            action='store_true',  default=False, dest='dryrun')
    p.add_option('--draw',               action='store_true',  default=False, dest='draw')
    p.add_option('--write',              action='store_true',  default=False, dest='write')

    p.add_option('--do-fake-cr',         action='store_true',  default=False)
    p.add_option('--do-prompt-cr',       action='store_true',  default=False)
    p.add_option('--do-prompt-sr',       action='store_true',  default=False)
    p.add_option('--do-2l-cr',           action='store_true',  default=False)
    p.add_option('--do-scan-sr',         action='store_true',  default=False)
    p.add_option('--do-plot',            action='store_true',  default=False, dest='do_plot')
    p.add_option('--do-analysis',        action='store_true',  default=False, dest='do_analysis')
    p.add_option('--do-eval',            action='store_true',  default=False, dest='do_eval')
    p.add_option('--do-elec',            action='store_true',  default=False, dest='do_elec')
    p.add_option('--do-muon',            action='store_true',  default=False, dest='do_muon')
    p.add_option('--do-loose',           action='store_true',  default=False, dest='do_loose')
    p.add_option('--mva-path',           type='string',        default=None,  dest='mva_path')
    p.add_option('--mva-train-opt',      type='string',        default='',    dest='mva_train_opt')
    p.add_option('--training-var',       type='string',        default=None,  dest='training_var')
    p.add_option('--bdt-opts',           type='string',        default=None,  dest='bdt_opts')
    p.add_option('--select-type',        type='string',        default=None,  dest='select_type')
    p.add_option('--btag-wp',            type='string',        default=None,  dest='btag_wp')

    #---------------------------------------------------------------------------------------------------
    # ttH options
    #   
    p.add_option('--use-raw-counts',     action='store_true',  default=False, dest='use_raw_counts')
    p.add_option('--do-timer',           action='store_true',  default=False, dest='do_timer')
    p.add_option('--no-weight',          action='store_true',  default=False, dest='no_weight')
    p.add_option('--do-tau',             action='store_true',  default=False, dest='do_tau')
    p.add_option('--do-cutflow',         action='store_true',  default=False, dest='do_cutflow')
    p.add_option('--do-pass-or',         action='store_true',  default=False, dest='do_pass_or')
    p.add_option('--do-study',           action='store_true',  default=False, dest='do_study')
        
    #---------------------------------------------------------------------------------------------------
    # WH options
    #   
    p.add_option('--ZjetsOR',            action='store_true',  default=False, dest='ZjetsOR')
    p.add_option('--ZjetsORreverse',     action='store_true',  default=False, dest='ZjetsORreverse')
    p.add_option('--doSherpa',           action='store_true',  default=False, dest='doSherpa')

    return p

#========================================================================================================
clog = physicsBase.getLog(os.path.basename(__file__))

#========================================================================================================
load_physics_wh_libs = None

def loadPhysicsAnpWHLib(ROOT):

    global load_physics_wh_libs

    if load_physics_wh_libs:
        return

    clog.info('loadPhysicsAnpWHLib - load shared libraries')

    from ROOT import Anp

    setPlotDefaults(ROOT)
    
    ROOT.gSystem.Load('libPhysicsAnpData')
    ROOT.gSystem.Load('libPhysicsAnpDataDict')
    ROOT.gSystem.Load('libPhysicsAnpBase')
    ROOT.gSystem.Load('libPhysicsAnpBaseDict')
    ROOT.gSystem.Load('libPhysicsAnpWH')

    #
    # Hack to force ROOT to load dictionary classes now
    #
    load_physics_wh_libs = ROOT.Anp.ReadNtuple()

#========================================================================================================
def prepareReadNtuple(ROOT, options, tree, hist_config=None):
    
    ROOT.gROOT.SetBatch(True)

    run = physicsBase.ReadNtuple('readNtuple')
    run.SetKey('TreeName',       tree)
    run.SetKey('PrintFiles',     'no')
    run.SetKey('NPrint',         options.nprint)
    run.SetKey('NEvent',         options.nevent)
    run.SetKey('Debug',          options.debug_run or options.debug_all)
    run.SetKey('FileKeys',       '.root')
    run.SetKey('CloseFile',      'yes')
    run.SetKey('Print',          'yes')
    run.SetPar('HistMan::Debug', 'no')
    run.SetPar('HistMan::Sumw2', 'yes')
    
    if options.output:
        run.SetKey('OutputFile', options.output)
        
    #
    # Read histogram definitions
    #
    histman  = ROOT.Anp.HistMan.Instance()
    histdirs = []
    
    testArea = os.environ.get('TestArea')

    if type(hist_config) == type([]):
        for hconfig in hist_config:
            if os.path.isdir(hconfig):
                histdirs += [hconfig]
                continue

            histPath = '%s/%s/' %(testArea, hconfig.rstrip('/'))
            
            if os.path.isdir(histPath):
                histdirs += [histPath]
            else:
                clog.warning('prepareReadNtuple - invalid path: %s' %histPath)

    for hdir in histdirs:
        clog.info('prepareReadNtuple - read xml files from: %s' %hdir)                
        for f in os.listdir(hdir):
            if f.count('.xml'):
                histman.ReadFile('%s/%s' %(hdir.rstrip('/'), f))

    return run


#========================================================================================================
# Load necessary shared libraries
#
def setPlotDefaults(root, options = None):

    root.gROOT.SetStyle('Plain')

    root.gStyle.SetFillColor(10)           
    root.gStyle.SetFrameFillColor(10)      
    root.gStyle.SetCanvasColor(10)         
    root.gStyle.SetPadColor(10)            
    root.gStyle.SetTitleFillColor(0)       
    root.gStyle.SetStatColor(10)   
    
    root.gStyle.SetCanvasBorderMode(0)
    root.gStyle.SetFrameBorderMode(0) 
    root.gStyle.SetPadBorderMode(0)   
    root.gStyle.SetDrawBorder(0)      
    root.gStyle.SetTitleBorderSize(0)
    
    root.gStyle.SetFuncWidth(2)
    root.gStyle.SetHistLineWidth(2)
    root.gStyle.SetFuncColor(2)
    
    root.gStyle.SetPadTopMargin(0.08)
    root.gStyle.SetPadBottomMargin(0.16)
    root.gStyle.SetPadLeftMargin(0.14)
    #root.gStyle.SetPadRightMargin(0.08)
    root.gStyle.SetPadRightMargin(0.12)
  
    # set axis ticks on top and right
    root.gStyle.SetPadTickX(1)         
    root.gStyle.SetPadTickY(1)         
  
    # Set the background color to white
    root.gStyle.SetFillColor(10)           
    root.gStyle.SetFrameFillColor(10)      
    root.gStyle.SetCanvasColor(10)         
    root.gStyle.SetPadColor(10)            
    root.gStyle.SetTitleFillColor(0)       
    root.gStyle.SetStatColor(10)           
  
  
    # Turn off all borders
    root.gStyle.SetCanvasBorderMode(0)
    root.gStyle.SetFrameBorderMode(0) 
    root.gStyle.SetPadBorderMode(0)   
    root.gStyle.SetDrawBorder(0)      
    root.gStyle.SetTitleBorderSize(0) 
  
    # Set the size of the default canvas
    root.gStyle.SetCanvasDefH(400)          
    root.gStyle.SetCanvasDefW(650)          
    #gStyle->SetCanvasDefX(10)
    #gStyle->SetCanvasDefY(10)   
  
    # Set fonts
    font = 42
    root.gStyle.SetLabelFont(font,'xyz')
    root.gStyle.SetStatFont(font)       
    root.gStyle.SetTitleFont(font)      
    root.gStyle.SetTitleFont(font,'xyz')
    root.gStyle.SetTextFont(font)       
    root.gStyle.SetTitleX(0.3)        
    root.gStyle.SetTitleW(0.4)        
  
   # Set Line Widths
   #gStyle->SetFrameLineWidth(0)
    root.gStyle.SetFuncWidth(2)
    root.gStyle.SetHistLineWidth(2)
    root.gStyle.SetFuncColor(2)
  
   # Set tick marks and turn off grids
    root.gStyle.SetNdivisions(505,'xyz')
  
   # Set Data/Stat/... and other options
    root.gStyle.SetOptDate(0)
    root.gStyle.SetDateX(0.1)
    root.gStyle.SetDateY(0.1)
   #gStyle->SetOptFile(0)
    #root.gStyle.SetOptStat(1110)
    root.gStyle.SetOptStat('reimo')
    root.gStyle.SetOptFit(111)
    root.gStyle.SetStatFormat('6.3f')
    root.gStyle.SetFitFormat('6.3f')
    root.gStyle.SetPaintTextFormat('0.2f')

   #gStyle->SetStatTextColor(1)
   #gStyle->SetStatColor(1)
   #gStyle->SetOptFit(1)
   #gStyle->SetStatH(0.20)
   #gStyle->SetStatStyle(0)
   #gStyle->SetStatW(0.30)
   #gStyle -SetStatLineColor(0)
    root.gStyle.SetStatX(0.919)
    root.gStyle.SetStatY(0.919)
    root.gStyle.SetOptTitle(0)
   #gStyle->SetStatStyle(0000)    # transparent mode of Stats PaveLabel
    root.gStyle.SetStatBorderSize(0)

    root.gStyle.SetLabelSize(0.065,'xyz')
   #gStyle -> SetLabelOffset(0.005,'xyz')
   #gStyle -> SetTitleY(.98)
    root.gStyle.SetTitleOffset(1.05,'xz')
    root.gStyle.SetTitleOffset(1.20,'y')
    root.gStyle.SetTitleSize(0.075, 'xyz')
    root.gStyle.SetLabelSize(0.075, 'xyz')
    #root.gStyle.SetTextAlign(22)
    root.gStyle.SetTextSize(0.12)
    
    #root.gStyle.SetPaperSize(root.TStyle.kA4)  
    root.gStyle.SetPalette(1)
  
   #root.gStyle.SetHistMinimumZero(True)
    root.TGaxis.SetExponentOffset(0.03, -0.055, 'x')

    root.gROOT.ForceStyle()

#========================================================================================================
canvases = {}

def getCanvas(name, x, y, ny=None):

    import ROOT

    global canvases

    if name in canvases:
        c = canvases[name]
        c.cd()
        c.Draw() 
        return c

    c = ROOT.TCanvas(name, name, x, y)
    
    if ny:
        c.Divide(1, ny, 0.01, 0.01, 0)

    c.cd()
    c.Draw()           

    canvases[name] = c
    return c

#========================================================================================================
def getCutValue(cuts, name, default):

    if type(cuts) != dict:
        return default

    try:
        return cuts[name]
    except KeyError:
        return default   

#========================================================================================================
def getRunChain(name, algs=None, cuts=None, options=None):
    
    alg = physicsBase.AlgConfig(name, 'RunChain')

    if type(cuts) == type([]):
        physicsBase.addCuts(alg, 'CutCand', cuts)
    
    if type(algs) == type([]) and len(algs):
        alg.AddAlg(algs)

    if options != None and cuts != None and options.print_cuts:
        clog.info('----------------------------------------')
        clog.info('Print candidate cuts for %s:' %name)
        raise Exception('getRunChain - this code is not yet implemented')

    return alg
