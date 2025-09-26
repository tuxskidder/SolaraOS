#!/usr/bin/env python3
"""
Solara Python - Educational Nmap Interface with Color Customization
A Python wrapper for Nmap with educational features, safety checks, and customizable colors
"""

import subprocess
import sys
import re
import json
import socket
import ipaddress
import tempfile
import shutil
import os
import time
import random
from datetime import datetime
import argparse

class ColorManager:
    """Manages text coloring with customizable themes"""
    
    def __init__(self):
        self.current_color = 1  # Default to white
        self.rainbow_colors = [
            '\033[91m',  # Red
            '\033[93m',  # Yellow
            '\033[92m',  # Green
            '\033[96m',  # Cyan
            '\033[94m',  # Blue
            '\033[95m',  # Magenta
        ]
        self.rainbow_index = 0
        
        self.color_map = {
            1: '\033[97m',   # White
            2: '\033[92m',   # Green
            3: '\033[91m',   # Red
            4: '\033[94m',   # Blue
            5: '\033[93m',   # Yellow
            6: '\033[95m',   # Magenta
            7: '\033[96m',   # Cyan
            8: '\033[90m',   # Dark Gray
            9: '\033[37m',   # Light Gray
            10: '\033[31m',  # Dark Red
            11: '\033[32m',  # Dark Green
            12: '\033[34m',  # Dark Blue
            13: '\033[35m',  # Dark Magenta
            14: '\033[36m',  # Dark Cyan
            15: '\033[33m',  # Dark Yellow
            16: '\033[1;91m', # Bright Red
            17: '\033[1;92m', # Bright Green
            18: '\033[1;94m', # Bright Blue
            19: '\033[1;95m', # Bright Magenta
            20: '\033[1;96m', # Bright Cyan
        }
        
        self.reset = '\033[0m'
        
    def set_color(self, color_num):
        """Set the current color theme"""
        if color_num == 99:
            self.current_color = 99  # Rainbow mode
        elif color_num in self.color_map:
            self.current_color = color_num
        else:
            print(f"Color {color_num} not available. Using default.")
            self.current_color = 1
            
    def get_color_code(self):
        """Get current color code"""
        if self.current_color == 99:
            # Rainbow mode - cycle through colors
            color = self.rainbow_colors[self.rainbow_index]
            self.rainbow_index = (self.rainbow_index + 1) % len(self.rainbow_colors)
            return color
        else:
            return self.color_map.get(self.current_color, self.color_map[1])
    
    def colorize(self, text, force_color=None):
        """Apply current color to text"""
        if force_color:
            color_code = self.color_map.get(force_color, self.color_map[1])
        else:
            color_code = self.get_color_code()
        
        return f"{color_code}{text}{self.reset}"
    
    def show_color_menu(self):
        """Display available colors"""
        print(self.colorize("\n🎨 AVAILABLE COLORS:", 4))
        print("=" * 50)
        
        for color_num, color_code in self.color_map.items():
            sample_text = f"Color {color_num:2d} - Sample Text"
            print(f"{color_code}{sample_text}{self.reset}")
        
        print(f"{self.rainbow_colors[0]}Color 99 - Rainbow Mode (cycles through colors){self.reset}")
        print("\n" + self.colorize("Usage: color <number>", 6))
        print(self.colorize("Example: color 2 (for green text)", 6))

