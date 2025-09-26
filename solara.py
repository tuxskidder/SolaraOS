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
║           {self.name} v{self.version} ║
║     Educational Nmap Interface        ║
║                                       ║
║  ⚠️  FOR AUTHORIZED TESTING ONLY ⚠️  ║
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
6. help                     - Show this help
7. exit                     - Quit Solara

📝 EXAMPLES:
   basic 127.0.0.1
   ports 192.168.1.1 80,443,8080
   stealth localhost
   vuln 10.0.0.1
   discover 192.168.1.0/24

⚠️  ETHICAL GUIDELINES:
• Only scan systems you own or have written permission to test
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
    parser.add_argument('--scan-type', choices=['basic', 'ports', 'stealth', 'vuln', 'discover'],
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
    else:
        # Interactive mode
        solara.interactive_mode()

if __name__ == "__main__":
    main()
