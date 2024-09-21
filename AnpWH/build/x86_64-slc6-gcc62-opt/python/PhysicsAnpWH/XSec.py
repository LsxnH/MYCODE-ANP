import os
import re
import sys
import time
import ROOT

import PhysicsAnpWH  .Config               as Config
import PhysicsAnpBase.PhysicsAnpBaseConfig as Base

clog = Base.getLog(os.path.basename(__file__))

#==================================================================================
class XSecData:
    """Data for MC run"""
        
    def __init__(self, line, ilumi=1.0):

        self.line  = line
        self.ilumi = ilumi
        self.match = False
        self.pdfw  = False
        
        parts = line.split()

        if len(parts) < 9:
            clog.error('XSecData - wrong input line: %s' %line)
            sys.exit(1)
            
        self.nevent    = 0.0
        self.ntotal    = 0.0            
        self.wevent    = 0.0
        self.run       = int  (parts[0])
        self.xsec      = float(parts[1])
        self.kfactor   = float(parts[2])
        self.feff      = float(parts[3])
        self.mass      = int  (parts[5])
        self.priority  = int  (parts[6])
        self.generator = parts[7]            
        self.process   = parts[8]
            
    def GetLine(self):
        return self.line

    def GetEventWeight(self):
        if self.wevent > 0.0:
            return self.GetEventExpect()/self.wevent
        return 0.0

    def GetEventExpect(self):
        return self.ilumi*self.xsec*self.GetScaleFactor()

    def GetEventPass(self, wpass):
        if self.wevent > 0.0:        
            return self.GetEventExpect()*wpass/self.wevent
        return 0.0

    def GetScaleFactor(self):
        return self.kfactor*self.feff

    def GetNEvent(self):
        return self.nevent

    def GetNTotal(self):
        return self.ntotal

    def Print(self):
        out  = 'run=%d '       %self.run
        out += 'xsec=%e '      %self.xsec
        out += 'kfactor=%e '   %self.kfactor
        out += 'feff=%e '      %self.feff
        out += 'nevent=%e '    %self.nevent
        out += 'weight=%e '    %self.GetEventWeight()
        out += 'expect=%e '    %self.GetEventExpect()
        out += '%s '           %self.priority
        out += '%s '           %self.process
        print out
    
    def AsTableRow(self):        
        out  = '%d '     %self.run
        out += '%e '     %self.GetEventWeight()
        out += '%e '     %self.wevent
        out += '%e '     %self.xsec
        out += '%e '     %self.GetScaleFactor()
        return out

    def GetTableHeader(self):         
        out  = 'Run '
        out += 'EventWeight '
        out += 'TotalWeight '
        out += 'CrossSection '
        out += 'ScaleFactor '
        return out
    
#==================================================================================
def readXSecFile(fpath, priority=1):
    
    if fpath == None or not os.path.isfile(fpath):
        clog.warning('readXSecFile - invalid path: %s' %fpath)
        return []
        
    xfile = open(fpath, 'r')

    xsecs = []
        
    for iline in xfile:
        line = iline.strip()
            
        if line.count('#') or len(line.split()) == 0:
            continue

        xsec = XSecData(line)

        if priority == None or priority == 0 or xsec.priority == priority:
            xsecs += [xsec]

    return xsecs

