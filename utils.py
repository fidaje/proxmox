
def get_containers(proxmox, node):

    containers = proxmox.nodes(node).lxc.get()
    containers.sort(key=lambda x: x['vmid'])

    return containers

def get_vms(proxmox, node):
    vms = proxmox.nodes(node).qemu.get()
    vms.sort(key=lambda x: x['vmid'])

    return vms


def get_cpu_usage(proxmox, node):
    cpu_percent = proxmox.nodes(node).status.get()['cpu'] * 100

    return cpu_percent


def get_memory_usage(proxmox, node):
    mem_used = proxmox.nodes(node).status.get()['memory']['used'] / (1024**3)
    mem_total = proxmox.nodes(node).status.get()['memory']['total'] / (1024**3)

    return mem_used, mem_total


def get_hdd_usage(proxmox):
    hdd = [disk for disk in proxmox.cluster().resources.get() 
             if 'plugintype' in disk and disk['plugintype'] == 'zfspool' 
             and 'storage' in disk and disk['storage'] == 'hdd']

    hdd_used = hdd[0]['disk'] / (1024**3)
    hdd_total = hdd[0]['maxdisk'] / (1024**3)

    return hdd_used, hdd_total


def get_ssd_usage(proxmox):
    ssd = [disk for disk in proxmox.cluster().resources.get() 
             if 'plugintype' in disk and disk['plugintype'] == 'zfspool' 
             and 'storage' in disk and disk['storage'] == 'local-zfs']

    ssd_used = ssd[0]['disk'] / (1024**3)
    ssd_total = ssd[0]['maxdisk'] / (1024**3)

    return ssd_used, ssd_total


def get_node_disk(proxmox, node):
    node_disk = [disk for disk in proxmox.cluster().resources.get() 
            if disk['type'] == 'node' and disk['node'] == node]


    node_used = node_disk[0]['disk'] / (1024**3)
    node_total = node_disk[0]['maxdisk'] / (1024**3)

    return node_used, node_total


def change_status(proxmox, node, vmid_to_change):
    
    resources = [r for r in proxmox.cluster().resources.get() if r['type'] == 'lxc' or r['type'] == 'qemu']

    for r in resources:
        if r['vmid'] == vmid_to_change:
            if r['type'] == 'lxc':
                if r['status'] == 'running':
                    proxmox.nodes(node).lxc(vmid_to_change).status.shutdown.post()
                    return f"Container {r['name']} is shutting down..."
                else:
                    proxmox.nodes(node).lxc(vmid_to_change).status.start.post()
                    return f"Container {r['name']} is starting up..."
            elif r['type'] == 'qemu':
                if r['status'] == 'running':
                    proxmox.nodes(node).qemu(vmid_to_change).status.shutdown.post()
                    return f"VM {r['name']} is shutting down..."
                else:
                    proxmox.nodes(node).qemu(vmid_to_change).status.start.post()
                    return f"VM {r['name']} is starting up..."


