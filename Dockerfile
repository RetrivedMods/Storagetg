Dockerfile# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV BOT_TOKEN=your_bot_token_here
ENV CHANNEL_ID=@your_channel_id_here
ENV SAFELINK_URL=https://your-koyeb-app-url/safelink.html

# Expose the port (if needed, e.g., for a web server)
# EXPOSE 8080

# Run the bot
CMD ["python", "main"]
