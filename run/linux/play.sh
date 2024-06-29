#!/bin/bash

# Get the current directory
CURRENT_DIR=$(pwd)

# Check if Python is installed
if command -v python3 &>/dev/null; then
    # Python is installed
    pyversion=$(python3 --version 2>&1 | awk '{print $2}')
    
    # Check Python version
    if [ "$(printf '%s\n' "3.12.4" "$pyversion" | sort -V | head -n1)" = "3.12.4" ]; then
        echo "=> Python $pyversion is already installed."
    else
        echo "=> Updating Python to version 3.12.4... This can take a little time!"
        
        # Update package lists
        sudo apt update
        
        # Install prerequisites
        sudo apt install -y software-properties-common
        
        # Add deadsnakes PPA for newer Python versions
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        
        # Update package lists again
        sudo apt update
        
        # Install Python 3.12.4
        sudo apt install -y python3.12
        
        # Install pip for Python 3.12
        sudo apt install -y python3.12-distutils
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3.12 get-pip.py
        rm get-pip.py
        
        # Set Python 3.12 as the default python3
        sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
        sudo update-alternatives --set python3 /usr/bin/python3.12
        
        echo "Python 3.12.4 has been installed and set as the default python3."
    fi
else
    # Python is not installed
    echo "=> Installing Python 3.12.4... This can take a little time!"
    
    # Update package lists
    sudo apt update
    
    # Install prerequisites
    sudo apt install -y software-properties-common
    
    # Add deadsnakes PPA for newer Python versions
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    
    # Update package lists again
    sudo apt update
    
    # Install Python 3.12.4
    sudo apt install -y python3.12
    
    # Install pip for Python 3.12
    sudo apt install -y python3.12-distutils
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3.12 get-pip.py
    rm get-pip.py
    
    # Set Python 3.12 as the default python3
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
    sudo update-alternatives --set python3 /usr/bin/python3.12
    
    echo "Python 3.12.4 has been installed and set as the default python3."
fi

python3 -m pip install --upgrade setuptools

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    # Install dependencies from requirements.txt
    echo "=> Installing dependencies from requirements.txt..."
    python3 -m pip install -r requirements.txt
else
    echo "=> requirements.txt not found. Skipping dependency installation."
fi

# Check pip version
pipversion=$(python3 -m pip --version | awk '{print $2}')

# Update pip if necessary
python3 -m pip install --upgrade pip

# Install pygame if not already installed
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "=> Installing pygame..."
    python3 -m pip install pygame
fi

# Run the Python file
echo "=> Launching Python file..."
python3 main.py

# Keep the terminal open
exec $SHELL
