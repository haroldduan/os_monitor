# -*- coding: utf-8 -*-
# Copyright 2019, AVATech
#
# Author Harold.Duan
# This module is REST API service implements.

import sys
from flask import Flask,render_template,request,json,jsonify
from os_monitor import get_sys_info

app = Flask(__name__)

@app.route('/')
def index():
    try:
        ret_data = get_sys_info()
        return jsonify(ret_data)
    except Exception as e:
        pass