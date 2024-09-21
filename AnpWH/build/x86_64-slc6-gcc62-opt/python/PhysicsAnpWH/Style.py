import os
import sys
import re

import PhysicsAnpBase.PhysicsAnpBaseConfig as physicsBase
import PhysicsAnpWH  .Config               as config
import PhysicsAnpWH  .XSec                 as XSec

from PhysicsAnpWH.XSec import MCSample
from PhysicsAnpWH.XSec import mergeSamples as merge

clog = physicsBase.getLog(os.path.basename(__file__))

#-------------------------------------------------------------------------
def setSampleStyle(sample):

    import ROOT

    color_ttbar = 632
    color_tth   = ROOT.kBlack
    color_ttz   = 799
    color_ttw   = 400  
    color_data  = ROOT.kBlack
    color_rare  = 920
    color_vv    = 410
    color_ww    = 420
    color_zz    = 430
    color_zjet  = 862
    color_wjet  = 419
    color_zgamma = 802
    color_wgamma = 822
    color_vvv   = 842

    styles = [
        (['ttbar', 'top', 'ttbar_top'],
        {'SetLineColor':ROOT.kBlack, 'SetLineWidth':0, 'SetFillStyle':1001, 'SetFillColor':color_ttbar, 'SetMarkerStyle': 0, 'SetLineWidth': 1}),
        (['tops_pp8'],
        {'SetLineColor':ROOT.kBlack, 'SetLineWidth':0, 'SetFillStyle':1001, 'SetFillColor':430, 'SetMarkerStyle': 0, 'SetLineWidth': 1}),
        
        (['tth','tth_p8','wh'],
        {'SetLineColor':color_tth,  'SetLineWidth':3}),

        (['ttz', 'ttz_nlo', 'ttV'],
        {'SetLineColor':ROOT.kBlack,  'SetLineWidth':0, 'SetFillStyle':1001, 'SetFillColor':color_ttz, 'SetLineWidth':1}),

        (['ttw', 'ttw_nlo'],
        {'SetLineColor':ROOT.kBlack,  'SetLineWidth':0, 'SetFillStyle':1001, 'SetFillColor':color_ttw, 'SetLineWidth':1}),        

        (['data'],
        {'SetLineWidth':0, 'SetMarkerStyle': 20, 'SetMarkerColor':1}),

        (['rare'],
        {'SetLineColor':ROOT.kBlack, 'SetFillStyle':1001, 'SetFillColor':color_rare, 'SetMarkerStyle': 0, 'SetLineWidth':1}),

        (['vv','wz'],
        {'SetLineColor':ROOT.kBlack, 'SetLineWidth':2, 'SetFillStyle':1001, 'SetFillColor':color_vv, 'SetMarkerStyle': 0, 'SetLineWidth': 1}),
        (['ww'],
        {'SetLineColor':ROOT.kBlack, 'SetLineWidth':2, 'SetFillStyle':1001, 'SetFillColor':color_ww, 'SetMarkerStyle': 0, 'SetLineWidth': 1}),

        (['zz'],
        {'SetLineColor':ROOT.kBlack, 'SetLineWidth':2, 'SetFillStyle':1001, 'SetFillColor':color_zz, 'SetMarkerStyle': 0, 'SetLineWidth': 1}),

        (['zjets'],
        {'SetLineColor':ROOT.kBlack, 'SetFillStyle':1001, 'SetFillColor':color_zjet, 'SetMarkerStyle': 0, 'SetLineWidth':1}),

        (['wjets'],
        {'SetLineColor':ROOT.kBlack, 'SetFillStyle':1001, 'SetFillColor':color_wjet, 'SetMarkerStyle': 0, 'SetLineWidth':1}),

        (['zgamma'],
        {'SetLineColor':ROOT.kBlack, 'SetFillStyle':1001, 'SetFillColor':color_zgamma, 'SetMarkerStyle': 0, 'SetLineWidth':1}),

        (['wgamma'],
        {'SetLineColor':ROOT.kBlack, 'SetFillStyle':1001, 'SetFillColor':color_wgamma, 'SetMarkerStyle': 0, 'SetLineWidth':1}),

        (['vvv'],
        {'SetLineColor':ROOT.kBlack, 'SetFillStyle':1001, 'SetFillColor':color_vvv, 'SetMarkerStyle': 0, 'SetLineWidth':1}),
        ]

    nmatch = 0

    for entry in styles:
        keys  = entry[0]
        style = entry[1]        
        
        if sample.name in keys:
            setattr(sample, 'style_map', style)
            nmatch += 1

    if nmatch == 0:
        clog.warning('setSampleStyle - missing style for: %s' %sample.name)

    return sample

