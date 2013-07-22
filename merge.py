# Merges the output of a job (.root) by collecting all downloaded files.
import os, shutil
from Ganga.GPI import RootMerger
def merge(job,files,outputdir="",args=""):
    rm = RootMerger()
    rm.files = files
    rm.args = ""
    list = []
    for j in job.subjobs.select(status='completed'):
        for f in files:
            src = os.path.join(j.outputdir,f)
            if os.path.isfile(src):
                list.append(j)
    print list
    if outputdir!="":
        rm.merge(list,outputdir)
    else:
        rm.merge(list)
    if outputdir!="":
        for f in files:
            src = os.path.join(outputdir,f)
            name = j.name + f
            dest = os.path.join(outputdir,name)
            print src
            print dest
            shutil.move(src,dest)
            
    
