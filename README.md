## Full Stack Nano - IAM Final Project

This application is a coffee shop recipe management system allowing managers, baristas and the public to create, edit, view and delete drink recipes depening on their assigned authorization roles. The application:

1. Displays graphics representing the ratios of ingredients in each drink.
2. Allows public users to view drink names and graphics.
3. Allows the shop baristas to see the recipe information.
4. Allows the shop managers to create new drinks and edit existing drinks.

---
## Getting Started

### Installing Dependencies

Development for this project requires **Python 3.6** or later, **Nodejs**, **pip** and the Node Package Manager (**NPM**) to be already installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. The required dependencies are found in the `/frontend/package.json` file located of this repository. After cloning the repository, open your terminal navigate to the `/frontend` folder and run:

    npm install

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Backend Dependencies

Setup and run a Python 3.6 or later virtual environment, navigate to the `/backend` directory and run:

    pip install -r requirements.txt

The backend uses Flask as a server and Auth0 for authentication.

### Configure Environment Variables

Ionic uses a configuration file to manage environment variables. These variables ship with the transpiled software and should not include secrets.

- Open `./src/environments/environments.ts` and ensure each variable reflects the system you stood up for the backend.

## Running Your Frontend in Dev Mode

Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, cd into the `frontend` directory and run:

```bash
ionic serve
```
The frontend is served to http://localhost:8100/tabs/drink-menu   

### Authentication

The authentication system used for this project is Auth0. `./src/app/services/auth.service.ts` contains the logic to direct a user to the Auth0 login page, managing the JWT token upon successful callback, and handle setting and retrieving the token from the local store. This token is then consumed by our DrinkService (`./src/app/services/drinks.service.ts`) and passed as an Authorization header when making requests to our backend.

### Authorization

The Auth0 JWT includes claims for permissions based on the user's role within the Auth0 system. This project makes use of these claims using the `auth.can(permission)` method which checks if particular permissions exist within the JWT permissions claim of the currently logged in user. This method is defined in  `./src/app/services/auth.service.ts` and is then used to enable and disable buttons in `./src/app/pages/drink-menu/drink-form/drink-form.html`.

### Running the Backend Server

From within the `/backend` directory activate the virtual environment and run the backend server.

To run the server, execute:

    export FLASK_APP=api.py
    export FLASK_ENV=development
    flask run --reload

The `--reload` flag will detect file changes and restart the backend server automatically.

## API Reference

### Getting Started
* Base URL: This application is hosted locally. The backend is hosted at `http://127.0.0.1:5000/` 
* Authentication: This application currently does not require authentication or API keys

### Error Handling

Errors are returned as a JSON object.

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API currently returns three classes of errors:

* 400 – bad request 
* 401 - unauthorized
* 404 – resource not found  
* 422 – unprocessable

---
### API Endpoints   

#### GET /drinks
returns:
`{"success": True, "drinks": drinks}` where drinks is the list of drinks
#### GET /drinks-detail
returns:
`{"success": True, "drinks": drinks}` where drinks is a detailed list of drinks
#### POST /drinks
returns:
`{"success": True, "drinks": drink}` where drink an array containing only the newly created drink
#### PATCH /drinks/<int: id>
returns:
`{"success": True, "drinks": drink}` where drink an array containing only the updated drink
#### DELETE /drinks/<int: id>
returns:
`{"success": True, "drinks": drink}` where drink an array containing only the updated drink   

---
### Testing

Tests are contained in the `/backend/udacity-fsnd-udaspicelatte.postman_collection.json` file.

To run the tests, install Postman https://www.postman.com/downloads, import the udacity-fsnd-uadspicelatte.postman_collection.json file into Postman and run the collection.  
After the first run, comment out the db_drop_and_create_all() line in the api.py file or the database will be reset each time the app is run.

---
### Authors
Kep Kaeppeler is the author of the backend API,  authorization suite, and documentation including the `api.py`, `auth.py`, and this `README` file.  
All other project files, including the models and frontend, were created by the Udacity team. This was meant as a project template for the Full Stack Web Developer Nanodegree.