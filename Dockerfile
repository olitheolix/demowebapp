FROM python:3.7.2-alpine3.9

# All source files will go into /src.
RUN mkdir -p /src
WORKDIR /src

# Copy the source code.
COPY ./ .

RUN python --version
