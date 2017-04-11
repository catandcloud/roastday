#!/bin/bash

# Install Xcode and Homebrew
/usr/bin/xcode-select --install
/usr/local/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Install python using brew
/usr/local/bin/brew install python

# Install pip
/usr/local/bin/python get-pip.py

# Install virtualenvwrapper
/usr/local/bin/pip install virtualenv

# Make virtualenv for app
/usr/local/bin/virtualenv $HOME/.virtualenvs/roastday
source $HOME/.virtualenvs/roastday/bin/activate

# Pip install requirements for app
$HOME/.virtualenvs/roastday/bin/pip install -r requirements.txt
