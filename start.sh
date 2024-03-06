# forward port 8888 from container
# mount volume of current dir (the project) to /home inside container
# start image named gc-parser

docker run -p 8888:8888 -v $(pwd):/home/ gc-parser