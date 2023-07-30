# Include Python
FROM continuumio/anaconda3:latest

# Define your working directory
WORKDIR /

# Install runpod
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --upgrade wheel && \
    pip install runpod

# Add your file
ADD Deliberate.py .

# Call your file when your container starts
# CMD [ "python", "-u", "/Deliberate.py" ]