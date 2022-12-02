import time
from termcolor import colored
import config

_log = list()

def Log(msg, evt="info"):
    f = open(config.PyCasterLogFile, "r")
    for line in f.readlines():
        _log.append(line.strip())
    f.close()
    m = ""
    if evt == "info":
        m = '[INF] - '+ time.ctime() + " " + msg
        ret = '['+colored("INF", 'green')+'] - ' + colored(time.ctime(), 'magenta', attrs=['underline']) + " "+ colored(msg, color="cyan")

    elif evt == "err":
        m = '[ERR] - ' + time.ctime() + " " + msg
        ret = '['+colored("ERR", 'red')+'] - ' + colored(time.ctime(), 'magenta', attrs=['underline']) + " "+ colored(msg, color="red")
    elif evt == "warn":
        m = '[WRN] - ' + time.ctime() + " " + msg
        ret = '['+colored("WRN", 'yellow')+'] - ' + colored(time.ctime(), 'magenta', attrs=['underline']) + " "+ colored(msg, color="yellow")
    if len(_log) == 0:
        _log.append(m)
        f=open(config.PyCasterLogFile, 'w')
        f.write("LOG STARTED: " + time.ctime() + '\n' + m)
        f.close()
    else:
        _log.append(m)
        f = open(config.PyCasterLogFile, 'w')
        f.write('\n'.join(_log))
        f.close()
 
def log(msg, evt="info"):
    print(Log(msg, evt))
