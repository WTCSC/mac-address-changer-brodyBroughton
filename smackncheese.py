import subprocess
import re
import random
import os

def get_original_mac_address(interface):
    """
    Gets the original MAC address directly from the ip link show command
    before any changes are made.
    """
    try:
        ip_output = subprocess.run(["ip", "link", "show", interface], capture_output=True, text=True, check=True).stdout
        
        # Look for the current hardware address
        # Using link/ether pattern which shows the actual hardware address
        mac_regex = r'link/ether\s+([0-9A-Fa-f:]+)'
        match = re.search(mac_regex, ip_output)
        
        if match:
            return match.group(1)
        
        return ""

    except subprocess.CalledProcessError:
        
        return ""

def find_network_interface():
    """
    Finds the first available network interface
    Returns the interface name as a string
    """
    try:
        ip_output = subprocess.run(["ip", "link", "show"], capture_output=True, text=True, check=True).stdout
        
        for line in ip_output.splitlines():
            # Match interface names, excluding loopback
            match = re.match(r'^\d+:\s+([^:@]+)[:@]', line)

            if match and match.group(1) != "lo":
                return match.group(1).strip()
            
        return None
        
    except subprocess.CalledProcessError:
        
        return None

def is_valid_mac(mac_address):

    # Checks if a MAC address is in the correct format.

    mac_regex = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
    return bool(re.match(mac_regex, mac_address))

def generate_random_mac():
    """
    Generates a random MAC address starting with 02.
    """
    return "02:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

def change_mac_address(interface, new_mac):
    """
    Changes the MAC address of the specified network interface.
    """
    try:
        # Disable interface
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
        
        # Change MAC
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac], check=True)
        
        # Enable interface
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)
        
        return True
    
    except subprocess.CalledProcessError as error:
        print(f"Error changing MAC address: {error}")
        # Try to bring interface back up
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"])
        return False

def main():
    interface = find_network_interface()
    if not interface:
        print("Error: Could not detect network interface")
        exit(1)

    # Check if the original MAC is already stored
    if os.path.exists("ogmacaddress.txt"):
        with open("ogmacaddress.txt", "r") as f:
            original_mac = f.read().strip()
        print("Original MAC address retrieved from ogmacaddress.txt")

    else:
        # Get and save the original MAC BEFORE making any changes
        original_mac = get_original_mac_address(interface)

        if original_mac:
            print("Original MAC address saved to ogmacaddress.txt")
            with open("ogmacaddress.txt", "w") as f:
                f.write(original_mac)

        else:
            print("Error: Could not get original MAC address")
            exit(1)

    # Generate and validate new MAC address
    new_mac = generate_random_mac()

    if not is_valid_mac(new_mac):
        print("Error: Invalid MAC address generated")
        exit(1)

    # Change the MAC address
    if change_mac_address(interface, new_mac):
        print(f"Network interface: {interface}")
        print(f"MAC address changed to: {new_mac}")

    else:
        print("Failed to change MAC address")
        exit(1)

if __name__ == "__main__":
    main()