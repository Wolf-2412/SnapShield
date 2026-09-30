import psutil
from collections import Counter


def collect_network_snapshot():
    connections = []

    try:
        raw_connections = psutil.net_connections(kind="inet")
    except Exception as e:
        return {
            "error": str(e),
            "connections": [],
            "summary": {}
        }

    for conn in raw_connections:
        local = conn.laddr
        remote = conn.raddr

        local_ip = local.ip if local else ""
        local_port = local.port if local else 0

        remote_ip = ""
        remote_port = 0

        if remote:
            try:
                remote_ip = remote.ip
                remote_port = remote.port
            except AttributeError:
                pass

        connections.append({
            "local_ip": local_ip,
            "local_port": local_port,
            "remote_ip": remote_ip,
            "remote_port": remote_port,
            "status": conn.status,
            "pid": conn.pid
        })

    remote_ports = [
        c["remote_port"]
        for c in connections
        if c["remote_port"]
    ]

    remote_ips = [
        c["remote_ip"]
        for c in connections
        if c["remote_ip"]
    ]

    established = sum(
        1 for c in connections
        if c["status"] == "ESTABLISHED"
    )

    listening = sum(
        1 for c in connections
        if c["status"] == "LISTEN"
    )

    return {
        "connections": connections,
        "summary": {
            "total_connections": len(connections),
            "established": established,
            "listening": listening,
            "unique_remote_ips": len(set(remote_ips)),
            "unique_remote_ports": len(set(remote_ports))
        }
    }