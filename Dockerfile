FROM continuumio/miniconda3

# Install utilities
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Create a new environment
RUN conda create -n hornet python=3.9
RUN conda install -c anaconda git

# Activate the environment
RUN echo "source activate hornet" > ~/.bashrc
ENV PATH /opt/conda/envs/hornet/bin:$PATH

# Copy the repository
ADD . HORNET

# Install hornet / test installation
RUN cd HORNET && pip install -e .

# Run unit tests
RUN cd HORNET && pytest tests/*/*.py

# Run
CMD cd HORNET && bash