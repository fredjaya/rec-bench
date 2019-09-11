FROM nfcore/base

LABEL maintainer="Fred Jaya <fredjaya1@gmail.com>"
LABEL description="WIP Docker image containing requirements for \
fredjaya/rec-bench pipeline"

COPY environment.yml /
RUN conda env create -f /environment.yml && conda clean -a
ENV PATH /opt/conda/envs/fredjaya-rec-bench-0.1.0/bin:$PATH
