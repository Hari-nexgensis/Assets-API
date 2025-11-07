# 1. Start from an official base image
FROM python:3.10-slim

# 2. Set a working directory inside the container
WORKDIR /app

# 3. Copy your project's dependency list
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install -r requirements.txt

# 5. Copy the rest of your project code into the container
COPY . .

# 6. Expose the port your app runs on
EXPOSE 8000

# 7. Define the command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]