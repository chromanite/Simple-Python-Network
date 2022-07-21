import argparse
from ipaddress import ip_address
import struct
import socket

def CIDR_to_subnet(CIDR) -> list:
    host_bits = 32 - int(CIDR)
    subnet = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return list(int(sub) for sub in subnet.split("."))

def class_parser(class_type, octets, CIDR) -> None:
    network_list = list()
    usable_range = list()
    total_num_host = 2**(32 - CIDR)
    if class_type == 'A':
        network = 7
        host = 24
        address_type = 'Network.Host.Host.Host'
    elif class_type == 'B':
        network = 14
        host = 16
        address_type = 'Network.Network.Host.Host'
    elif class_type == 'C':
        network = 21
        host = 8
        address_type = 'Network.Network.Network.Host'

    if CIDR >= 8 and CIDR <= 15:
        CIDR_class = 'A'
    elif CIDR >= 16 and CIDR <= 23:
        CIDR_class = 'B'
    elif CIDR >= 24 and CIDR <= 32:
        CIDR_class = 'C'

    dec_cidr = CIDR_to_subnet(CIDR)

    for i in range(4):
        network_list.append(bin(octets[i] & dec_cidr[i])[2:].zfill(8))

    FORMATTING = "{:<15} | {:<8} | {:<8} | {:<8} | {:<8} |"

    print(FORMATTING.format("IP Address", octets[0], octets[1], octets[2], octets[3]))
    print(FORMATTING.format("IP Add (bin)", bin(octets[0])[2:].zfill(8), bin(octets[1])[2:].zfill(8), bin(octets[2])[2:].zfill(8), bin(octets[3])[2:].zfill(8)))
    print(FORMATTING.format(("/" + str(CIDR)), bin(dec_cidr[0])[2:].zfill(8), bin(dec_cidr[1])[2:].zfill(8), bin(dec_cidr[2])[2:].zfill(8), bin(dec_cidr[3])[2:].zfill(8)))
    print(FORMATTING.format("Network Prefix", network_list[0], network_list[1], network_list[2], network_list[3]))

    network_list = [int(octet, 2) for octet in network_list]
    print(FORMATTING.format(" ", network_list[0], network_list[1], network_list[2], network_list[3]))

    available_address = int(total_num_host / 256)

    print(f"\nNetwork Class Type: {class_type}")
    print(f"Network address: {address_type}\n")
    
    print(f"IP Class Type: {CIDR_class}")
    print(f"Number of address available for networks: {2**network}")
    print(f"Number of address available for hosts: {2**host}")
    print(f"Number of available addresses: {available_address}")
    ip_addr = str(f"{network_list[0]}.{network_list[1]}.{network_list[2]}.{network_list[3]}")

    print(f"\nNetwork Address: {ip_addr}/{CIDR}")
    
    if CIDR_class == 'A':
        for i in range(total_num_host):
            usable_range.append(network_list[0] + "." + network_list[1] + "." + network_list[2] + "." + str(i))
    elif CIDR_class == 'B':
        for i in range (total_num_host):
            usable_range.append(f"{network_list[0]}.{network_list[1]}.{network_list[2]}.{network_list[3]}")
            network_list[3] += 1
            if network_list[3] > 255:
                network_list[3] = 0
                network_list[2] += 1
                if network_list[2] > 255:
                    network_list[2] = 0
                    network_list[1] += 1
                    if network_list[1] > 255:
                        network_list[1] = 0
                        network_list[0] += 1
    elif CIDR_class == 'C':
        for i in range (total_num_host):
            usable_range.append(f"{network_list[0]}.{network_list[1]}.{network_list[2]}.{network_list[3]}")
            network_list[3] += 1
            if network_list[3] > 255:
                network_list[3] = 0
                network_list[2] += 1
                if network_list[2] > 255:
                    network_list[2] = 0
                    network_list[1] += 1
                    if network_list[1] > 255:
                        network_list[1] = 0
                        network_list[0] += 1

    usable_range.pop(0)
    broadcast_addr = usable_range.pop()
    
    with open(f'usable_range {ip_addr}.txt', 'w') as f:
        for i in usable_range:
            f.write(i + '\n')

    print(f"Usable Host IP Range: {usable_range[0]} - {usable_range[-1]}")
    print(f"Broadcast Address: {broadcast_addr}")
    print(f"Total number of hosts: {total_num_host}")
    print(f"Number of usable hosts: {total_num_host - 2}\n")
    print(f"Subnet Mask: {dec_cidr[0]}.{dec_cidr[1]}.{dec_cidr[2]}.{dec_cidr[3]}")
    print(f"Wildcard Mask: {255 - dec_cidr[0]}.{255 - dec_cidr[1]}.{255 - dec_cidr[2]}.{255 - dec_cidr[3]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="IP address", required=True)
    parser.add_argument("-c", "--cidr", help="CIDR range", required=True)
    IP = parser.parse_args().ip
    CIDR = parser.parse_args().cidr

    octets = list(int(octet) for octet in IP.split("."))

    if octets[0] <= 127:
        class_parser(class_type='A', octets=octets, CIDR=int(CIDR))
    elif octets[0] <= 191:
        class_parser(class_type='B', octets=octets, CIDR=int(CIDR))
    elif octets[0] <= 223:
        class_parser(class_type='C', octets=octets, CIDR=int(CIDR))


if __name__ == "__main__":
    main()
