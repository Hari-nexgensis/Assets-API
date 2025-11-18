# 1. Start from an official base image
FROM python:3.10-slim

# 2. Install Node.js and npm
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Verify Node.js and npm installation
RUN node --version && npm --version

# 4. Set a working directory inside the container
WORKDIR /app

# 5. Copy your project's dependency list
COPY requirements.txt .

# 6. Install Python dependencies
RUN pip install -r requirements.txt

# 7. Copy the rest of your project code into the container
COPY . .

# 8. Build the React frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# 9. Go back to app directory
WORKDIR /app

# 10. Expose the port your app runs on
EXPOSE 8000

# 11. Define the command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]