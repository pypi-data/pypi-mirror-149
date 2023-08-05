from colorama import init, Fore
import datetime

init(autoreset=True)
time = datetime.datetime.now()
levelColor = {
    'debug': Fore.BLUE,
    'info': Fore.BLACK,
    'warn': Fore.YELLOW,
    'error': Fore.LIGHTRED_EX,
    'critical': Fore.RED
}

def log(level, logMessage):
    if not level in levelColor.keys():
        print(f'{Fore.LIGHTGREEN_EX}[ {time.hour}:{time.minute}:{time.second} ] {level.upper()}: {logMessage}')

    else:
        color = levelColor.get(level.lower())

        if level.lower() == 'critical':
            print(f'{color}[ {time.hour}:{time.minute}:{time.second} ] {level.upper()}: {logMessage}')
            exit(1)

        print(f'{color}[ {time.hour}:{time.minute}:{time.second} ] {level.upper()}: {logMessage}')