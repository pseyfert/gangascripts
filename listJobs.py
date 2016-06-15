# mainly written by Manuel Schiller
# recommendations for colors['fishy'] are welcome!

from Ganga.GPI import jobs


def ljobs(self = jobs, interactive = 1):
    retVal = 'Job slice: ' + self._impl.name + ' (' + str(len(self)) + ' jobs):\n\n'
    if (0 != interactive):
        colors = { 'failed':'31', 'killed':'31', 'submitted':'33',
                   'completed':'34', 'running':'32' };
    else:
        colors = { 'failed':'', 'killed':'', 'submitted':'', 'completed':'',
                   'running':'' };
    retVal = (retVal + '%4s %4s/%4s/%4s/%4s/%4s/%4s %10s %10s %10s %8s %s\n' %
              ('id', 'sub', 'run', 'err', '???', 'done', 'tot', 'status', 'backend',
               'appl', 'version', 'name'));
    for j in self:
        # set job status color
        col='';
        if (j.status in colors): col=colors[j.status];
        # handle single jobs and arrays of subjobs properly
        njobs = len(j.subjobs);
        nfishy = nsubmitted = nrunning = nfailed = ncompleted = 0;
        if (0 != njobs):
            nsubmitted = len(j.subjobs.select(status='submitted'));
            nrunning = len(j.subjobs.select(status='running'));
            nfailed = (len(j.subjobs.select(status='failed')) +
                       len(j.subjobs.select(status='killed')));
            ncompleted = len(j.subjobs.select(status='completed'));
            nfishy = njobs-ncompleted-nfailed-nrunning-nsubmitted;
        else:
            if ('submitted' == j.status): nsubmitted = nsubmitted + 1;
            if ('running' == j.status): nrunning = nrunning + 1;
            if (j.status in ['failed', 'killed']): nfailed = nfailed + 1;
            if ('completed' == j.status): ncompleted = ncompleted + 1;
            if ('new' != j.status): njobs = njobs + 1;
        # protect against invalid backend/application
        backendname = '';
        appname = '';
        appver = '';
        if (None != j.backend.__class__):
            backendname = j.backend.__class__.__name__;
        if (None != j.backend.actualCE):
            backendname = j.backend.actualCE;
        while (15>len(backendname)) :
            backendname = backendname+" ";
        if (15<len(backendname)) :
            backendbuffer = ""
            for i in range(15):
               backendbuffer = backendbuffer + backendname[i];
            backendname = backendbuffer;
        if (None != j.application.__class__):
            appname = j.application.__class__.__name__;
            try:
                appver = j.application.version;
            except KeyError:
                appver = "n/a";
        # print output for current job
        retVal = (retVal +
                  '%4d \033[%sm%4d\033[m/\033[%sm%4d\033[m/\033[%sm%4d\033[m/%4d\033[m/'
                  '\033[%sm%4d\033[m/%4d \033[%sm%10s\033[m '
                  '%10s %10s %8s %s\n' % (
                          j.id,
                          colors['submitted'], nsubmitted,
                          colors['running'], nrunning,
                          colors['failed'], nfailed,
                          nfishy,
                          colors['completed'], ncompleted,
                          njobs, col, j.status,
                          backendname, appname, appver, j.name));
    print retVal
    return ""

# patch jobs to use ljobs as new display method
jobs.__class__._olddisplay=jobs.__class__._display;
jobs.__class__._display=ljobs;

