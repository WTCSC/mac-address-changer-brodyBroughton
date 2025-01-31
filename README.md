[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/tp86o73G)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17729752)

# MAC Address Changer

This MAC Address changer **Python and Bash script** safely changes your network interface's MAC address while preserving the original address for future reference. The script generates a random MAC address and handles the entire process of bringing the interface down, changing the address, and bringing it back up.

## Features and Key Benefits

- Automatically detects the primary network interface
- Generates cryptographically sound random MAC addresses
- Preserves the original MAC address in a separate file
- Includes comprehensive error handling and validation
- Requires minimal user intervention
- Maintains network security best practices

## Installation Instructions and Dependencies

### Prerequisites
- **Python 3.x** (Tested with Python 3.8+)
- Linux-based operating system
- Root/sudo privileges
- Basic command line knowledge
- `ip` command (usually pre-installed on most Linux distributions)

### Installation Steps
1. Clone the repository:
```bash
git clone https://github.com/WTCSC/mac-address-changer-brodyBroughton.git
cd mac-address-changer-brodyBroughton
```

2. Ensure Python is installed and check the version:
```bash
python3 --version
```

3. Run the script:
```bash
sudo python3 smackncheese.py
```

4. Alternatively, for the Bash script:
```bash
chmod +x macncheese.sh
sudo ./macncheese.sh
```

## Usage Examples with Command-line Arguments

Basic usage:
```bash
sudo python3 smackncheese.py
```

Check current MAC address:
```bash
ip link show
```

View original MAC address:
```bash
cat ogmacaddress.txt
```

## Error Handling and Validation

The script includes comprehensive error handling for common scenarios:

### Python Error Handling

1. **Interface Detection:**
```python
if not interface:
    print("Error: Could not detect network interface")
    exit(1)
```

2. **MAC Address Validation:**
```python
if not is_valid_mac(new_mac):
    print("Error: Invalid MAC address generated")
    exit(1)
```

3. **Network Interface Operations:**
```python
try:
    subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
except subprocess.CalledProcessError:
    print("Error: Failed to bring interface down")
    exit(1)
```

### Bash Error Handling

1. **Interface Detection:**
```bash
if [[ -z "$interface" ]]; then
    echo "Error: Could not detect network interface"
    exit 1
fi
```

2. **MAC Address Validation:**
```bash
if ! [[ $random_mac =~ ^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$ ]]; then
    echo "Error: Invalid MAC address generated"
    exit 1
fi
```

3. **Network Interface Operations:**
```bash
if ! sudo ip link set dev $interface down; then
    echo "Error: Failed to bring interface down"
    exit 1
fi

if ! sudo ip link set dev $interface address $random_mac; then
    echo "Error: Failed to change MAC address"
    sudo ip link set dev $interface up
    exit 1
fi

if ! sudo ip link set dev $interface up; then
    echo "Error: Failed to bring interface up"
    exit 1
fi
```

## Common Troubleshooting Tips

1. **Permission Issues**
   - Error: "Permission denied"
   - Solution: Ensure you're running with sudo privileges
   ```bash
   sudo python3 smackncheese.py
   ```

2. **Interface Not Found**
   - Error: "Could not detect network interface"
   - Solution: List available interfaces and verify network connection
   ```bash
   ip link show
   ```

3. **MAC Address Change Failed**
   - Error: "Failed to change MAC address"
   - Solution: Verify no other processes are using the interface
   ```bash
   sudo lsof -i
   ```

## Script Demonstration

Here's what happens when you run the script:

1. **Initial Check:**
```bash
$ sudo python3 smackncheese.py
Original MAC address can be found in ogmacaddress.txt
```

2. **Process Output:**
```bash
Network interface: wlan0
MAC address changed to: 02:45:78:9A:BC:DE
```

3. **Check Original MAC Address (optional):**
```bash
$ cat ogmacaddress.txt
```
# Shell
![Shell Gif demonstration](shelldemonstration.gif)

# Python
![Python Gif demonstration](pythondemonstration.gif)

## Security Considerations

- Always backup your original MAC address (automatically done by the script)
- Use with caution on production systems
- May need to reconfigure network settings after MAC change
- Some networks may block devices with changed MAC addresses

## Project Structure
```
mac-address-changer-brodyBroughton/
├── demonstration.gif      # Gif demonstration
├── smackncheese.py        # Python script
├── macncheese.sh          # Bash script
├── ogmacaddress.txt       # Original MAC address backup
└── README.md              # This file
```

## Script Components

### MAC Address Detection:
```python
def get_original_mac_address(interface):
    try:
        ip_output = subprocess.run(
            ["ip", "link", "show", interface],
            capture_output=True,
            text=True,
            check=True
        ).stdout
        match = re.search(r'link/ether\s+([0-9A-Fa-f:]+)', ip_output)
        return match.group(1) if match else ""
    except subprocess.CalledProcessError:
        return ""
```

### Interface Detection:
```python
def find_network_interface():
    try:
        ip_output = subprocess.run(["ip", "link", "show"], capture_output=True, text=True, check=True).stdout
        for line in ip_output.splitlines():
            match = re.match(r'^\d+:\s+([^:@]+)[:@]', line)
            if match and match.group(1) != "lo":
                return match.group(1).strip()
        return None
    except subprocess.CalledProcessError:
        return None
```

### Random MAC Generation:
```python
def generate_random_mac():
    return "02:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )
```

### Exit Codes
- 0: Success
- 1: General error (interface not found, invalid MAC, etc.)