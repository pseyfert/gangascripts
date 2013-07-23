# Downloads the output which is saved on the grid to your local output directory.
# Skips already downloaded files.
import os, commands, re, glob
def download(job,targetDir=None,force_redownload=False):
    # check if job id or job object has been given
    if isinstance (job, int) :
        job = jobs(job)

    # check if job has subjobs
    jobList = []
    if len(job.subjobs)>0:
        jobList = job.subjobs.select(status="completed")
    else:
        if job.status=="completed":
            jobList = [job]
    # if no targetdir specified, don't do magic with it
    if isinstance(targetDir, str):
        commands.getstatusoutput('mkdir -p ' + targetDir)
        # explicitly create directory and delete files with same name pattern
        #try:    
        #    os.mkdir(targetDir)
        #except:
        #    print "Directory {0} already exists.".format(outputdir)
        #
        #    print "Deleting files with same name pattern as output."
        #    try:
        #        files = []
        #        for f in job.outputfiles:
        #            files += [f for f in glob.glob(f.namePattern+"*")]
        #        for f in files:
        #            os.remove(f)
        #        print "Delete directory."
        #    except:
        #        print "Something went wrong."
        # if targetdir doesn't end with / then add it                
        if not targetDir.endswith("/"):
            targetDir = targetDir + "/"

    # download files
    for sj in jobList:
        for f in sj.outputfiles.get("*.root"):
            if ""==f.lfn:
                print "no lfn for file ", f.namePattern, " from job", str(job.id), ".", str(sj.id)
                continue
            if isinstance(targetDir,str):
                f.localDir = targetDir
                ending = re.sub(".*\.","",f.namePattern)  # the file ending is everything after the last .
                mainPart = re.sub("\."+ending,"",f.namePattern) # the main part of the filename is everything before the ending (removing the .)
                newMainPart = mainPart + "_" + str(sj.id)
                targetFileName = targetDir + newMainPart + "." + ending
                automaticName = f.localDir + f.namePattern
            else:
                automaticName = sj.outputdir + f.namePattern
                targetFileName = sj.outputdir + f.namePattern
            if (os.path.isfile(targetFileName)) :
                print "file ", f.namePattern, " from job", str(job.id), ".", str(sj.id), " already loaded"
                if force_redownload:
                    print "load it anyway"
                    f.get()
                    if automaticName!=targetFileName:
                        commands.getstatusoutput("mv " + automaticName + " " + targetFileName)
                        #shutil.move(automaticName,targetFileName)
            else:
                f.get()
                if automaticName!=targetFileName:
                    commands.getstatusoutput("mv " + automaticName + " " + targetFileName)
                    #shutil.move(automaticName,targetFileName)
        

import merge

def downloadAndMerge(job,files,outputdir="",args=""):
    # check if job id or job object has been given
    if isinstance (job, int) :
        job = jobs(job)
    download(job)
    merge(job,files,outputdir,args)
    print "Download and merging of job {0} done".format(job.id)

import shutil
def move(job,outputdir,remove = False, overwrite = False):
    if isinstance (job, int) :
        job = jobs(job)
    for j in job.subjobs:
        dir = j.outputdir
        files = os.listdir(dir)
        try:    
            os.mkdir(outputdir)
        except:
            print "Directory {0} already exists.".format(outputdir)
            if (overwrite):
                print "Deleting old directory."
                try:
                    shutil.rmtree(outputdir)
                    print "Delete directory."
                except:
                    print "Something went wrong."

        for file in files:
            if file.endswith(".root"):
                dest = file
                dest = dest.replace(".root","_"+str(j.id)+".root")
                dest = os.path.join(outputdir,dest)
                src = os.path.join(dir,file)
                print dest
                print src
                shutil.move(src,dest)
                if (remove):
                    os.remove(src)
