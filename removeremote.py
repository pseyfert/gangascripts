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
  diracfile.replicate('CERN-USER')
  reps = diracfile.getReplicas()
  if 'CERN-USER' in reps[0].keys():
     for key in reps[0].keys():
        if key != 'CERN-USER':
            return diracfile.lfn
  return None

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
        for fileobject in ds:
            retval = move_lfn_to_eos(fileobject)
            if retval is not None:
                files_which_need_cleaning.append(retval)
        if 0!=len(files_which_need_cleaning):
            import subprocess
            subprocess.call(["lb-run","LHCbDirac","v8r2p41","python","/afs/cern.ch/user/p/pseyfert/gangascripts/clean_replicas.py"]+files_which_need_cleaning)
