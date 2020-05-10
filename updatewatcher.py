import os
import time
#Time of last file modification
open("updates.txt", "w").close()
open("x.txt", "w").close()
lastChanged = os.stat("updates.txt").st_size

while 1:
    #Wait 100ms between checking
    time.sleep(.100)
    #Check for changes
    newChanged = os.stat("updates.txt").st_size
    if newChanged != lastChanged :
        #File has changed; Make a new file and swap it with updates.txt
        os.rename("updates.txt", "process.txt")
        os.rename("x.txt", "updates.txt")
        #Set the new lastChanged time
        lastChanged = os.stat("updates.txt").st_size
        #Process updates
        processFile = open("process.txt", "r+")
        processLine = processFile.readline()
        while len(processLine) != 0 :
            processLine = processLine.split(':')
            if processLine[0] == 'a' :
                fatFile = open("fat.txt", "a")
                fatFile.write(processLine[1]+"\t"+processLine[2]+"\t"+processLine[3]+"\n")
                fatFile.close()
            processLine = processFile.readline()
        #Set up for next swap
        processFile.truncate(0)
        os.rename("process.txt", "x.txt")
