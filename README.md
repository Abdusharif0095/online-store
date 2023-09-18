# Online-store
An online store is planning to launch a campaign in different regions. In order for the sales strategy to be effective, market analysis is necessary. The store has a supplier who regularly sends (for example, by email) data exports with information about residents.

For this purpose, a REST API service has been developed in Python that analyzes the provided data and identifies demand for gifts among residents of different age groups in different cities by month.

The service implements the following handlers:

`POST /imports` - Adds a new data export; <br>
`GET /imports/$import_id/citizens` - Returns residents of the specified data export; <br>
`PATCH /imports/$import_id/citizens/$citizen_id` - Modifies information about a resident (and their relatives) in the specified data export; <br>
`GET /imports/$import_id/citizens/birthdays` - Calculates the number of gifts that each resident of the data export will purchase for their first-order relatives, grouped by month; <br>
`GET /imports/$import_id/towns/stat/percentile/age` - Calculates the 50th, 75th, and 99th percentiles of the ages (in full years) of residents by city in the specified sample. <br>

# Project Structure
```
.
├── online-store
|     └── main
|     |     └── migrations
|     |     ├── test_data
|     |     ├── __init__.py
|     |     ├── admin.py
|     |     ├── apps.py
|     |     ├── checkers.py
|     |     ├── models.py
|     |     ├── tests.py
|     |     ├── urls.py
|     |     └── views.py
|     ├── online_store
|     |     └── __init__.py
|     |     ├── asgi.py
|     |     ├── settings.py
|     |     ├── urls.py
|     |     └── wsgi.py
|     ├── Dockerfile
|     ├── db.sqlite3
|     ├── docker-compose.test.yml
|     ├── docker-compose.yml
|     ├── manage.py
|     ├── requirements.txt
|     ├── run_app.sh
|     └── run_tests.sh
├── README.md
└── TASK.pdf
```
# To run this Service you should:
- Give permission to execute the script `chmod +x run_app.sh`;
- Run the command `./run_app.sh`;
- After 2 first steps, the application will start listening for requests at `0.0.0.0:8080`.
# To run tests you should follow these commands:
- Give permission to execute the script `chmod +x run_tests.sh`;
- Run the command `./run_tests.sh`.
# Technology stack:
- Docker - is a platform designed to help developers build, share, and run modern applications;
- Django - API web framework.
