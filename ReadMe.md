# Week 1: CRUD backend API
A small API that manages a task list: create, read, update, search, delete tasks.
# How to install/run API
Download/Extract this respository

Install python 3.10+

For Windows:

***
    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r .\Backend\requirement.txt
    uvicorn Backend.CRUD:app --reload
***
| Endpoints | 
|-----------|
| POST /tasks |
| GET /tasks - GET /tasks?search={task} - GET /tasks?done={bool} - GET /tasks?search={task}&done={bool}  - GET /tasks/3 |
| PUT /tasks/3 |
| DELETE /tasks/3 |
| GET /stats |
| POST /reset |


curl -i -X PUT http://localhost:8000/tasks/4 -H "Content-Type: application/json" -d "{\"id\":\"4\",\"done\":\"true\"}"
HTTP/1.1 200 OK
date: Tue, 04 Aug 2026 21:47:35 GMT
server: uvicorn
content-length: 39
content-type: application/json

The tasks I created are not saved. The client is running a local list, and it is not sending any data across the network.

![Swagger UI](./image/Swagger.png)
# Week 2 SQL database
I run this query: "SELECT count(*) FROM tasks;"
It returns a table with a cell with the number eight. The column has a label with "count(*)", and the row has a label with "1".

Why SQLite was chosen?
It is because SQLite is built into Python, so there is no need to install it. SQLite is serverless, self-contained, zero-configuration, and transactional feature. So there is no need to install a client. There is no need to mess with the configuration files.


The database lives at the root of the directory.

When adding the column created_at and updated_at, the table become wider. I have to edit a class for the new columns and methods.
How to run the database:

Download/Extract this respository

Install python 3.10+

For Windows:

***
    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r .\Backend\requirement.txt
    uvicorn Backend.CRUD:app --reload
***
![Database](./image/Database.PNG)

## Containerize your stack

A docker container that run the CRUD API and the POSTGRESQL database in a isolation linux environment.

How to run it:
***
  docker compose up -d
***
In the .env file set DATABASE_URL=postgres://postgres:dev@localhost:5432/tasks

curl -i http://localhost:8000/tasks
HTTP/1.1 200 OK
date: Fri, 07 Aug 2026 18:12:27 GMT
server: uvicorn
content-length: 1017
content-type: application/json

[[1,"Sample Task 1","2026-08-07 18:07:52.852293+00","2026-08-07 18:07:52.852293+00",false],[2,"Sample Task 2","2026-08-07 18:07:52.852293+00","2026-08-07 18:07:52.852293+00",false],[3,"Sample Task 3","2026-08-07 18:07:52.852293+00","2026-08-07 18:07:52.852293+00",false],[4,"string","2026-08-07 18:12:02.78342+00","2026-08-07 18:12:02.78342+00",false],[5,"string","2026-08-07 18:12:04.440603+00","2026-08-07 18:12:04.440603+00",false],[6,"string","2026-08-07 18:12:04.900374+00","2026-08-07 18:12:04.900374+00",false],[7,"string","2026-08-07 18:12:05.078744+00","2026-08-07 18:12:05.078744+00",false],[8,"string","2026-08-07 18:12:05.198832+00","2026-08-07 18:12:05.198832+00",false],[9,"string","2026-08-07 18:12:08.180305+00","2026-08-07 18:12:08.180305+00",false],[10,"string","2026-08-07 18:12:08.36599+00","2026-08-07 18:12:08.36599+00",false],[11,"string","2026-08-07 18:12:08.510635+00","2026-08-07 18:12:08.510635+00",false],[12,"string","2026-08-07 18:12:08.685753+00","2026-08-07 18:12:08.685753+00",false]]


| Endpoints | 
|-----------|
| POST /tasks |
| GET /tasks - GET /tasks?search={task} - GET /tasks?done={bool} - GET /tasks?search={task}&done={bool}  - GET /tasks/3 |
| GET /sort |
| PUT /tasks/3 |
| DELETE /tasks/3 |
| GET /stats |
| POST /reset |

Why volume exist because it is to store the data for the Postgresql. If it is removed, it returns a Internal Server Error.
![Database](./image/BrowserDatabase.PNG)