#==================================================================================
class InputFileCollection:
    '''Wrapper for TFile to handle lists and directories'''

    def __init__(self, files, search_key='.*root'):
        self.file_list  = []
        self.search_key = search_key
        self.list_of_keys = []
        self.cache = {}

        if isinstance(files, list):
            for f in files:
                if os.path.isdir(f):
                    for subf in os.listdir(f):                        
                        self.AddFile('%s/%s' %(f.rstrip('/'), subf))
                else:
                    self.AddFile(f)
                        
        elif isinstance(files, str):
            self.AddFiles(files)
        else:
            raise Exception('InputFileCollection - invalid data: %s' %files)
        for f in self.file_list:
            ROOT.gROOT.GetListOfFiles().Remove(f)

    def __del__(self):
        
        clog.info('%s - InputFileCollection - enter destructor' %(time.asctime(time.localtime())))

        for f in self.file_list:
            ROOT.gROOT.GetListOfFiles().Remove(f)
            f.Close()

        clog.info('%s - InputFileCollection - exit destructor' %(time.asctime(time.localtime())))

    def AddFile(self, path):

        if os.path.isfile(path):
            if re.search(self.search_key, path):
                clog.info('InputFileCollection - add file: %s' %path)
                self.file_list += [ ROOT.TFile(path, 'READ') ]
        elif path.count('eos'):
            self.file_list += [ ROOT.TFile.Open(path, 'READ') ]
        else:
            raise Exception('AddFile - invalid file: %s' %path)

    def HistogramFileCache(self,path):
        dsid = path.split('/')[0]
       
        if (len(dsid) == 6 or dsid == 'data') and not dsid == 'Counts':
            if dsid in self.cache:
                return self.cache[dsid]
            files_containing = [f for f in self.file_list if f.Get(dsid)]
            self.cache[dsid] = files_containing
            return files_containing
        else:
            return self.file_list
        
        
    def Get(self, path):
        out_histo = None

        for f in self.HistogramFileCache(path):
        #for f in self.file_list:
            current_obj = f.Get(path)
            if current_obj:
                if current_obj.InheritsFrom('TH1'):
                    if not out_histo:
                        out_histo = current_obj
                    else:
                        out_histo.Add(current_obj)
                else:
                    return current_obj

        return out_histo

    def GetListOfKeys(self):
        if len(self.list_of_keys):
            return self.list_of_keys

        #implicit else
        ListOfKeys = []
        #get the list of keys for all files
        for f in self.file_list:
            ListOfKeys += [key for key in f.GetListOfKeys()]

        #make the list of keys unique by the name of the TKey object
        UniqueNames = set()
        SetOfKeys = set()
        for k in ListOfKeys:
            if k.GetName() not in UniqueNames:
                UniqueNames.add(k.GetName())
                SetOfKeys.add(k)
        self.list_of_keys = list(SetOfKeys)
        return self.list_of_keys

