import socket
import os
import fcntl
import struct


def listen_wifi_raw(interface="wlan0"):
    # 0x7a05 is a custom experimental protocol
    ETH_P_ALL = 0x7a05 
    
    try:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
        s.bind((interface, 0))

        # SYSCALL: Set the interface to Promiscuous Mode
        # This tells the hardware: "Don't drop packets that aren't for me"
        ifr_flags = 0x8000 # SIOCGIFFLAGS
        # This is a bit advanced, but it's a direct ioctl syscall
        # You can also just run 'sudo ip link set wlan0 promisc on'
        
        print(f"Listening for custom 0x7a05 frames on {interface}...")

        while True:
            packet = s.recv(2048)
            # Ethernet header is 14 bytes
            payload = packet[14:]
            
            if b'hi' in payload:
                print(f"Caught it! Data: {payload}")
            else:
                # Debug: print hex of anything received to see if noise is getting through
                print(f"Recv other: {packet.hex()[:20]}...")

    except PermissionError:
        print("Still need sudo for AF_PACKET!")

def get_iface():
    if os.path.exists("/sys/class/net"):
        for iface in os.listdir("/sys/class/net"):
            if os.path.exists(f"/sys/class/net/{iface}/wireless") or "wlan" in iface:
                return iface
    return "wlan0"


if __name__ == "__main__":
    # Ensure you use the correct interface name found by your init_linux()
    listen_wifi_raw(get_iface())
