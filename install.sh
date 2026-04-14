#!/usr/bin/env bash

loading() {
    local message="$1"
    local duration="${2:-3}"
    local dots=""

    for n in $(seq 1 $duration); do
            dots+="."
            echo -ne "\r$message $dots"
            sleep 0.3
    done
    echo ""
}

succes() {
    printf "\033[32m%s\033[0m\n" "$1"
}

info() {
    printf "\033[34m%s\033[0m\n" "$1"
}

error() {
    printf "\033[31m%s\033[0m\n" "$1"
}

loading "Checking venv directory"
if [ ! -e ".venv" ]; then
    info "Venv not found"
    loading "Creating environment"
    python -m venv .venv
    succes "Environment created"

    loading "Upgrading pip"
    pip install --upgrade pip
    succes "Pip upgraded"
else
    info "Venv found"
fi

loading "Activating environment"
if [ -d ".venv" ]; then
    source .venv/bin/activate
    succes "Environment activated"
else
    error "Could not find venv"
fi

loading "Installing dependencies"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo ""
    succes "All dependencies installed"
else
    error "No requirements.txt file"
fi


echo ""
info "Activate venv: source .venv/bin/activate"
info "Run: python -m src.app.main"
echo ""
