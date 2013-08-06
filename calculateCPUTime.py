# Calculates the CPU time of a job by looping over all completed subjobs.
# Allows you a better estimate for setting j.backend.settings['CPUTime']=XXXXXXX

from exceptions import ValueError
from math import sqrt
def calculateCPUTime(job):
    sumTime = 0.0
    sumTime2 = 0.0
    n = 0
    for j in job.subjobs:
        if not (j.status == 'completed'):
            continue
        cpuTime = 0.0
        try:
            cpuTime = float(j.backend.normCPUTime)
        except ValueError:
            continue
        sumTime = sumTime + cpuTime
        sumTime2 = sumTime2 + cpuTime*cpuTime
        n = n+1
    mean = sumTime/(n)
    sigma = sqrt(1./(n-1) * (sumTime2 - n*mean*mean))
    print "cpu time = {0} \pm {1}".format(mean,sigma)
