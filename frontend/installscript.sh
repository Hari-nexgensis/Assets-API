#!/bin/bash

# ======================================================
# UI Components Library Installation Script
# Handles authentication, installation, and cleanup
# ======================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Registry and package configuration
REGISTRY_URL="https://nexus.nexgensis.com/repository/frontend/"
USERNAME=""
PASSWORD=""
PACKAGE_NAME="@nexgensis/core"

echo -e "${BLUE}🚀 Starting UI Library Installation${NC}"
echo "=================================================="

# ------------------------------
# Function: Prompt for credentials
# ------------------------------
prompt_credentials() {
    echo -e "${YELLOW}📝 Please enter your Nexus registry credentials${NC}"
    echo ""
    
    # Prompt for username
    read -p "Username: " USERNAME
    
    # Prompt for password (hidden input)
    read -s -p "Password: " PASSWORD
    echo ""
    echo ""
    
    # Validate credentials are not empty
    if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
        echo -e "${RED}❌ Username and password cannot be empty${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Credentials received${NC}"
}

# ------------------------------
# Function: Check npm installation
# ------------------------------
check_npm() {
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm is not installed. Please install Node.js and npm first.${NC}"
        exit 1
    fi
}

# ------------------------------
# Function: Authenticate with Nexus
# ------------------------------
authenticate() {
    echo -e "${YELLOW}🔐 Authenticating with Nexus registry...${NC}"

    npm config set @nexgensis:registry $REGISTRY_URL
    npm config set "//nexus.nexgensis.com/repository/frontend/:username" $USERNAME
    npm config set "//nexus.nexgensis.com/repository/frontend/:_password" $(echo -n $PASSWORD | base64)
    npm config set "//nexus.nexgensis.com/repository/frontend/:_auth" $(echo -n "$USERNAME:$PASSWORD" | base64)

    echo -e "${GREEN}✅ Nexus authentication configured${NC}"
}

# ------------------------------
# Function: Install UI library
# ------------------------------
install_ui_library() {
    echo -e "${YELLOW}📦 Installing ${PACKAGE_NAME} from Nexus...${NC}"
    npm install $PACKAGE_NAME --legacy-peer-deps
    echo -e "${GREEN}✅ ${PACKAGE_NAME} installed successfully${NC}"
}

# ------------------------------
# Function: Cleanup authentication
# ------------------------------
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up authentication info...${NC}"
    npm config delete "//nexus.nexgensis.com/repository/frontend/:_password" 2>/dev/null || true
    npm config delete "//nexus.nexgensis.com/repository/frontend/:_auth" 2>/dev/null || true
    npm config delete "//nexus.nexgensis.com/repository/frontend/:username" 2>/dev/null || true
    echo -e "${GREEN}✅ Cleanup complete${NC}"
}

# ------------------------------
# Main execution
# ------------------------------
main() {
    check_npm
    prompt_credentials
    authenticate
    install_ui_library
    echo -e "\n${BLUE}🎉 Installation Completed!${NC}"
    echo -e "${YELLOW}You can now import and use the UI components:${NC}"
    echo -e "${GREEN}import { Button } from '@nexgensis/core'${NC}"
}

trap cleanup EXIT

main "$@"
