#!/bin/bash

#=============================================================================
# Solara Installation Script
# Educational Nmap Interface - Automated Setup
#=============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script info
SCRIPT_VERSION="1.0"
SOLARA_DIR="$HOME/.solara"
SOLARA_BIN="/usr/local/bin/solara"

print_banner() {
    echo -e "${PURPLE}"
    echo "╔═════════════════════════════════════════════════════════════╗"
    echo "║                    SOLARA INSTALLER v${SCRIPT_VERSION}                 ║"
    echo "║            Educational Nmap Interface Setup                 ║"
    echo "║                                                             ║"
    echo "║  🔥 Automated installation for Kali/Debian/Ubuntu/RHEL     ║"
    echo "╚═════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
}

print_step() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "This script should not be run as root for security reasons."
        print_warning "Some operations will use sudo when needed."
        echo
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

detect_os() {
    print_step "Detecting operating system..."
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VERSION=$VERSION_ID
        
        case $ID in
            "kali"|"debian"|"ubuntu")
                PKG_MANAGER="apt"
                INSTALL_CMD="apt install -y"
                UPDATE_CMD="apt update"
                ;;
            "rhel"|"centos"|"fedora")
                PKG_MANAGER="yum"
                INSTALL_CMD="yum install -y"
                UPDATE_CMD="yum update -y"
                
                # Check for dnf on newer systems
                if command -v dnf &> /dev/null; then
                    PKG_MANAGER="dnf"
                    INSTALL_CMD="dnf install -y"
                    UPDATE_CMD="dnf update -y"
                fi
                ;;
            "arch"|"manjaro")
                PKG_MANAGER="pacman"
                INSTALL_CMD="pacman -S --noconfirm"
                UPDATE_CMD="pacman -Sy"
                ;;
            *)
                print_error "Unsupported OS: $ID"
                print_error "Supported: Kali, Debian, Ubuntu, RHEL, CentOS, Fedora, Arch"
                exit 1
                ;;
        esac
        
        print_success "Detected: $OS ($ID)"
        print_success "Package manager: $PKG_MANAGER"
    else
        print_error "Cannot detect OS. /etc/os-release not found."
        exit 1
    fi
}

check_dependencies() {
    print_step "Checking dependencies..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python 3 found: $PYTHON_VERSION"
    else
        print_error "Python 3 not found"
        MISSING_DEPS+=("python3")
    fi
    
    # Check Git
    if command -v git &> /dev/null; then
        print_success "Git found"
    else
        print_warning "Git not found - needed for installation"
        MISSING_DEPS+=("git")
    fi
    
    # Check if we're installing from git or have local files
    if [ ! -f "solara.py" ]; then
        NEED_GIT=true
    fi
}

install_system_deps() {
    if [ ${#MISSING_DEPS[@]} -eq 0 ] && command -v nmap &> /dev/null; then
        print_success "All system dependencies satisfied"
        return 0
    fi
    
    print_step "Installing system dependencies..."
    
    # Update package manager
    print_step "Updating package manager..."
    case $PKG_MANAGER in
        "apt")
            sudo $UPDATE_CMD
            if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
                sudo $INSTALL_CMD "${MISSING_DEPS[@]}"
            fi
            
            # Install nmap if not present
            if ! command -v nmap &> /dev/null; then
                print_step "Installing Nmap..."
                sudo $INSTALL_CMD nmap
            fi
            ;;
            
        "yum"|"dnf")
            sudo $UPDATE_CMD
            if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
                sudo $INSTALL_CMD "${MISSING_DEPS[@]}"
            fi
            
            if ! command -v nmap &> /dev/null; then
                print_step "Installing Nmap..."
                sudo $INSTALL_CMD nmap
            fi
            ;;
            
        "pacman")
            sudo $UPDATE_CMD
            if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
                sudo $INSTALL_CMD "${MISSING_DEPS[@]}"
            fi
            
            if ! command -v nmap &> /dev/null; then
                print_step "Installing Nmap..."
                sudo $INSTALL_CMD nmap
            fi
            ;;
    esac
    
    # Verify nmap installation
    if command -v nmap &> /dev/null; then
        NMAP_VERSION=$(nmap --version | head -1)
        print_success "Nmap installed: $NMAP_VERSION"
    else
        print_error "Failed to install Nmap"
        exit 1
    fi
}

download_solara() {
    if [ -f "solara.py" ]; then
        print_success "Solara script found locally"
        return 0
    fi
    
    print_step "Downloading Solara from GitHub..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # Clone or download
    if git clone https://github.com/yourusername/solara.git . 2>/dev/null; then
        print_success "Downloaded via git clone"
    else
        print_step "Git clone failed, trying wget..."
        if command -v wget &> /dev/null; then
            wget -O solara.py https://raw.githubusercontent.com/yourusername/solara/main/solara.py
        elif command -v curl &> /dev/null; then
            curl -o solara.py https://raw.githubusercontent.com/yourusername/solara/main/solara.py
        else
            print_error "Cannot download Solara. Please install git, wget, or curl"
            exit 1
        fi
    fi
    
    if [ ! -f "solara.py" ]; then
        print_error "Failed to download solara.py"
        exit 1
    fi
    
    # Move to original directory
    cp solara.py "$OLDPWD/"
    cd "$OLDPWD"
    rm -rf "$TEMP_DIR"
}

