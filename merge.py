# Merges the output of a job (.root) by collecting all downloaded files.
import os, shutil
from Ganga.GPI import RootMerger
import getjoblist

def merge(job,files,outputdir="",args=""):
    rm = RootMerger()
    rm.files = files
    rm.args = ""
    jobsToMerge = []
    job, jobList = getJobList(job)
    for j in jobList:
        for f in files:
            src = os.path.join(j.outputdir,f)
            if os.path.isfile(src):
                jobsToMerge.append(j)
    print jobsToMerge

    #if outputdir!="":
    #    rm.merge(jobsToMerge,outputdir)
    #else:
    # Merge first in jobs own outputdirectory
    print job.outputdir
    rm.merge(jobsToMerge,job.outputdir)
    if outputdir!="":
        for f in files:
            src = os.path.join(job.outputdir,f)
            name = j.name +"_"+ f
            dest = os.path.join(outputdir,name)
            print src
            print dest
            shutil.move(src,dest)

    print "Merging of {0} done".format(job.name)
            
    
