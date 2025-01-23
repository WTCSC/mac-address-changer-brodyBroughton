import subprocess

# Store original MAC address
original_mac = subprocess.run(ip link show | awk -F'ether ' '/ether/ {print $2}' | head -n1)
echo "Original MAC address can be found in ogmacaddress.txt"

# Save original MAC address to a file
echo "$original_mac" > ogmacaddress.txt

# Get network interface
interface=$(ip link show | awk -F': ' '/^[0-9]+/ {print $2}' | grep -v 'lo' | head -n1)

if [[ -z "$interface" ]]; then
    echo "Error: Could not detect network interface"
    exit 1
fi

# Generate a random MAC address
random_mac=$(printf '02:%02x:%02x:%02x:%02x:%02x' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)))

# Validate MAC address format
if ! [[ $random_mac =~ ^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$ ]]; then
    echo "Error: Invalid MAC address generated"
    exit 1
fi

# Set the interface down
if ! sudo ip link set dev $interface down; then
    echo "Error: Failed to bring interface down"
    exit 1
fi

# Add the random MAC
if ! sudo ip link set dev $interface address $random_mac; then
    echo "Error: Failed to change MAC address"
    sudo ip link set dev $interface up
    exit 1
fi

# Set the interface up
if ! sudo ip link set dev $interface up; then
    echo "Error: Failed to bring interface up"
    exit 1
fi

echo "Network interface: $interface"
echo "MAC address changed to: $random_mac"