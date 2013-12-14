import shutil
import os, commands, re, glob
from Ganga.GPI import jobs

def fixLFNs(job):
    j,joblist=getJobList(job)
    for sj in joblist:
        for f in sj.outputfiles.get("*.root"):
            if ""==f.lfn:
                for line in open(str(Ganga.Core.FileWorkspace.OutputWorkspace().getPath())+str(j.id)+"/"+str(sj.id)+'/output/std.out','r'):
                    if re.search('Will attempt',line):
                      if re.search(f.namePattern,line):
                        thelfn = re.sub(" to .*","",re.sub('.*to replicate ',"",line))
                        print thelfn,"\tfor",str(j.id),".",str(sj.id)
                        f.lfn = thelfn

