FROM ubuntu:20.04

# Set container as a root user
USER root

ENV TZ=US
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y
RUN apt-get install -y automake pkg-config libsdl-pango-dev libicu-dev libcairo2-dev bc wget unzip tesseract-ocr python3-pip

# Optional dev tools
RUN apt-get install -y git vim

# Copy files into the container
COPY ./config/requirements.txt /tmp/requirements.txt

# Install defined dependencies
RUN pip3 install -r /tmp/requirements.txt --no-deps

# Install Jupyter to cli
RUN pip3 install jupyter

# flag to turn off token
ENV JUPYTER_TOKEN=easy
# still requires password - server config, move to correct location
COPY ./config/jupyter_server_config.py /root/.jupyter/jupyter_server_config.py

# Set the working directory - need to mount files here with -v <path to project>:/home/
WORKDIR /home/

# Start Jupyter Notebook server when the container starts
## port and ip set in config file
# 0.0.0.0:8888

# run with project dir mounted to home and port forwarding
# docker run -p 8888:8888 -v $(pwd):/home/ gc-parser

ENTRYPOINT ["jupyter", "notebook", "--no-browser", "--allow-root", "--debug"]