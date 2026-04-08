# Use a lightweight Python base image
FROM python:3.9-slim

# Set up a new user named "user" with user ID 1000 to avoid permission issues
# This is a strict requirement for Hugging Face Docker Spaces
RUN useradd -m -u 1000 user

# Set environment variables for the user's home and local bin path
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's app folder
WORKDIR $HOME/app

# Copy requirements and install them as the non-root user
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application files, ensuring the user owns them
COPY --chown=user . .

# Expose the standard port for Hugging Face Spaces
EXPOSE 7860

# Start the FastAPI application using uvicorn
# Note: --host 0.0.0.0 is critical for container accessibility
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
