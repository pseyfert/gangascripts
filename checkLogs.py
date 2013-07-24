def checkLogs(job,sub_list=[],hack_ignoreTerminated=False):
    """ Check output logs for jobs producing MicroDSTs"""
    
    KnownErrors={'KillHltBanks':[],'FileRecordDataSvc':[]}
    
    n_complete = 0
    n_ok = 0
    evt_tot = 0
    plist = {}
    pllist = []
    zooev = 0
    
    evt_wrt = 0
    lumi_value = 0
    lumi_uncertainty = 0
    
    jobCounters = {}
    mandat_failers = []

    #in case the job has no subjobs, a slice is made out of it
    if len(job.subjobs)==0:
        subjobs = jobSlice([job])
        #print 'the job has no subjobs'
    else:
        subjobs = job.subjobs
    
    if not sub_list==[]:
        subjobs = []
        for i in sub_list:
           subjobs+=[job.subjobs(i)]
    for subjob in subjobs:
        counters ={}
        flags    =set()
        
        if subjob.status != 'completed': continue
        
        n_complete +=1
        
        outputdir = subjob.outputdir
        if not os.path.exists(outputdir):
            print 'ERROR : output directory of subjob %d do not exists'%(subjob.id)
            continue
        
        filenames = os.listdir(outputdir)
        logs = filter(filterLogExt,filenames)
        if len(logs)==0:
            print 'ERROR : log file for subjob %d do not exists'%(subjob.id)
            continue
        if len(logs)>1:
            print 'ERROR : too many logfiles (%d) for subjob %d' % (len(logs),subjob.id)
            
        f=file(os.path.join(outputdir,logs[0]))
        for Line in f:
            
            line  = Line.strip()
            words = line.split()
            if len(words)<2: continue
            alg   = words[0]
            level = words[1]
            
            if level == 'ERROR':
                
                ###FIXME
                ####print str(subjob.id) + "\t" + Line
                known = True#False
                if alg in KnownErrors.keys():
                    if len(KnownErrors[alg])==0: known=True
                    for err in KnownErrors[alg]:
                        if line.rfind(err)>-1: known=True
                ###FIXME
                ######if not known:        
                ######    print '%4s : %s'%(subjob.id,line)
                    
            if level == 'INFO':
                
                if alg=='EventLoopMgr':
                    if line.rfind("No more events in event selection")>-1:
                        flags.add('All events')
 
           
                if alg=='ApplicationMgr':

                    if line.rfind('Application Manager Finalized successfully')>-1:
                        flags.add('Finalized')
                    if line.rfind('Application Manager Terminated successfully')>-1:
                        flags.add('Terminated')           
                            
                if re.search('IntegrateBeamCr.*',alg) :
                    if line.rfind("Integrated luminosity:")>-1:
                        if float(words[4])<0:
                            print '%4s : negative luminosity'%(subjob.id)
                            counters['Int. lum'] = 0
                            counters['Int. lum uncert.'] = 0
                             
                        else:
                            counters['Int. lum']=float(words[4])
                            counters['Int. lum uncert.']=float(words[6])
                        
            if level == 'SUCCESS':
                if alg=='z':
                    if line.rfind("events processed")>-1:
                        flags.add('zoosumm')
                        counters['ZooEvents']=int(words[2])
                    if line.rfind("particles of decay")>-1:
                        counters['ZooParticles'+words[6]]=int(words[2])
                        if not words[6] in pllist :
                           pllist +=[words[6]]
                           plist.update({words[6]:int(words[2])})
                        else:
                           plist[words[6]]+=int(words[2])
                
                if alg=='DaVinciInitAlg':
                    if line.rfind("events processed")>-1:
                        counters['events processed']=int(words[2])
                        flags.add("events processed")
        f.close()
        
        if hack_ignoreTerminated:
          MandatoryFlags = set(['All events','zoosumm','Finalized','events processed'])
        else:
          MandatoryFlags = set(['All events','zoosumm','Finalized','events processed','Terminated'])
        if len(MandatoryFlags-flags)>0:
            print '%4s : not complete'%(subjob.id),', missing :',MandatoryFlags-flags
            mandat_failers += [subjob.id]
            continue
   
        #if counters['EVENT LOOP']==0:
        #    print logs,'NO EVENT processes in EVENT LOOP'
        #    continue
        
        evt_tot           += counters['events processed']
        zooev             += counters['ZooEvents']
        
        #lumi_value        += counters['Int. lum']
        #lumi_uncertainty  += counters['Int. lum uncert.']
        
#        if 'CopyODIN_SeqJpsi2MuMu' in counters.keys():
#            evt_wrt+= counters['CopyODIN_SeqJpsi2MuMu']
#        if 'CopyODIN_SeqDiMuonInc' in counters.keys():
#            evt_wrt+= counters['CopyODIN_SeqDiMuonInc']
        n_ok +=1
        
        jobCounters  = _addCounters(jobCounters, counters)
    print "Nb of jobs completed = %3d"%(n_complete)
    print "Nb of jobs OK        = %3d"%(n_ok)
    print "Nb of events read    = %10d"%(evt_tot)
    print "Int. luminosity      = %10f +/- %10f [pb-1]"%(lumi_value, lumi_uncertainty)
    for particle in pllist:
        print "Nb of " + particle + "   %4d"%(plist[particle])
    print "Nb of ZooEvents      = %4d"%(zooev)
    print "mandatory failures: ", mandat_failers
#    print "Nb of events written = %10d"%(evt_wrt)
    jobCounters['failed subjobs'] = len(mandat_failers)
    return jobCounters, mandat_failers


