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

