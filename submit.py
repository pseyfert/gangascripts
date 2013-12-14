import getJobList
from Ganga.GPI import queues

def sub(j):
  j,jl = getJobList(j)
  j.subjobs.select(status="new").submit()

def resub(j):
  j,jl = getJobList(j)
  j.subjobs.select(status="failed").submit()

def queuesubmission(joblist):
  for j in joblist:
    queues.add(sub,kwargs={"j":j})


def queueresubmission(joblist):
  for j in joblist:
    queues.add(resub,kwargs={"j":j})
