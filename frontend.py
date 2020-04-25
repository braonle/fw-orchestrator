from flask import Flask, request, render_template_string, render_template
from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network
from engine.objects.base_objects import HostObject, FqdnObject, NetworkObject, AddrRangeObject, ReturnCode 
from engine.objects.ftd.ftd_host_object import FtdHostObject
from engine.objects.ftd.ftd_fqdn_object import FtdFqdnObject
from engine.objects.ftd.ftd_network_object import FtdNetworkObject
from engine.objects.ftd.ftd_range_object import FtdRangeObject
from engine.objects.base_objects import ReturnCode
from engine.objects.asa.asa_host_object import AsaHostObject
from engine.objects.asa.asa_fqdn_object import AsaFqdnObject
from engine.objects.asa.asa_network_object import AsaNetworkObject
from engine.objects.asa.asa_range_object import AsaRangeObject
from engine.objects.base_objects import ReturnCode


app = Flask(__name__)

FTD_ADDRESS = "10.62.18.27"
ASA_ADDRESS = "10.62.18.24"
#192.168.0.100

@app.route('/')
def index():
    return render_template('main.html')



@app.route('/host', methods=['GET', 'POST'])
def host():
    ip_addr = ''

    ftd_list= []
    if request.method == 'POST':
        ip_addr = request.form.get('ip_addr')

        obj = AsaHostObject(origin_address=ASA_ADDRESS, ip_addr=ip_address(ip_addr))
        obj.fetch_config()

        ftd_list = [str(obj.fetch_config()),str(obj.name)]
        print(str(obj.ip_addr) + " -> " + str(obj.name))

    return render_template("host.html", ip_addr=ip_addr, ftd_list=ftd_list)



@app.route('/fqdn', methods=['GET', 'POST'])
def fqdn():
    ftd_list= []
    if request.method == "POST":
        fqdn = request.form.get('fqdn')
        obj = AsaFqdnObject(origin_address=ASA_ADDRESS, fqdn=fqdn)
        obj.fetch_config()

        ftd_list = [str(obj.fetch_config()),str(obj.name)]
        print(str(obj.fqdn) + " -> " + str(obj.name))
        
    return render_template('fqdn.html', ftd_list=ftd_list) 




@app.route('/rangeof', methods=['GET','POST'])
def rangeof():
    first=''
    last=''
    ftd_list=[]
    if request.method == "POST":
        lst = request.form.getlist('values')
        first = str(lst[0])
        last = str(lst[1])

        obj = AsaRangeObject(origin_address=ASA_ADDRESS, first=ip_address(lst[0]), last=ip_address(lst[1]))
        obj.fetch_config()
        
        ftd_list = [str(obj.fetch_config()),str(obj.name)]
        print(str(obj.first_addr) + " - " + str(obj.last_addr) + " -> " + str(obj.name))

    return render_template('rangeof.html', first=first, last=last, ftd_list=ftd_list) 




@app.route('/network', methods=['GET', 'POST'])
def network():
    ftd_list=''
    prefix=''
    if request.method == "POST":
        prefix = request.form.get('prefix')
        
        obj = AsaNetworkObject(origin_address=ASA_ADDRESS, prefix=ip_network(prefix))

        obj.fetch_config()
        ftd_list = [str(obj.fetch_config()),str(obj.name)]
        print(str(obj.prefix) + " -> " + str(obj.name))

    return render_template('network.html',prefix=prefix, ftd_list=ftd_list) 
       

app.run()