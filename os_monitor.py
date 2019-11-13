# -*- coding: utf-8 -*-
# Copyright 2019, AVATech
#
# Author Harold.Duan
# This module is os monitor operator.

__author__ = 'Harold.Duan'
__all__ = ['get_sys_info']

import json
from marshmallow import Schema, fields
import psutil

class SystemInfo(object):
    os_info = {}
    cpu_info = {}
    memory_info = {}
    disk_info = []
    net_info = {}
    pids = []
    pass

class SystemInfoSchema(Schema):
    os_info = fields.Dict()
    cpu_info = fields.Dict()
    memory_info = fields.Dict()
    disk_info = fields.List(fields.Dict())
    net_info = fields.Dict()
    pids = fields.List(fields.Dict())

sys_info = SystemInfo()
schema_sys_info = SystemInfoSchema()

def get_sys_info():
    try:
        sys_info.os_info = __get_os_info()
        sys_info.cpu_info = __get_cpu_info()
        sys_info.memory_info = __get_memory_info()
        sys_info.disk_info = __get_disk_info()
        sys_info.net_info = __get_net_info()
        sys_info.pids = __get_pids()
        ret_data = schema_sys_info.dump(sys_info)
        return ret_data
        pass
    except Exception as e:
        pass
    pass

def __get_os_info():
    try:
        data = psutil.os.uname()
        if data:
            ret_data = {
                'nodename':data.nodename,
                'sysname':data.sysname,
                'machine':data.machine,
                'release':data.release,
                'version':data.version
            }
        return ret_data
        pass
    except Exception as e:
        print(e)
        pass
    pass

def __get_cpu_info():
    try:
        core = psutil.cpu_count()
        logical_core = psutil.cpu_count(logical=True)
        cpu_times = psutil.cpu_times()
        ret_data = {
            'core':core,
            'logical_core':logical_core,
            'user':cpu_times.user,
            'nice':cpu_times.nice,
            'system':cpu_times.system,
            'idle':cpu_times.idle
        }
        return ret_data
        pass
    except Exception as e:
        print(e)
        pass
    pass

def __get_memory_info():
    try:
        virtual = psutil.virtual_memory()
        swap = psutil.swap_memory()
        ret_data = {
            'virtual_memory':
            {
                'total':virtual.total,
                'available':virtual.available,
                'percent':virtual.percent,
                'used':virtual.used,
                'free':virtual.free,
                'active':virtual.active
            },
            'swap_memory':
            {
                'total':swap.total,
                'used':swap.used,
                'free':swap.free,
                'percent':swap.percent,
                'sin':swap.sin,
                'sout':swap.sout
            }
        }
        return ret_data
        pass
    except Exception as e:
        print(e)
        pass
    pass

def __get_disk_info():
    try:
        partitions = psutil.disk_partitions()
        ret_data = []
        if partitions:
            for i in partitions:
                f =  psutil.disk_usage(i.mountpoint)
                if f:
                    ret_data.append(
                        {
                            'device':i.device,
                            'mountpoint':i.mountpoint,
                            'fstype':i.fstype,
                            'disk_usage_total':f.total,
                            'disk_usage_used':f.used,
                            'disk_usage_free':f.free,
                            'disk_usage_percent':f.percent
                        }
                    )
            pass
        return ret_data
        pass
    except Exception as e:
        print(e)
        pass
    pass

def __get_net_info():
    try:
        addrs = psutil.net_if_addrs()
        if addrs:
            for i in addrs.values():
                for j in i:
                    if j.netmask == '255.255.255.0':
                        io = psutil.net_io_counters()
                        ret_data = {
                            'address':j.address,
                            'bytes_sent':io.bytes_sent,
                            'bytes_recv':io.bytes_recv,
                            'packets_sent':io.packets_sent,
                            'packets_recv':io.packets_recv
                        }
                        break
                        pass
                    pass
            pass
        # connect = psutil.net_connections()
        return ret_data
        pass
    except Exception as e:
        print(e)
        pass
    pass

def __get_pids():
    try:
        pids = psutil.pids()
        ret_data = []
        if pids:
            for i in pids:
                try:
                    p = psutil.Process(i)
                    ret_data.append(
                        {
                            'id':i,
                            'name':p.name(),
                            'exe':p.exe(),
                            'cwd':p.cwd(),
                            'cmdline':p.cmdline(),
                            'ppid':p.ppid(),
                            # 'parent':p.parent(),
                            # 'children':p.children(),
                            'status':p.status(),
                            'username':p.username(),
                            'create_time':p.create_time(),
                            'terminal':p.terminal(),
                            # 'cpu_times':p.cpu_times(),
                            # 'memory_info':p.memory_info(),
                            'open_files':p.open_files(),
                            'connections':p.connections(),
                            'num_threads':p.num_threads()
                            # 'threads':p.threads()
                        }
                    )
                    pass
                except (psutil.ZombieProcess, psutil.AccessDenied, psutil.NoSuchProcess):
                    continue
                pass
            pass
        return ret_data
        pass
    except Exception as e:
        print(e)
        pass