#!/bin/bash

#=============================================================================
# Solara Update Script
# Educational Nmap Interface - Automated Updates
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
GITHUB_REPO="https://github.com/yourusername/solara"
GITHUB_RAW="https://raw.githubusercontent.com/yourusername/solara/main"
BACKUP_DIR="$SOLARA_DIR/backups"
UPDATE_LOG="$SOLARA_DIR/update.log"

print_banner() {
    echo -e "${PURPLE}"
    echo "╔═════════════════════════════════════════════════════════════╗"
    echo "║                    SOLARA UPDATER v${SCRIPT_VERSION}                  ║"
    echo "║            Keep Your Tools Sharp & Current                  ║"
    echo "║                                                             ║"
    echo "║  🔄 Automated updates from GitHub repository                ║"
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

log_action() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$UPDATE_LOG"
}

check_solara_installed() {
    print_step "Checking if Solara is installed..."
    
    if [ ! -d "$SOLARA_DIR" ]; then
        print_error "Solara not found in $SOLARA_DIR"
        print_error "Please run the installer first: ./install.sh"
        exit 1
    fi
    
    if [ ! -f "$SOLARA_DIR/solara.py" ]; then
        print_error "Solara script not found in $SOLARA_DIR"
        print_error "Installation may be corrupted. Please reinstall."
        exit 1
    fi
    
    print_success "Solara installation found"
}

get_current_version() {
    print_step "Checking current version..."
    
    if [ -f "$SOLARA_DIR/solara.py" ]; then
        # Extract version from script
        CURRENT_VERSION=$(grep -o 'self.version = "[^"]*"' "$SOLARA_DIR/solara.py" 2>/dev/null | cut -d'"' -f2)
        
        if [ -z "$CURRENT_VERSION" ]; then
            CURRENT_VERSION="unknown"
        fi
        
        print_success "Current version: $CURRENT_VERSION"
    else
        CURRENT_VERSION="not found"
        print_warning "Cannot determine current version"
    fi
}

check_internet_connection() {
    print_step "Checking internet connection..."
    
    if command -v ping &> /dev/null; then
        if ping -c 1 github.com &> /dev/null; then
            print_success "Internet connection verified"
            return 0
        fi
    elif command -v curl &> /dev/null; then
        if curl -s --head https://github.com &> /dev/null; then
            print_success "Internet connection verified"
            return 0
        fi
    elif command -v wget &> /dev/null; then
        if wget --spider -q https://github.com; then
            print_success "Internet connection verified"
            return 0
        fi
    fi
    
    print_error "No internet connection or GitHub is unreachable"
    print_error "Please check your connection and try again"
    exit 1
}

get_latest_version() {
    print_step "Checking for updates on GitHub..."
    
    # Try to get latest version from GitHub API
    if command -v curl &> /dev/null; then
        LATEST_INFO=$(curl -s "https://api.github.com/repos/yourusername/solara/releases/latest" 2>/dev/null)
        if [ $? -eq 0 ] && echo "$LATEST_INFO" | grep -q "tag_name"; then
            LATEST_VERSION=$(echo "$LATEST_INFO" | grep '"tag_name"' | cut -d'"' -f4 | sed 's/^v//')
            RELEASE_NOTES=$(echo "$LATEST_INFO" | grep '"body"' | cut -d'"' -f4)
        fi
    fi
    
    # Fallback: try to get version from raw file
    if [ -z "$LATEST_VERSION" ]; then
        print_step "Trying alternative version check..."
        
        if command -v curl &> /dev/null; then
            TEMP_FILE=$(mktemp)
            if curl -s "$GITHUB_RAW/solara.py" -o "$TEMP_FILE"; then
                LATEST_VERSION=$(grep -o 'self.version = "[^"]*"' "$TEMP_FILE" 2>/dev/null | cut -d'"' -f2)
                rm -f "$TEMP_FILE"
            fi
        elif command -v wget &> /dev/null; then
            TEMP_FILE=$(mktemp)
            if wget -q "$GITHUB_RAW/solara.py" -O "$TEMP_FILE"; then
                LATEST_VERSION=$(grep -o 'self.version = "[^"]*"' "$TEMP_FILE" 2>/dev/null | cut -d'"' -f2)
                rm -f "$TEMP_FILE"
            fi
        fi
    fi
    
    if [ -z "$LATEST_VERSION" ]; then
        LATEST_VERSION="unknown"
        print_warning "Could not determine latest version"
    else
        print_success "Latest version available: $LATEST_VERSION"
    fi
}

