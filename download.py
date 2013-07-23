# Downloads the output which is saved on the grid to your local output directory.
# Skips already downloaded files.
import os
def download(job,min=-1,targetdir=None,force_redownload=False):
    # if no targetdir specified, don't do magic with it
    if isinstance(targetdir, str):
      # otherwise create target dir (-p = don't complain if it already exists)
      commands.getstatusoutput('mkdir -p ' + targetdir)
      # if targetdir doesn't end with / then add it
      if targetdir.endswith("/"):
       # nothing to do
      else:
       targetdir = targetdir + "/"

    # check if job id or job object has been given
    if isinstance (job, int) :
       thejob = jobs(job)
    else :
       thejob = job

    for j in thejob.subjobs:
        if j.status=="completed" and j.id>min:
            for f in j.outputfiles.get("*.root"):
                if ""==f.lfn:
                    print "no lfn for file ", f.namePattern, " from job", str(thejob.id), ".", str(j.id)
                    continue
                if isinstance(targetdir,str):
                  f.localDir = targetdir
                  ending = re.sub(".*\.","",f.namePattern)  # the file ending is everything after the last .
                  mainpart = re.sub("\."+ending,"",f.namePattern) # the main part of the filename is everything before the ending (removing the .)
                  newmainpart = mainpart + "_" + str(j.id)
                  targetfilename = targetdir + "/" + newmainpart + "." + ending
                  automaticname = f.localDir + "/" + f.namePattern
                else:
                  automaticname = f.outputdir + f.namePattern
                  targetfilename = f.outputdir + f.namePattern
                if (os.path.isfile(targetfilename)) :
                    print "file ", f.namePattern, " from job", str(thejob.id), ".", str(j.id), " already loaded"
                    if force_redownload:
                        print "load it anyway"
                        f.get()
                        if automaticname!=targetfilename:
                          commands.getstatusoutput("mv " + automaticfilename + " " + targetfilename)
                else:
                        f.get()
                        if automaticname!=targetfilename:
                          commands.getstatusoutput("mv " + automaticfilename + " " + targetfilename)
                
        
