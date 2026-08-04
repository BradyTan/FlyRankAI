# CRUD backend API
A small API that manages a task list: create, read update, search, delete tasks.
# How to install/run API
Download/Extract this respository
Install python 3.10+
***
For Windows: run .venv\Scripts\activate
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