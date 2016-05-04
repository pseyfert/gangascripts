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

def move_lfn_to_eos(lfn):
  lfn.replicate('CERN-USER')
  reps = lfn.getReplicas()
  if 'CERN-USER' in reps[0].keys():
     for key in reps[0].keys():
        if key != 'CERN-USER':
            print "there is still a replica at ",key
            print "removal atm not implemented"

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
        for lfn in ds:
            move_lfn_to_eos(lfn)
