def whatsfishy(list):
  retlist = {}
  for j in list:
    retlist[j.id] = []
    for sj in j.subjobs:
       if (sj.status == 'submitted'): continue;
       if (sj.status == 'completed'): continue;
       if (sj.status == 'failed'): continue;
       if (sj.status == 'running'): continue;
       print 'job ',str(j.id),'.',str(sj.id),' is in state ', sj.status
       retlist[j.id] += [sj.id]
  return retlist

