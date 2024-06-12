FROM python:3
# Simple Dockerfile used to run 'ckan_to_gn.py' script

# Install pip and requests library
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir requests

# Set work dir
WORKDIR /usr/app/src

# Copy python script
COPY ckan_to_gn.py ./

# Run it
CMD ["python3", "ckan_to_gn.py"]
