# Downloads the output which is saved on the grid to your local output directory.
# Skips already downloaded files.
import shutil
import os, commands, re, glob
from Ganga.GPI import jobs

def getJobList(job,sub_list=None):
    if isinstance (job, int) :
        job = jobs(job)

    # check if job has subjobs
    jobList = []
    if len(job.subjobs)>0:
        if type(sub_list) is list:
            jobList = []
            for sj in sub_list:
                jobList += job.subjobs.select(sj,sj,status="completed")
        else:
            jobList = job.subjobs.select(status="completed")
    else:
        if job.status=="completed":
            jobList = [job]
    return job,jobList

def download(job,targetDir=None,force_redownload=False,sub_list=None):
    # check if job id or job object has been given
    job, jobList = getJobList(job,sub_list)
    # Ok sub_list overwrites the rest
    # if no targetdir specified, don't do magic with it
    if isinstance(targetDir, str):
        commands.getstatusoutput('mkdir -p ' + targetDir)
        if not targetDir.endswith("/"):
            targetDir = targetDir + "/"
    downloadedIDs = []
    failedIDs = []
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
                f.localDir = sj.outputdir
                automaticName = sj.outputdir + f.namePattern 
                targetFileName = sj.outputdir + f.namePattern
            successful = False
            if (os.path.isfile(targetFileName)) :
                print "file ", f.namePattern, " from job", str(job.id), ".", str(sj.id), " already loaded"
                if force_redownload:
                    print "load it anyway"
                    f.get()
                    if automaticName!=targetFileName:
                        stat, out = commands.getstatusoutput("mv " + automaticname + " " + targetfilename)
                        if stat!=0:
                            print "error in renaming ", output
                if (os.path.isfile(targetFileName)) :
                    downloadedIDs.append(sj.id)
                else:
                    print "Download of {0} failed".format(sj.id)
                    failedIDs.append(sj.id)
            else:
                f.get()
                if automaticName!=targetFileName:
                    #shutil.move(automaticName,targetFileName)
                    stat, out = commands.getstatusoutput("mv " + automaticname + " " + targetfilename)
                    if stat!=0:
                        print "error in renaming ", output

                if (os.path.isfile(targetFileName)) :
                    downloadedIDs.append(sj.id)
                else:
                    failedIDs.append(sj.id)
                    print "Download of {0} failed".format(sj.id)
    if  ( (len(job.subjobs)>0 ) and ( len(downloadedIDs)==len(job.subjobs) ) ):
        print "All subjobs downloaded!!! Have fun!"
    return downloadedIDs,failedIDs



# Merges the output of a job (.root) by collecting all downloaded files.
import os, shutil
from Ganga.GPI import RootMerger
def merge(job,files,outputdir="",args=""):
    rm = RootMerger()
    rm.files = files
    rm.args = ""
    list = []
    job, jobList = getJobList(job)
    for j in jobList:
        for f in files:
            src = os.path.join(j.outputdir,f)
            if os.path.isfile(src):
                list.append(j)
    print list

    #if outputdir!="":
    #    rm.merge(list,outputdir)
    #else:
    # Merge first in jobs own outputdirectory
    print job.outputdir
    rm.merge(list,job.outputdir)
    if outputdir!="":
        for f in files:
            src = os.path.join(job.outputdir,f)
            name = j.name +"_"+ f
            dest = os.path.join(outputdir,name)
            print src
            print dest
            shutil.move(src,dest)

    print "Merging of {0} done".format(job.name)


def downloadAndMerge(job,files,outputdir="",args=""):
    # check if job id or job object has been given
    #if isinstance (job, int) :
    #    job = jobs(job)
    download(job)
    merge(job,files,outputdir,args)
    print "Download and merging of job {0} done".format(job.id)




def move(job,outputdir,remove = False, overwrite = False):
    job, jobList = getJobList(job)
    for j in jobList:
        dir = j.outputdir
        files = os.listdir(dir)
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


# Removes locally stored files.
def remove(job):
    job, jobList = getJobList(job)
    for j in jobList:
        dir = j.outputdir
        files = os.listdir(dir)
        for file in files:
            if file.endswith(".root"):
                #print os.path.join(dir,file)
                os.remove(os.path.join(dir,file))
                

