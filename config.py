def setConfig(configData) :
    configFile = open("config.txt", "r")
    config = configFile.readline()
    while len(config) != 0:
        if config[0] != '#' :
            break
        else :
            config = configFile.readline()
    config = config.split(':')
    configData.append(int(config[0]))
    configData.append(config[1])
    config = configFile.readline()
    while len(config) != 0:
        if config[0] == '#' :
            config = configFile.readline()
        else :
            configData.append(config.split('\n')[0])
            config = configFile.readline()
    configFile.close()
