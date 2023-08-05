import datetime

time = datetime.datetime.now()

def createLogger(fileName):
    global logFile
    logFile = fileName

def save(level, logMessage):
    with open(logFile, 'a+') as fileObject:
        fileObject.write(f'[ {time.hour}:{time.minute}:{time.second} ] {level.upper()}: {logMessage}\n')