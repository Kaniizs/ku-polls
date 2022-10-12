[![codecov](https://codecov.io/gh/oMojiko/ku-polls/branch/main/graph/badge.svg?token=KE2L6KMD8B)](https://codecov.io/gh/oMojiko/ku-polls)

# KU Polls

## Online Polls And Surveys

An application for conducting online polls and surveys based
on the [Django Tutorial project][django-tutorial], with
additional features.

App created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University.

## How to Install and Run

- Clone a repository into your location.
  ```
  git clone https://github.com/oMojiko/ku-polls.git ku-polls
  ```

- Go to directory of the project 
  
  ```
  cd ku-polls
  ```

- Create the virtual environment.
  ```
  python -m venv env
  ```

- Activate the virtual environment.
    * For windows.
        ```
        env\Scripts\activate
        ```
    * For MAC OS and Linux.
        ```
        source venv/bin/activate
        ```

- Install a requirements package by using.
  ```
  pip install -r requirements.txt
  ```

- Run the development server using.
  ```
  python manage.py runserver
  ``` 
- Go to the following url.
  ```
  http://localhost:8000/polls/
  ```

## Demo user

| Username  | Password  |
|-----------|-----------|
|   Mojy   | Testing235 |
|   Test2  | Nowtesting212 |


## Project Documents

All project documents are in the [Project Wiki](https://github.com/oMojiko/ku-polls/wiki).

- [Vision Statement](https://github.com/oMojiko/ku-polls/wiki/Vision-Statement)

- [Requirements](https://github.com/oMojiko/ku-polls/wiki/Requirements)
  
- [Project Plan](https://github.com/oMojiko/ku-polls/wiki/Development-plan)

## iteration plan

- [Iteration 1 Plan](https://github.com/oMojiko/ku-polls/wiki/iteration-1-Plan)

- [Iteration 2 Plan](https://github.com/oMojiko/ku-polls/wiki/iteration-2-Plan)

- [Iteration 3 Plan](https://github.com/oMojiko/ku-polls/wiki/iteration-3-Plan)

- [Iteration 4 Plan](https://github.com/oMojiko/ku-polls/wiki/iteration-4-Plan)

- [Task Board](https://github.com/users/oMojiko/projects/3/views/1)

[django-tutorial]: https://docs.djangoproject.com/en/4.1/intro/tutorial01/
