import os
import shutil

#Raspberry Pi Cluster IP/hostname Generator Tool- ipconfgen V1.0
#Created by Yuan Wang <bg3mdo@gmail.com>
#
#Copyright (C) 2019 by Yuan Wang BG3MDO
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Library General Public
#License as published by the Free Software Foundation; either
#version 2 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Library General Public License for more details.
#
#You should have received a copy of the GNU Library General Public
#License along with this library; if not, write to the
#Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
#Boston, MA  02110-1301, USA.

script_path = os.path.dirname(os.path.abspath( __file__ ))

host_name = "pifarm_c"
node_name_st_no = 1
node_no = 25
node_st_ip = 10
node_preip = "192.168.100"
node_mask = 24
node_gateway = "192.168.100.1"
node_dns1 = "192.168.100.1"
node_dns2 = ""

confs_folder = "confs"
confs_abspath = script_path + "/" + confs_folder

print("Raspberry Pi Cluster IP/hostname Generator Tool- ipconfgen V1.0")
print("Created by Yuan Wang <bg3mdo@gmail.com>")
print("Under GNU Library General Public License.")
print("")

# Read dhcpcd.conf templet file
try:
    dhcpcd_f = open("dhcpcd.conf", "r")
    dhcpcd_templet = dhcpcd_f.read();
    print("read dhcpcd.conf templet successfully.")
except Exception as e:
    print("cannot read the dhcpcd.conf templet, do you have it in the folder?")
    print(e)
    exit()

if(os.path.isdir(confs_abspath)):
    try:
        shutil.rmtree(confs_abspath)
        print("found 'confs', now removing it.")
    except Exception as e:
        print("cannot remove the 'confs' folder!")
        print(e)
        exit()
    try:
        os.mkdir(confs_abspath)
        print("created a new 'confs' folder.")
    except Exception as e:
        print("cannot create 'confs' folder!")
        print(e)
        exit()
else:
    try:
        os.mkdir(confs_abspath)
        print("created a new 'confs' folder.")
    except Exception as e:
        print("cannot create 'confs' folder!")
        print(e)
        exit()

for i in range (node_name_st_no, node_no + 1):
    try:
        os.mkdir(confs_abspath + "/" + host_name + str(i))
        print("created a new node configration folder.")
    except Exception as e:
        print("cannot create node configration folders!")
        print(e)
        exit()
    try:
        file_dhcpcd = open(confs_abspath + "/" + host_name + str(i) + "/dhcpcd.conf", "w")
        file_dhcpcd.writelines(dhcpcd_templet)
        file_dhcpcd.write("\n")
        file_dhcpcd.write("#Static IP configration, generated by ipconfgen, Yuan Wang <bg3mdo@gmail.com>\n")
        file_dhcpcd.write("interface eth0\n")      
        file_dhcpcd.write("static ip_address=" + node_preip + "." + str(node_st_ip + i - 1) + "/" + str(node_mask) + "\n")
        file_dhcpcd.write("static routers=" + node_gateway + "\n")
        file_dhcpcd.write("static domain_name_servers=" + node_dns1 + " " + node_dns2 + "\n")  
        file_dhcpcd.close();
        print("created a node dhcpcd.conf successfully.")
    except Exception as e:
        print("cannot create a node dhcpcd.conf!")
        print(e)
        exit()
    try:
        file_host = open(confs_abspath + "/" + host_name + str(i) + "/hostname", "w")
        file_host.write(host_name + str(node_name_st_no + i - 1) + "\n")
        file_host.close();
        print("created a node hostname successfully.")
    except Exception as e:
        print("cannot create a node hostname!")
        print(e)
        exit()

print ("Job done :)");
