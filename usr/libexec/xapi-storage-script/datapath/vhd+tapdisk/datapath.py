#!/usr/bin/env python

import urlparse
import os
import sys
import xapi
import xapi.storage.api.v5.datapath
import xapi.storage.api.v5.volume
import importlib
from xapi.storage.libs.libcow.datapath import TapdiskDatapath
from xapi.storage import log


def get_sr_callbacks(dbg, uri):
    u = urlparse.urlparse(uri)
    sr = u.netloc
    sys.path.insert(
        0,
        '/usr/libexec/xapi-storage-script/volume/org.xen.xapi.storage.' + sr)
    mod = importlib.import_module(sr)
    return mod.Callbacks()


class Implementation(xapi.storage.api.v5.datapath.Datapath_skeleton):

    def activate(self, dbg, uri, domain):
        cb = get_sr_callbacks(dbg, uri)
        TapdiskDatapath.activate(dbg, uri, domain, cb)

    def attach(self, dbg, uri, domain):
        cb = get_sr_callbacks(dbg, uri)
        return TapdiskDatapath.attach(dbg, uri, domain, cb)

    def detach(self, dbg, uri, domain):
        cb = get_sr_callbacks(dbg, uri)
        TapdiskDatapath.detach(dbg, uri, domain, cb)

    def deactivate(self, dbg, uri, domain):
        cb = get_sr_callbacks(dbg, uri)
        TapdiskDatapath.deactivate(dbg, uri, domain, cb)

    def open(self, dbg, uri, persistent):
        cb = get_sr_callbacks(dbg, uri)
        TapdiskDatapath.epc_open(dbg, uri, persistent, cb)
        return None

    def close(self, dbg, uri):
        cb = get_sr_callbacks(dbg, uri)
        TapdiskDatapath.epc_close(dbg, uri, cb)
        return None


if __name__ == "__main__":
    log.log_call_argv()
    cmd = xapi.storage.api.v5.datapath.Datapath_commandline(Implementation())
    base = os.path.basename(sys.argv[0])
    if base == "Datapath.activate":
        cmd.activate()
    elif base == "Datapath.attach":
        cmd.attach()
    elif base == "Datapath.close":
        cmd.close()
    elif base == "Datapath.deactivate":
        cmd.deactivate()
    elif base == "Datapath.detach":
        cmd.detach()
    elif base == "Datapath.open":
        cmd.open()
    else:
        raise xapi.storage.api.v5.datapath.Unimplemented(base)
