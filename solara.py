#!/usr/bin/env python3
"""
Solara - Educational Nmap Interface
A Python wrapper for Nmap with educational features and safety checks
"""

import subprocess
import sys
import re
import json
from datetime import datetime
import argparse

class Solara:
    def __init__(self):
        self.name = "Solara"
        self.version = "1.0"
        self.banner = f"""
╔═══════════════════════════════════════╗
║           {self.name} v{self.version}                    ║
║     Educational Nmap Interface        ║
║                                       ║
║  ⚠️  FOR AUTHORIZED TESTING ONLY ⚠️   ║
╚═══════════════════════════════════════╝
"""
        self.safe_ranges = [
            "127.0.0.1",
            "10.0.0.0/8",
            "172.16.0.0/12", 
            "192.168.0.0/16"
        ]

    def print_banner(self):
        print(self.banner)
        print("Remember: Only scan networks you own or have explicit permission to test!\n")

    def check_nmap_installed(self):
        """Check if nmap is installed on the system"""
        try:
            result = subprocess.run(['nmap', '--version'], 
                                  capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Error: Nmap is not installed or not in PATH")
            print("Install with: sudo apt install nmap (Debian/Ubuntu)")
            print("             sudo yum install nmap (RHEL/CentOS)")
            return False

    def validate_target(self, target):
        """Basic validation to encourage responsible use"""
        # Check for localhost/private ranges
        private_patterns = [
            r'^127\.',
            r'^10\.',
            r'^172\.(1[6-9]|2[0-9]|3[01])\.',
            r'^192\.168\.',
            r'^localhost$'
        ]
        
        for pattern in private_patterns:
            if re.match(pattern, target):
                return True
        
        print(f"⚠️  Warning: '{target}' appears to be a public IP/domain")
        response = input("Are you authorized to scan this target? (yes/no): ")
        return response.lower() in ['yes', 'y']

    def basic_scan(self, target):
        """Perform a basic Nmap scan"""
        if not self.validate_target(target):
            print("❌ Scan cancelled for safety reasons")
            return
        
        print(f"🔍 Running basic scan on {target}...")
        cmd = ['nmap', '-sV', target]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            print("\n" + "="*60)
            print("BASIC SCAN RESULTS")
            print("="*60)
            print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
        except subprocess.TimeoutExpired:
            print("❌ Scan timed out after 5 minutes")
        except Exception as e:
            print(f"❌ Error running scan: {e}")

    def port_scan(self, target, ports="1-1000"):
        """Scan specific ports"""
        if not self.validate_target(target):
            print("❌ Scan cancelled for safety reasons")
            return
        
        print(f"🔍 Scanning ports {ports} on {target}...")
        cmd = ['nmap', '-p', ports, target]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            print("\n" + "="*60)
            print(f"PORT SCAN RESULTS ({ports})")
            print("="*60)
            print(result.stdout)
        except subprocess.TimeoutExpired:
            print("❌ Scan timed out")
        except Exception as e:
            print(f"❌ Error: {e}")

    def stealth_scan(self, target):
        """SYN stealth scan"""
        if not self.validate_target(target):
            print("❌ Scan cancelled for safety reasons")
            return
        
        print(f"🥷 Running stealth scan on {target}...")
        print("Note: This may require root privileges")
        cmd = ['nmap', '-sS', '-O', target]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            print("\n" + "="*60)
            print("STEALTH SCAN RESULTS")
            print("="*60)
            print(result.stdout)
        except subprocess.TimeoutExpired:
            print("❌ Scan timed out")
        except Exception as e:
            print(f"❌ Error: {e}")

    def vulnerability_scan(self, target):
        """Basic vulnerability detection"""
        if not self.validate_target(target):
            print("❌ Scan cancelled for safety reasons")
            return
        
        print(f"🔍 Running vulnerability scan on {target}...")
        cmd = ['nmap', '--script', 'vuln', target]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            print("\n" + "="*60)
            print("VULNERABILITY SCAN RESULTS")
            print("="*60)
            print(result.stdout)
        except subprocess.TimeoutExpired:
            print("❌ Scan timed out")
        except Exception as e:
            print(f"❌ Error: {e}")

    def get_local_network(self):
        """Get the local network range"""
        try:
            # Get default gateway and network info
            import socket
            import ipaddress
            
            # Connect to a remote address to get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            # Get network interface info using ip command
            result = subprocess.run(['ip', 'route', 'show'], 
                                  capture_output=True, text=True)
            
            # Parse for local network
            for line in result.stdout.split('\n'):
                if 'src ' + local_ip in line and '/' in line:
                    parts = line.split()
                    for part in parts:
                        if '/' in part and not part.startswith('169.254'):
                            return part, local_ip
            
            # Fallback: assume /24 network
            network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
            return str(network), local_ip
            
        except Exception as e:
            print(f"❌ Could not detect local network: {e}")
            return None, None

    def wifi_scan(self):
        """Discover devices on current WiFi network"""
        print("🔍 Detecting local WiFi network...")
        
        network, local_ip = self.get_local_network()
        if not network:
            print("❌ Could not detect local network. Try manual discovery with: discover 192.168.1.0/24")
            return
        
        print(f"📡 Local IP: {local_ip}")
        print(f"🌐 Network: {network}")
        print(f"🔍 Scanning for devices on your WiFi network...")
        
        # Enhanced discovery with device info
        cmd = ['nmap', '-sn', '--dns-resolution', network]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            print("\n" + "="*70)
            print("🏠 WIFI NETWORK DEVICES")
            print("="*70)
            
            # Parse and format the output nicely
            lines = result.stdout.split('\n')
            devices = []
            current_device = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith('Nmap scan report for'):
                    if current_device:
                        devices.append(current_device)
                    current_device = {}
                    # Extract IP and hostname
                    if '(' in line and ')' in line:
                        hostname = line.split('for ')[1].split(' (')[0]
                        ip = line.split('(')[1].split(')')[0]
                        current_device['hostname'] = hostname
                        current_device['ip'] = ip
                    else:
                        ip = line.split('for ')[1]
                        current_device['hostname'] = 'Unknown'
                        current_device['ip'] = ip
                elif line.startswith('MAC Address:'):
                    mac_info = line.replace('MAC Address: ', '')
                    if '(' in mac_info:
                        mac = mac_info.split(' (')[0]
                        vendor = mac_info.split('(')[1].replace(')', '')
                        current_device['mac'] = mac
                        current_device['vendor'] = vendor
                    else:
                        current_device['mac'] = mac_info
                        current_device['vendor'] = 'Unknown'
                elif 'Host is up' in line:
                    current_device['status'] = 'UP'
            
            # Add last device
            if current_device:
                devices.append(current_device)
            
            # Display results in a nice format
            if devices:
                print(f"Found {len(devices)} devices on the network:\n")
                for i, device in enumerate(devices, 1):
                    print(f"🔹 Device {i}:")
                    print(f"   IP Address: {device.get('ip', 'Unknown')}")
                    print(f"   Hostname:   {device.get('hostname', 'Unknown')}")
                    if 'mac' in device:
                        print(f"   MAC:        {device.get('mac', 'Unknown')}")
                        print(f"   Vendor:     {device.get('vendor', 'Unknown')}")
                    print(f"   Status:     {device.get('status', 'Unknown')}")
                    print()
                
                # Show your device
                print(f"🏠 Your device IP: {local_ip}")
                print(f"📊 Total devices found: {len(devices)}")
            else:
                print("No devices found or unable to parse results")
                print("\nRaw output:")
                print(result.stdout)
                
        except subprocess.TimeoutExpired:
            print("❌ WiFi scan timed out after 5 minutes")
        except Exception as e:
            print(f"❌ Error during WiFi scan: {e}")

    def website_scan(self):
        """Interactive website port scanning"""
        print("🌐 Website Port Scanner")
        print("="*50)
        
        # Get website from user
        while True:
            website = input("Enter website/domain to scan: ").strip()
            if not website:
                print("❌ Please enter a valid website")
                continue
            
            # Remove protocol if present
            website = website.replace('https://', '').replace('http://', '')
            website = website.split('/')[0]  # Remove path if present
            
            # Validate domain format
            if '.' not in website:
                print("❌ Please enter a valid domain (e.g., example.com)")
                continue
            
            break
        
        # Warning for external scanning
        print(f"\n⚠️  You are about to scan: {website}")
        print("⚠️  Make sure you have permission to scan this target!")
        print("⚠️  Unauthorized scanning may violate terms of service or laws.")
        
        confirm = input("\nDo you have permission to scan this website? (yes/no): ").lower()
        if confirm not in ['yes', 'y']:
            print("❌ Scan cancelled for safety reasons")
            return
        
        # Scan type selection
        print("\n🎯 Select scan type:")
        print("1. Quick scan (common ports)")
        print("2. Web services (80, 443, 8080, 8443)")
        print("3. Full scan (1-65535) - WARNING: Very slow!")
        print("4. Custom port range")
        print("5. Single port")
        
        choice = input("Choose scan type (1-5): ").strip()
        
        if choice == '1':
            ports = "1-1000"
            scan_name = "Quick Scan"
        elif choice == '2':
            ports = "80,443,8080,8443,8000,3000,5000,9000"
            scan_name = "Web Services Scan"
        elif choice == '3':
            print("⚠️  Full scan can take 30+ minutes and may trigger security alerts!")
            confirm_full = input("Are you sure? (yes/no): ").lower()
            if confirm_full not in ['yes', 'y']:
                print("❌ Full scan cancelled")
                return
            ports = "1-65535"
            scan_name = "Full Port Scan"
        elif choice == '4':
            ports = input("Enter port range (e.g., 1-1000, 80,443,8080): ").strip()
            if not ports:
                print("❌ Invalid port range")
                return
            scan_name = f"Custom Scan ({ports})"
        elif choice == '5':
            port = input("Enter single port to scan: ").strip()
            if not port.isdigit():
                print("❌ Invalid port number")
                return
            ports = port
            scan_name = f"Single Port Scan ({port})"
        else:
            print("❌ Invalid choice")
            return
        
        print(f"\n🔍 Running {scan_name} on {website}...")
        print(f"📊 Scanning ports: {ports}")
        print("⏳ This may take a while depending on scan type...")
        
        # Build nmap command
        cmd = ['nmap', '-sV', '-sC', '--open', '-p', ports, website]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
            
            print("\n" + "="*70)
            print(f"🌐 WEBSITE SCAN RESULTS: {website}")
            print("="*70)
            
            # Parse and display results nicely
            lines = result.stdout.split('\n')
            open_ports = []
            service_info = {}
            
            for line in lines:
                if '/tcp' in line and 'open' in line:
                    parts = line.split()
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else 'unknown'
                    version = ' '.join(parts[3:]) if len(parts) > 3 else ''
                    
                    open_ports.append(port)
                    service_info[port] = {'service': service, 'version': version}
            
            if open_ports:
                print(f"🎯 Found {len(open_ports)} open ports:\n")
                
                for port in open_ports:
                    service = service_info[port]['service']
                    version = service_info[port]['version']
                    
                    print(f"🔹 Port {port}:")
                    print(f"   Service: {service}")
                    if version:
                        print(f"   Version: {version}")
                    
                    # Add common port descriptions
                    port_descriptions = {
                        '21': 'FTP - File Transfer Protocol',
                        '22': 'SSH - Secure Shell',
                        '23': 'Telnet',
                        '25': 'SMTP - Email (outgoing)',
                        '53': 'DNS - Domain Name Service',
                        '80': 'HTTP - Web Server',
                        '110': 'POP3 - Email (incoming)',
                        '143': 'IMAP - Email (incoming)',
                        '443': 'HTTPS - Secure Web Server',
                        '993': 'IMAPS - Secure IMAP',
                        '995': 'POP3S - Secure POP3',
                        '3389': 'RDP - Remote Desktop',
                        '5432': 'PostgreSQL Database',
                        '3306': 'MySQL Database',
                        '8080': 'HTTP Alternative/Proxy',
                        '8443': 'HTTPS Alternative'
                    }
                    
                    if port in port_descriptions:
                        print(f"   Info: {port_descriptions[port]}")
                    print()
                
                # Security recommendations
                print("🔒 SECURITY NOTES:")
                if '21' in open_ports:
                    print("   ⚠️  FTP (21) - Consider using SFTP/FTPS instead")
                if '23' in open_ports:
                    print("   ⚠️  Telnet (23) - Unencrypted! Use SSH instead")
                if '80' in open_ports and '443' not in open_ports:
                    print("   ⚠️  Only HTTP (80) - Consider adding HTTPS (443)")
                if '22' in open_ports:
                    print("   ✅ SSH (22) - Ensure strong authentication")
                if '443' in open_ports:
                    print("   ✅ HTTPS (443) - Good security practice")
                    
            else:
                print("❌ No open ports found in the scanned range")
                print("   This could mean:")
                print("   • Ports are filtered by firewall")
                print("   • Services are not running")
                print("   • Different ports are in use")
            
            print(f"\n📊 Scan completed for {website}")
            print(f"🔍 Ports scanned: {ports}")
            
            # Show raw output option
            show_raw = input("\nShow raw nmap output? (y/n): ").lower()
            if show_raw in ['y', 'yes']:
                print("\n" + "="*70)
                print("RAW NMAP OUTPUT")
                print("="*70)
                print(result.stdout)
                if result.stderr:
                    print("\nErrors/Warnings:")
                    print(result.stderr)
                    
        except subprocess.TimeoutExpired:
            print("❌ Scan timed out (30 minutes)")
            print("   Try a smaller port range or single ports")
        except Exception as e:
            print(f"❌ Error during website scan: {e}")

    def network_discovery(self, network):
        """Discover hosts on a network"""
        if not self.validate_target(network):
            print("❌ Scan cancelled for safety reasons")
            return
        
        print(f"🌐 Discovering hosts on {network}...")
        cmd = ['nmap', '-sn', network]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            print("\n" + "="*60)
            print("HOST DISCOVERY RESULTS")
            print("="*60)
            print(result.stdout)
        except subprocess.TimeoutExpired:
            print("❌ Scan timed out")
        except Exception as e:
            print(f"❌ Error: {e}")

    def show_help(self):
        """Display help information"""
        help_text = """
🎯 SOLARA COMMANDS:

1. basic <target>           - Basic version detection scan
2. ports <target> [range]   - Scan specific ports (default: 1-1000)
3. stealth <target>         - SYN stealth scan with OS detection
4. vuln <target>            - Vulnerability detection scan
5. discover <network>       - Host discovery (e.g., 192.168.1.0/24)
6. wifi                     - Discover devices on current WiFi network
7. website                  - Interactive website port scanner
8. help                     - Show this help
9. exit                     - Quit Solara

📝 EXAMPLES:
   basic 127.0.0.1
   ports 192.168.1.1 80,443,8080
   stealth localhost
   vuln 10.0.0.1
   discover 192.168.1.0/24
   wifi
   website

⚠️  ETHICAL GUIDELINES:
• Only scan systems you own or have written permission to test
• WiFi scanning only works on networks you're connected to and authorized to test
• Website scanning may violate terms of service - ensure you have permission!
• Respect rate limits and don't overwhelm targets
• Be aware of legal implications in your jurisdiction
• Use knowledge responsibly for defense, not offense

📚 LEARNING RESOURCES:
• Nmap official documentation: https://nmap.org/book/
• Practice on: TryHackMe, HackTheBox, VulnHub
• Set up your own lab environment for safe testing
"""
        print(help_text)

    def interactive_mode(self):
        """Run in interactive mode"""
        self.print_banner()
        
        if not self.check_nmap_installed():
            return
        
        self.show_help()
        
        while True:
            try:
                command = input("\n🔥 solara> ").strip().split()
                
                if not command:
                    continue
                
                cmd = command[0].lower()
                
                if cmd == 'exit':
                    print("👋 Thanks for using Solara responsibly!")
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'basic':
                    if len(command) > 1:
                        self.basic_scan(command[1])
                    else:
                        print("❌ Usage: basic <target>")
                elif cmd == 'ports':
                    if len(command) > 1:
                        ports = command[2] if len(command) > 2 else "1-1000"
                        self.port_scan(command[1], ports)
                    else:
                        print("❌ Usage: ports <target> [port_range]")
                elif cmd == 'stealth':
                    if len(command) > 1:
                        self.stealth_scan(command[1])
                    else:
                        print("❌ Usage: stealth <target>")
                elif cmd == 'vuln':
                    if len(command) > 1:
                        self.vulnerability_scan(command[1])
                    else:
                        print("❌ Usage: vuln <target>")
                elif cmd == 'website':
                    self.website_scan()
                elif cmd == 'wifi':
                    self.wifi_scan()
                elif cmd == 'discover':
                    if len(command) > 1:
                        self.network_discovery(command[1])
                    else:
                        print("❌ Usage: discover <network>")
                else:
                    print(f"❌ Unknown command: {cmd}. Type 'help' for commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 Exiting Solara...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Solara - Educational Nmap Interface')
    parser.add_argument('--target', help='Target to scan')
    parser.add_argument('--scan-type', choices=['basic', 'ports', 'stealth', 'vuln', 'discover', 'wifi', 'website'],
                       help='Type of scan to perform')
    
    args = parser.parse_args()
    
    solara = Solara()
    
    if args.target and args.scan_type:
        # Command line mode
        if not solara.check_nmap_installed():
            sys.exit(1)
        
        if args.scan_type == 'basic':
            solara.basic_scan(args.target)
        elif args.scan_type == 'ports':
            solara.port_scan(args.target)
        elif args.scan_type == 'stealth':
            solara.stealth_scan(args.target)
        elif args.scan_type == 'vuln':
            solara.vulnerability_scan(args.target)
        elif args.scan_type == 'discover':
            solara.network_discovery(args.target)
        elif args.scan_type == 'wifi':
            solara.wifi_scan()
        elif args.scan_type == 'website':
            solara.website_scan()
    else:
        # Interactive mode
        solara.interactive_mode()

if __name__ == "__main__":
    main()
