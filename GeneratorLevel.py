## script to determine generator level cut efficiencies for recent productions
## provided by Mike Williams (MIT)
## all appreciation go to Mike, all accusation to me

import urllib2
from Ganga.GPI import jobs

def ErrorFormula(acc,gen):
  # error from arXiv:0701199
  fgen = float(gen)
  facc = float(acc)
  err = (facc+1.)*(facc+2.)/(fgen+2.)/(fgen+3.) - (facc+1.)*(facc+1.)/(fgen+2.)/(fgen+2.)
  return err


def GeneratorEfficiencyFromDataset(dataset):
  gen = 0
  acc = 0
  for f in dataset:
    furl = f.name.replace('ALLSTREAMS.DST','LOG')
    furl = furl.replace('_1.allstreams.dst','')
    id = furl.split('/')[5]
    furl = furl.replace(id+'_','')
    furl = "http://lhcb-logs.cern.ch/storage"+furl+'/'
    #print furl
    fgen = 0
    facc = 0
    try:
        furl =  urllib2.urlopen(furl)
        lines = furl.readlines()
        the_line = ''
        for l in lines:
            if l.find('_5.AllStreams.dst') > 0: 
                the_line = l.replace('<td> ','').replace(' </td>\n','')
                break
        info = the_line.split(';')
        for i in info:
            url = i.replace('ALLSTREAMS.DST','LOG')
            url = url.replace('_5.AllStreams.dst','/GeneratorLog.xml')
            id = url.split('/')[5]
            url = "http://lhcb-logs.cern.ch/storage/"+url.replace(id+'_','')
            this_gen = -1
            this_acc = -1
            try:
                file =  urllib2.urlopen(url)
                lines = file.readlines()
                found_tag = False
                for l in lines:
                    if l.find('generator level cut') > 0: found_tag = True
                    if not found_tag: continue
                    if l.find('after') > 0: 
                        this_acc = int(l.replace('<after>','').replace('</after>',''))
                    if l.find('before') > 0:
                        this_gen = int(l.replace('<before>','').replace('</before>',''))
                    if this_gen > 0 and this_acc >= 0: break
                fgen += this_gen
                facc += this_acc
                #print this_acc, this_gen, this_acc/(1.0*this_gen)
            except urllib2.HTTPError:
                print 'Error! %s not found!' % url
        print f.name, facc, fgen, facc/(1.0*fgen)
        gen += fgen
        acc += facc
    except urllib2.HTTPError:
        print 'Error! %s not found!' % furl

  from math import sqrt

  print 'total:', acc, gen, acc/(1.0*gen), sqrt(ErrorFormula(acc,gen))
  return acc, gen

def GeneratorEfficiencyFromJob(jid):
  if isinstance (jid, int) :
     j = jobs(jid)
  else :
     j = jid
  GeneratorEfficiencyFromDataset(j.inputdata)


