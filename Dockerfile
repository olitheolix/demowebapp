FROM python:3.7.2-alpine3.9

# All source files will go into /src.
RUN mkdir -p /src
WORKDIR /src

# Copy and install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the source code.
COPY ./ .

ENTRYPOINT ["python"]
CMD ["app.py"]
