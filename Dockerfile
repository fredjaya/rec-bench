FROM nfcore/base

LABEL maintainer="Fred Jaya <fredjaya1@gmail.com>"
LABEL description="WIP Docker image containing requirements for \
fredjaya/rec-bench pipeline"

# Add conda recipe and SANTA-SIM .jar to container
COPY environment.yml /
COPY bin/santa_bp.jar /usr/bin/

# Create conda environment
RUN conda update -n base -c defaults conda
RUN conda env create -f /environment.yml && conda clean -a

# Add to path
ENV PATH /opt/conda/envs/fredjaya-rec-bench-0.1.0/bin:$PATH
#ENV PATH /usr/bin/santa-bp.jar:$PATH
