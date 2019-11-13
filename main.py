# -*- coding: utf-8 -*-
# Copyright 2019, AVATech
#
# Author Harold.Duan
# This module is web api startup.

from web import app

if __name__ == "main":
    try:
        app.run(threaded=True)
        pass
    except Exception as e:
        pass