import os
import subprocess
from config import setConfig

#Configure with config.txt
configData = []
setConfig(configData)
print(configData)
blockSize = configData[0]
thisNode = configData[1]
otherNodes = configData
otherNodes.remove(blockSize)
otherNodes.remove(thisNode)
#Run server listening on 'thisNode' port
server = subprocess.Popen(["./server", thisNode])
#Create FAT if there isn't one
#if not os.path.exists("fat.txt") :
fatFile = open("fat.txt", "w")
fatFile.write("Filename\tBlock\tNode\n")
fatFile.close()
#Watch updates.txt
watcher = subprocess.Popen(["python", "updatewatcher.py"])
#Continuously ask for input
while 1 :
    command = input("Enter command: \n\
    showfat\n\
    add <filename>\n\
    get <filename>\n\
    exit\n")
    #Print FAT
    if command == "showfat" :
        fatFile = open("fat.txt", "r")
        print(fatFile.read())
        fatFile.close()
    #Terminate server before exiting
    elif command == "exit" :
        server.kill()
        watcher.kill()
        exit()
    #Input has more than one word
    else :
        command = command.split()
        if(len(command) < 2) :
            print("Insufficient arguments")
        #First word is 'add' second should be name of file
        elif command[0] == "add" :
            #Check if file is in FAT
            fatFile = open("fat.txt", "r")
            fatLine = fatFile.readline()
            found = 0
            while len(fatLine) != 0 :
                fatLine = fatLine.split('\t')
                #Stop looking when file is found
                if command[1] == fatLine[0] :
                    found = 1
                    break
                fatLine = fatFile.readline()
            fatFile.close()
            #File is new
            if found == 0 :
                if not os.path.exists(command[1]) :
                    print("File not found")
                else :
                    filename = command[1]
                    fileSize = os.path.getsize(filename)
                    newFile = open(filename, "rb")
                    bytesRead = 0
                    blockNum = 0
                    counter = 0
                    blocks = []
                    error = 0
                    #Chop up file and distribute
                    while bytesRead < fileSize :
                        #Make block file
                        blockName = filename+".b"+str(blockNum)
                        newBlock = open(blockName, "wb")
                        newBlock.write(newFile.read(blockSize))
                        bytesRead += blockSize
                        newBlock.close()
                        blocks.append(blockName)
                        #Send block file
                        destinationIndex = counter % (len(otherNodes)+1)
                        if destinationIndex == len(otherNodes) :
                            destinationNode = thisNode
                        else :
                            destinationNode = otherNodes[destinationIndex]
                        error = subprocess.call(["./client", "w", blockName, destinationNode])
                        if not error == 0 :
                            break
                        #Update FAT
                        fatFile = open("fat.txt", "a")
                        fatFile.write(command[1] + '\t' + str(blockNum) + '\t' + destinationNode + '\n')
                        fatFile.close()
                        os.remove(blockName)
                        #Update other nodes
                        for i in otherNodes :
                            error = subprocess.call(["./client", "u", "a:"+filename+":"+str(blockNum)+":"+destinationNode+":", i])
                        blockNum += 1
                        counter += 1
                    newFile.close()
            #File already in FAT
            else :
                print("File with given name already exists")
        #First word is 'get, second should be file name'
        elif command[0] == "get" :
            #Check FAT for file and count number of blocks
            fatFile = open("fat.txt", "r")
            fatLine = fatFile.readline()
            blocks = []
            while len(fatLine) != 0 :
                fatLine = fatLine.split('\n')[0]
                fatLine = fatLine.split('\t')
                if command[1] == fatLine[0] :
                    blocks.append(fatLine[0]+":"+fatLine[1]+":"+fatLine[2])
                fatLine = fatFile.readline()
            fatFile.close()
            #File found, retrieve
            if len(blocks) > 0 :
                getFile = open(command[1], "ab")
                error = 0
                for i in blocks :
                    fileBlockEntry = i.split(':')
                    blockName = fileBlockEntry[0]+".b"+fileBlockEntry[1]
                    #If block is local, copy to node directory
                    if fileBlockEntry[2] == thisNode :
                        subprocess.call(["cp", "./files/"+blockName, "."])
                    else :
                        error = subprocess.call(["./client", "r", blockName, fileBlockEntry[2]])
                    blockFile = open(blockName, "rb")
                    getFile.write(blockFile.read())
                    os.remove(blockName)
                getFile.close()
            #File not found
            else :
                print("File not found\n")
        #Default
        else :
            print("Unknown command\n")
print ("exit")
