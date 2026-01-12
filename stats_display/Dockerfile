FROM python3.13

#ُSet working directory
WORKDIR /app

#Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy application files
COPY . .

EXPOSE 5002

#Run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002"]
