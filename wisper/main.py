import struct
import socket
import netifaces
import threading

MCAST_GRP = '255.1.1.1'
PORT = 5005

def get_wifi_ip() -> str:
    ifaces = netifaces.interfaces()
    ip = ''

    for iface in ifaces:
        if 2 in netifaces.ifaddresses(iface).keys():
            if '10.' in netifaces.ifaddresses(iface)[2][0]['addr']:
                ip = netifaces.ifaddresses(iface)[2][0]['addr']
                break

    return ip

def listener(ip: str) -> None:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("", PORT))

    ifindex = socket.if_nametoindex('wlx00e030006065')

    mreq = struct.pack(
        "4sll",
        socket.inet_aton(MCAST_GRP),  # multicast group
        socket.INADDR_ANY,            # local address
        ifindex                       # interface index (THIS fixes it)
    )

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print("Listening for multicast...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received: {data.decode()} from {addr}")


def caster(ip: str) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    sock.sendto("hello".encode('utf-8'), (MCAST_GRP, PORT))

def main() -> None:
    ip = get_wifi_ip()

    t = threading.Thread(target=listener, args=(ip,), daemon=True)
    t.start()

    caster(ip)

    t.join()

if __name__ == '__main__':
    main()
