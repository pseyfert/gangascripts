# USAGE
# SetupLHCbDirac
# lhcb-proxy-init
# python SCRIPTNAME lfn <lfn <lfn ....>>
from DIRAC.Core.Base import Script
Script.parseCommandLine(ignoreErrors=False)
import sys
import re

import DIRAC.Interfaces.API.Dirac as Dirac
d = Dirac.Dirac()
lfns = sys.argv[1:]
try:
    large_dict = d.getReplicas(lfns)['Value']['Successful']
except KeyError:
    print "didn't work with input ",lfns
else:
    print "got all replicas"
    sites = []
    site_lfn_maps = {}
    for lfn in lfns:
        try:
            thismap = large_dict[lfn]
        except KeyError:
            print "failed with ", lfn
        else:
            try:
                site_lfn_maps[thismap.keys()[-1]]
            except KeyError:
                site_lfn_maps[thismap.keys()[-1]] = [lfn]
            else:
                site_lfn_maps[thismap.keys()[-1]].append(lfn)
    sites = site_lfn_maps.keys()
    print "mapped sites to lfns"
    for site in sites:
        print "processing ", site
        if re.match("CNAF.*",site) is None:
            try:
                site_lfn_maps[site]
            except KeyError:
                pass
            else:
                try:
                    access_dict = d.getAccessURL(site_lfn_maps[site],site)['Value']['Successful']
                except KeyError:
                    print "failed resolving access urls (in standard treatment) at ", site
                else:
                    for k in access_dict.keys():
                        print access_dict[k]
        else:
            try:
                site_lfn_maps[site]
            except KeyError:
                pass
            else:
                import subprocess
                output = subprocess.check_output(["dirac-dms-lfn-accessURL","--Protocol=root,xroot"]+site_lfn_maps[site]+[site])
                urllines = []
                local_dict = {}
                for line in output.split('\n'):
                  if re.match(".* : .*root.*://.*",line) is not None:
                        #print "the line is ", line
                        lfn = re.sub(" *: .*root.*://.*$","",re.sub("^ *","",line))
                        url = re.sub(" *$","",re.sub(" *"+lfn+" * :  *","",line))
                        #print "lfn: ",lfn
                        #print "url: ",url
                        local_dict[lfn] = url
                #print "looking for ", site_lfn_maps[site]
                #print "got ",local_dict
                for lfn in site_lfn_maps[site]:
                    try:
                        print local_dict[lfn]
                    except KeyError:
                        print "failed resolving access urls (in CNAF treatment) at ", site
