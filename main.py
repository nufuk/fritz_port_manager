#!./venv/bin/python
from fritzconnection import FritzConnection
from fritzconnection.core.exceptions import FritzConnectionException
import argparse


parser = argparse.ArgumentParser(description="Fritzbox Portfreigabe script",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-m", "--mode",  choices=['open', 'close'], required=True, help="Choose between opening or closing a port forwarding")
parser.add_argument("-u", "--username", required=True, help="username for your fritzbox")
parser.add_argument("-p", "--password", required=True, help="password for the fritzbox user")
parser.add_argument("-l", "--fritz_port", default="49443", type=int, help="port for the fritzbox")
parser.add_argument("-f", "--fritz_ip", default="192.168.178.1", help="IP of your fritzbox")
parser.add_argument("-a", "--fritz_action", default="WANPPPConnection1", help="which action to use")
parser.add_argument("-t", "--use_tls", action="store_false", help="turn off use tls")
parser.add_argument("-r", "--protocol", choices=['TCP', 'UDP'], default="TCP", help="choose which port")
parser.add_argument("-i", "--in_port", required=True, type=int, help="Port reachable from the internet")
parser.add_argument("-o", "--out_port", required=True, type=int, help="Port inside your network")
parser.add_argument("-s", "--server_ip", required=True, help="ip of the endpoint for the port forwarding")
parser.add_argument("-d", "--description", required=True, help="description of your Port forwarding")

args = vars(parser.parse_args())

mode = args["mode"]

def main(args):
    print(args)
    username = args["username"]
    password = args["password"]
    fritz_port = args["fritz_port"]
    fritz_ip = args["fritz_ip"]
    fritz_action = args["fritz_action"]
    use_tls = args["use_tls"]
    protocol = args["protocol"]
    in_port = args["in_port"]
    out_port = args["out_port"]
    server_ip = args["server_ip"]
    description = args["description"]
    fritz_function = ""
    PortInfos = {}

    if mode == 'open':
        fritz_function = "AddPortMapping"
        PortInfos['NewEnabled'] = 1
        PortInfos['NewExternalPort'] = in_port
        PortInfos['NewInternalClient'] = server_ip
        PortInfos['NewInternalPort'] = out_port
        PortInfos['NewLeaseDuration'] = 0
        PortInfos['NewPortMappingDescription'] = description
        PortInfos['NewProtocol'] = protocol
        PortInfos['NewRemoteHost'] = ''
    elif mode == 'close':
        fritz_function = "DeletePortMapping"
        PortInfos['NewExternalPort'] = in_port
        PortInfos['NewProtocol'] = protocol
        PortInfos['NewRemoteHost'] = ''
 

    try:
        fc = FritzConnection(address=fritz_ip, user=username, password=password, port=fritz_port, use_tls=use_tls)
        fc.call_action(fritz_action, fritz_function, **PortInfos)
        
    except FritzConnectionException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main(args)