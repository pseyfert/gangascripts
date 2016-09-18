def write_lfn_to_txt(jobidlist,targetdir = "."):
    """write lfns of a job to text file "jobname.jobid.lfn.txt"

    Keyword arguments:
    targetdir (optional) -- target directory (trailing slash not necessary)
    jobidlist            -- job(s) of interest (job object, jobid, list of ids, list of jobs, mixed list)
    """
    if not isinstance(jobidlist,list):
        jobidlist = [jobidlist]
    for jid in jobidlist:
        if isinstance(jid,int):
            job = jobs(jid)
            jid = jid
        else:
            job = jid
            jid = job.id
        with open(targetdir + "/" + job.name + "." + str(jid) + ".lfn.txt","w") as f:
            j = job
            for sj in j.subjobs.select(status="completed"):
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



def write_access_url_to_txt(jobidlist,targetdir = "."):
    """write access urls of a job to text file "jobname.jobid.pfn.txt"

    Keyword arguments:
    targetdir (optional) -- target directory (trailing slash not necessary)
    jobidlist            -- job(s) of interest (job object, jobid, list of ids, list of jobs, mixed list)
    """
    if not isinstance(jobidlist,list):
        jobidlist = [jobidlist]
    for jid in jobidlist:
        if isinstance(jid,int):
            job = jobs(jid)
            jid = jid
        else:
            job = jid
            jid = job.id
        with open(targetdir + "/" + job.name + "." + str(jid) + ".pfn.txt","w") as f:
            j = job
            lfns = []
            for sj in j.subjobs.select(status="completed"):
                for of in sj.outputfiles:
                    if of.namePattern == 'summary.xml':
                        continue
                    try:
                        of.lfn
                    except AttributeError:
                        pass
                    else:
                        lfns.append(of.lfn)
            import subprocess
            import os
            try:
                gangascriptdir = os.environ['GANGASCRIPTS']
            except KeyError:
                gangascriptdir = os.environ['HOME'] + "/gangascripts"
            f.write(subprocess.check_output(["lb-run","LHCbDirac","prod","python",gangascriptdir+"/get_access_urls.py"]+lfns))