class Solara:
    def __init__(self):
        self.name = "Solara Python"
        self.version = "1.1"
        self.colors = ColorManager()
        self.safe_ranges = [
            "127.0.0.1",
            "10.0.0.0/8",
            "172.16.0.0/12", 
            "192.168.0.0/16"
        ]

    def print_banner(self):
        banner_lines = [
            "╔═══════════════════════════════════════╗",
            f"║        {self.name} v{self.version}             ║",
            "║     Educational Nmap Interface        ║",
            "║          🎨 With Color Themes         ║",
            "║                                       ║",
            "║  ⚠️  FOR AUTHORIZED TESTING ONLY ⚠️   ║",
            "╚═══════════════════════════════════════╝"
        ]
        
        for line in banner_lines:
            print(self.colors.colorize(line))
        
        print("\n" + self.colors.colorize("Remember: Only scan networks you own or have explicit permission to test!", 3))
        print(self.colors.colorize("Type 'color' to see available color themes!", 6))
        print()

    def check_nmap_installed(self):
        """Check if nmap is installed on the system"""
        try:
            result = subprocess.run(['nmap', '--version'], 
                                  capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(self.colors.colorize("❌ Error: Nmap is not installed or not in PATH", 3))
            print(self.colors.colorize("Install with: sudo apt install nmap (Debian/Ubuntu)", 4))
            print(self.colors.colorize("             sudo yum install nmap (RHEL/CentOS)", 4))
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
        
        print(self.colors.colorize(f"⚠️  Warning: '{target}' appears to be a public IP/domain", 3))
        response = input(self.colors.colorize("Are you authorized to scan this target? (yes/no): ", 4))
        return response.lower() in ['yes', 'y']

    def basic_scan(self, target):
        """Perform a basic Nmap scan"""
        if not self.validate_target(target):
            print(self.colors.colorize("❌ Scan cancelled for safety reasons", 3))
            return
        
        print(self.colors.colorize(f"🔍 Running basic scan on {target}...", 2))
        cmd = ['nmap', '-sV', target]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            print("\n" + self.colors.colorize("="*60, 4))
            print(self.colors.colorize("BASIC SCAN RESULTS", 2))
            print(self.colors.colorize("="*60, 4))
            
            # Colorize the output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'open' in line.lower():
                    print(self.colors.colorize(line, 2))  # Green for open ports
                elif 'closed' in line.lower() or 'filtered' in line.lower():
                    print(self.colors.colorize(line, 3))  # Red for closed/filtered
                elif 'Nmap scan report' in line:
                    print(self.colors.colorize(line, 4))  # Blue for headers
                else:
                    print(self.colors.colorize(line))     # Current color for rest
                    
            if result.stderr:
                print(self.colors.colorize("Errors:", 3), result.stderr)
        except subprocess.TimeoutExpired:
            print(self.colors.colorize("❌ Scan timed out after 5 minutes", 3))
        except Exception as e:
            print(self.colors.colorize(f"❌ Error running scan: {e}", 3))

    def port_scan(self, target, ports="1-1000"):
        """Scan specific ports"""
        if not self.validate_target(target):
            print(self.colors.colorize("❌ Scan cancelled for safety reasons", 3))
            return
        
        print(self.colors.colorize(f"🔍 Scanning ports {ports} on {target}...", 2))
        cmd = ['nmap', '-p', ports, target]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            print("\n" + self.colors.colorize("="*60, 4))
            print(self.colors.colorize(f"PORT SCAN RESULTS ({ports})", 2))
            print(self.colors.colorize("="*60, 4))
            
            # Colorize port scan output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if '/tcp' in line and 'open' in line:
                    print(self.colors.colorize(line, 2))
                elif '/tcp' in line and ('closed' in line or 'filtered' in line):
                    print(self.colors.colorize(line, 3))
                else:
                    print(self.colors.colorize(line))
                    
        except subprocess.TimeoutExpired:
            print(self.colors.colorize("❌ Scan timed out", 3))
        except Exception as e:
            print(self.colors.colorize(f"❌ Error: {e}", 3))

    def get_local_network(self):
        """Get the local network range"""
        try:
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
            print(self.colors.colorize(f"❌ Could not detect local network: {e}", 3))
            return None, None

    def wifi_scan(self):
        """Discover devices on current WiFi network"""
        print(self.colors.colorize("🔍 Detecting local WiFi network...", 2))
        
        network, local_ip = self.get_local_network()
        if not network:
            print(self.colors.colorize("❌ Could not detect local network. Try manual discovery with: discover 192.168.1.0/24", 3))
            return
        
        print(self.colors.colorize(f"📡 Local IP: {local_ip}", 4))
        print(self.colors.colorize(f"🌐 Network: {network}", 4))
        print(self.colors.colorize(f"🔍 Scanning for devices on your WiFi network...", 2))
        
        # Enhanced discovery with device info
        cmd = ['nmap', '-sn', '--dns-resolution', network]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            print("\n" + self.colors.colorize("="*70, 4))
            print(self.colors.colorize("🏠 WIFI NETWORK DEVICES", 2))
            print(self.colors.colorize("="*70, 4))
            
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
                print(self.colors.colorize(f"Found {len(devices)} devices on the network:\n", 2))
                for i, device in enumerate(devices, 1):
                    print(self.colors.colorize(f"🔹 Device {i}:", 4))
                    print(self.colors.colorize(f"   IP Address: {device.get('ip', 'Unknown')}", 6))
                    print(self.colors.colorize(f"   Hostname:   {device.get('hostname', 'Unknown')}", 6))
                    if 'mac' in device:
                        print(self.colors.colorize(f"   MAC:        {device.get('mac', 'Unknown')}", 6))
                        print(self.colors.colorize(f"   Vendor:     {device.get('vendor', 'Unknown')}", 6))
                    print(self.colors.colorize(f"   Status:     {device.get('status', 'Unknown')}", 2))
                    print()
                
                # Show your device
                print(self.colors.colorize(f"🏠 Your device IP: {local_ip}", 5))
                print(self.colors.colorize(f"📊 Total devices found: {len(devices)}", 2))
            else:
                print(self.colors.colorize("No devices found or unable to parse results", 3))
                
        except subprocess.TimeoutExpired:
            print(self.colors.colorize("❌ WiFi scan timed out after 5 minutes", 3))
        except Exception as e:
            print(self.colors.colorize(f"❌ Error during WiFi scan: {e}", 3))

    def website_scan(self):
        """Interactive website port scanning"""
        print(self.colors.colorize("🌐 Website Port Scanner", 4))
        print(self.colors.colorize("="*50, 4))
        
        # Get website from user
        while True:
            website = input(self.colors.colorize("Enter website/domain to scan: ", 6)).strip()
            if not website:
                print(self.colors.colorize("❌ Please enter a valid website", 3))
                continue
            
            # Remove protocol if present
            website = website.replace('https://', '').replace('http://', '')
            website = website.split('/')[0]  # Remove path if present
            
            # Validate domain format
            if '.' not in website:
                print(self.colors.colorize("❌ Please enter a valid domain (e.g., example.com)", 3))
                continue
            
            break
        
        # Warning for external scanning
        print(self.colors.colorize(f"\n⚠️  You are about to scan: {website}", 3))
        print(self.colors.colorize("⚠️  Make sure you have permission to scan this target!", 3))
        print(self.colors.colorize("⚠️  Unauthorized scanning may violate terms of service or laws.", 3))
        
        confirm = input(self.colors.colorize("\nDo you have permission to scan this website? (yes/no): ", 4)).lower()
        if confirm not in ['yes', 'y']:
            print(self.colors.colorize("❌ Scan cancelled for safety reasons", 3))
            return
        
        # Scan type selection
        print(self.colors.colorize("\n🎯 Select scan type:", 4))
        options = [
            "1. Quick scan (common ports)",
            "2. Web services (80, 443, 8080, 8443)",
            "3. Full scan (1-65535) - WARNING: Very slow!",
            "4. Custom port range",
            "5. Single port"
        ]
        
        for option in options:
            print(self.colors.colorize(option, 6))
        
        choice = input(self.colors.colorize("Choose scan type (1-5): ", 4)).strip()
        
        if choice == '1':
            ports = "1-1000"
            scan_name = "Quick Scan"
        elif choice == '2':
            ports = "80,443,8080,8443,8000,3000,5000,9000"
            scan_name = "Web Services Scan"
        elif choice == '3':
            print(self.colors.colorize("⚠️  Full scan can take 30+ minutes and may trigger security alerts!", 3))
            confirm_full = input(self.colors.colorize("Are you sure? (yes/no): ", 4)).lower()
            if confirm_full not in ['yes', 'y']:
                print(self.colors.colorize("❌ Full scan cancelled", 3))
                return
            ports = "1-65535"
            scan_name = "Full Port Scan"
        elif choice == '4':
            ports = input(self.colors.colorize("Enter port range (e.g., 1-1000, 80,443,8080): ", 6)).strip()
            if not ports:
                print(self.colors.colorize("❌ Invalid port range", 3))
                return
            scan_name = f"Custom Scan ({ports})"
        elif choice == '5':
            port = input(self.colors.colorize("Enter single port to scan: ", 6)).strip()
            if not port.isdigit():
                print(self.colors.colorize("❌ Invalid port number", 3))
                return
            ports = port
            scan_name = f"Single Port Scan ({port})"
        else:
            print(self.colors.colorize("❌ Invalid choice", 3))
            return
        
        print(self.colors.colorize(f"\n🔍 Running {scan_name} on {website}...", 2))
        print(self.colors.colorize(f"📊 Scanning ports: {ports}", 4))
        print(self.colors.colorize("⏳ This may take a while depending on scan type...", 6))
        
        # Build nmap command
        cmd = ['nmap', '-sV', '-sC', '--open', '-p', ports, website]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
            
            print("\n" + self.colors.colorize("="*70, 4))
            print(self.colors.colorize(f"🌐 WEBSITE SCAN RESULTS: {website}", 2))
            print(self.colors.colorize("="*70, 4))
            
            # Parse and display results nicely
            lines = result.stdout.split('\n')
            open_ports = []
            
            for line in lines:
                if '/tcp' in line and 'open' in line:
                    parts = line.split()
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else 'unknown'
                    open_ports.append((port, service, line))
            
            if open_ports:
                print(self.colors.colorize(f"🎯 Found {len(open_ports)} open ports:\n", 2))
                
                for port, service, full_line in open_ports:
                    print(self.colors.colorize(f"🔹 Port {port}:", 4))
                    print(self.colors.colorize(f"   Service: {service}", 6))
                    
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
                        print(self.colors.colorize(f"   Info: {port_descriptions[port]}", 5))
                    print()
            else:
                print(self.colors.colorize("❌ No open ports found in the scanned range", 3))
                    
        except subprocess.TimeoutExpired:
            print(self.colors.colorize("❌ Scan timed out (30 minutes)", 3))
        except Exception as e:
            print(self.colors.colorize(f"❌ Error during website scan: {e}", 3))

    def show_help(self):
        """Display help information"""
        help_sections = [
            ("\n🎯 SOLARA PYTHON COMMANDS:", 4),
            ("", 1),
            ("1. basic <target>           - Basic version detection scan", 6),
            ("2. ports <target> [range]   - Scan specific ports (default: 1-1000)", 6),
            ("3. stealth <target>         - SYN stealth scan with OS detection", 6),
            ("4. vuln <target>            - Vulnerability detection scan", 6),
            ("5. discover <network>       - Host discovery (e.g., 192.168.1.0/24)", 6),
            ("6. wifi                     - Discover devices on current WiFi network", 6),
            ("7. website                  - Interactive website port scanner", 6),
            ("8. color [number]           - Change text color theme", 5),
            ("9. help                     - Show this help", 6),
            ("10. exit                    - Quit Solara", 6),
            ("", 1),
            ("🎨 COLOR COMMANDS:", 4),
            ("", 1),
            ("color          - Show available colors", 6),
            ("color 1        - White text", 1),
            ("color 2        - Green text", 2),
            ("color 3        - Red text", 3),
            ("color 4        - Blue text", 4),
            ("color 5        - Yellow text", 5),
            ("color 99       - Rainbow mode!", 99),
            ("", 1),
            ("📝 EXAMPLES:", 4),
            ("", 1),
            ("basic 127.0.0.1", 6),
            ("ports 192.168.1.1 80,443,8080", 6),
            ("wifi", 6),
            ("website", 6),
            ("color 2", 2),
            ("", 1),
            ("⚠️  ETHICAL GUIDELINES:", 3),
            ("• Only scan systems you own or have explicit permission to test", 6),
            ("• Use responsibly for defense, not offense", 6),
        ]
        
        for text, color in help_sections:
            if color == 99:
                # Special handling for rainbow text
                for char in text:
                    print(self.colors.colorize(char, force_color=None), end='')
                print()
            else:
                print(self.colors.colorize(text, color))

    def interactive_mode(self):
        """Run in interactive mode"""
        self.print_banner()
        
        if not self.check_nmap_installed():
            return
        
        self.show_help()
        
        while True:
            try:
                prompt = self.colors.colorize("🔥 solara> ", force_color=5)
                command = input(f"\n{prompt}").strip().split()
                
                if not command:
                    continue
                
                cmd = command[0].lower()
                
                if cmd == 'exit':
                    print(self.colors.colorize("👋 Thanks for using Solara responsibly!", 2))
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'color':
                    if len(command) > 1:
                        try:
                            color_num = int(command[1])
                            old_color = self.colors.current_color
                            self.colors.set_color(color_num)
                            if color_num == 99:
                                print(self.colors.colorize("🌈 Rainbow mode activated! Colors will cycle!", force_color=None))
                            else:
                                print(self.colors.colorize(f"Color changed from {old_color} to {color_num}"))
                        except ValueError:
                            print(self.colors.colorize("❌ Invalid color number", 3))
                    else:
                        self.colors.show_color_menu()
                elif cmd == 'basic':
                    if len(command) > 1:
                        self.basic_scan(command[1])
                    else:
                        print(self.colors.colorize("❌ Usage: basic <target>", 3))
                elif cmd == 'ports':
                    if len(command) > 1:
                        ports = command[2] if len(command) > 2 else "1-1000"
                        self.port_scan(command[1], ports)
                    else:
                        print(self.colors.colorize("❌ Usage: ports <target> [port_range]", 3))
                elif cmd == 'wifi':
                    self.wifi_scan()
                elif cmd == 'website':
                    self.website_scan()
                else:
                    print(self.colors.colorize(f"❌ Unknown command: {cmd}. Type 'help' for commands.", 3))
                    
            except KeyboardInterrupt:
                print(self.colors.colorize("\n👋 Exiting Solara...", 2))
                break
            except Exception as e:
                print(self.colors.colorize(f"❌ Error: {e}", 3))

def main():
    parser = argparse.ArgumentParser(description='Solara Python - Educational Nmap Interface with Colors')
    parser.add_argument('--target', help='Target to scan')
    parser.add_argument('--scan-type', choices=['basic', 'ports', 'wifi', 'website'],
                       help='Type of scan to perform')
    parser.add_argument('--color', type=int, help='Set color theme (1-20, 99 for rainbow)')
    
    args = parser.parse_args()
    
    solara = Solara()
    
    # Set color if specified
    if args.color:
        solara.colors.set_color(args.color)
    
    if args.target and args.scan_type:
        # Command line mode
        if not solara.check_nmap_installed():
            sys.exit(1)
        
        if args.scan_type == 'basic':
            solara.basic_scan(args.target)
        elif args.scan_type == 'ports':
            solara.port_scan(args.target)
        elif args.scan_type == 'wifi':
            solara.wifi_scan()
        elif args.scan_type == 'website':
            solara.website_scan()
    else:
        # Interactive mode
        solara.interactive_mode()

if __name__ == "__main__":
    main()