#--------------------------------------------------------------------
def getttHSamples(keys = None):

    samples = [
        MCSample(name='ttbar', title='ttbar PP8',
                  keys=['410501']),
        MCSample(name='ttbar_dilep', title='ttbar PP8 dilep',
                  keys=['410503']),
        MCSample(name='ttbar_dilep_pp8', title='ttbar pp8 dilep',
                  keys=['410503']),
        MCSample(name='ttbar_nonallhad', title='ttbar PP8 nonallhad',
                  keys=['410470']),

        MCSample(name='tth_dilep',   title='ttH dilep',
                 keys=['343365']),
        MCSample(name='tth_semilep', title='ttH semilep',
                 keys=['343366']),
        MCSample(name='tth_allhad',  title='ttH allhad',
                 keys=['343367']),

        MCSample(name='wh_dilep',  title='WH dilep',
                 keys=['341422','341424','341425','341428','341430','341432','341433','341436']),
        MCSample(name='wh_trilep', title='WH trilep',
                 keys=['345326','345327']),
        MCSample(name='wh_silep',  title='WH silep',
                 keys=['341426','341434']),

        MCSample(name='zh_pp8',  title='ZH',
                 keys=['345337','345446']),

        MCSample(name='wz_zerolep', title='WZ sherpa zerolep',
                 keys=['363357']),
        MCSample(name='wz_silep',  title='WZ sherpa silep',
                 keys=['363489']),
        MCSample(name='wz_dilep',  title='WZ sherpa dilep',
                 keys=['363358']),
        MCSample(name='wz_trilep', title='WZ sherpa trilep',
                 keys=['364253', '364289']),
        MCSample(name='wz_EW', title='WZ sherpa EW',
                 keys=['364284']),

        MCSample(name='ttw',       title='ttW',
                 keys=['410155']),
        MCSample(name='ttznn',     title='ttZnn',
                 keys=['410156']),
        MCSample(name='ttzqq',     title='ttZqq',
                 keys=['410157']),
        MCSample(name='ttzee',     title='ttZee',
                 keys=['410218']),
        MCSample(name='ttzmumu',   title='ttZmumu',
                 keys=['410219']),
        MCSample(name='ttztautau', title='ttZtautau',
                 keys=['410220']),

        MCSample(name='tchan',        title='t-channel',
                 keys=['410658-410659']),
        MCSample(name='wt_inclusive', title='Wt inclusive',
                 keys=['410648-410649 ']),
        MCSample(name='schan',        title='s-channel',
                 keys=['410644-410645']),

        MCSample(name='ttww',    title='ttWW',
                 keys=['410081']),
        MCSample(name='4topSM',  title='4top',
                 keys=['410080']),
        MCSample(name='tz',   title='tZ',
                 keys=['410550']),
        MCSample(name='triboson_sherpa',  title='Triboson',
                 keys=['364242-364249']),
        MCSample(name='vh',  title='VH',
                 keys=['342284-342285']),

        MCSample(name='diboson_sherpa',           title='Diboson',
                 keys=['361063-361073']),
        MCSample(name='ww_sherpa',           title='WW',
                 keys=['364254', '364290']),
        MCSample(name='zz_sherpa',           title='ZZ',
                 keys=['364250', '364283', '364288', '345705', '345706', '363356', '363355']),

        MCSample(name='diboson_sherpa_improved',  title='Diboson',
                 keys=['361091-361097']),
        MCSample(name='diboson_ggllvv',           title='Diboson',
                 keys=['361077']),

        MCSample(name='ttw_nlo',       title='ttW (NLO)',
                 keys=['410155']),

        MCSample(name='ttzqq_nlo',     title='ttZqq',
                 keys=['410157']),
        MCSample(name='ttzee_nlo',     title='ttZee',
                 keys=['410218']),
        MCSample(name='ttzmumu_nlo',   title='ttZmumu',
                 keys=['410219']),
        MCSample(name='ttztautau_nlo', title='ttZtautau',
                 keys=['410220']),

        MCSample(name='zee_sherpa',            title='Z#rightarrowee+jets (Sherpa)',
                 keys=['364114-364127']),
        MCSample(name='zmumu_sherpa',           title='Z#rightarrow#mu#mu+jets (Sherpa)',
                 keys=['364100-364113']),
        MCSample(name='ztautau_sherpa',        title='Z#rightarrow#tau#tau+jets (Sherpa)',
                 keys=['364128-364141']),
        MCSample(name='zee_sherpa_lowmll',       title='Z#rightarrowee+jets (Sherpa)',
                 keys=['364204-364209']),
        MCSample(name='zmumu_sherpa_lowmll',     title='Z#rightarrow#mu#mu+jets (Sherpa)',
                 keys=['364198-364203']),
        MCSample(name='ztautau_sherpa_lowmll',   title='Z#rightarrow#tau#tau+jets (Sherpa)',
                 keys=['364210-364215']),
        MCSample(name='zll2jets_sherpa',            title='Z#rightarrowll+2jets (Sherpa)',
                 keys=['308092-308094']),
       
        MCSample(name='zee_mgp8',            title='Z#rightarrowee+jets (MadGraph)',
                 keys=['363147-363170']),
        MCSample(name='zmumu_mgp8',           title='Z#rightarrow#mu#mu+jets (MadGraph)',
                 keys=['363123-363146']),
        MCSample(name='ztautau_mgp8',        title='Z#rightarrow#tau#tau+jets (MadGraph)',
                 keys=['361510-361514']),

        MCSample(name='zee_pp8',            title='Z#rightarrowee+jets (Powheg)',
                 keys=['361106']),
        MCSample(name='zmumu_pp8',           title='Z#rightarrow#mu#mu+jets (Powheg)',
                 keys=['361107']),
        MCSample(name='ztautau_pp8',        title='Z#rightarrow#tau#tau+jets (Powheg)',
                 keys=['361108']),

        MCSample(name='wjets_sherpa',       title='W+jets (Sherpa)',
                 keys=['364156-364197']),

        MCSample(name='wjets_powheg',       title='W+jets (Powheg)',
                 keys=['361100-361105']),

        MCSample(name='zgamma_sherpa',       title='Z+#gamma (Sherpa)',
                 keys=['364500-364514']),
        MCSample(name='wgamma_sherpa',       title='W+#gamma (Sherpa)',
                 keys=['364521-364535']),

        MCSample(name='tth_dilep_p8',   title='ttH dilep',
                 keys=['343365']),
        MCSample(name='tth_semilep_p8', title='ttH semilep',
                 keys=['343366']),
        MCSample(name='tth_allhad_p8',  title='ttH allhad',
                 keys=['343367']),
        ]

    merge_samples = [
        merge(MCSample(name='wh',       title='WH'),     samples, ['wh_trilep', 'wh_dilep', 'wh_silep']),
        merge(MCSample(name='zh',       title='ZH'),     samples, ['zh_pp8']),
        merge(MCSample(name='ttbar',    title='ttbar'),  samples, ['ttbar_nonallhad']),
        #merge(MCSample(name='zjets',    title='Sherpa Z+jets'), samples, ['zee_sherpa', 'zmumu_sherpa', 'ztautau_sherpa','zee_sherpa_lowmll', 'zmumu_sherpa_lowmll', 'ztautau_sherpa_lowmll', 'zll2jets_sherpa']),
        #merge(MCSample(name='zjets',    title='MG Z+jets'), samples, ['zee_mgp8', 'zmumu_mgp8', 'ztautau_mgp8','zll2jets_sherpa']),
        #merge(MCSample(name='zjets',    title='PP8 Z+jets'), samples, ['zee_pp8', 'zmumu_pp8', 'ztautau_pp8','zll2jets_sherpa']),
        merge(MCSample(name='zjets',    title='Sherpa Z+jets'), samples, ['zee_sherpa', 'zmumu_sherpa', 'ztautau_sherpa','zee_sherpa_lowmll', 'zmumu_sherpa_lowmll', 'ztautau_sherpa_lowmll']),
        #merge(MCSample(name='zjets',    title='MG Z+jets'), samples, ['zee_mgp8', 'zmumu_mgp8', 'ztautau_mgp8']),
        #merge(MCSample(name='zjets',    title='PP8 Z+jets'), samples, ['zee_pp8', 'zmumu_pp8', 'ztautau_pp8']),
        merge(MCSample(name='wz',       title='WZ'),     samples, ['wz_trilep','wz_dilep','wz_silep','wz_zerolep','wz_EW']),
        merge(MCSample(name='ww',       title='WW'),     samples, ['ww_sherpa']),
        merge(MCSample(name='zz',       title='ZZ'),     samples, ['zz_sherpa']),
        merge(MCSample(name='vvv',      title='VVV'),    samples, ['triboson_sherpa']),
        merge(MCSample(name='ttz',      title='ttZ'),    samples, ['ttzee','ttzmumu','ttztautau','ttzqq', 'ttznn']),    
        merge(MCSample(name='ttw',      title='ttW'),    samples, ['ttw']),
        merge(MCSample(name='tops_pp8', title='top+X'),  samples, ['tchan', 'wt_inclusive', 'schan', 'tz']),
        merge(MCSample(name='top',      title='top'),    samples, ['ttbar_nonallhad', 'ttzee','ttzmumu','ttztautau','ttzqq', 'ttznn', 'ttw', 'tchan', 'wt_inclusive', 'schan', 'tz']),    
        merge(MCSample(name='ttV',      title='ttZ+ttW'),    samples, ['ttzee','ttzmumu','ttztautau','ttw']),    
        merge(MCSample(name='ttbar_top', title='ttbar+topX'), samples, ['ttbar_nonallhad', 'tchan', 'wt_inclusive', 'schan', 'tz']),
        merge(MCSample(name='zgamma',    title='Z+#gamma'),   samples, ['zgamma_sherpa']),
        merge(MCSample(name='wjets',     title='W+jets'),     samples, ['wjets_powheg']),
        merge(MCSample(name='wgamma',    title='W+#gamma'),   samples, ['wgamma_sherpa']),

        merge(MCSample(name='tth',          title='ttH'),    samples, ['tth_dilep', 'tth_semilep', 'tth_allhad']),
        merge(MCSample(name='rare',         title='Rare'),         samples, ['ttww', '4topSM', 'tz', 'triboson_sherpa','vh']),
        merge(MCSample(name='vv',           title='VV'),           samples, ['diboson_sherpa','diboson_sherpa_improved','diboson_ggllvv']),
        merge(MCSample(name='ttw_nlo',      title='ttW'),          samples, ['ttw_nlo']),
        merge(MCSample(name='ttz_nlo',      title='ttZ'),          samples, ['ttzee_nlo','ttzmumu_nlo','ttztautau_nlo','ttzqq_nlo']),
        merge(MCSample(name='tth_p8',       title='ttH'),          samples, ['tth_dilep_p8',   'tth_semilep_p8',   'tth_allhad_p8']),
        merge(MCSample(name='tops_dilep_pp8',title='top+X'),       samples, ['ttbar_dilep_pp8','tchan', 'wt_inclusive', 'schan']),
        merge(MCSample(name='tops_other',   title='top+X'),        samples, ['ttbar_dilep_pp8']),
   	]
    
    for sample in samples + merge_samples:
      if sample.name in keys:
          setSampleStyle(sample)
    
    return XSec.filterSamples(samples + merge_samples, keys)