#==================================================================================
class XSecMan:
    '''Manager for xsec normalization'''
        
    def __init__(self, xsec_list, hfile, ilumi, priority=0, pdf_samples=None, debug=False, dirname='prepReco', norm_count_bin=2, extra_config_path=None):

        self.bin_norm  = norm_count_bin
        self.bin_total = 2
        self.bin_pdf   = 21
        self.priority  = priority
        self.ilumi     = ilumi        
        self.debug     = debug
        self.dirname   = dirname
        self.xsecs     = self.getXSecs(xsec_list, hfile, pdf_samples, extra_config_path)

    def __del__(self):
        clog.info('%s - XSecMan - enter destructor' %(time.asctime(time.localtime())))

    def getXSecs(self, xsec_list, hfile, pdf_samples, extra_config_path):
        if not xsec_list:
            clog.error('Missing xsec file parameter')
            sys.exit(1)

        if not hfile:
            clog.error('Missing xsec file parameter')
            sys.exit(1)

        if not os.path.isfile(xsec_list):
            clog.error('Invalid xsec file: %s' %xsec_list)
            sys.exit(1)
            
        xfile        = open(xsec_list, 'r')
        xsec_dict    = {}
        extra_counts = self.readExtraCounts(extra_config_path)

        for xline in xfile.readlines():
            xpath = xline.replace('$TestArea', os.getenv('TestArea', '')).strip()

            if not os.path.isfile(xpath):
                clog.warning('Missing xsec file: %s' %xpath)
                continue
            
            clog.info('Read xsec file: %s' %xpath)            
            xsec_list = readXSecFile(xpath, self.priority)

            for xsec in xsec_list:
                if xsec.run in xsec_dict:
                    clog.warning('Skip duplicate dataset id=%d (keep first value)' %xsec.run)
                else:
                    xsec_dict[xsec.run] = xsec        

        for xsec in xsec_dict.itervalues():
            xsec.ilumi = self.ilumi

            is_pdf = False

            if pdf_samples:
                for pdf in pdf_samples:
                    for pdf_run in pdf.GetRuns():
                        if xsec.run == pdf_run:
                            is_pdf = True
                            break

            if is_pdf:
                clog.info('XSecMan - PDF weight for: %d  %s  %s' %(xsec.run, xsec.generator, xsec.process))
            
            count_path = '%s/%s/nominal_Count' %(self.dirname, xsec.run)
            event_path = '%s/%s/event' %(self.dirname, xsec.run)

            count_hist = hfile.Get(count_path)
            event_hist = hfile.Get(event_path)
            
            if count_hist:
                xsec.ntotal = count_hist.GetBinContent(self.bin_total)

                if is_pdf:
                    xsec.wevent = count_hist.GetBinContent(self.bin_pdf)
                else:
                    xsec.wevent = count_hist.GetBinContent(self.bin_norm)
            elif event_hist:
                xsec.ntotal = event_hist.GetBinContent(1)
                xsec.nevent = event_hist.GetBinContent(1)
                xsec.wevent = event_hist.GetBinContent(2)
            else:
                clog.debug('Missing "Count" histogram %s: %s' %(event_path, xsec.process))
                clog.debug('Missing "event" histogram %s: %s' %(count_path, xsec.process))

            if xsec.run in extra_counts:
                xsec.ntotal = extra_counts[xsec.run][0]
                xsec.wevent = extra_counts[xsec.run][1]

                clog.info('getXSecs - override counts for %d: %s' %(xsec.run, extra_counts[xsec.run]))

        return xsec_dict

    def readExtraCounts(self, config_path):
        results = {}

        if config_path == None or not os.path.isfile(config_path):
            return results

        cfile = open(config_path, 'r')

        for line in cfile.readlines():
            cline = line.rstrip('\n')
            
            if cline.count('Counts') == 0:
                continue

            parts = cline.partition(':')[2].split()
            
            if len(parts) == 3:
                results[int(parts[0])] = (float(parts[1]), float(parts[2]))

                clog.info('ReadExtraCounts - update counts: %s' %parts)

        return results

    def GetEventExpect(self, run):
        xsec = self.GetXSec(run)
        if xsec:
            return xsec.GetEventExpect()
        return 0.0

    def GetEventPass(self, run, wpass):
        xsec = self.GetXSec(run)
        if xsec:
            return xsec.GetEventPass(wpass)
        return 0.0

    def GetXSec(self, run):
        if type(run) != int:
            clog.warning('GetXSec - need int type run="%s"' %run)
            raise KeyError
            return None
        
        try:
            return self.xsecs[run]
        except:
            if self.debug:
                clog.warning('XSecMan - bad run: %s' %run)
            
        return None      

    def PrintXSecs(self, print_all=False):

        if not self.xsecs or not self.ilumi:
            clog.warning('No valid cross-section entries')
            return

        for xkey in sorted(self.xsecs.keys()):
            xsec = self.xsecs[xkey]
            
            if print_all or xsec.wevent > 0.0:
                xsec.Print()
        
        for xkey in sorted(self.xsecs.keys()):
            xsec = self.xsecs[xkey]
            
            if xsec.mass > 0:
                mass = '%d' %xsec.mass
            else:
                mass = ''
                
            nraw = '{0:13.2f}'.format(xsec.wevent)
            nsum = '{0:13.2f}'.format(xsec.wevent)            
            nexp = '{0:13.2f}'.format(self.GetEventExpect(xsec.run))
            
            if print_all or xsec.wevent > 0.0:
                clog.info('XSec %s Nexp=%s  Nsum=%s  %s %s' %(xsec.run, nexp, nsum, xsec.process, mass))

    def SetCountBinTotal(self, bin):
        self.bin_total = bin
                
