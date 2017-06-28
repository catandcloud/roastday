#!/bin/bash

# Install Xcode and Homebrew
command -v /usr/bin/xcode-select >/dev/null 2>&1 || { echo >&2 "I require Xcode but it's not installed – Consult Alex.  Aborting."; exit 1; }
/usr/bin/xcode-select --install

command -v /usr/bin/ruby >/dev/null 2>&1 || { echo >&2 "I require Ruby but it's not installed – Consult Alex.  Aborting."; exit 1; }
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Install python using brew
command -v /usr/local/bin/brew >/dev/null 2>&1 || { echo >&2 "I require Homebrew but it's not installed – Consult Alex.  Aborting."; exit 1; }
/usr/local/bin/brew install python

# Install pip
command -v /usr/local/bin/python >/dev/null 2>&1 || { echo >&2 "I require Python but it's not installed – Consult Alex.  Aborting."; exit 1; }
/usr/local/bin/python get-pip.py

# Install virtualenvwrapper
command -v /usr/local/bin/pip >/dev/null 2>&1 || { echo >&2 "I require Pip but it's not installed – Consult Alex.  Aborting."; exit 1; }
/usr/local/bin/pip install virtualenv

# Make virtualenv for app
command -v /usr/local/bin/virtualenv >/dev/null 2>&1 || { echo >&2 "I require Virtualenv but it's not installed – Consult Alex.  Aborting."; exit 1; }
/usr/local/bin/virtualenv $HOME/.virtualenvs/roastday
source $HOME/.virtualenvs/roastday/bin/activate

# Pip install requirements for app
command -v $HOME/.virtualenvs/roastday/bin/pip >/dev/null 2>&1 || { echo >&2 "Virtualenv not installed correctly – Consult Alex. Aborting."; exit 1; }
$HOME/.virtualenvs/roastday/bin/pip install -r "$HOME/Dropbox/Cat & Cloud Admin/Roastery Folders/Roasting/roastdayapp/requirements.txt"
