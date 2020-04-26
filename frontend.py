from flask import Flask, request, render_template, json
from ipaddress import ip_address, ip_network
from engine.objects.ftd.ftd_host_object import FtdHostObject
from engine.objects.ftd.ftd_fqdn_object import FtdFqdnObject
from engine.objects.ftd.ftd_network_object import FtdNetworkObject
from engine.objects.ftd.ftd_range_object import FtdRangeObject
from engine.objects.asa.asa_host_object import AsaHostObject
from engine.objects.asa.asa_fqdn_object import AsaFqdnObject
from engine.objects.asa.asa_network_object import AsaNetworkObject
from engine.objects.asa.asa_range_object import AsaRangeObject

from engine.managers.device import DeviceTypes
from hosts import HOSTS

app = Flask(__name__)

FTD_ADDRESS = "10.62.18.27"
ASA_ADDRESS = "10.62.18.24"


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/host', methods=['GET', 'POST'])
def host():
    ip_addr = ''
    name = ''

    device_list = []
    result_list = []
    output_list=[]

    if request.method == 'POST':
        ip_addr = request.form.get('ip_addr')
        name = request.form.get('name')

        if len(name) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaHostObject(origin_address=x.ip_addr, obj_name=name))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdHostObject(origin_address=x.ip_addr, ip_addr=ip_address(ip_addr)))
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

        for x in device_list:
            x.fetch_config()
            obj = x.usage()
            result_list.append(obj)

            output = 'Name: ' + str(obj.obj_name) +'\n'+ ' | Origin Address: '+ str(obj.origin_addr)+ '\n'+' | ACL: '+ str(obj.acl_list).strip('[]')+'\n'+' | DNS: '+ str(obj.dns)+ '\n' +' | NTP: ' + str(obj.ntp)+'\n\n'
            output_list.append(output)
            print(output)

    return render_template("host.html", ip_addr=ip_addr, name=name, output_list=output_list)



@app.route('/fqdn', methods=['GET', 'POST'])
def fqdn():
    fqdn_str=''
    device_list= []
    result_list=[]
    output_list=[]
    if request.method == "POST":
        fqdn_str = request.form.get('fqdn_str')

        if len(fqdn_str) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaFqdnObject(origin_address=x.ip_addr, fqdn=fqdn_str))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdFqdnObject(origin_address=x.ip_addr, fqdn=fqdn_str))
        else:
            fqdn_str='Empty field'

        for x in device_list:
            x.fetch_config()
            obj = x.usage()
            result_list.append(obj)

            output = 'Name: ' + str(obj.obj_name) +'\n'+ ' | Origin Address: '+ str(obj.origin_addr)+ '\n'+' | ACL: '+ str(obj.acl_list).strip('[]')+'\n'+' | DNS: '+ str(obj.dns)+ '\n' +' | NTP: ' + str(obj.ntp)+'\n\n'
            output_list.append(output)
            print(output)
        
    return render_template('fqdn.html', fqdn_str=fqdn_str, output_list=output_list) 


@app.route('/rangeof', methods=['GET','POST'])
def rangeof():
    first = ''
    last = ''
    result_list = []
    device_list = []
    output_list=[]

    if request.method == "POST":
        lst = request.form.getlist('values')
        first = str(lst[0])
        last = str(lst[1])

        if len(first) and len(last) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaRangeObject(origin_address=x.ip_addr, first=ip_address(lst[0]), last=ip_address(lst[1])))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdRangeObject(origin_address=x.ip_addr, first=ip_address(lst[0]), last=ip_address(lst[1])))
        else:
            first = 'Please fill out both fields'
            last = 'Please fill out both fields'

        for x in device_list:
            x.fetch_config()
            obj = x.usage()
            result_list.append(obj)

            output = 'Name: ' + str(obj.obj_name) +'\n'+ ' | Origin Address: '+ str(obj.origin_addr)+ '\n'+' | ACL: '+ str(obj.acl_list).strip('[]')+'\n'+' | DNS: '+ str(obj.dns)+ '\n' +' | NTP: ' + str(obj.ntp)+'\n\n'
            output_list.append(output)
            print(output)

    return render_template('rangeof.html', first=first, last=last, output_list=output_list) 


@app.route('/network', methods=['GET', 'POST'])
def network():
    result_list = []
    device_list = []
    prefix = ''
    output_list=[]

    if request.method == "POST":
        prefix = request.form.get('prefix')
        
        if len(prefix) != 0:
            for x in HOSTS:
                if x.type == DeviceTypes.ASA:
                    device_list.append(AsaNetworkObject(origin_address=x.ip_addr, prefix=ip_network(prefix)))
                elif x.type == DeviceTypes.FTD:
                    device_list.append(FtdNetworkObject(origin_address=x.ip_addr, prefix=ip_network(prefix)))
        else:
            prefix = 'Empty field'

        for x in device_list:
            x.fetch_config()
            obj = x.usage()
            result_list.append(obj)

            output = 'Name: ' + str(obj.obj_name) +'\n'+ ' | Origin Address: '+ str(obj.origin_addr)+ '\n'+' | ACL: '+ str(obj.acl_list).strip('[]')+'\n'+' | DNS: '+ str(obj.dns)+ '\n' +' | NTP: ' + str(obj.ntp)+'\n\n'
            output_list.append(output)
            print(output)

    return render_template('network.html', prefix=prefix, output_list=output_list)
       

app.run()