compare_versions() {
    if [ "$CURRENT_VERSION" = "unknown" ] || [ "$LATEST_VERSION" = "unknown" ]; then
        print_warning "Cannot compare versions - updating anyway"
        return 0
    fi
    
    if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
        print_success "You already have the latest version ($CURRENT_VERSION)"
        
        echo
        read -p "Force update anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Update cancelled."
            exit 0
        fi
        return 0
    fi
    
    print_step "Update available: $CURRENT_VERSION → $LATEST_VERSION"
    return 0
}

create_backup() {
    print_step "Creating backup of current installation..."
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR"
    
    # Create timestamped backup
    BACKUP_NAME="solara_backup_$(date +%Y%m%d_%H%M%S)"
    BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
    
    if cp "$SOLARA_DIR/solara.py" "$BACKUP_PATH.py" 2>/dev/null; then
        print_success "Backup created: $BACKUP_PATH.py"
        log_action "Backup created: $BACKUP_PATH.py (version: $CURRENT_VERSION)"
        
        # Keep only last 5 backups
        cd "$BACKUP_DIR"
        ls -t solara_backup_*.py 2>/dev/null | tail -n +6 | xargs rm -f
        
        return 0
    else
        print_error "Failed to create backup"
        return 1
    fi
}

download_update() {
    print_step "Downloading latest version..."
    
    TEMP_FILE=$(mktemp)
    
    # Try curl first, then wget
    if command -v curl &> /dev/null; then
        if curl -s "$GITHUB_RAW/solara.py" -o "$TEMP_FILE"; then
            DOWNLOAD_SUCCESS=true
        fi
    elif command -v wget &> /dev/null; then
        if wget -q "$GITHUB_RAW/solara.py" -O "$TEMP_FILE"; then
            DOWNLOAD_SUCCESS=true
        fi
    fi
    
    if [ "$DOWNLOAD_SUCCESS" = true ] && [ -s "$TEMP_FILE" ]; then
        # Verify it's a valid Python script
        if head -1 "$TEMP_FILE" | grep -q "#!/usr/bin/env python3"; then
            print_success "Download successful"
            echo "$TEMP_FILE"
            return 0
        else
            print_error "Downloaded file doesn't appear to be valid"
            rm -f "$TEMP_FILE"
            return 1
        fi
    else
        print_error "Failed to download update"
        rm -f "$TEMP_FILE"
        return 1
    fi
}

install_update() {
    local temp_file="$1"
    
    print_step "Installing update..."
    
    # Copy new version
    if cp "$temp_file" "$SOLARA_DIR/solara.py"; then
        chmod +x "$SOLARA_DIR/solara.py"
        print_success "Update installed successfully"
        
        # Update system symlink if it exists
        if [ -L "$SOLARA_BIN" ] && [ -e "$SOLARA_BIN" ]; then
            print_step "Updating system command..."
            sudo ln -sf "$SOLARA_DIR/solara.py" "$SOLARA_BIN" 2>/dev/null && \
                print_success "System command updated" || \
                print_warning "Could not update system command"
        fi
        
        log_action "Update installed: $CURRENT_VERSION → $LATEST_VERSION"
        return 0
    else
        print_error "Failed to install update"
        return 1
    fi
}

verify_update() {
    print_step "Verifying update..."
    
    # Check if script runs
    if "$SOLARA_DIR/solara.py" --help &>/dev/null; then
        print_error "Updated script has issues"
        return 1
    fi
    
    # Get new version
    NEW_VERSION=$(grep -o 'self.version = "[^"]*"' "$SOLARA_DIR/solara.py" 2>/dev/null | cut -d'"' -f2)
    
    if [ -n "$NEW_VERSION" ]; then
        print_success "Update verified - now running version: $NEW_VERSION"
        log_action "Update verified: version $NEW_VERSION"
        return 0
    else
        print_warning "Could not verify new version, but update appears successful"
        return 0
    fi
}

rollback_update() {
    print_error "Update failed. Attempting rollback..."
    
    # Find most recent backup
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/solara_backup_*.py 2>/dev/null | head -1)
    
    if [ -n "$LATEST_BACKUP" ] && [ -f "$LATEST_BACKUP" ]; then
        if cp "$LATEST_BACKUP" "$SOLARA_DIR/solara.py"; then
            chmod +x "$SOLARA_DIR/solara.py"
            print_success "Rollback successful"
            log_action "Rollback completed to: $LATEST_BACKUP"
        else
            print_error "Rollback failed - manual intervention required"
            log_action "Rollback failed"
        fi
    else
        print_error "No backup found for rollback"
        log_action "Rollback failed - no backup available"
    fi
}

