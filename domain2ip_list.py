import socket
import ipranges
import requests
from cymruwhois import Client
from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
from colorama import init
from concurrent.futures import ThreadPoolExecutor
import colorama
import os
import platform
import subprocess

reset = colorama.Style.RESET_ALL
gr = colorama.Fore.GREEN
bl = colorama.Fore.BLUE
yl = colorama.Fore.YELLOW
ro = colorama.Fore.RED
try:
    os.mkdir("Results")
except os.error:
    pass


def clear():
    if platform.system() == "Windows":
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear', shell=True)


def getip(domain):
    domains = domain.replace("\n", "").replace("\r", "").replace(" ", "")
    try:
        host_ip = socket.gethostbyname(domains)
        dupi = open("Results/Duplicated_ips.txt", "a")
        dupi.write(f'{host_ip}\n')
        dupi.close()
        gezien = set()
        with open("Results/domain2ip.txt", "w") as output_file:
            for ips_found in open("Results/Duplicated_ips.txt", "r"):
                if ips_found not in gezien:
                    output_file.write(ips_found)
                    gezien.add(ips_found)
        print(f"{bl}{domains}{reset} --> {gr}{host_ip}{reset}")
        output_file.close()
    except (socket.error, socket.gaierror, socket.herror):
        pass


def getasn(domijntjes):
    domains = domijntjes.replace("\n", "").replace("\r", "").replace(" ", "")
    try:
        c = Client()
        ip = socket.gethostbyname(domains)
        r = c.lookup(ip)
        dupis = open("Results/Duplicated_asn.txt", "a")
        dupis.write(f'AS{r.asn}\n')
        dupis.close()
        gezien = set()
        with open("Results/asn.txt", "w") as output_file:
            for elke in open("Results/Duplicated_asn.txt", "r"):
                if elke not in gezien:
                    output_file.write(elke)
                    gezien.add(elke)
        print(f"{bl}Found{reset}: {gr}AS{r.asn}{reset}")
        output_file.close()
    except Exception as e:
        print(e)


def asn_iprange(AS):
    asn = AS.replace("\n", "").replace("\r", "").replace(" ", "")
    r = requests.get(f'https://api.bgpview.io/asn/{asn}/prefixes').json()
    rather = r['data']['ipv4_prefixes']
    for Yh in range(0, int(len(rather)) - 1):
        ipss = r['data']['ipv4_prefixes'][Yh]
        gass = ipss['ip'] + '/' + str(ipss['cidr'])
        ips_list = ipranges.IP4Net(gass)
        for IP in ips_list:
            dupiss = open(f"Results/{asn}_Duplicated_ipslist.txt", "a")
            dupiss.write(f'{IP}\n')
            dupiss.close()
            gezien = set()
            with open(f"Results/{asn}_IPS.txt", "w") as output_file:
                for voor_elke in open(f"Results/{asn}_Duplicated_ipslist.txt", "r"):
                    if voor_elke not in gezien:
                        output_file.write(voor_elke)
                        gezien.add(voor_elke)
            print(f"{gr}{IP}{reset} : {bl} FOUND")
            output_file.close()


def startip():
    with ThreadPoolExecutor(max_workers=Thread) as poolip:
        try:
            poolip.map(getip, domaina)
        except:
            pass
    domijntjes = open("Results/domain2ip.txt", "r")
    with ThreadPoolExecutor(max_workers=Thread) as poolasn:
        try:
            poolasn.map(getasn, domijntjes)
        except:
            pass
    AS = open("Results/asn.txt", "r")
    with ThreadPoolExecutor(max_workers=Thread) as poole:
        poole.map(asn_iprange, AS)


if __name__ == '__main__':
    clear()
    print(f"{bl}Telegram : @Freshesleadsever\n"
          f'{gr}Emperors Tools\n'
          f'{yl}https://t.me/freshesleadsb\n'
          f"{yl}EMPERORS-TOOLS DOMAIN TO ALL IPS ON ASN v3")
    domaina = open(input(f"{gr}Your list Domain Please{reset}? "), 'r')
    Thread = int(input(f"{bl}How many threads{reset}? "))
    startip()
