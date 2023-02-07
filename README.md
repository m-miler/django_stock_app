# Content of Project
* [General info](#general-info)
* [Technologies](#technologies)
* [Environment](#environment)
* [Setup](#setup)
* [Application view](#application-view)

## General Info
<details>
<summary>Click here to see general information about <b> Django Stock Application</b></summary>
Stock Application is a django application project in which we have the possibility to create investment portfolios,
follow current stock prices and tweets for stock exchange companies. The application allows to automatically download 
data regarding the stock prices and save them into database using celery schedule. 
</details>

## Technologies
<ul>
<li>Python 3.10</li>
<li>Django 4.14</li>
<li>Docker</li>
<li>PostgreSQL</li>
<li>Celery</li>
<li>Dash</li>
<li>Plotly</li>
<li>Factory-Boy</li>
<li>Requests</li>
<li>Tweepy</li>
</ul>

## Environment

For testing create a .env file in main folder with following variables: <br>
`DEBUG=True` <br>
`DEVELOPMENT=True`

For twitter functionality Twitter-api credentials should be provided in .env: <br>
`API_KEY`<br>
`API_KEY_SECRET`<br>
`BEARER_TOKEN`<br>
`ACCESS_TOKEN`<br>
`ACCESS_TOKEN_SECRET`<br>

Application runs with **PostgreSQL** as default database. <br>
Set `POSTGRES=False` in `.env` if you want to run SQLite3.

## Setup

1. Clone the repository: `git clone https://github.com/m-miler/django_stock_app.git` <br>
2. Install docker and docker-compose then run in project file: `$ docker-compose up` <br>
3. Application will be available at  `127.0.0.1.8080`, `login: admin`, `passowrd: admin` <br>


## Application view

Home Page <br>
<img src="https://user-images.githubusercontent.com/62297597/217302367-2d3f8136-1134-4167-96fc-d51f54db4d95.jpg"></img>

WIG20 <br>
<img src="https://user-images.githubusercontent.com/62297597/217300581-d39ebbf4-980d-4072-a97e-07224058659f.jpg"></img>

Portfolio <br>
<img src="https://user-images.githubusercontent.com/62297597/217301278-4fb0630b-4447-4262-b032-fb64031bb7c1.JPG"></img>

Profile <br>
<img src="https://user-images.githubusercontent.com/62297597/217302618-dccc598f-6503-4d5f-9f9d-110993acc301.jpg"></img>

