FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy everything from our local directory to the working directory
COPY . .

CMD ["python", "./server/app.py"]
