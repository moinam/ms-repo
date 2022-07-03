FROM python:3.7

WORKDIR /app
COPY . .

# This uses pip to install the requirements of the Python application into the container. Gunicorn is a Python web server that will be used to run the web app.
RUN pip install gunicorn
RUN pip install -r requirements.txt

# The environment variable sets the port that the application will run on (in this case, 8080). The last line runs the web app using the gunicorn web server.
ENV PORT=8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app