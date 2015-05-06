#! /usr/local/bin/python3

import os,sys

changeDirectory = "cd Geolife\ Trajectories\ 1.2/ &&"

resAdd = os.system(changeDirectory+"git add Data/01*/*")
print ("============ "+str(resAdd)+" ============")
resCommit = os.system(changeDirectory+"git commit -m \"10-19\"")
print ("============ "+str(resCommit)+" ============")
resPush = os.system(changeDirectory+"git push")
print ("============ "+str(resPush)+" ============")


