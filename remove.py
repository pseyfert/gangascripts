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
                

