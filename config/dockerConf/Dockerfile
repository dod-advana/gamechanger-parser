FROM ubuntu:20.04

# Set container as a root user
USER root

ENV TZ=US
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y
RUN apt-get install -y automake pkg-config libsdl-pango-dev libicu-dev libcairo2-dev bc wget unzip tesseract-ocr python3-pip

# Optional dev tools
RUN apt-get install -y git

# Copy app root into the container
COPY . /home/

# Install defined dependencies
RUN pip3 install -r /home/config/requirements.txt --no-deps

# Install Jupyter
RUN pip3 install jupyter

# Set the working directory
WORKDIR /home/

# Start Jupyter Notebook server when the container starts
ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--debug"]