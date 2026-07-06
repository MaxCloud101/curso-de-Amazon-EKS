FROM python:3.10.13

RUN apt-get update && apt install -y curl

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV SERVER_ENV=development

EXPOSE 8000

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "main.py" ]
