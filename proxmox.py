import os
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
from utils import *

load_dotenv()

PROXMOX_HOST = os.getenv('PROXMOX_HOST')
PROXMOX_USER = os.getenv('PROXMOX_USER')
PROXMOX_TOKEN = os.getenv('PROXMOX_TOKEN')
SYS = os.getenv('SYS')
SYS_USER = os.getenv('SYS_USER')
NODE = os.getenv('NODE')
NAME_PROXMOX = os.getenv('NAME_PROXMOX')
NAME_SYS = os.getenv('NAME_SYS')

proxmox = ProxmoxAPI(host=PROXMOX_HOST, user=PROXMOX_USER, token_name=NAME_PROXMOX, token_value=PROXMOX_TOKEN, verify_ssl=False)
sys = ProxmoxAPI(host=PROXMOX_HOST, user=SYS_USER, token_name=NAME_SYS, token_value=SYS, verify_ssl=False)

def list_all():

    containers = get_containers(proxmox, NODE)
    vms = get_vms(proxmox, NODE)

    msg = f"Containers and virtual machines status on {NODE}:\n\n"
    for container in containers:
        msg += f"📦 {container['vmid']}: {container['name']} {'🛑' if container['status'] == 'stopped' else '🟢'}\n"
    msg += "\n"
    for vm in vms:
        msg += f"🖥️  {vm['vmid']}: {vm['name']} {'🛑' if vm['status'] == 'stopped' else '🟢'}\n"

    return msg


def list_containers():

    containers = get_containers(proxmox, NODE)
    msg = f"Containers on {NODE}:\n"
    for container in containers:
        msg += f"📦 {container['vmid']}: {container['name']} {'🛑' if container['status'] == 'stopped' else '🟢'}\n"
    return msg


def list_vms():
    vms = get_vms(proxmox, NODE)
    msg = f"Virtual machines on {NODE}:\n"
    for vm in vms:
        msg += f"🖥️  {vm['vmid']}: {vm['name']} {'🛑' if vm['status'] == 'stopped' else '🟢'}\n"
    return msg


def get_cpu():

    msg = f"CPU usage on {NODE}:\n"

    cpu = get_cpu_usage(sys, NODE)

    return f"{msg}🧠: {round(cpu, 2)}%"


def get_ram():

    msg = f"RAM usage on {NODE}:\n"

    mem_used, mem_total = get_memory_usage(sys, NODE)

    return f"{msg}🕊️: {round((mem_used/mem_total)*100, 2)}% ({mem_used:.2f} GB / {mem_total:.2f} GB)"


def get_hdd():

    msg = f"HDD usage on {NODE}:\n"

    hdd_used, hdd_total = get_hdd_usage(sys)

    return f"{msg}💽: {round((hdd_used/hdd_total)*100, 2)}% ({hdd_used:.2f} GB / {hdd_total:.2f} GB)"

def get_ssd():

    msg = f"SSD usage on {NODE}:\n"

    ssd_used, ssd_total = get_ssd_usage(sys)

    return f"{msg}💾: {round((ssd_used/ssd_total)*100, 2)}% ({ssd_used:.2f} GB / {ssd_total:.2f} GB)"


def get_disk_usage():

    msg = f"Disk usage on {NODE}:\n"

    hdd_used, hdd_total = get_hdd_usage(sys)
    ssd_used, ssd_total = get_ssd_usage(sys)
    node_used, node_total = get_node_disk(sys, NODE)

    used = hdd_used + ssd_used + node_used
    total = hdd_total + ssd_total + node_total

    return f"{msg}💿: {round((used/total)*100, 2)}% ({used:.2f} GB / {total:.2f} GB)"


def summary():

    msg = get_cpu() + "\n\n"
    msg += get_ram() + "\n\n"
    msg += get_hdd() + "\n\n"
    msg += get_ssd() + "\n\n"
    msg += get_disk_usage() + "\n"

    return msg


def stop_or_start(vmid_to_change: int):
    return change_status(proxmox, NODE, vmid_to_change)


if __name__ == "__main__":

    id_to_change = 101

    print(f"Changing status of VMID: {id_to_change}")
    print(stop_or_start(id_to_change))
