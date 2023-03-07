# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.10** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=1
flask run
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

---

## API Reference

- base url: when you start server, The backend is hosted at http://127.0.0.1:5000

---

### backend/flaskr/views/form_views.py

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

> Request

- Method: GET
- URL path: /categories
- Request arguments: None
  > Response
- Status code: 200 OK
- Content-type: application/json

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

---

### backend/flaskr/views/question_views.py

`GET '/questions'`

- Fetches a paginated list of questions with each page containing 10 questions.
- Request Arguments: page (optional, default=1)
- Returns: Returns: An object with the following keys:
  - 'success' (boolean)
  - 'questions' (list of question objects)
  - 'total_questions' (integer)
  - 'categories' (dictionary of category id: category string key-value pairs)
  - 'current_category' (null)

> Request

- Method: GET
- URL path: /questions
- Request arguments: page (optional, default=1)
  > Response
- Status code: 200 OK
- Content-type: application/json

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

`POST '/questions`

- Adds a new question to the database and returns the ID of the new question.
- Request Arguments: A JSON object that contains the following key-value pairs:
  - question: The question text (string)
  - answer: The answer text (string)
  - category: The ID of the category (integer)
  - difficulty: The difficulty level of the question (integer)
- Returns: An object with a single key, question_id, that contains the ID of the new question.

> Request

- Method: POST
- URL path: /questions
- Request arguments: body

```json
{
  {
    "question": "What is the capital city of France?",
    "answer": "Paris",
    "category": 3,
    "difficulty": 2
  }
}

```

> Response

- Status code: 200 OK
- Content-type: application/json

```json
{
  "success": true,
  "question_id":[number]
}
```

`DELETE '/questions/<int:question_id>'`

- Deletes the question with the given question_id.
- Request Arguments: question_id - integer, the ID of the question to be deleted.
- Returns: An object with a single key, success, that is true if the deletion was successful.

> Request

- Method: POST
- URL path: /questions/{question_id}
- Request arguments: `question_id` - integer, the ID of the question

> Response

- Status code: 200 OK
- Status code: 404 Not Found (`question_id`)
- Status code: 422 Unprocessable
- Content-type: applicatoin/json

```json
{
  "success": true
}
```

`POST '/questions/search'`

- Search questions that match a search term
- Request Arguments: None
- Request Body: An object with a single key, searchTerm, that contains the search term string
- Returns: An object with a single key, questions, that contains a list of questions that match the search term. Each question is represented as an object with id, question, answer, category, and difficulty keys. Also returns the total_questions that match the search term and current_category which is always None.

> Request

- Method: POST
- URL path: /questions/search
- Request arguments: body

```json
{
  "searchTerm": "title?"
}
```

> Response

- Status code: 200 OK
- Content-type: application/json

```json
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

`GET '/categories/<int:category_id>/questions'`

- Fetches a list of questions filtered by the given category id
- Request Arguments: category_id (integer)
- Returns: An object with the following key-value pairs:
  - success (boolean): true if the request was successful, false otherwise.
  - questions (list): a list of question objects, where each question contains the following key-value pairs:
    - id (integer): the question ID.
    - question (string): the question text.
    - answer (string): the answer text.
    - difficulty (integer): the difficulty level of the question.
    - category (integer): the category ID of the question.
  - total_questions (integer): the total number of questions that match the search criteria.
  - current_category (integer): the category ID of the current search criteria.

> Request

- Method: GET
- URL path: /categories/{category_id}/questions
- Request arguments: category_id (integer)

> Response

- Status code: 200 OK
- Content-type: application/json

```json
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

---

### backend/flaskr/views/quiz_view.py

`POST '/quizzes'`

- Plays a quiz game by returning random questions based on the specified category and previous questions.
- Request Arguments: A JSON object containing previous_questions list and a quiz_category object with an id key that represents the category of questions to be selected. The previous_questions list contains a list of question IDs that have been shown in the previous requests and should be excluded in the current request.
- Returns: A JSON object with a single key, question, that contains the next random question to be displayed to the user.

> Request

- Method: POST
- URL path: /quizzes
- Request arguments:
  - previous_questions: A list of question IDs that have been shown in the previous requests and should be excluded in the current request.
  - quiz_category: A JSON object with an id key that represents the category of questions to be selected.
- Example: {"id": "1", "type": "Science"}
- Request body: JSON object

```json
{
  "previous_questions": [2, 4],
  "quiz_category": { "id": 1, "type": "Science" }
}
```

> Response

- Status code: 200 OK
- Content-type: application/json
- JSON object with a single key, question, that contains the next random question to be displayed to the user.

```json
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

---

Error handler

`ERROR 400: Bad Request`

- Description: The request could not be understood or was missing required parameters.
- Response body: An object with the following keys: success (boolean), error (integer), message (string).
- Response example:

```json
{
  "success": false,
  "error": 400,
  "message": "Bad request"
}
```

`ERROR 404: Not Found`

- Description: The requested resource could not be found.
- Response body: An object with the following keys: success (boolean), error (integer), message (string).
- Response example:

```json
{
  "success": false,
  "error": 404,
  "message": "Not found"
}
```

`ERROR 422: Unprocessable Entity`

- Description: The request was well-formed but was unable to be followed due to semantic errors.
- Response body: An object with the following keys: success (boolean), error (integer), message (string).
- Response example:

```json
{
  "success": false,
  "error": 422,
  "message": "Can not process the request"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
