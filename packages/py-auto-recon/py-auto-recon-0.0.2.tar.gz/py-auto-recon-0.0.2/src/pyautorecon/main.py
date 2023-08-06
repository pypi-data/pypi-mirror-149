# Import Everthing Here
import argparse
import os
import socket
import time
import xml.etree.ElementTree as ET
from multiprocessing import Process
from typing import Optional
from typing import Sequence

from rich import print
from rich.console import Console

console = Console()

# Assuming no services
svc = {}

# Main Function
def main(argv: Optional[Sequence[str]] = None) -> None:
    def script_end(sysname) -> None:
        print("Thank you for using our script\nPython Recon Team.")
        os.system(f"rm -r {sysname}")
        os.system("reset")
        exit()

    # Checking for root access
    if os.geteuid() != 0:
        os.system("[red]Please run as root.[/red]")
        exit()

    # Argument Parsing
    parser = argparse.ArgumentParser()

    # Adding Arguments to pass to functions
    parser.add_argument(
        "-ip", type=str, help="IP to run scans on, do not enter range.", required=True
    )
    parser.add_argument(
        "-sys",
        type=str,
        help="Enter a identifier of the system for the report to be generated.",
        required=True,
    )
    parser.add_argument(
        "-l",
        type=int,
        help="Enter the level of enumeration. Range is 1 to 5. Default is 2",
        default=2,
    )

    # Processing Arguments
    args = parser.parse_args(argv)

    # Defining variables from argument parser variables
    sysname = args.sys
    ip = args.ip
    level = args.l

    # Welcome Print Message
    os.system("clear")
    print("[white]#Welcome to All-In-One Python Recon Script[white]")
    print("[white]##You can check the report_<machine_name>.txt for output.[/white]")
    print(
        "[white]We are not responsible for any damages or laws broken by running this script.[/white]"
    )
    time.sleep(2)

    # Creating necessary dir's
    os.system("clear")
    os.system(f"mkdir {sysname}")
    reportname = "report_" + sysname + ".txt"

    # Creating report file
    f = open(reportname, "a")

    level = int(level)

    if level == 1:
        phase1(ip, sysname)
        script_end(sysname)

    elif level == 2:
        phase2(ip, sysname)
        script_end(sysname)

    elif level == 3:
        phase3(ip, sysname)
        script_end(sysname)

    elif level == 4:
        phase4(ip, sysname)
        script_end(sysname)

    elif level == 5:
        phase5(ip, sysname)
        script_end(sysname)

    else:
        print(
            "[red]The wrong level has been entered the script does not have this {level} of enumeration capabilities.\nExiting now...."
        )
        exit()


# End Of Main Function

# Phase 1 Enumeration and Parsing and HTTP Enumeration
def phase1(ip, sysname):
    def phase1results(sysname):
        print("[red]Printing phase 1 results.[/red]]")
        os.system(f"clear;cat report_{sysname}.txt")
        print("[green]Phase 2 starting[/green].........")

    def phase1parser(webapp, sysname):
        def goparser():
            # Cat to simply put gobuster output into report_{sysname}.txt
            os.system(
                f"echo '\n####################################### GOBUSTER #############################################' >> report_{sysname}.txt"
            )
            os.system(f"cat {sysname}/gobusterresults.txt >> report_{sysname}.txt")

        def niktoparser():
            # Cat to simply put gobuster output into report_{sysname}.txt
            os.system(
                f"echo '\n####################################### NIKTO ################################################' >> report_{sysname}.txt"
            )
            os.system(f"cat {sysname}/niktoresults.txt >> report_{sysname}.txt")

        def wpscanparser():
            # Cat to simply put gobuster output into report_{sysname}.txt
            os.system(
                f"echo '\n######################################## WPSCAN ###############################################' >> report_{sysname}.txt"
            )
            os.system(f"cat {sysname}/wpscanresults.txt >> report_{sysname}.txt")

        def nsescriptparser():
            # Cat to simply put gobuster output into report_{sysname}.txt
            os.system(
                f"echo '\n######################################### NMAP ################################################\n' >> report_{sysname}.txt;"
            )
            os.system(f"cat {sysname}/nsescriptresults.txt >> report_{sysname}.txt")

        portlist = []
        portstate = []
        svcname = []
        mytree = ET.parse(f"{sysname}/phase1.xml")
        myroot = mytree.getroot()
        for a in myroot.findall("host"):
            for b in a.findall("ports"):
                for c in b.findall("port"):
                    portlist.append(int(c.attrib["portid"]))
                    for d in c.findall("state"):
                        portstate.append(d.attrib["state"])
                    for e in c.findall("service"):
                        svcname.append(e.attrib["name"])

        # Code to Pretty Print To Report
        reportdir = f"report_{sysname}.txt"
        file2 = open(reportdir, "w+")
        file2.write("Initial Nmap Scan Successful!\n")
        file2.write(
            "Nmap found the following services and ports open, these will be enumerated in more details through further phases\n"
        )
        for i in range(0, len(svcname)):
            portlist[i] = int(portlist[i])
            svc[i] = {svcname[i]: portlist[i]}
            file2.write(
                f"Port Number: {portlist[i]}    Service Name: {svcname[i]}     State Of Port: {portstate[i]}\n"
            )
        file2.close()
        if webapp == 0:
            print("Webapp parser")
            time.sleep(10)
            nsescriptparser()
            wpscanparser()
            niktoparser()
            goparser()
            print("[green]Phase 1 Success[/green]")

    try:
        # Printing initiation Message
        print(
            "[green]Phase 1 Enumeration will run your basic gobuster, nikto and nmap.[green]"
        )
        print(f"IP Address Provided: {ip}           System Name: {sysname}")
        print(f"Report Will be Stored in: report_{sysname}.txt")

        # Kicking off the nmap scan in a new process.
        t1 = Process(target=nmap_main, args=(ip, 2, sysname))
        t1.start()

        # Checking for webapp on port 80
        webappstat = port_check(ip, 80)
        if webappstat == 0:
            print(
                "[yellow]We have some sign of a web application running, we'll do the tooling in the background aside nmap. You can continue manual enumeration.[/yellow]"
            )
            print(
                "[yellow]We'll show gobuster results on the screen as they come along, please hold tight.[/yellow]"
            )
            t2 = Process(
                target=http_enum,
                args=(
                    ip,
                    sysname,
                ),
            )
            t2.start()
            t1.join()
            t2.join()

            t3 = Process(target=phase1parser, args=(webappstat, sysname))
            t3.start()
            t3.join()

            # Calling Phase 1 Result Parser.
            phase1results(sysname)

        else:
            print(
                "[yellow]Port 80 is not open on the system, we're continuing phase 1 with just nmap.[/yellow]"
            )

            # Waiting for the nmap scan to get over
            t2 = Process(target=phase1parser, args=(webappstat, sysname))

            # Starting Phase 1 parser once the nmap scan is over.
            t1.join()
            t2.start()
            t2.join()

            # Phase 1 scan is over.
            print("[green]Phase 1 Success[/green]")

            # Calling Phase 1 Result Parser.
            phase1results(sysname)

    except Exception as e:
        if e:
            print(
                f"[red]The script has malfunctioned with the following error message: {e}[/red]"
            )
        else:
            print(
                "[red]Well something went wrong with the script and python isn't erroring out, use our github forum for help.[/red]"
            )


