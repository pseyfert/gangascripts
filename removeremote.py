def removeLFNs_subjobs(job,sublist):
    ds = LHCbDataset()
    if type(job.backend)==Dirac:
        for sjid in sublist:
            sj = job.subjobs(sjid)
            if sj.status == 'completed':
                 for of in sj.outputfiles:
                     try:
                          the_lfn = of.lfn
                     except AttributeError:
                          pass
                     else:
                          ds.extend(of)
        for lfn in ds:
            lfn.remove()
def removeLFNs(job):
    ds = LHCbDataset()
    if type(job.backend)==Dirac:
        for sj in job.subjobs:
            if sj.status == 'completed':
                 for of in sj.outputfiles:
                     try:
                          the_lfn = of.lfn
                          if the_lfn=="":
                               raise AttributeError
                     except AttributeError:
                          pass
                     else:
                          ds.extend(of)
        for lfn in ds:
            lfn.remove()

def removeJobAndData(job):
    removeLFNs(job)
    job.remove()

def move_lfn_to_eos(diracfile):
    '''
    returns None if the only replicate is at cern, the lfn (as string) otherwise
    '''
    reps = diracfile.getReplicas()
    if 'CERN-USER' not in reps[0].keys():
        retval = diracfile.replicate('CERN-USER')
        try:
             isOkay = retval['OK']
        except:
             isOkay = True
    reps = diracfile.getReplicas()
    if 'CERN-USER' in reps[0].keys():
       for key in reps[0].keys():
          if key != 'CERN-USER':
              # file is not only at CERN-USER, needs cleaning
              return "cleanme"
       return "onlycern"
    return "notcern"

def move_job_to_eos(job):
    ds = LHCbDataset()
    if type(job.backend)==Dirac:
        for sj in job.subjobs:
            if sj.status == 'completed':
                for of in sj.outputfiles:
                    try:
                        print "fixing ", of.lfn
                    except AttributeError:
                        pass
                    else:
                        ds.extend(of)
        files_which_need_cleaning = []
        failures = []
        for fileobject in ds:
            retval = move_lfn_to_eos(fileobject)
            if retval == "cleanme":
                files_which_need_cleaning.append(fileobject.lfn)
            if retval == "notcern":
                failures.append(fileobject.lfn)
        if 0!=len(files_which_need_cleaning):
            import subprocess
            import os
            homedir = os.environ['HOME']
            subprocess.call(["lb-run","LHCbDirac","prod","python",homedir+"/gangascripts/clean_replicas.py"]+files_which_need_cleaning)
        if 0!=len(failures):
            print "SOME FILES DIDN'T REACH CERN"

