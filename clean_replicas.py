from DIRAC.Core.Base import Script
Script.parseCommandLine(ignoreErrors=False)
import sys

import DIRAC.Interfaces.API.Dirac as Dirac
d = Dirac.Dirac()
lfns = sys.argv[1:]
try:
    large_dict = d.getAllReplicas(lfns)['Value']['Successful']
except KeyError:
    print "didn't work with input ",lfns
    for lfn in lfns:
        print type(lfn)
        print "received for ",lfn,": ",d.getAllReplicas(lfn)
else:
    for lfn in large_dict.keys():
        if 'CERN-USER' in large_dict[lfn].keys():
            for site in large_dict[lfn].keys():
                if site == 'CERN-USER':
                    continue
                else:
                    d.removeReplica(lfn,site)




