# 1. Use an official Python runtime as the base image
FROM python:3.10-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements.txt file into the container
COPY requirements.txt /app/

# 4. Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application files into the container
COPY . /app/

# 6. Creating the data directory 
RUN mkdir -p /app/data

# 7. Expose the port that Streamlit runs on
EXPOSE 8501

# 8. Set environment variables (for example, load the .env file if required)
ENV STREAMLIT_SERVER_PORT=8501

# 9. Run the app
CMD ["streamlit", "run", "app.py"]
