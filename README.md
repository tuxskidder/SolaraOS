# 🔥 Solara - Educational Nmap Interface

<div align="center">

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Security](https://img.shields.io/badge/use-authorized_only-red.svg)

**A powerful, user-friendly Python wrapper for Nmap with enhanced features for network security education and authorized penetration testing.**

</div>

## ⚡ Features

### 🎯 Core Scanning Capabilities
- **Basic Scanning** - Version detection and service enumeration
- **Port Scanning** - Custom port ranges and targeted scanning  
- **Stealth Scanning** - SYN stealth scans with OS detection
- **Vulnerability Detection** - Built-in vulnerability scanning scripts
- **Network Discovery** - Host discovery on network ranges

### 🏠 Local Network Tools
- **WiFi Network Scanner** - Auto-discover devices on your current WiFi network
- **Device Information** - Shows IP addresses, hostnames, MAC addresses, and vendors
- **Network Mapping** - Visualize your local network topology

### 🌐 Website Analysis
- **Interactive Website Scanner** - User-friendly website port scanning
- **Multiple Scan Types** - Quick, web services, full, custom, and single port scans
- **Service Detection** - Identify running services and versions
- **Security Recommendations** - Built-in security analysis and suggestions

### 🛡️ Safety & Ethics First
- **Permission Validation** - Multiple confirmation prompts for external scanning
- **Private Network Detection** - Automatic detection of safe scanning targets
- **Educational Focus** - Learning resources and ethical guidelines included
- **Rate Limiting** - Respectful scanning practices built-in

## 🚀 Quick Start

### Prerequisites
```bash
# Install Nmap (required dependency)
sudo apt install nmap              # Debian/Ubuntu
sudo yum install nmap              # RHEL/CentOS  
sudo pacman -S nmap                # Arch Linux
brew install nmap                  # macOS
```

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/solara.git
cd solara

# Make executable
chmod +x solara.py

# Run interactive mode
./solara.py
```

## 💻 Usage

### Interactive Mode (Recommended)
```bash
./solara.py
```

### Command Line Mode
```bash
# Basic scan
./solara.py --target 127.0.0.1 --scan-type basic

# Port scan
./solara.py --target 192.168.1.1 --scan-type ports

# WiFi network discovery
./solara.py --scan-type wifi

# Website scanning
./solara.py --scan-type website
```

## 🎮 Commands Reference

### Core Commands
| Command | Description | Example |
|---------|-------------|---------|
| `basic <target>` | Version detection scan | `basic 127.0.0.1` |
| `ports <target> [range]` | Port scanning | `ports 192.168.1.1 80,443,8080` |
| `stealth <target>` | SYN stealth + OS detection | `stealth localhost` |
| `vuln <target>` | Vulnerability detection | `vuln 10.0.0.1` |
| `discover <network>` | Network host discovery | `discover 192.168.1.0/24` |
| `wifi` | WiFi network device scan | `wifi` |
| `website` | Interactive website scanner | `website` |
| `help` | Show help information | `help` |
| `exit` | Quit Solara | `exit` |

### WiFi Scanner Output Example
```
🏠 WIFI NETWORK DEVICES
======================================================================
Found 5 devices on the network:

🔹 Device 1:
   IP Address: 192.168.1.1
   Hostname:   router.home
   MAC:        aa:bb:cc:dd:ee:ff
   Vendor:     Netgear
   Status:     UP

🔹 Device 2:
   IP Address: 192.168.1.10
   Hostname:   Johns-iPhone
   MAC:        11:22:33:44:55:66
   Vendor:     Apple
   Status:     UP
```

### Website Scanner Features
- **Quick Scan**: Common ports (1-1000)
- **Web Services**: HTTP/HTTPS focused (80, 443, 8080, etc.)
- **Full Scan**: All ports (1-65535) with warnings
- **Custom Range**: User-defined port ranges
- **Single Port**: Target specific services

## 🔒 Security & Ethics

### ⚠️ IMPORTANT WARNINGS
- **ONLY scan networks and systems you own or have explicit written permission to test**
- **Unauthorized scanning may violate laws, terms of service, or organizational policies**
- **This tool is for EDUCATIONAL and AUTHORIZED TESTING purposes only**

### Built-in Safety Features
- Multiple permission confirmation prompts
- Automatic detection of private vs public IP ranges
- Educational warnings and ethical guidelines
- Respectful scanning practices and rate limiting

### Recommended Use Cases
✅ **AUTHORIZED:**
- Your own home/office network
- Lab environments and virtual machines  
- Systems with explicit written permission
- Educational environments with proper authorization
- Authorized penetration testing engagements

❌ **UNAUTHORIZED:**
- Public websites without permission
- Corporate networks you don't own
- Third-party systems without consent
- Scanning to find vulnerabilities for malicious purposes

## 🎓 Educational Resources

### Learning Path
1. **Start with local scanning** - Practice on `127.0.0.1` and your WiFi network
2. **Set up a lab environment** - Use VirtualBox/VMware with vulnerable VMs
3. **Study the results** - Understand what services and ports mean
4. **Learn from the community** - Join ethical hacking communities

### Recommended Platforms
- [TryHackMe](https://tryhackme.com) - Beginner-friendly cybersecurity challenges
- [HackTheBox](https://hackthebox.eu) - Advanced penetration testing practice
- [VulnHub](https://vulnhub.com) - Vulnerable VMs for practice
- [OverTheWire](https://overthewire.org) - War games and challenges

### Further Reading
- [Nmap Official Documentation](https://nmap.org/book/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Penetration Testing Execution Standard](http://www.pentest-standard.org/)

## 🛠️ Technical Details

### System Requirements
- **OS**: Linux (tested on Kali, Ubuntu, CentOS)
- **Python**: 3.6 or higher
- **Dependencies**: Nmap, standard Python libraries
- **Privileges**: Some scans require root/sudo

### Architecture
```
solara.py
├── Core Scanning Engine
├── Safety Validation Layer  
├── Interactive CLI Interface
├── Network Discovery Module
├── WiFi Analysis Tools
└── Website Scanner Interface
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Guidelines
- Maintain the educational focus
- Preserve security warnings and ethical guidelines
- Include documentation for new features
- Test thoroughly before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Disclaimer

**IMPORTANT**: This tool is provided for educational and authorized testing purposes only. Users are solely responsible for complying with all applicable laws, regulations, and organizational policies. The authors and contributors assume no responsibility for misuse of this tool.

- Only use on systems you own or have explicit permission to test
- Unauthorized network scanning may be illegal in your jurisdiction
- Always respect rate limits and avoid overwhelming target systems
- Use this knowledge responsibly for defensive purposes

## 🙏 Acknowledgments

- **Nmap Project** - For the incredible network scanning capabilities
- **Kali Linux Team** - For providing the platform that inspired this tool
- **Security Community** - For promoting ethical hacking and responsible disclosure
- **Educational Platforms** - TryHackMe, HackTheBox, and others for fostering learning

## 📞 Support

- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/yourusername/solara/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/yourusername/solara/discussions)
- **Security**: Report security issues privately via email

---

<div align="center">

**Made with ❤️ for the hacking teams*

⭐ **Star this repo if you find it helpful!** ⭐

</div>
