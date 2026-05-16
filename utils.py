
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
    memory_info = proxmox.nodes(node).status.get()['memory']

    mem_used = memory_info.get('used', 0) / (1024**3)
    mem_total = memory_info.get('total', 1) / (1024**3)

    return mem_used, mem_total


def get_resource_usage(proxmox, **filters):
    resources = proxmox.cluster().resources.get()
    
    for resource in resources:

        if all(resource.get(k) == v for k, v in filters.items()):
            used = resource.get('disk', 0) / (1024**3)
            total = resource.get('maxdisk', 1) / (1024**3)
            return used, total

    return 0, 1


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


