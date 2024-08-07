FROM python:3.10.14-alpine3.19
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 3333
ENTRYPOINT [ "python" ]
CMD ["manage.py", "runserver", "0.0.0.0:3333"]