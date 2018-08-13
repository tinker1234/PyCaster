import time


_log = list()

def log(msg, evt="info"):
    f = open("log/PyCasterServer.log", "r")
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
        f=open("log/PyCasterServer.log", 'w')
        f.write("LOG STARTED: " + time.ctime() + '\n' + m)
        f.close()
    else:
        _log.append(m)
        f = open("log/PyCasterServer.log", 'w')
        f.write('\n'.join(_log))
        f.close()