#==================================================================================
class MCSample:
    '''MCSample - list of MC channels per MC sample, plus additional plotting info'''
        
    def __init__(self, **kwargs):

        self.name       = None
        self.title      = None
        self.latex      = None                
        self.color      = None
        self.fill_style = None
        
        self._scalef    = 1.0
        self.keys       = []
        self.debug      = False

        for k, v in kwargs.iteritems():
            setattr(self, k.lower(), v)
                                
        self.runs = self.MakeRuns(self.keys)

    def MakeRuns(self, keys):

        runs = []

        for key in keys:
            if type(key) == int:
                runs += [(key, '%d' %key)]
            elif type(key) == type(''):
                if key.count('-'):
                    rparts = key.partition('-')
                    for r in range(int(rparts[0]), int(rparts[2])+1):
                        runs += [(int(r), '%d' %r)]
                else:
                    if len(key) == 6:
                        if key.isdigit():
                            runs += [(int(key), key)]
                        else:
                            clog.warning('MCSample - error 1: failed to process key="%s"' %key)
                            
                    elif key.count('_') == 1:
                        rparts = key.partition('_')
                            
                        if len(rparts[0]) == 6 and rparts[0].isdigit():
                                runs += [(int(rparts[0]), key)]
                        else:
                            clog.warning('MCSample - error 2: failed to process key="%s"' %key)
                    else:
                        clog.warning('MCSample - error 3: failed to process key="%s"' %key)


        return sorted(list(set(runs)))

    def PrintSample(self):
        clog.info('MCSample - %s: print %d run(s)' %(self.name, len(self.runs)))        
        for run in self.runs:
            clog.info('   %s' %str(run))

    def SetScaleFactor(self, value):
        self._scalef = value

    def GetScaleFactor(self):
        return self._scalef

    def GetLatex(self):
        if self.latex:
            return self.latex
        return self.title

    def AddRuns(self, runs):
        self.runs += runs

    def GetRuns(self):
        runs = []
        
        for r in self.runs:
            runs += [r[0]]
            
        return runs

    def UpdateHistStyle(self, hist):
        hist.SetDirectory(0)
        
        if not hasattr(self, 'style_map'):
            return

        for key, val in self.style_map.iteritems():

            if not hasattr(hist, key):
                clog.warning('UpdateHistStyle - invalid hist function: %s' %key)
                continue

            if val:
                func = getattr(hist, key)
                func(val)
        