install_solara() {
    print_step "Installing Solara..."
    
    # Create Solara directory
    mkdir -p "$SOLARA_DIR"
    
    # Copy script
    cp solara.py "$SOLARA_DIR/"
    chmod +x "$SOLARA_DIR/solara.py"
    
    # Create system-wide symlink
    print_step "Creating system-wide command..."
    if sudo ln -sf "$SOLARA_DIR/solara.py" "$SOLARA_BIN" 2>/dev/null; then
        print_success "Solara installed to $SOLARA_BIN"
    else
        print_warning "Could not create system-wide command. Creating user alias..."
        
        # Add to user's bashrc/zshrc
        SHELL_RC=""
        if [ "$SHELL" = "/bin/zsh" ] || [ "$SHELL" = "/usr/bin/zsh" ]; then
            SHELL_RC="$HOME/.zshrc"
        else
            SHELL_RC="$HOME/.bashrc"
        fi
        
        if [ -f "$SHELL_RC" ]; then
            echo "" >> "$SHELL_RC"
            echo "# Solara alias" >> "$SHELL_RC"
            echo "alias solara='$SOLARA_DIR/solara.py'" >> "$SHELL_RC"
            print_success "Added alias to $SHELL_RC"
            print_warning "Run 'source $SHELL_RC' or restart your terminal"
        fi
    fi
}

verify_installation() {
    print_step "Verifying installation..."
    
    # Test if Solara runs
    if "$SOLARA_DIR/solara.py" --help &>/dev/null; then
        print_error "Solara script has issues. Testing basic execution..."
    fi
    
    # Check if nmap is accessible
    if command -v nmap &> /dev/null; then
        print_success "Nmap is accessible"
    else
        print_error "Nmap is not in PATH"
    fi
    
    # Check permissions
    if [ -x "$SOLARA_DIR/solara.py" ]; then
        print_success "Solara script is executable"
    else
        print_error "Solara script is not executable"
        chmod +x "$SOLARA_DIR/solara.py"
    fi
}

show_completion_message() {
    echo
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗"
    echo -e "║                   🎉 INSTALLATION COMPLETE! 🎉                ║"
    echo -e "╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${CYAN}🚀 Quick Start:${NC}"
    
    if command -v solara &> /dev/null; then
        echo -e "   ${YELLOW}solara${NC}                    # Launch interactive mode"
        echo -e "   ${YELLOW}solara --scan-type wifi${NC}  # Scan WiFi network"
    else
        echo -e "   ${YELLOW}$SOLARA_DIR/solara.py${NC}              # Launch interactive mode"
        echo -e "   ${YELLOW}source ~/.bashrc${NC}                   # Load alias (if created)"
    fi
    
    echo
    echo -e "${CYAN}📚 Learning Resources:${NC}"
    echo -e "   • TryHackMe: ${BLUE}https://tryhackme.com${NC}"
    echo -e "   • HackTheBox: ${BLUE}https://hackthebox.eu${NC}"
    echo -e "   • Nmap Guide: ${BLUE}https://nmap.org/book/${NC}"
    
    echo
    echo -e "${RED}⚠️  IMPORTANT REMINDERS:${NC}"
    echo -e "   • Only scan networks you own or have permission to test"
    echo -e "   • Start with localhost (127.0.0.1) for safe learning"
    echo -e "   • Use responsibly for educational purposes only"
    
    echo
    echo -e "${PURPLE}📁 Installed to: ${SOLARA_DIR}${NC}"
    echo -e "${PURPLE}🔗 System command: ${SOLARA_BIN} (if available)${NC}"
    echo
}

cleanup_on_error() {
    print_error "Installation failed. Cleaning up..."
    rm -rf "$SOLARA_DIR" 2>/dev/null
    sudo rm -f "$SOLARA_BIN" 2>/dev/null
    exit 1
}

# Main installation flow
main() {
    # Initialize variables
    MISSING_DEPS=()
    NEED_GIT=false
    
    # Set up error handling
    trap cleanup_on_error ERR
    
    # Run installation steps
    print_banner
    
    echo -e "${YELLOW}🔒 This installer will set up Solara for educational network security learning.${NC}"
    echo -e "${YELLOW}📖 Please ensure you use this tool responsibly and ethically.${NC}"
    echo
    
    read -p "Continue with installation? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    
    check_root
    detect_os
    check_dependencies
    install_system_deps
    download_solara
    install_solara
    verify_installation
    show_completion_message
    
    print_success "Solara installation completed successfully!"
}

# Run main function
main "$@"
