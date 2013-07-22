# Removes or moves locally stored files.
import os
def remove(job):
    for j in job.subjobs:
        dir = j.outputdir
        files = os.listdir(dir)
        for file in files:
            if file.endswith(".root"):
                #print os.path.join(dir,file)
                os.remove(os.path.join(dir,file))
                
import shutil
def move(job,outputdir,remove = False, overwrite = False):
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
                    print "Deletet directory."
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
