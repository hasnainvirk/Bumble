#!/bin/bash

# Variables
PI_USER="bumble"  
PI_HOST="bumble.local"

# Function to display error message and exit
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# SSH into the Raspberry Pi and execute commands
ssh -t "$PI_USER@$PI_HOST" << 'EOF'
  # Variables
  REPO_NAME="Bumble"
  PI_PATH="/home/bumble"
  REPO_PATH="$PI_PATH/$REPO_NAME"
  VENV_PATH="$PI_PATH/.virtualenvs/bumble"
  REPO_URL="https://github.com/hasnainvirk/Bumble.git"  

  # Check if the project directory exists
  if [ ! -d "$REPO_PATH" ]; then
    # Clone the repository if the directory doesn't exist
    git clone "https://github.com/hasnainvirk/Bumble.git" "$PI_PATH" || { echo "Error: Failed to clone repository."; exit 1; }
  else
    # Navigate to the repository directory and pull the latest changes
    cd "$REPO_PATH" || { echo "Error: Failed to navigate to repository directory."; exit 1; }
    git pull || { echo "Error: Failed to pull latest changes."; exit 1; }
  fi

  # Activate the virtual environment
  source "$VENV_PATH/bin/activate" || { echo "Error: Failed to activate virtual environment."; exit 1; }
  
  # Navigate to the repository directory
  cd "$REPO_PATH" || { echo "Error: Failed to navigate to repository directory."; exit 1; }
  
  # Install the program
  pip install -e . || { echo "Error: Failed to install the program."; exit 1; }

# Install Dev Requirements 
  pip install -r requirements-dev.txt || { echo "Error: Failed to install dev requirements."; exit 1; }

# Install Requirements
  pip install -r requirements.txt || { echo "Error: Failed to install requirements."; exit 1; }
  
  # Execute the bumble --help command and store the output in a file
  bumble --help | tee bumble_help_output.txt || { echo "Error: Failed to execute 'bumble --help' command."; exit 1; }
EOF

# Check the exit status of the SSH command
if [ $? -eq 0 ]; then
    echo "Script executed successfully."
else
    echo "Script failed."
fi