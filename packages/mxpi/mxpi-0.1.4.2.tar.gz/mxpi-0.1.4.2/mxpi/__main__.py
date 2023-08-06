import sys,os,socket
import argparse
from rich.console import Console
import mxpi,platform


def cmds(cmd):
    os.system(cmd)

def get_host_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            #print(ip)
            return ip
        finally:
            s.close()

def main():
    parser = argparse.ArgumentParser()
    parser.description='You can specify ip and port'
    parser.add_argument("-b", "--ip", help="Ip Address", default=False)
    parser.add_argument("-p", "--post", help="Access Port", default=False)
    parser.add_argument("-r", "--run", help="Run Program", default=False)
    args = parser.parse_args()
    if args.run==False:
        if args.ip==False:
            ip=get_host_ip()
        else:
            ip=args.ip
        if args.post==False:
            post='80'
        else:
            post=args.post

        console = Console()
        console.print("Welcome to MxPi(0.1.4)!:smiley:   System:"+platform.system()+"   IP: "+ip+":"+post,style="bold red")
        console.print("Press Ctrl+c to exit!",style="bold red")
        if(platform.system()=='Windows'):
            cmds('cd '+os.path.dirname(mxpi.__file__)+' & daphne mxpi.app.asgi:django_application -b '+ip+" -p "+post)
        else:
            cmds('cd '+os.path.dirname(mxpi.__file__)+' & sudo daphne mxpi.app.asgi:django_application -b '+ip+" -p "+post)
    else:
        if(platform.system()=='Windows'):
            cmds('python '+os.path.abspath(os.path.dirname(mxpi.__file__))+'/file/test.py')
        else:
            cmds('sudo python3 '+os.path.abspath(os.path.dirname(mxpi.__file__))+'/file/test.py')
