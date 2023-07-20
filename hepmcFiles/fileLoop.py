#!/usr/bin/env python3

import os
import sys

for filename in os.scandir(sys.argv[1]):
	print(filename.path)
	os.system("./DVMuEfficiencies.py %s"%filename.path)
