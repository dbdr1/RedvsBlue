import os
import datetime

def get_arp_table():
    arp_table_data = os.popen('arp -a').read()
    arp_lines = arp_table_data.split('\n')
    arp_dict = {}

    for line in arp_lines:
        if line.strip() and 'dynamic' in line:
            parts = line.split()
            ip = parts[0]
            mac = parts[1]
            arp_dict[ip] = mac

    return arp_dict

def log_arp_spoof_event(ip, mac):
    event_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"Arp spoofed! \nThe address is: {mac} for IP: {ip} \nDATE: {event_time}"

    with open("arp_spoof_log.txt", "a") as log_file:
        log_file.write(log_message)

def check_mac_duplication(arp_data):
    mac_addresses = []
    event_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for ip, mac in arp_data.items():
        if mac in mac_addresses:
            print(f"Arp spoofed! \nThe address is: {mac} for IP: {ip} \nDATE: {event_time}")
            log_arp_spoof_event(ip, mac)
        else:
            mac_addresses.append(mac)

def main():
    arp_data = get_arp_table()
    check_mac_duplication(arp_data)

if __name__ == "__main__":
    main()