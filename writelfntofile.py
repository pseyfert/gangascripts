def write_lfn_to_txt(jobidlist):
    with open(jobs(jobidlist[0]).name + ".txt","w") as f:
        for jid in jobsidlist:
            j = jobs(jid)
            for sj in j.subjobs:
                for of in sj.outputfiles:
                    if of.namePattern == 'summary.xml':
                        continue
                    try:
                        of.lfn
                    except AttributeError:
                        pass
                    else:
                        f.write(of.lfn)
                        f.write("\n")
    # draft
    #import subprocess
    #subprocess.call("dirac-dms-lfn-accessURL "+jobs(jobidlist[0]).name +'.txt CERN-USER | grep eoslhcb | sed "s/ *$//" | sed "s/.* //"[ >> '+jobs(jobidlist[0]).name +'.replace '


