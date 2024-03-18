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
COPY . /home/

# Install defined dependencies
RUN pip3 install -r /home/config/requirements.txt --no-deps

# Install Jupyter to cli
RUN pip3 install jupyter

# flag to turn off token
ENV JUPYTER_TOKEN=easy

# still requires password - server config, move to correct location
COPY ./config/jupyter_server_config.py /root/.jupyter/jupyter_server_config.py

# Set the working directory
WORKDIR /home/

ENTRYPOINT ["jupyter", "notebook", "--no-browser", "--allow-root"]