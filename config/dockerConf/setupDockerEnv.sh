# #!/bin/bash

# # Check for VS Code
# if which code > /dev/null; then
#     echo "VS Code is installed, installing extensions..."

#     # Install Jupyter Extension
#     code --install-extension ms-toolsai.jupyter || { echo "Failed to install Jupyter extension"; exit 1; }
#     echo "Jupyter Extension installed."

#     # Install Remote Containers Extension
#     code --install-extension ms-vscode-remote.remote-containers || { echo "Failed to install Remote Containers extension"; exit 1; }
#     echo "Remote Connection Installed."

#     echo "Dependency Installation Complete."
# else
#     echo "VS Code is not installed, please install it to continue."
#     exit 1
# fi

# # Define container and image names
CONTAINER_NAME=gc-parser
IMAGE_NAME=gc-parser
PORT=8888

# # Stop and remove the container if it's running
# if docker ps -a | grep -q $CONTAINER_NAME; then
#     echo "Stopping running container..."
#     docker stop $CONTAINER_NAME || { echo "Failed to stop container"; exit 1; }
#     echo "Removing existing container..."
#     docker rm $CONTAINER_NAME || { echo "Failed to remove container"; exit 1; }
# fi

# # Remove the image if it exists
# if docker images -a | grep -q $IMAGE_NAME; then
#     echo "Removing existing image..."
#     docker rmi -f $IMAGE_NAME || { echo "Failed to remove image"; exit 1; }
# fi

# # cd to app's root
# cd ../../ || { echo "Failed to change directory"; exit 1; }

# # Build the Docker container
# echo "Building the Docker container..."
# docker build -f config/dockerConf/Dockerfile --no-cache -t $IMAGE_NAME . || { echo "Docker build failed"; exit 1; }
# echo "Build complete."

# Start container
echo "Starting Container on port: $PORT..."
docker run -it -p $PORT:$PORT $IMAGE_NAME 2>&1 | awk '/Or copy and paste one of these URLs:/{exit}1' # Stop logging once links have been provided

echo "

Server is still running
logs have been stopped to prevent flooding
enter \"docker ps\" to capture container ID
\"docker stop <CONTAINER_ID>\", to kill container" #TODO: Add easy ability to kill