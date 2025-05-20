FROM python:3.11-slim

WORKDIR /home/myapp
COPY requirements.txt ./
RUN pip install --no-cache-dir -q -r requirements.txt

COPY sample_app.py ./
COPY templates/    ./templates/
COPY static/       ./static/

EXPOSE 3000
CMD ["python3", "sample_app.py"]
