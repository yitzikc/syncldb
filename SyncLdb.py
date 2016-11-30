#!/usr/bin/env python3

# We use the Pathlib standard package, which is available in Python 3.4 and higher
import sys
import time

import DirectoryHardLinkSynchronizer
	
class LdbSynchronizer(DirectoryHardLinkSynchronizer.DirectoryHardLinkSynchronizer):
	def __init__(self, srcDir, dstDir):
		super().__init__(srcDir, dstDir)
		self.skipGlobs.append("LOCK")
		
def main():
	#TODO: parse args mroe cleanly using argparse
	src, dst = sys.argv[1:3]

	handler = LdbSynchronizer(src, dst)
	observer = handler.Start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
	return

if __name__ == "__main__":
	main()
