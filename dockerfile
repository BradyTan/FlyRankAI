FROM python:3.14.7-alpine3.24

WORKDIR /app

COPY . .

RUN python -m pip install -r ./Backend/requirement.txt;

EXPOSE 8000

CMD [ "python", "-m","uvicorn", "Backend.CRUD:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]


