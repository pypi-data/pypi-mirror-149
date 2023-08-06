#!/usr/bin/env python3
# This file is placed in the Public Domain.


"commands"


import threading
import time


from .hdl import Bus, Commands, starttime
from .irc import Config
from .obj import Class, Db, Object, edit, find, format, get, last, save, update
from .rpt import elapsed
from .thr import getname


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


Class.add(Log)


def cmd(event):
    event.reply(",".join(sorted(Commands.cmd)))


Commands.add(cmd)


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Bus.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))


Commands.add(flt)


def fnd(event):
    if not event.args:
        db = Db()
        res = ",".join(
            sorted({x.split(".")[-1].lower() for x in db.types()}))
        if res:
            event.reply(res)
        else:
            event.reply("no types yet.")
        return
    bot = event.bot()
    otype = event.args[0]
    res = list(find(otype))
    if bot.cache:
         if len(res) > 3:
             bot.extend(event.channel, [x[1].txt for x in res])
             bot.say(event.channel, "%s left in cache, use !mre to show more" % bot.cache.size())
             return
    nr = 0
    for _fn, o in res:
        txt = "%s %s" % (str(nr), format(o))
        nr += 1
        event.reply(txt)
    if nr:
        event.reply("no result")


Commands.add(fnd)


def log(event):
    if not event.rest:
        event.reply("log <txt>")
        return
    o = Log()
    o.txt = event.rest
    save(o)
    event.reply("ok")


Commands.add(log)


def thr(event):
    result = []
    for t in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(t).startswith("<_"):
            continue
        o = Object()
        update(o, vars(t))
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        result.append((up, t.getName()))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s(%s)" % (txt, elapsed(up)))
    if res:
        event.reply(" ".join(res))


Commands.add(thr)
