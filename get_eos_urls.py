# USAGE
# SetupLHCbDirac
# lhcb-proxy-init
# python SCRIPTNAME lfn <lfn <lfn ....>>
from DIRAC.Core.Base import Script
Script.parseCommandLine(ignoreErrors=False)
import sys

import DIRAC.Interfaces.API.Dirac as Dirac
d = Dirac.Dirac()
lfns = sys.argv[1:]
try:
    large_dict = d.getAccessURL(lfns,'CERN-USER')['Value']['Successful']
except KeyError:
    print "didn't work with input ",lfns
else:
    for k in large_dict.keys():
        print large_dict[k]




