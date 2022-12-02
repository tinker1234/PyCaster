import time
from termcolor import colored
import config

_log = list()

def Log(msg, evt="info"):
    global _log
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
        s = "[INF] - LOG STARTED: " + time.ctime() + '\n' + m
        _log.append(s)
        f=open(config.PyCasterLogFile, 'w')
        f.write(s)
        f.close()
    else:
        _log.append(m)
        f = open(config.PyCasterLogFile, 'w')
        f.write('\n'.join(_log))
        f.close()
    return ret
 
def log(msg, evt="info"):
    print(Log(msg, evt))
