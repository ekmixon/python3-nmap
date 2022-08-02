# Author : HAYDAR TECH
#
# Data structure sample:
#
# {
#     "127.0.0.1": [
#         {
#             "host": "127.0.0.1",
#             "portid": "5000",
#             "protocol": "tcp",
#             "reason": "syn-ack",
#             "reason_ttl": "64",
#             "service": {
#                 "conf": "3",
#                 "method": "table",
#                 "name": "upnp"
#             },
#             "state": "open"
#         },
#         {
#             "host": "127.0.0.1",
#             "portid": "5432",
#             "protocol": "tcp",
#             "reason": "syn-ack",
#             "reason_ttl": "64",
#             "service": {
#                 "conf": "3",
#                 "method": "table",
#                 "name": "postgresql"
#             },
#             "state": "open"
#         }
#     ],
#     "runtime": {
#         "elapsed": "20.24",
#         "exit": "success",
#         "summary": "Nmap done at Sun May 24 12:45:28 2020; 1 IP address (1 host up) scanned in 20.24 seconds",
#         "time": "1590320728",
#         "timestr": "Sun May 24 12:45:28 2020"
#     },
#     "stats": {
#         "args": "/usr/local/bin/nmap -oX - -Pn -O --osscan-guess 127.0.0.1",
#         "scanner": "nmap",
#         "start": "1590320708",
#         "startstr": "Sun May 24 12:45:08 2020",
#         "version": "7.80",
#         "xmloutputversion": "1.04"
#     }
# }

import sys
import nmap3
import simplejson as json
from pygments import highlight, lexers, formatters


def scan_techniques(nmt, scan_type, target):
    if scan_type == '-sF':
        return nmt.nmap_fin_scan(target)

    elif scan_type == '-sI':
        idle_scan = nmt.nmap_idle_scan(target)
        return

    elif scan_type == '-sP':
        return nmt.nmap_ping_scan(target)

    elif scan_type == '-sS':
        return nmt.nmap_syn_scan(target)

    elif scan_type == '-F':
        return nmt.nmap_syn_scan(target)

    elif scan_type == '-sT':
        return nmt.nmap_tcp_scan(target)

    elif scan_type == '-sU':
        return nmt.nmap_udp_scan(target)

    else:
        raise ValueError("Not a scan technique")


def scan_discovery(nmd, scan_type, target, ports_num):
    if scan_type == '-Pn':
        return nmd.nmap_portscan_only(target)

    elif scan_type == '-sn':
        return nmd.nmap_no_portscan(target)

    elif scan_type == '-PR':
        return nmd.nmap_no_portscan(target)

    elif scan_type == '-n':
        return nmd.nmap_disable_dns(target)

    elif scan_type == '-O --osscan-guess':
        return nmd.nmap_portscan_only(target, args=scan_type)

    elif scan_type == '-A -T2':
        return nmd.nmap_portscan_only(target, args=scan_type)

    elif scan_type == '-A':
        return nmd.nmap_portscan_only(target, args=scan_type)

    elif scan_type == '-A -v':
        return nmd.nmap_portscan_only(target, args=scan_type)

    elif scan_type == '-T4 -sV':
        return nmd.nmap_portscan_only(target, args=scan_type)

    elif scan_type == '-n -A':
        return nmd.nmap_portscan_only(target, args=scan_type)

    elif scan_type == '-n -V':
        return nmd.nmap_portscan_only(target, args=scan_type)

    elif scan_type == '-f -A':
        return nmd.nmap_portscan_only(target, args=scan_type)

    elif scan_type == '-n -sV --version-intensity 3':
        return nmd.nmap_portscan_only(target, args=scan_type)

    elif scan_type == '-O --osscan-guess -p ':
        scan_type = scan_type + str(ports_num)
        return nmd.nmap_portscan_only(target, args=scan_type)

    else:
        raise ValueError("Not a scan technique")


def scan_command(nm, scan_type, target, domain):
    if scan_type == '-sA':
        return nm.nmap_detect_firewall(target)

    elif scan_type == '-O':
        return nm.nmap_os_detection(target)

    elif scan_type == '--top-ports':
        return nm.scan_top_ports(target)

    elif scan_type == '20 -sZ':
        return nm.scan_top_ports(target)

    elif scan_type == '-script dns-brute':
        return nm.nmap_dns_brute_script(domain)

    elif scan_type == '-sL':
        return nm.nmap_list_scan(target)

    elif scan_type == '-p-':
        return nm.nmap_subnet_scan(target)

    elif scan_type == '-sV':
        return nm.nmap_version_detection(target)

    elif scan_type == '-sX':
        return nm.nmap_version_detection(target, args=scan_type)

    else:
        raise ValueError("Not a scan technique")


