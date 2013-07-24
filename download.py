# Downloads the output which is saved on the grid to your local output directory.
# Skips already downloaded files.
import os, commands, re, tempfile
def download(job,min=-1,targetdir=None,force_redownload=False,sub_list=None):
    # if no targetdir specified, don't do magic with it
    if isinstance(targetdir, str):
      # otherwise create target dir (-p = don't complain if it already exists)
      stat, output = commands.getstatusoutput('mkdir -p ' + targetdir)
      if 0!=stat:
         print "error creating target directory", output
         return
      # if targetdir doesn't end with / then add it
      if targetdir.endswith("/"):
       dummy = 1+1
       # nothing to do
      else:
       targetdir = targetdir + "/"

    # check if job id or job object has been given
    if isinstance (job, int) :
       print "sorry, this doesn't work if you just import my script. needs to be in ~/.ganga.py"
       thejob = jobs(job)
    else :
       thejob = job

    if type(sub_list) is list:
       subjobs = []
       for sj in sub_list:
          subjobs += thejob.subjobs.select(sj,sj,status="completed")
    else:
       subjobs = thejob.subjobs.select(status="completed")
    for sj in subjobs:
        if sj.id>min:
            for f in sj.outputfiles.get("*.root"):
                if ""==f.lfn:
                    print "no lfn for file ", f.namePattern, " from job", str(thejob.id), ".", str(sj.id)
                    continue
                if isinstance(targetdir,str):
                  targettempdir = tempfile.mkdtemp(dir=targetdir)
                  f.localDir = targettemp
                  ending = re.sub(".*\.","",f.namePattern)  # the file ending is everything after the last .
                  mainpart = re.sub("\."+ending,"",f.namePattern) # the main part of the filename is everything before the ending (removing the .)
                  newmainpart = mainpart + "_" + str(sj.id)
                  targetfilename = targetdir + newmainpart + "." + ending
                  automaticname = f.localDir + f.namePattern
                else:
                  automaticname = sj.outputdir + f.namePattern
                  targetfilename = sj.outputdir + f.namePattern
                if (os.path.isfile(targetfilename)) :
                    print "file ", f.namePattern, " from job", str(thejob.id), ".", str(sj.id), " already loaded"
                    if force_redownload:
                        print "load it anyway"
                        f.get()
                        if automaticname!=targetfilename:
                          stat, out = commands.getstatusoutput("mv " + automaticname + " " + targetfilename)
                          if stat!=0:
                             print "error in renaming ", output
                else:
                        f.get()
                        if automaticname!=targetfilename:
                          stat, out = commands.getstatusoutput("mv " + automaticname + " " + targetfilename)
                          if stat!=0:
                             print "error in renaming ", output
                if isinstance(targetdir,str):
                  shutil.rmtree(targettempdir)
                
        
