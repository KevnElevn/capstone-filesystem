import os
import time
#Time of last file modification
lastChanged = os.stat("updates.txt").st_mtime

while 1:
    #Wait 100ms between checking
    time.sleep(.100)
    #Check for changes
    newChanged = os.stat("updates.txt").st_mtime
    if newChanged != lastChanged :
        #File has changed; Make a new file and swap it with updates.txt
        newUpdatesFile = open("x.txt", "w")
        newUpdatesFile.close()
        os.rename("updates.txt", "process.txt")
        os.rename("x.txt", "updates.txt")
        #Set the new lastChanged time
        lastChanged = os.stat("updates.txt").st_mtime
        #Process updates
        processFile = open("process.txt", "r")
        processLine = processFile.readline()
        while len(processLine) != 0 :
            processLine = processLine.split(':')
            if processLine[0] == 'a' :
                fatFile = open("fat.txt", "a")
                fatFile.write(processLine[1]+"\t"+processLine[2]+"\t"+processLine[3]+"\n")
                fatFile.close()
            processLine = processFile.readline()
        processFile.close()
        os.remove("process.txt")