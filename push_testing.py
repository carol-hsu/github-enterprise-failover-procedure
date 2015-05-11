#! /usr/local/bin/python3

import os,sys,time

changeDirectory = "cd Geolife\ Trajectories\ 1.2/ &&"

startCrashTime = ""
recoveryTime =""


startTime = time.time()
dirNum = 15

while dirNum <= 19:
	resAdd = os.system(changeDirectory+"git add Data/0"+str(dirNum)+"/*")
	print ("========"+str(dirNum)+" ADD "+str(resAdd)+" ============")

	resCommit = os.system(changeDirectory+"git commit -m \""+str(dirNum)+" commit\"")
	print ("========"+str(dirNum)+" COMMIT "+str(resCommit)+" ======")
	
	resPush = os.system(changeDirectory+"git push")
	if resPush > 0:
		if startCrashTime == "":
			startCrashTime = time.time()
			print ("******** Primary Node is deading ********")
		continue
	else:
		if startCrashTime != "" and recoveryTime == "" :
			recoveryTime = time.time()
			print ("******** Primary Node is Alive ********")
		print ("========"+str(dirNum)+" PUSH "+str(resPush)+" ==========")

	dirNum += 1	

endTime = time.time() 

print ("============== Summary =============")
print (" Total RunTime %s sec" % (endTime - startTime) )
print (" User Feeling DownTime %s sec" % (recoveryTime - startCrashTime) )


