# defaults defined in ./setupDockerEnv.sh
# forward port, default:8888 from container
# start image named, default: gc-parser

docker run -p 8888:8888 -v $(pwd):/home/ gc-parser 2>&1 | awk '/Use Control-C to stop this server and shut down all kernels \(twice to skip confirmation\)\./{exit}1' #Stops logging once links have been provided
    
    echo "
Server is running
logs have been stopped to prevent flooding
enter \"docker ps\" to capture container ID
\"docker stop <CONTAINER_ID>\", to kill container" #TODO: Add easy ability to kill