# Phase 2 Enumeration Function
def phase2(ip, sysname):
    def svccheck() -> list:
        portlist = []
        portstate = []
        svcname = []
        mytree = ET.parse(f"{sysname}/phase1.xml")
        myroot = mytree.getroot()
        for a in myroot.findall("host"):
            for b in a.findall("ports"):
                for c in b.findall("port"):
                    portlist.append(int(c.attrib["portid"]))
                    for d in c.findall("state"):
                        portstate.append(d.attrib["state"])
                    for e in c.findall("service"):
                        svcname.append(e.attrib["name"])
        return svcname

    phase1(ip, sysname)

    processes = []
    parsers = []

    svc = svccheck()

    # Try cause I'm shit at coding
    try:
        for service in svc:
            time.sleep(0.5)
            print(f"Service name: {service}")
            time.sleep(2)

            if "rpcbind" in service:
                p = Process(
                    target=rpcbind_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("rpcbind")

            elif "ftp" in service:
                p = Process(
                    target=ftp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("ftp")

            elif "telnet" in service:
                p = Process(
                    target=telnet_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("telnet")

            elif "modbus" in service:
                p = Process(
                    target=modbus_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("modbus")

            elif "rexec" in service:
                p = Process(
                    target=rexec_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("rexec")

            elif "dns" in service:
                p = Process(
                    target=dns_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("dns")

            elif "pop" in service:
                p = Process(
                    target=pop_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("pop")

            elif "msrpc" in service:
                p = Process(
                    target=msrpc_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("msrpc")

            elif "netbios" in service:
                p = Process(
                    target=netbios_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("netbios")

            elif "imap" in service:
                p = Process(
                    target=imap_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("imap")

            elif "smb" in service:
                p = Process(
                    target=smb_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("smb")

            elif "ssh" in service:
                p = Process(
                    target=ssh_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("ssh")

            elif "smtp" in service:
                p = Process(
                    target=smtp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("smtp")

            elif "whois" in service:
                p = Process(
                    target=whois_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("whois")

            elif "tftp" in service:
                p = Process(
                    target=tftp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("tftp")

            elif "finger" in service:
                p = Process(
                    target=finger_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("finger")

            elif "ntp" in service:
                p = Process(
                    target=ntp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("ntp")

            elif "snmp" in service:
                p = Process(
                    target=snmp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("snmp")

            elif "irc" in service:
                p = Process(
                    target=irc_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("irc")

            elif "bgmp" in service:
                p = Process(
                    target=firewall_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("bgmp")

            elif "ldap" in service:
                p = Process(
                    target=ldap_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("ldap")

            elif "isakmp" in service:
                p = Process(
                    target=ike_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("isakmp")

            elif "login" in service:
                p = Process(
                    target=rlogin_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("login")

            elif "afp" in service:
                p = Process(
                    target=afp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("afp")

            elif "rtsp" in service:
                p = Process(
                    target=rtsp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("rtsp")

            elif "oob-ws-http" in service:
                p = Process(
                    target=ipmi_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("oob-ws-http")

            elif "rsync" in service:
                p = Process(
                    target=rsync_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("rsync")

            elif "socks" in service:
                p = Process(
                    target=socks_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("socks")

            elif "rmiactivation" in service:
                p = Process(
                    target=rmi_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("rmiactivation")

            elif "ms-sql-s" in service:
                p = Process(
                    target=mssql_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("ms-sql-s")

            elif "oracle" in service:
                p = Process(
                    target=oracle_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("oracle")

            elif "pptp" in service:
                p = Process(
                    target=pptp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("pptp")

            elif "mqtt" in service:
                p = Process(
                    target=mqtt_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("mqtt")

            elif "nfs" in service:
                p = Process(
                    target=nfs_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("nfs")

            elif "docker" in service:
                p = Process(
                    target=docker_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("docker")

            elif "iscsi" in service:
                p = Process(
                    target=iscsi_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("iscsi")

            elif "mysql" in service:
                p = Process(
                    target=mysql_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("mysql")

            elif "ms-wbt-server":
                p = Process(
                    target=rdp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("ms-wbt-server")

            elif "distccd" in service:
                p = Process(
                    target=distccd_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("distccd")

            elif "svn" in service:
                p = Process(
                    target=svn_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("svn")

            elif "ws-discovery" in service:
                p = Process(
                    target=ws_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("ws-discovery")

            elif "postgresql" in service:
                p = Process(
                    target=pgsql_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("postgresql")

            elif "amqp" in service:
                p = Process(
                    target=amqp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("amqp")

            elif "vnc" in service:
                p = Process(
                    target=vnc_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("vnc")

            elif "couchdb" in service:
                p = Process(
                    target=couchDB_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("couchdb")

            elif "X11" in service:
                p = Process(
                    target=x11_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("X11")

            elif "redis" in service:
                p = Process(
                    target=redis_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("redis")

            elif "ajp13" in service:
                p = Process(
                    target=ajp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("ajp13")

            elif "cassandra" in service:
                p = Process(
                    target=cassandra_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("cassandra")

            elif "jetdirect" in service:
                p = Process(
                    target=jetdirect_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("jetdirect")

            elif "snet-sensor-mgmt" in service:
                p = Process(
                    target=ndmp_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("snet-sensor-mgmt")

            elif "memcache" in service:
                p = Process(
                    target=memcache_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("memcache")

            elif "mongod" in service:
                p = Process(
                    target=mongodb_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("mongod")

            elif "EtherNetIP-2" in service:
                p = Process(
                    target=enip_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("EtherNetIP-2")

            elif "bacnet" in service:
                p = Process(
                    target=bacnet_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("bacnet")

            elif "hadoop" in service:
                p = Process(
                    target=hadoop_enum,
                    args=(
                        ip,
                        sysname,
                    ),
                )
                p.start()
                processes.append(p)
                parsers.append("hadoop")

        time.sleep(50)

        # End of for loop
        for process in processes:
            process.join()

        for parser in parsers:
            if parser == "rpcbind":
                rpcinfoparser()
                nmaprpcbindparser()

            elif parser == "ftp":
                nsecriptparserftp()

            elif parser == "telnet":
                telnetnmapparser()

            elif parser == "modbus":
                modbusnmapparser()

            elif parser == "rexec":
                rexecnmapparser()

            elif parser == "dns":
                digparserdns()
                hostparserdns()
                nmapparserdns()

            elif parser == "pop":
                nmapparserpop()

            elif parser == "msrpc":
                nmapmsrpcparser()
                rpcclientparser()

            elif parser == "netbios":
                nmblookupnetbiosparser()
                nbtscannetbiosparser()
                nmapnetbiosparser()

            elif parser == "imap":
                opensslimapparser()
                nmapimapparser()

            elif parser == "smb":
                smbclientparser()
                smbmapparser()
                smbnmapparser()
                enum4linuxparser()

            elif parser == "ssh":
                sshnmapparser()
                sshbannerparser()

            elif parser == "smtp":
                smtpnmapparser()
                smtpopensslparser()

            elif parser == "whois":
                whoisparser()

            elif parser == "tftp":
                tftpparser()

            elif parser == "finger":
                fingerparser()

            elif parser == "snmp":
                snmpnmapparser()
                snmpcheckparser()

            elif parser == "irc":
                ircopensslparser()
                ircnmapparser()

            elif parser == "firewall":
                firewallparser()

            elif parser == "ldap":
                ldapparser()

            elif parser == "ike":
                ikescanparser()
                ikenmapparser()

            elif parser == "rlogin":
                rloginparser()

            elif parser == "afp":
                afpparser()

            elif parser == "rtsp":
                rtspparser()

            elif parser == "ipmi":
                ipmiparser()

            elif parser == "rsync":
                rsyncnmapparser()
                rsyncbannerparser()

            elif parser == "socks":
                socksparser()

            elif parser == "rmi":
                rmiparser()

            elif parser == "mssql":
                mssqlparser()

            elif parser == "oracle":
                oracleparser()

            elif parser == "pptp":
                pptpparser()

            elif parser == "mqtt":
                mqttparser()

            elif parser == "nfs":
                nfsparser()

            elif parser == "docker":
                dockerparser()

            elif parser == "iscsi":
                iscsiparser()

            elif parser == "mysql":
                mysqlparser()

            elif parser == "rdp":
                rdpparser()

            elif parser == "distccd":
                distccdparser()

            elif parser == "svn":
                svnparser()

            elif parser == "ws":
                wsparser()

            elif parser == "epmd":
                epmdparser()

            elif parser == "pgsql":
                pgsqlparser()

            elif parser == "amqp":
                amqpparser()

            elif parser == "vnc":
                vncparser()

            elif parser == "couchDB":
                couchDBparser()

            elif parser == "x11":
                x11parser()

            elif parser == "redis":
                redisnmapparser()
                redisbannerparser()

            elif parser == "ajp":
                ajpparser()

            elif parser == "cassandra":
                cassandraparser()

            elif parser == "jetdirect":
                jetdirectparser()

            elif parser == "ndmp":
                ndmpparser()

            elif parser == "memcache":
                memcacheparser()

            elif parser == "mongodb":
                mongodbparser()

            elif parser == "enip":
                enipparser()

            elif parser == "bacnet":
                bacnetparser()

            elif parser == "hadoop":
                hadoopparser()

    except Exception as e:
        if e:
            print(
                f"[red]The phase2 script has malfunctioned with the following error message: {e}[/red]"
            )
        else:
            print(
                "[red]Well something went wrong with the script and python isn't erroring out, use our github forum for help.[/red]"
            )


# Phase 3 Enumeration Function
def phase3(ip, sysname):

    phase2(ip, sysname)

    products = []
    versions = []

    mytree = ET.parse(f"{sysname}/phase1.xml")
    myroot = mytree.getroot()
    for a in myroot.findall("host"):
        for b in a.findall("ports"):
            for c in b.findall("port"):
                for d in c.findall("service"):
                    try:
                        products.append(d.attrib["product"])
                    except Exception:
                        continue
                    try:
                        versions.append(d.attrib["version"])
                    except Exception:
                        versions.append(" ")

    for product in products:
        version = versions[products.index(product)]
        os.system(f'searchsploit {product} {version} > {sysname}/"{product}".txt')
        os.system(
            f"echo '\n############################ {product} with version {version} ########################################\n' >> report_{sysname}.txt"
        )
        os.system(f'cat {sysname}/"{product}".txt >> report_{sysname}.txt')


# Phase 4 Enumeration Function
def phase4(ip, sysname):
    phase3(ip, sysname)
    print("Phase 4 is not ready yet")
    time.sleep(10)


# Phase 5 Enumeration Function
def phase5(ip, sysname):
    phase4(ip, sysname)
    print("Phase 5 is not ready yet")
    time.sleep(10)


# Nmap Level Scan Function
def nmap_main(ip, level, sysname):
    level = int(level)
    if level > 6 or level < 1:
        print("Invalid nmap scan level.")
        exit()
    else:
        if level == 2:
            os.system(
                "nmap -sVC " + ip + " -oX " + sysname + "/" + "phase1.xml > /dev/null"
            )


# Enumeration Scanners
def http_enum(ip, sysname):
    def gobuster(ip, sysname):
        os.system(
            f"gobuster dir -q -u {ip} -w /root/go.txt -o {sysname}/gobusterresults.txt -t 200 --wildcard > /dev/null"
        )

    def nikto(ip, sysname):
        os.system(
            f"nikto -h {ip} -maxtime 40s -ask no -o {sysname}/niktoresults.txt > /dev/null"
        )

    def wpscan(ip, sysname):
        os.system(
            f"wpscan --url {ip} --no-banner --no-update > {sysname}/wpscanresults.txt"
        )

    def nsescript(ip, sysname):
        os.system(
            f"nmap -p80 --script=http-enum.nse {ip} -oN {sysname}/nsescriptresults.txt > /dev/null"
        )

    # Starting Enumeration
    p1 = Process(
        target=gobuster,
        args=(
            ip,
            sysname,
        ),
    )
    p2 = Process(
        target=nikto,
        args=(
            ip,
            sysname,
        ),
    )
    p3 = Process(
        target=wpscan,
        args=(
            ip,
            sysname,
        ),
    )
    p4 = Process(
        target=nsescript,
        args=(
            ip,
            sysname,
        ),
    )
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()


def ssh_nmap(ip, sysname):
    os.system(
        f"nmap -p 22 --script=ssh2-enum-algos,ssh-auth-methods,ssh-brute,ssh-hostkey,ssh-publickey-acceptance {ip} -oN {sysname}/ssh_nmap.txt > /dev/null"
    )


def ssh_banner(ip, sysname):
    os.system(f"nc -vn {ip} 22 {sysname}/ssh_banner.txt > /dev/null")


def ssh_enum(ip, sysname):
    p1 = Process(
        target=ssh_nmap,
        args=(
            ip,
            sysname,
        ),
    )
    p2 = Process(
        target=ssh_banner,
        args=(
            ip,
            sysname,
        ),
    )
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def smtp_nmap():
    os.system(
        f"""nmap -p 25 --script=smtp-brute,smtp-commands,smtp-enum-users,
        smtp-ntlm-info,smtp-open-relay,smtp-strangeport {ip} -oN {sysname}/smtp_nmap.txt > /dev/null"""
    )


def smtp_openssl():
    os.system(
        f"openssl s_client -starttls smtp -crlf -connect {ip}:25 {sysname}/smtp_openssl.txt > /dev/null"
    )


def smtp_enum(ip, sysname):
    p1 = Process(
        target=smtp_openssl,
        args=(
            ip,
            sysname,
        ),
    )
    p2 = Process(
        target=smtp_nmap,
        args=(
            ip,
            sysname,
        ),
    )
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def whois_enum(ip, sysname):
    os.system(
        f"nmap -p 43 --script=whois-domain,whois-ip {ip} -oN {sysname}/whois_nmap.txt > /dev/null"
    )


def tftp_enum(ip, sysname):
    os.system(
        f"nmap -p 69 --script=tftp-enum {ip} -oN {sysname}/tftp_nmap.txt > /dev/null"
    )


def finger_enum(ip, sysname):
    os.system(
        f"nmap -p 79 --script=fingerprint-strings,finger {ip} -oN {sysname}/finger_nmap.txt > /dev/null"
    )


def ntp_enum(ip, sysname):
    os.system(
        f"nmap -p 123 --script=ntp-info,ntp-monlist {ip} -oN {sysname}/ntp_nmap.txt > /dev/null"
    )


def snmp_nmap():
    os.system(
        f"nmap -p 161 --script=snmp-brute,snmp-hh3c-logins,snmp-info,snmp-interfaces,snmp-processes {ip} -oN {sysname}/snmp_nmap.txt > /dev/null"
    )


def snmp_check():
    os.system(f"snmp-check -c -v 2c {ip} {sysname}/snmp_check.txt > /dev/null")


def snmp_enum(ip, sysname):
    p1 = Process(
        target=snmp_nmap,
        args=(
            ip,
            sysname,
        ),
    )
    p2 = Process(
        target=snmp_check,
        args=(
            ip,
            sysname,
        ),
    )
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def irc_openssl(ip, sysname):
    os.system(
        f"openssl s_client -connect {ip}:194 {sysname}/irc_openssl.txt > /dev/null"
    )


def irc_nmap(ip, sysname):
    os.system(
        f"nmap -p 194,6660-7000 --script=irc-botnet-channels,irc-brute,irc-info,irc-sasl-brute {ip} -oN {sysname}/irc_nmap.txt > /dev/null"
    )


def irc_enum(ip, sysname):
    p1 = Process(
        target=irc_nmap,
        args=(
            ip,
            sysname,
        ),
    )
    p2 = Process(
        target=irc_openssl,
        args=(
            ip,
            sysname,
        ),
    )
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def firewall_enum(ip, sysname):
    os.system(
        f"nmap -p 264 --script=firewall-bypass {ip} -oN {sysname}/firewall_nmap.txt > /dev/null"
    )


def ldap_enum(ip, sysname):
    os.system(
        f"nmap -p 389 --script=ldap-brute,ldap-novell-getpass,ldap-rootdse,ldap-search {ip} -oN {sysname}/ldap_nmap.txt > /dev/null"
    )


def ike_scan(ip, sysname):
    os.system(f"ike-scan {ip} -M-A {sysname}/ike_scan.txt > /dev/null")


def ike_nmap(ip, sysname):
    os.system(
        f"nmap -p 500 --script=ike-version {ip} -oN {sysname}/ike_nmap.txt > /dev/null"
    )


def ike_enum(ip, sysname):
    p1 = Process(
        target=ike_scan,
        args=(
            ip,
            sysname,
        ),
    )
    p2 = Process(
        target=ike_nmap,
        args=(
            ip,
            sysname,
        ),
    )
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def rlogin_enum(ip, sysname):
    os.system(
        f"nmap -p 513 --script=rlogin-brute {ip} -oN {sysname}/rlogin_nmap.txt > /dev/null"
    )


def afp_enum(ip, sysname):
    os.system(
        f"nmap -p 548 --script=afp-brute,afp-path-vuln,afp-ls,afp-serverinfo,afp-showmount {ip} -oN {sysname}/afp_nmap.txt > /dev/null"
    )


def rtsp_enum(ip, sysname):
    os.system(
        f"nmap -p 554 --script=rtsp-methods,rtsp-url-brute {ip} -oN {sysname}/rtsp_nmap.txt > /dev/null"
    )


def ipmi_enum(ip, sysname):
    os.system(
        f"nmap -p 623 --script=ipmi-brute,ipmi-cipher-zero,supermicro-ipmi-conf {ip} -oN {sysname}/ipmi_nmap.txt > /dev/null"
    )


def rsync_nmap(ip, sysname):
    os.system(
        f"nmap -p 873 --script=rsync-brute,rsync-list-modules {ip} -oN {sysname}/rsync_nmap.txt > /dev/null"
    )


def rsync_banner(ip, sysname):
    os.system(f"nc -vn {ip} 873 {sysname}/rsync_banner.txt > /dev/null")


def rsync_enum(ip, sysname):
    p1 = Process(
        target=rsync_nmap,
        args=(
            ip,
            sysname,
        ),
    )
    p2 = Process(
        target=rsync_banner,
        args=(
            ip,
            sysname,
        ),
    )
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def socks_enum(ip, sysname):
    os.system(
        f"nmap -p 1080 --script=socks-auth-info,socks-brute,socks-open-proxy {ip} -oN {sysname}/socks_nmap.txt > /dev/null"
    )


def rmi_enum(ip, sysname):
    os.system(
        f"nmap -p 1098 --script=informix-brute,informix-query,informix-tables,rmi-dumpregistry,rmi-vuln-classloader,supermicro-ipmi-conf {ip} -oN {sysname}/rmi_nmap.txt > /dev/null"
    )


def mssql_enum(ip, sysname):
    os.system(
        f"nmap -p 1433 --script=ms-sql-brute,ms-sql-config,ms-sql-dac,ms-sql-empty-password,ms-sql-info,ms-sql-ntlm-info,ms-sql-query,ms-sql-tables {ip} -oN {sysname}/mssql_nmap.txt > /dev/null"
    )


def oracle_enum(ip, sysname):
    os.system(
        f"nmap -p 1521 --script=oracle-brute,oracle-brute-stealth,oracle-enum-users,oracle-sid-brute,oracle-tns-version {ip} -oN {sysname}/oracle_nmap.txt > /dev/null"
    )


def pptp_enum(ip, sysname):
    os.system(
        f"nmap -p 1723 --script=pptp-version {ip} -oN {sysname}/pptp_nmap.txt > /dev/null"
    )


def mqtt_enum(ip, sysname):
    os.system(
        f"nmap -p 1883 --script=mqtt-subscribe {ip} -oN {sysname}/mqtt_nmap.txt > /dev/null"
    )


def nfs_enum(ip, sysname):
    os.system(
        f"nmap -p 2049 --script=nfs-ls,nfs-showmount,nfs-statfs {ip} -oN {sysname}/nfs_nmap.txt > /dev/null"
    )


def docker_enum(ip, sysname):
    os.system(
        f"nmap -p 2375,2376 --script=docker-versions {ip} -oN {sysname}/docker_nmap.txt > /dev/null"
    )


def iscsi_enum(ip, sysname):
    os.system(
        f"nmap -p 3260 --script=iscsi-info,iscsi-brute {ip} -oN {sysname}/iscsi_nmap.txt > /dev/null"
    )


def mysql_enum(ip, sysname):
    os.system(
        f"nmap -p 3306 --script=mysql-audit,mysql-brute,mysql-databases,mysql-empty-password,mysql-enum,mysql-users,mysql-query {ip} -oN {sysname}/mysql_nmap.txt > /dev/null"
    )


def rdp_enum(ip, sysname):
    os.system(
        f"nmap -p 3389 --script=rdp-enum-encryption,rdp-ntlm-info,rdp-vuln-ms12-020 {ip} -oN {sysname}/rdp_nmap.txt > /dev/null"
    )


def distccd_enum(ip, sysname):
    os.system(
        f"nmap -p 3632 --script=distcc-cve2004-2687 {ip} -oN {sysname}/distccd_nmap.txt > /dev/null"
    )


def svn_enum(ip, sysname):
    os.system(
        f"nmap -p 3690 --script=http-svn-enum,http-svn-info,svn-brute {ip} -oN {sysname}/svn_nmap.txt > /dev/null"
    )


def ws_enum(ip, sysname):
    os.system(
        f"nmap -p 3702 --script=wsdd-discover,broadcast-wsdd-discover {ip} -oN {sysname}/ws-disc_nmap.txt > /dev/null"
    )


def epmd_enum(ip, sysname):
    os.system(
        f"nmap -p 4369 --script=epmd-info {ip} -oN {sysname}/epmd_nmap.txt > /dev/null"
    )


def pgsql_enum(ip, sysname):
    os.system(
        f"nmap -p 5432 --script=pgsql-brute {ip} -oN {sysname}/pgsql_nmap.txt > /dev/null"
    )


def amqp_enum(ip, sysname):
    os.system(
        f"nmap -p 5672 --script=amqp-info {ip} -oN {sysname}/amqp_nmap.txt > /dev/null"
    )


def vnc_enum(ip, sysname):
    os.system(
        f"nmap -p 5900 --script=vnc-brute,vnc-info,vnc-title,realvnc-auth-bypass {ip} -oN {sysname}/vnc_nmap.txt > /dev/null"
    )


def couchDB_enum(ip, sysname):
    os.system(
        f"nmap -p 5984 --script=couchdb-databases,couchdb-stats {ip} -oN {sysname}/couchdb_nmap.txt > /dev/null"
    )


def x11_enum(ip, sysname):
    os.system(
        f"nmap -p 6000 --script=x11-access {ip} -oN {sysname}/x11_nmap.txt > /dev/null"
    )


def redis_nmap(ip, sysname):
    os.system(
        f"nmap -p 6379--script=redis-info,redis-brute {ip} -oN {sysname}/redis_nmap.txt > /dev/null"
    )


def redis_banner(ip, sysname):
    os.system(f"nc -vn {ip} 6379 {sysname}/redis_banner.txt > /dev/null")


def redis_enum(ip, sysname):
    p1 = Process(
        target=redis_nmap,
        args=(
            ip,
            sysname,
        ),
    )
    p2 = Process(
        target=redis_banner,
        args=(
            ip,
            sysname,
        ),
    )
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def ajp_enum(ip, sysname):
    os.system(
        f"nmap -p 8009 --script=ajp-auth,ajp-brute,ajp-headers,ajp-methods,ajp-request {ip} -oN {sysname}/ajp_nmap.txt > /dev/null"
    )


def cassandra_enum(ip, sysname):
    os.system(
        f"nmap -p 9042 --script=cassandra-brute,cassandra-info {ip} -oN {sysname}/cassandra_nmap.txt > /dev/null"
    )


def jetdirect_enum(ip, sysname):
    os.system(
        f"nmap -p 9100 --script=pjl-ready-message {ip} -oN {sysname}/jetdirect_nmap.txt > /dev/null"
    )


def ndmp_enum(ip, sysname):
    os.system(
        f"nmap -p 10000 --script=ndmp-fs-info,ndmp-version {ip} -oN {sysname}/ndmp_nmap.txt > /dev/null"
    )


def memcache_enum(ip, sysname):
    os.system(
        f"nmap -p 11211 --script=memcached-info {ip} -oN {sysname}/memcache_nmap.txt > /dev/null"
    )


def mongodb_enum(ip, sysname):
    os.system(
        f"nmap -p 27017,27018 --script=mongodb-brute,mongodb-databases,mongodb-info {ip} -oN {sysname}/mongodb_nmap.txt > /dev/null"
    )


def enip_enum(ip, sysname):
    os.system(
        f"nmap -p 44818 --script=enip-info {ip} -oN {sysname}/enip_nmap.txt > /dev/null"
    )


def bacnet_enum(ip, sysname):
    os.system(
        f"nmap -p 47808 --script=bacnet-info {ip} -oN {sysname}/bacnet_nmap.txt > /dev/null"
    )


def hadoop_enum(ip, sysname):
    os.system(
        f"nmap -p 50070 --script=hadoop-datanode,hadoop-jobtracker-info,hadoop-namenode-info,hadoop-tasktracker-info {ip} -oN {sysname}/hadoop_nmap.txt > /dev/null"
    )


# Start of parser section


def rpcinfoparser():

    os.system(
        f"echo '\n############################ RPC INFO ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/rpcinfo.txt >> report_{sysname}.txt")


def nmaprpcbindparser():

    os.system(
        f"echo '\n################################# NMAP RPC ########################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nmapresultrpcbind.txt >> report_{sysname}.txt")


# FTP


def nsescriptparserftp():
    os.system(
        f"echo '\n############################ NSESCRIPTS FOR FTP ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nsescriptftp.txt >> report_{sysname}.txt")


# TELNET


def telnetnmapparser():
    # Cat to simply put telnetnmap output into report_{sysname}.txt
    os.system(
        f"echo '\n####################################### TELNET NMAP #############################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/telnetnmap.txt >> report_{sysname}.txt")


# MODBUS


def modbusnmapparser():
    # Cat to simply put modbusnmap output into report_{sysname}.txt
    os.system(
        f"echo '\n####################################### NMAP For MODBUS #############################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/modbusnmap.txt >> report_{sysname}.txt")


# REXEC


def rexecnmapparser():
    # Cat to simply put rexecnmap output into report_{sysname}.txt
    os.system(
        f"echo '\n####################################### REXEC NMAP #############################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/rexecnmap.txt >> report_{sysname}.txt")


# DNS


def digparserdns():
    os.system(
        f"echo '\n############################ DIG DNS ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/digdns.txt >> report_{sysname}.txt")


def hostparserdns():
    os.system(
        f"echo '\n################################# HOST ########################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/hostdns.txt >> report_{sysname}.txt")


def nmapparserdns():
    os.system(
        f"echo '\n########################## NMAP DNS ################################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nmapresultdns.txt >> report_{sysname}.txt")


# POP


def nmapparserpop():
    os.system(
        f"echo '\n############################ NMAP FOR POP ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nmapresultpop.txt >> report_{sysname}.txt")


# MSRPC


def nmapmsrpcparser():
    os.system(
        f"echo '\n############################ NMAP MSRPC ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nmapmsrpcresult.txt >> report_{sysname}.txt")


def rpcclientparser():
    os.system(
        f"echo '\n################################# RPC Client ########################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/rpcclient.txt >> report_{sysname}.txt")


# NETBIOS


def nmblookupnetbiosparser():
    os.system(
        f"echo '\n############################ nmblookup ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nmblookupnetbios.txt >> report_{sysname}.txt")


def nbtscannetbiosparser():
    os.system(
        f"echo '\n################################# nbtscan ########################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nbtscannetbios.txt >> report_{sysname}.txt")


def nmapnetbiosparser():
    os.system(
        f"echo '\n########################## NMAP netbios ################################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nmapnetbiosresult.txt >> report_{sysname}.txt")


# IMAP


def opensslimapparser():
    os.system(
        f"echo '\n############################ Openssl IMAP ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/opensslimap.txt >> report_{sysname}.txt")


def nmapimapparser():
    os.system(
        f"echo '\n################################# NMAP IMAP ########################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nmapimapresult.txt >> report_{sysname}.txt")


# SMB


def smbclientparser():
    # Cat to simply put smbclient output into report_{sysname}.txt
    os.system(
        f"echo '\n####################################### SMB CLIENT #############################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/smbclient.txt >> report_{sysname}.txt")


def smbmapparser():
    # Cat to simply put smbmap output into report_{sysname}.txt
    os.system(
        f"echo '\n####################################### SMB MAP #############################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/smbmap.txt >> report_{sysname}.txt")


def smbnmapparser():
    # Cat to simply put smbnmap output into report_{sysname}.txt
    os.system(
        f"echo '\n####################################### SMB NMAP #############################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/smbnmap.txt >> report_{sysname}.txt")


def enum4linuxparser():
    # Cat to simply put enum4linux output into report_{sysname}.txt
    os.system(
        f"echo '\n####################################### Enum4linux #############################################' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/enum4linux.txt >> report_{sysname}.txt")


# SSH
# Parser Function
def sshnmapparser():
    os.system(
        f"echo '\n############################ ssh nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ssh_nmap.txt >> report_{sysname}.txt")


def sshbannerparser():
    os.system(
        f"echo '\n############################ ssh banner ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ssh_banner.txt >> report_{sysname}.txt")


# SMTP
# Parser Function
def smtpnmapparser():
    os.system(
        f"echo '\n############################ smtp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/smtp_nmap.txt >> report_{sysname}.txt")


def smtpopensslparser():
    os.system(
        f"echo '\n############################ smtp openssl ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/smtp_openssl.txt >> report_{sysname}.txt")


# Whois
# Parser Function
def whoisparser():
    os.system(
        f"echo '\n############################ whois nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/whois_nmap.txt >> report_{sysname}.txt")


# TFTP
# Parser Function
def tftpparser():
    os.system(
        f"echo '\n############################ tftp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/tftp_nmap.txt >> report_{sysname}.txt")


# FINGER
# Parser Function
def fingerparser():
    os.system(
        f"echo '\n############################ finger nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/finger_nmap.txt >> report_{sysname}.txt")


# NTP
# Parser Function
def ntpparser():
    os.system(
        f"echo '\n############################ ntp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ntp_nmap.txt >> report_{sysname}.txt")


# SNMP
# Parser Function
def snmpnmapparser():
    os.system(
        f"echo '\n############################ snmp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/snmp_nmap.txt >> report_{sysname}.txt")


def snmpcheckparser():
    os.system(
        f"echo '\n############################ snmp check ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/snmp_check.txt >> report_{sysname}.txt")


# IRC
# Parser Function
def ircopensslparser():
    os.system(
        f"echo '\n############################ irc openssl ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/irc_openssl.txt >> report_{sysname}.txt")


def ircnmapparser():
    os.system(
        f"echo '\n############################ irc nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/irc_nmap.txt >> report_{sysname}.txt")


# FIREWALL
# Parser Function
def firewallparser():
    os.system(
        f"echo '\n############################ firewall nmap  ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/firewall_nmap.txt >> report_{sysname}.txt")


# LDAP
# Parser Function
def ldapparser():
    os.system(
        f"echo '\n############################ ldap nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ldap_nmap.txt >> report_{sysname}.txt")


# IKE
# Parser Function
def ikescanparser():
    os.system(
        f"echo '\n############################ ike scan ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ike_scan.txt >> report_{sysname}.txt")


def ikenmapparser():
    os.system(
        f"echo '\n############################ ike nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ike_nmap.txt >> report_{sysname}.txt")


# RLOGIN
# Parser Function
def rloginparser():
    os.system(
        f"echo '\n############################ rlogin nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/rlogin_nmap.txt >> report_{sysname}.txt")


# AFP
def afpparser():
    os.system(
        f"echo '\n############################ afp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/afp_nmap.txt >> report_{sysname}.txt")


# RTSP
# Parser Function
def rtspparser():
    os.system(
        f"echo '\n############################ rtsp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/rtsp_nmap.txt >> report_{sysname}.txt")


# IPMI
# Parser Function
def ipmiparser():
    os.system(
        f"echo '\n############################ ipmi nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ipmi_nmap.txt >> report_{sysname}.txt")


# RSYNC
# Parser Function
def rsyncnmapparser():
    os.system(
        f"echo '\n############################ rsync nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/rsync_nmap.txt >> report_{sysname}.txt")


def rsyncbannerparser():
    os.system(
        f"echo '\n############################ rsync banner ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/rsync_banner.txt >> report_{sysname}.txt")


# SOCKS
# Parser Function
def socksparser():
    os.system(
        f"echo '\n############################ socks nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/socks_nmap.txt >> report_{sysname}.txt")


# RMI
# Parser Function
def rmiparser():
    os.system(
        f"echo '\n############################ rmi nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/rmi_nmap.txt >> report_{sysname}.txt")


# MSSQL
# Parser Function
def mssqlparser():
    os.system(
        f"echo '\n############################ mssql nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/mssql_nmap.txt >> report_{sysname}.txt")


# ORACLE
# Parser Function
def oracleparser():
    os.system(
        f"echo '\n############################ oracle nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/oracle_nmap.txt >> report_{sysname}.txt")


# PPTP
# Parser Function
def pptpparser():
    os.system(
        f"echo '\n############################ pptp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/pptp_nmap.txt >> report_{sysname}.txt")


# MQTT
# Parser Function
def mqttparser():
    os.system(
        f"echo '\n############################ mqtt nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/mqtt_nmap.txt >> report_{sysname}.txt")


# NFS
# Parser Function
def nfsparser():
    os.system(
        f"echo '\n############################ nfs nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/nfs_nmap.txt >> report_{sysname}.txt")


# DOCKER
# Parser Function
def dockerparser():
    os.system(
        f"echo '\n############################ docker nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/docker_nmap.txt >> report_{sysname}.txt")


# ISCSI
# Parser Function
def iscsiparser():
    os.system(
        f"echo '\n############################ iscsi nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/iscsi_nmap.txt >> report_{sysname}.txt")


# MYSQL
# Parser Function
def mysqlparser():
    os.system(
        f"echo '\n############################ mysql nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/mysql_nmap.txt >> report_{sysname}.txt")


# RDP
# Parser Function
def rdpparser():
    os.system(
        f"echo '\n############################ rdp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/rdp_nmap.txt >> report_{sysname}.txt")


# DISTCCD
# Parser Function
def distccdparser():
    os.system(
        f"echo '\n############################ distccd nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/distccd_nmap.txt >> report_{sysname}.txt")


# SVN
# Parser Function
def svnparser():
    os.system(
        f"echo '\n############################ svn nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/svn_nmap.txt >> report_{sysname}.txt")


# WS-DISC
# Parser Function
def wsparser():
    os.system(
        f"echo '\n############################ ws-disc nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ws-disc_nmap.txt >> report_{sysname}.txt")


# EPMD
# Parser Function
def epmdparser():
    os.system(
        f"echo '\n############################ epmd nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/epmd_nmap.txt >> report_{sysname}.txt")


# PGSQL
# Parser Function
def pgsqlparser():
    os.system(
        f"echo '\n############################ pgsql nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/pgsql_nmap.txt >> report_{sysname}.txt")


# AMQP
# Parser Function
def amqpparser():
    os.system(
        f"echo '\n############################ amqp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/amqp_nmap.txt >> report_{sysname}.txt")


# VNC
# Parser Function
def vncparser():
    os.system(
        f"echo '\n############################ vnc nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/vnc_nmap.txt >> report_{sysname}.txt")


# COUCH-DB
# Parser Function
def couchDBparser():
    os.system(
        f"echo '\n############################ couchdb nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/couchdb_nmap.txt >> report_{sysname}.txt")


# X11
# Parser Function
def x11parser():
    os.system(
        f"echo '\n############################ x11 nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/x11_nmap.txt >> report_{sysname}.txt")


# REDIS
# Parser Function
def redisnmapparser():
    os.system(
        f"echo '\n############################ redis nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/redis_nmap.txt >> report_{sysname}.txt")


def redisbannerparser():
    os.system(
        f"echo '\n############################ redis banner  ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/redis_banner.txt >> report_{sysname}.txt")


# AJP
# Parser Function
def ajpparser():
    os.system(
        f"echo '\n############################ ajp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ajp_nmap.txt >> report_{sysname}.txt")


# CASSANDRA
# Parser Function
def cassandraparser():
    os.system(
        f"echo '\n############################ cassandra nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/cassandra_nmap.txt >> report_{sysname}.txt")


# JETDIRECT
# Parser Function
def jetdirectparser():
    os.system(
        f"echo '\n############################ jetdirect nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/jetdirect_nmap.txt >> report_{sysname}.txt")


# NDMP
# Parser Function
def ndmpparser():
    os.system(
        f"echo '\n############################ ndmp nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/ndmp_nmap.txt >> report_{sysname}.txt")


# MEMCACHE
# Parser Function
def memcacheparser():
    os.system(
        f"echo '\n############################ memcache nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/memcache_nmap.txt >> report_{sysname}.txt")


# MONGODB
# Parser Function
def mongodbparser():
    os.system(
        f"echo '\n############################ mongodb nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/mongodb_nmap.txt >> report_{sysname}.txt")


# ETHERNET-IP
# Parser Function
def enipparser():
    os.system(
        f"echo '\n############################ enip nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/enip_nmap.txt >> report_{sysname}.txt")


# BACNET
# Parser Function
def bacnetparser():
    os.system(
        f"echo '\n############################ bacnet nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/bacnet_nmap.txt >> report_{sysname}.txt")


# HADOOP
# Parser Function
def hadoopparser():
    os.system(
        f"echo '\n############################ hadoop nmap ########################################\n' >> report_{sysname}.txt"
    )
    os.system(f"cat {sysname}/hadoop_nmap.txt >> report_{sysname}.txt")


def port_check(ip, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (ip, port)
    webappstat = a_socket.connect_ex(location)
    a_socket.close()
    return webappstat
