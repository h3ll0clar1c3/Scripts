#!/usr/bin/python

import sys, binascii, re
from subprocess import Popen, PIPE

f = open(sys.argv[1], 'r')
for line in f:
    wepKey = re.sub(r'\W+', '', line)

    if len(wepKey) != 5 :
        continue
    hexKey = binascii.hexlify(wepKey)
    print "Trying with WEP Key: " +wepKey + " Hex: " + hexKey
    p = Popen(['/usr/bin/airdecap-ng', '-w', hexKey, 'WEP-Advanced.cap'], stdout=PIPE)
    output = p.stdout.read()
    finalResult = output.split('\n')[4]

    if finalResult.find('1') != -1 :
        print "Success WEP Key Found: " + wepKey
        sys.exit(0)
print "Failure! WEP Key Could not be Found with the existing dictionary!"
