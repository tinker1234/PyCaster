import termcolor
import time
colored = termcolor.colored

_log = list()

def Log(msg, evt="info"):
    if evt == 0: evt = "info"
    if evt == 1: evt = "warn"
    if evt == 2: evt = "err"
    f = open("log/PyCaster.log", "r")
    for line in f.readlines():
        _log.append(line.strip())
    f.close()
    m = ""
    if evt == "info":
        m = '[INF] - '+ time.ctime() + " " + msg
        return '['+colored("INF", 'green')+'] - ' + colored(time.ctime(), 'magenta', attrs=['underline']) + " "+ colored(msg, color="cyan")

    elif evt == "err":
        m = '[ERR] - ' + time.ctime() + " " + msg
        return '['+colored("ERR", 'red')+'] - ' + colored(time.ctime(), 'magenta', attrs=['underline']) + " "+ colored(msg, color="red")
    elif evt == "warn":
        m = '[WRN] - ' + time.ctime() + " " + msg
        return '['+colored("WRN", 'yellow')+'] - ' + colored(time.ctime(), 'magenta', attrs=['underline']) + " "+ colored(msg, color="yellow")
    if len(_log) == 0:
        _log.append(m)
        f=open("log/PyCaster.log", 'w')
        f.write("LOG STARTED: " + time.ctime() + '\n' + m)
        f.close()
    else:
        _log.append(m)
        f = open("log/PyCaster.log", 'w')
        f.write('\n'.join(_log))
        f.close()

def log(msg, evt="info"):
    print(Log(msg, evt))
