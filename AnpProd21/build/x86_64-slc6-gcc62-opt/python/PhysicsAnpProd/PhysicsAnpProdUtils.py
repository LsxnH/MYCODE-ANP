
import os
import logging
import re
import sys

loggers = {}
    
#========================================================================================================
def getLog(name, level='INFO', debug=False, print_time=False):

    global loggers

    if name in loggers:
        return loggers[name]

    if print_time:
        f = logging.Formatter('%(asctime)s - %(name)s: %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    else:
        f = logging.Formatter('%(name)s: %(levelname)s - %(message)s')
        
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(f)
    
    log = logging.getLogger(name)
    log.addHandler(h)
    
    if debug:
        log.setLevel(logging.DEBUG)
    else:
        if level == 'DEBUG':   log.setLevel(logging.DEBUG)
        if level == 'INFO':    log.setLevel(logging.INFO)
        if level == 'WARNING': log.setLevel(logging.WARNING)    
        if level == 'ERROR':   log.setLevel(logging.ERROR)

    return log

#========================================================================================================
clog = getLog(os.path.basename(__file__))

#======================================================================================
def findInputFilesInDir(dpath):

    if not os.path.isdir(dpath):
        log.error('findInputFilesInDir - input path is not a directory: 5s' %dpath)
        return []
    
    files = []
    
    for f in os.listdir(dpath):
        fpath = '%s/%s' %(dpath.rstrip('/'), f)

        if os.path.isfile(fpath):
            files += [fpath]

    return files

#======================================================================================
def getItemFromInputSummary(inputFileSummary, key, position=None, default=''):

    try:
        values = inputFileSummary[key]
    except KeyError:
        return default

    if type(values) == type(''):
        return values

    if position != None and position < len(values):
        return values[position]

    return values


#======================================================================================
# Helper classes
#======================================================================================
class AlgData: 

    '''Analysis algorithm from PhysicsAnpPackage
       -- Athena algorithm instance
       -- Output vector name
       -- Output variable list    
    '''

    def __init__(self, athena_alg, out_vars=None):

        self.athena_alg = athena_alg
        self.out_vars   = {}
        self.top_vars   = []
    
        if out_vars and hasattr(athena_alg, 'outputVectorName'):
            self.AddBranchVars(getattr(athena_alg, 'outputVectorName'), out_vars)

    def AddBranchVars(self, branch, out_vars):
        
        try:
            self.out_vars[branch] += out_vars
        except KeyError:
            self.out_vars[branch]  = out_vars
 
        self.CheckOutVars()

    def AddEventVars(self, top_vars):
        self.top_vars = top_vars

    def GetEventVarsAsStr(self):
        return ','.join(self.top_vars).replace(' ', '')

    def GetAllBranchVarsAsList(self):
        out = []

        for branch, out_vars in self.out_vars.iteritems():
            out += ['%s|%s' %(branch, ','.join(out_vars).replace(' ', ''))]

        return out

    def CheckOutVars(self):

        for branch, out_vars in self.out_vars.iteritems():
            seen = set()

            for v in out_vars:
                if v not in seen:
                    seen.add(v)
                else:
                    raise Exception('AlgData::CheckOutVars - duplicate output variable: "%s"' %v)
        
