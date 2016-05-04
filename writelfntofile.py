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


