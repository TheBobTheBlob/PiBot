FROM python:3.13.2-slim-bookworm

# Copy the current directory contents into the container at /app
WORKDIR /app
COPY requirements.txt ./
COPY main.py ./
COPY static ./static
COPY components ./components

# Install dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

# Run discord bot
CMD ["python", "main.py"]
