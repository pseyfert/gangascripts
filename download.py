# Downloads the output which is saved on the grid to your local output directory.
# Skips already downloaded files.
import os
def download(job,min=-1):
    for j in job.subjobs:
        if j.status=="completed" and j.id>min:
            for f in j.outputfiles.get("*.root"):
                if (not os.path.isfile(j.outputdir+f.namePattern)):
                    if (f.lfn!=''):
                        f.get()
                    else:
                        print "LFN of file ({2}) job {0}.{1} not there".format(job.id,j.id,f.namePattern)
                else:
                    print "File({2}) of job {0}.{1} already downloaded".format(job.id,j.id,f.namePattern)
                
        
