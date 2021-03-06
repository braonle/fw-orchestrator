#
#	Copyright (c) 2020 Cisco and/or its affiliates.
#
#	This software is licensed to you under the terms of the Cisco Sample
#	Code License, Version 1.1 (the "License"). You may obtain a copy of the
#	License at
#
#		       https://developer.cisco.com/docs/licenses
#
#	All use of the material herein must be in accordance with the terms of
#	the License. All rights not expressly granted by the License are
#	reserved. Unless required by applicable law or agreed to separately in
#	writing, software distributed under the License is distributed on an "AS
#	IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#	or implied.
#
import multiprocessing as mp
from typing import List
from flask import Flask, request, render_template
from ipaddress import ip_address, ip_network
from engine.objects.base_objects import FwObject
from engine.objects.ftd.ftd_host_object import FtdHostObject
from engine.objects.ftd.ftd_fqdn_object import FtdFqdnObject
from engine.objects.ftd.ftd_network_object import FtdNetworkObject
from engine.objects.ftd.ftd_range_object import FtdRangeObject
from engine.objects.asa.asa_host_object import AsaHostObject
from engine.objects.asa.asa_fqdn_object import AsaFqdnObject
from engine.objects.asa.asa_network_object import AsaNetworkObject
from engine.objects.asa.asa_range_object import AsaRangeObject
from engine.objects.device import DeviceTypes
from frontend.web.mp_support import mp_get_object_usage
from hosts import HOSTS


app = Flask(__name__)
pool = mp.Pool(mp.cpu_count())

def get_object_usage(device_list: List[FwObject]) -> List[str]:
    output_list = pool.map(mp_get_object_usage, device_list)
    output_list = list(filter(lambda a: a != "", output_list))
    return output_list


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/host', methods=['GET', 'POST'])
def host():
    device_list = []
    output_list = []
    ip_addr = name = ''

    if request.method == 'POST':
        ip_addr = request.form.get('ip_addr')
        name = request.form.get('name')

        if len(name) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaHostObject(origin_address=x.ip_addr, obj_name=name))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdHostObject(origin_address=x.ip_addr, obj_name=name))
        else:
            name = 'Empty hostname'

        if len(ip_addr) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaHostObject(origin_address=x.ip_addr, ip_addr=ip_address(ip_addr)))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdHostObject(origin_address=x.ip_addr, ip_addr=ip_address(ip_addr)))
        else:
            ip_addr = 'Empty address'

        output_list = get_object_usage(device_list)

    return render_template("host.html", ip_addr=ip_addr, name=name, output_list=output_list)


@app.route('/fqdn', methods=['GET', 'POST'])
def fqdn():
    fqdn_str = ''
    device_list = []
    output_list = []
    name=''

    if request.method == "POST":
        fqdn_str = request.form.get('fqdn_str')
        name = request.form.get('name')

        if len(name) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaFqdnObject(origin_address=x.ip_addr, obj_name=name))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdFqdnObject(origin_address=x.ip_addr, obj_name=name))
        else:
            name = 'Empty field'

        if len(fqdn_str) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaFqdnObject(origin_address=x.ip_addr, fqdn=fqdn_str))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdFqdnObject(origin_address=x.ip_addr, fqdn=fqdn_str))
        else:
            fqdn_str = 'Empty field'

        output_list = get_object_usage(device_list)
        
    return render_template('fqdn.html', name=name, fqdn_str=fqdn_str, output_list=output_list) 


@app.route('/rangeof', methods=['GET', 'POST'])
def rangeof():
    device_list = []
    output_list = []
    first = last = ''
    name = ''

    if request.method == "POST":
        lst = request.form.getlist('values')
        first = str(lst[0])
        last = str(lst[1])
        name = request.form.get('name')

        if len(name) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaHostObject(origin_address=x.ip_addr, obj_name=name))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdHostObject(origin_address=x.ip_addr, obj_name=name))
        else:
            name = 'Empty field'


        if len(first) and len(last) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaRangeObject(origin_address=x.ip_addr, first=ip_address(lst[0]), last=ip_address(lst[1])))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdRangeObject(origin_address=x.ip_addr, first=ip_address(lst[0]), last=ip_address(lst[1])))
        else:
            first = 'Please fill out both fields'
            last = 'Please fill out both fields'

        output_list = get_object_usage(device_list)

    return render_template('rangeof.html', first=first, last=last, name=name, output_list=output_list) 


@app.route('/network', methods=['GET', 'POST'])
def network():
    device_list = []
    output_list = []
    prefix = ''
    name=''

    if request.method == "POST":
        prefix = request.form.get('prefix')
        name = request.form.get('name')

        if len(name) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaHostObject(origin_address=x.ip_addr, obj_name=name))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdHostObject(origin_address=x.ip_addr, obj_name=name))
        else:
            name = 'Empty field'


        if len(prefix) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaNetworkObject(origin_address=x.ip_addr, prefix=ip_network(prefix)))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdNetworkObject(origin_address=x.ip_addr, prefix=ip_network(prefix)))
        else:
            prefix = 'Empty field'

        output_list = get_object_usage(device_list)

    return render_template('network.html', name=name, prefix=prefix, output_list=output_list)
