FROM nvidia/cuda:11.2.0-cudnn8-runtime-ubuntu18.04

SHELL ["/bin/bash", "-c"]

# Install essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git wget unzip python-pip libgl1-mesa-dev tar nano sudo systemd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setup conda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh -o Miniconda3-py39_4.10.3-Linux-x86_64.sh
RUN bash Miniconda3-py39_4.10.3-Linux-x86_64.sh -b
ENV PATH=/root/miniconda3/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN conda init bash
RUN conda update -y conda

RUN git clone https://github.com/discus0434/tweetgen-from-timeline.git
WORKDIR /tweetgen-from-timeline

# Setup conda environment
RUN conda create -n tweetgen python=3.9
RUN echo "source activate tweetgen" > ~/.bashrc
RUN conda run -n tweetgen pip install -r requirements.txt