show_changelog() {
    if [ -n "$RELEASE_NOTES" ] && [ "$RELEASE_NOTES" != "null" ]; then
        echo
        echo -e "${CYAN}📝 CHANGELOG:${NC}"
        echo -e "${YELLOW}$RELEASE_NOTES${NC}"
        echo
    fi
}

show_completion_message() {
    echo
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗"
    echo -e "║                   🎉 UPDATE COMPLETE! 🎉                      ║"
    echo -e "╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo
    
    if [ -n "$NEW_VERSION" ]; then
        echo -e "${CYAN}✨ Updated to version: ${YELLOW}$NEW_VERSION${NC}"
    fi
    
    echo -e "${CYAN}🚀 Ready to use:${NC}"
    if command -v solara &> /dev/null; then
        echo -e "   ${YELLOW}solara${NC}                    # Launch interactive mode"
    else
        echo -e "   ${YELLOW}$SOLARA_DIR/solara.py${NC}    # Launch interactive mode"
    fi
    
    echo
    echo -e "${PURPLE}📁 Installation: ${SOLARA_DIR}${NC}"
    echo -e "${PURPLE}📋 Update log: ${UPDATE_LOG}${NC}"
    echo -e "${PURPLE}💾 Backups: ${BACKUP_DIR}${NC}"
    
    show_changelog
    
    echo -e "${CYAN}🔗 Stay updated: ${BLUE}${GITHUB_REPO}${NC}"
    echo
}

show_update_options() {
    echo -e "${CYAN}🔄 UPDATE OPTIONS:${NC}"
    echo "1. Update now (recommended)"
    echo "2. View changelog first"
    echo "3. Cancel update"
    echo
    read -p "Choose option (1-3): " -n 1 -r
    echo
    
    case $REPLY in
        1)
            return 0
            ;;
        2)
            show_changelog
            read -p "Proceed with update? (Y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Nn]$ ]]; then
                echo "Update cancelled."
                exit 0
            fi
            return 0
            ;;
        3)
            echo "Update cancelled."
            exit 0
            ;;
        *)
            echo "Invalid option. Update cancelled."
            exit 1
            ;;
    esac
}

cleanup() {
    # Clean up temporary files
    if [ -n "$TEMP_FILE" ] && [ -f "$TEMP_FILE" ]; then
        rm -f "$TEMP_FILE"
    fi
}

# Main update flow
main() {
    # Set up error handling
    trap cleanup EXIT
    
    print_banner
    
    echo -e "${YELLOW}🔄 This will update Solara to the latest version from GitHub.${NC}"
    echo -e "${YELLOW}📦 A backup of your current installation will be created.${NC}"
    echo
    
    # Create log directory
    mkdir -p "$(dirname "$UPDATE_LOG")"
    log_action "Update process started"
    
    # Run update steps
    check_solara_installed
    get_current_version
    check_internet_connection
    get_latest_version
    compare_versions
    
    # Show update options if changelog available
    if [ -n "$RELEASE_NOTES" ] && [ "$RELEASE_NOTES" != "null" ]; then
        show_update_options
    else
        read -p "Continue with update? (Y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            echo "Update cancelled."
            exit 0
        fi
    fi
    
    # Perform update
    if create_backup; then
        TEMP_FILE=$(download_update)
        if [ $? -eq 0 ] && [ -n "$TEMP_FILE" ]; then
            if install_update "$TEMP_FILE"; then
                if verify_update; then
                    show_completion_message
                    log_action "Update completed successfully"
                else
                    print_warning "Update completed but verification failed"
                fi
            else
                rollback_update
                exit 1
            fi
        else
            print_error "Failed to download update"
            exit 1
        fi
    else
        print_error "Cannot proceed without backup"
        exit 1
    fi
}

# Check for command line arguments
case "${1:-}" in
    --check|-c)
        print_banner
        check_solara_installed
        get_current_version
        check_internet_connection
        get_latest_version
        compare_versions
        echo
        echo -e "${CYAN}💡 Run './update.sh' to update${NC}"
        exit 0
        ;;
    --help|-h)
        print_banner
        echo -e "${CYAN}USAGE:${NC}"
        echo "  ./update.sh           # Interactive update"
        echo "  ./update.sh --check   # Check for updates only"
        echo "  ./update.sh --help    # Show this help"
        echo
        exit 0
        ;;
    *)
        # Run main update flow
        main "$@"
        ;;
esac