def launch(target, domain, ports, templates):
    def tpl(i):
        template = {
            # OPTIONS FOR THE SCAN TECHNIQUE FUNCTION
            1: '-sF',  # 'FIN scan'
            2: '-sI',  # 'Idle scan'
            3: '-sS',  # 'Default: TCP SYN scan'
            4: '-sP',  # 'ping-only'
            5: '-sT',  # 'TCP connect() scan'
            6: '-sU',  # 'UDP scan'
            7: '-F',  # 'Fast scan'

            # OPTIONS FOR THE SCAN DISCOVERY FUNCTION
            8: '-Pn',  # 'No ping scan'
            9: '-sn',  # 'Liveness detection: no port scan'
            10: '-PR',  # 'ARP scan: local network only'
            11: '-n',  # 'Disable DNS resolution: reduces noise'
            12: '-O --osscan-guess',  # 'Used with no ping: aggressive OS detection'
            13: '-A',
            # 'Used with no ping: Advanced detection: OS detection and Version detection, Script scanning and Traceroute'
            14: '-A -T2',  # 'Used with no ping: Advanced detection: with stealth scan mode'
            15: '-A -v',  # 'Used with no ping: Advanced detection: verbose'
            16: '-n -A',  # 'Used with no ping: Advanced detection: scan with no DNS resolution'
            17: '-f -A',  # 'Used with no ping: Advanced detection: combined with packet fragmentation'
            18: '-T4 -sV',  # 'Used with no ping: Aggressive service detection'
            19: '-n -sV --version-intensity 3',
            # 'Used with no ping: Aggressive service detection: with version-intensity 3'
            20: '-n -V',  # 'Used with no ping: Number version detection'
            21: '-O --osscan-guess -p ',  # 'Used with no ping: OS detection with port selection'

            # OPTIONS FOR THE SCAN COMMAND FUNCTION
            22: '-sX',  # 'Basic service detection combined with Xmas scan'
            23: '-sA',  # 'Firewall rule detection: ACK scan'
            24: '-O',  # 'OS detection'
            25: '20 -sZ',  # 'SCTP: Advanced silent scan for top20 ports'
            26: '--top-ports',  # 'Top ports scan (1000 ports)'
            27: '-script dns-brute',  # 'Dns-brute-script( to get subdomains )'
            28: '-sL',
            # 'List scan: lists each host on the network(s) specified, without sending any packets to the target hosts'
            29: '-p-',  # 'Subnet scan'
            30: '-sV'  # 'Basic service detection'
        }

        return template.get(i)

    # try:
    #     nm  = nmap3.Nmap()

    # except nmap3.Nmap:
    #     print('Nmap not found', sys.exc_info()[0])
    #     sys.exit(1)
    # except:
    #     print("Unexpected error:", sys.exc_info()[0])
    #     sys.exit(1)

    nm = nmap3.Nmap()
    nmt = nmap3.NmapScanTechniques()
    nmd = nmap3.NmapHostDiscovery()

    if templates or domain:
        if ports:
            # Not in the final code - just for debug
            choice = tpl(21) + str(ports)
            print("\n\nTrying option: ", choice)

            tpl = tpl(21)
            res = scan_discovery(nmd, tpl, target, ports)

            # Print for debug
            colored_json = highlight(json.dumps(res, indent=4, sort_keys=True), lexers.JsonLexer(),
                                     formatters.TerminalFormatter())
            print("\n\n", colored_json)

        elif domain:
            tpl = tpl(27)
            res = scan_command(nm, tpl, None, domain)

            # Print for debug
            colored_json = highlight(json.dumps(res, indent=4, sort_keys=True), lexers.JsonLexer(),
                                     formatters.TerminalFormatter())
            print("\n\n", colored_json)

        else:
            tpl = tpl(templates)
            print("\n\nTrying option: ", tpl)

            if templates <= 7:
                res = scan_techniques(nmt, tpl, target)

                # Print for debug
                colored_json = highlight(json.dumps(res, indent=4, sort_keys=True), lexers.JsonLexer(),
                                         formatters.TerminalFormatter())
                print("\n\n", colored_json)

            elif templates in range(8, 22):
                res = scan_discovery(nmd, tpl, target, None)

                # Print for debug
                colored_json = highlight(json.dumps(res, indent=4, sort_keys=True), lexers.JsonLexer(),
                                         formatters.TerminalFormatter())
                print("\n\n", colored_json)

            else:
                res = scan_command(nm, tpl, target, None)

                # Print for debug
                colored_json = highlight(json.dumps(res, indent=4, sort_keys=True), lexers.JsonLexer(),
                                         formatters.TerminalFormatter())
                print("\n\n", colored_json)

    else:
        tpl = tpl(3)
        res = scan_techniques(nmt, tpl, target)

        # Print for debug
        colored_json = highlight(json.dumps(res, indent=4, sort_keys=True), lexers.JsonLexer(),
                                 formatters.TerminalFormatter())
        print("No option was set\n\n", colored_json)


if __name__ == '__main__':
    launch("localhost", None, None, 24)