#==================================================================================
class SampleMan:
    '''Manager for summing sample histograms'''
        
    def __init__(self, samples, xman, debug=False, no_weight=False):

        self.samples   = samples
        self.debug     = debug
        self.xman      = xman
        self.no_weight = no_weight
        self.misshists = set()
        self.missxsecs = set()

    def __del__(self):
        clog.info('%s - SampleMan - enter destructor' %(time.asctime(time.localtime())))

    def PrintLatex(self, keys=None):
        #
        # Print latex table
        #
        text  = '\\resizebox{1.0\\textwidth}{!}{\n'
        text += '\\begin{tabular}{|l|r|l|}\n'        
        text += '\\hline\n'
        text += ' & $\\sigma [\\text{pb}]$ & \\\\\n'
        text += '\\hline\n'
        
        for sample in self.samples:
            
            if not keys:
                match = True
            else:
                match = False

                for key in keys:
                    if type(key) == str and key == sample.name:
                        match = True
                    elif getattr(key, 'name', None) == sample.name:
                        match = True

            if not match:
                continue
            
            row = '%-20s & & ' %sample.GetLatex()

            for run in sample.GetRuns():
                row += ' %s' %run

            text += row + '\\\\\n'
            
        text += '\\hline\n'
        text += '\\end{tabular}}\n'

        return text

    def PrintSamples(self):
        clog.info('SampleMan - print %d sample(s)' %len(self.samples))

        for sample in self.samples:
            kvalue = ''

            for r in sorted(sample.GetRuns()):
                kvalue += '%s, ' %r
            
            print '   %-10s: %s' %(sample.name, kvalue)

    def GetLatexTable(self):
        text  = '\\resizebox{1.0\\textwidth}{!}{\n'
        text += '\\begin{tabular}{|l|p{10cm}|}\n'
        text += '\\hline\n'

        for sample in self.samples:
            text += '%s & ' %sample.GetLatex()

            for r in sorted(sample.GetRuns()):
                x = self.xman.GetXSec(r)
                
                if x and x.GetNTotal() > 0:
                    text += '\\textcolor{blue}{%s} ' %r
                else:
                    text += '\\textcolor{red}{%s} ' %r
            
            text += '\\\\\n'
            text += '\\hline\n'

        text += '\\end{tabular}}\n'

        return text

    def GetLatexTableMiss(self):
        text  = '\\resizebox{1.0\\textwidth}{!}{\n'
        text += '\\begin{tabular}{|l|r|r|}\n'
        text += '\\hline\n'

        for sample in self.samples:
            for r in sorted(sample.GetRuns()):
                x = self.xman.GetXSec(r)
                
                if x and x.GetNTotal() > 0:
                    continue

                text += '\\textcolor{red}{%s} ' %r

                if x:
                    text += ' & %s & $%s$ \\\\\n' %(x.generator, x.process)
                else:
                    text += ' & &\\\\\n'

        text += '\\hline\n'
        text += '\\end{tabular}}\n'

        return text

    def GetSample(self, key):
        for s in self.samples:
            if s.name == key:
                return s

        return None

    def GetSampleRuns(self, samples):
        runs = []

        for sample in samples:
            s = self.GetSample(sample)

            if s:
                runs += s.GetRuns()

        return runs
        
    def GetHist(self, hfile, hpath, key):
        if not self.xman:
            clog.warning('SampleMan - missing XSecMan')
            return None            

        sample = self.GetSample(key)
        
        if sample == None:
            clog.warning('SampleMan - unknown sample: %s' %key)
            return None

        hist = None

        for val in sample.runs:
            run  = val[0]
            key  = val[1]
            xsec = self.xman.GetXSec(run)

            npath = '%s/%s' %(key, hpath)
            hnext = hfile.Get(npath)
            
            if not xsec:
                if sample.name not in self.missxsecs:
                    clog.warning('SampleMan - missing xsec: %s %s' %(npath, sample.name))
                    self.missxsecs.add(sample.name)
                continue

            if not hnext:
                if run not in self.misshists:
                    clog.debug('SampleMan - missing histogram: %s  %-10s  %s' %(npath, sample.name, xsec.process))
                    self.misshists.add(run)
                continue

            hint = hnext.Integral()
            hexp = self.xman.GetEventPass(run, hint)*sample.GetScaleFactor()

            if hexp > 0.0 and not self.no_weight: 
                hnext.Scale(hexp/hint)         

                sint = '{0:13.2f}'.format(hint)
                sexp = '{0:13.2f}'.format(hexp)

                clog.debug('SampleMan - %s: hint=%s hexp=%s  %-10s  %s' %(npath, sint, sexp, sample.name, xsec.process))
            
            if hist == None:
                hist = hnext.Clone()
                hist.SetDirectory(0)
                sample.UpdateHistStyle(hist)
                
            else:
                hist.Add(hnext)

            hnext.SetDirectory(0)
            del hnext

        return hist

    def GetSampleRunHists(self, hfile, hpath, key):
        if not self.xman:
            raise Exception('SampleMan::GetSampleRunHists - missing XSecMan')
            return None            

        sample = self.GetSample(key)
        
        if sample == None:
            raise Exception('SampleMan - unknown sample: %s' %key)

        hists = {}

        for val in sample.runs:
            run  = val[0]
            key  = val[1]
            xsec = self.xman.GetXSec(run)

            npath = '%s/%s' %(key, hpath)
            hnext = hfile.Get(npath)
            
            if not xsec:
                if sample.name not in self.missxsecs:
                    clog.warning('SampleMan::GetSampleRunHists - missing xsec: %s %s' %(npath, sample.name))
                    self.missxsecs.add(sample.name)
                continue

            if not hnext:
                if run not in self.misshists:
                    clog.warning('SampleMan::GetSampleRunHists - missing histogram: %s  %-10s  %s' %(npath, sample.name, xsec.process))
                    self.misshists.add(run)
                continue

            hint = hnext.Integral()
            hexp = self.xman.GetEventPass(run, hint)*sample.GetScaleFactor()

            if hexp > 0.0 and not self.no_weight: 
                hnext.Scale(hexp/hint)         

            hnext.SetDirectory(0)            
            hists[run] = hnext
            
        return hists

    def GetData(self, hfile, hpath):
        
        path = 'data/%s' %(hpath)
        hist = hfile.Get(path)
            
        if not hist:
            clog.warning('SampleMan - missing data histogram: %s' %path)
            return None

        hist = hist.Clone()
        hist.SetDirectory(0)

        hist.SetLineWidth  (0)
        hist.SetMarkerStyle(20)
        hist.SetMarkerColor(1)        

        return hist

    def GetCutFlow(self, hfile, hpath, key):
        if not self.xman:
            clog.warning('SampleMan - missing XSecMan')
            return None

        sample = self.GetSample(key)
        
        if sample == None:
            clog.warning('GetCutFlow - unknown sample: %s' %key)
            return None

        hist = None

        for val in sample.runs:
            run  = val[0]
            key  = val[1]
            xsec = self.xman.GetXSec(run)

            if not xsec:
                if sample.name not in self.missxsecs:
                    clog.warning('SampleMan - missing xsec %s: %s' %(val, sample.name))
                    self.missxsecs.add(sample.name)
                continue

            npath = '%s/%s' %(key, hpath)
            hnext = hfile.Get(npath)            
            
            if not hnext:
                if key not in self.misshists:
                    clog.warning('SampleMan - missing histogram: %s  %-10s  %s' %(npath, sample.name, xsec.process))
                    self.misshists.add(key)
                continue

            if not self.no_weight:
                for ibin in range(1, hnext.GetNbinsX()+1):

                    hint = hnext.GetBinContent(ibin)
                    hexp = self.xman.GetEventPass(run, hint)*sample.GetScaleFactor()

                    if hexp > 0.0:                
                        hnext.SetBinContent(ibin, hexp)
                        hnext.SetBinError  (ibin, hnext.GetBinError(ibin)*hexp/hint)

                    if self.debug:
                        sint = '{0:13.2f}'.format(hint)
                        sexp = '{0:13.2f}'.format(hexp)

                        clog.debug('SampleMan - %s: %d hint=%s hexp=%s  %-10s  %s' %(npath, run, sint, sexp, sample.name, xsec.process))
            
            if hist == None:
                hist = hnext.Clone()
                hist.SetDirectory(0)
            else:
                hist.Add(hnext)

            hnext.SetDirectory(0)
            del hnext
                
        if hist:
            hist.SetDirectory(0)

        return hist
    
#==================================================================================
def mergeSamples(sample, samples, keys):

    if keys == None:
        slist = samples
    else:
        slist = [s for s in samples if s.name in keys]
        
        if len(slist) != len(keys):
            clog.warning('mergeSamples - missing %d key(s):' %(len(keys) - len(slist)))
            
            for k in keys:
                m = False
                for s in slist:
                    if s.name == k:
                        m = True

                if not m:
                    clog.warning('   %s' %k)

    for s in slist:
        sample.AddRuns(s.runs)

    return sample

#==================================================================================
def filterSamples(samples, keys):

    if keys == None:
        return samples

    out = []

    for key in keys:
        match = None

        for sample in samples:
            if key == sample.name:
                match = sample
        
        if match:
            out += [match]
        if not match:
            raise RuntimeError('Sample %s not defined.'%key)

    return out
