# Item Catalog - Udacity FSND
This is a project for the Udacity Full-Stack Nanodegree program. It allows users to view, create, edit, and delete "items" containing a name, description, and icon. Items are organized by category, which users are free to edit as well. Login via Google or Facebook is required to modify entries. It was created using the following:
* Flask
* Vagrant
* Python
* Oauth2
* Bootstrap
* Popper.js
* JQuery

## Getting Started
Running this web application requires a download and installation of the source code and a registration with the Google and Facebook Oauth APIs.

### Download and Installation
To acquire the program files, clone the GitHub repository. If Python 2.7 is not installed, do so now. The database can be initialized by running 'database_setup.py', which will create the catalog database `catalog.db`. If desired, run `populate_db.py` to initialize the database with some categories and items (these should be used for demonstrative purposes only).

### Setting up Google Authentication
Registration is required to use Google Oauth functionality. The details of how to do this may change from the time of writing this, so it's best to consult the most up to date documentation on the Google Developer's website. At the moment, instructions can be found at this [url]: https://developers.google.com/identity/sign-in/web/devconsole-project. You should obtain a Client ID, Project ID, and Client Secret, which need to be inserted into the provided `client_secrets.json` file in the root directory. Additionally, you need to update the `redirect_uris` and `javascript_origins` keys in the JSON file to reflect the domain at which you will be hosting the web app (I had been using `http://localhost:8000`). These entries should match the domains that you have provided during the Google registration. Additionally, you need to insert your Client ID into the `login.html` file. More specifically, you need to modify the `data-clientid` property of the <span> with a class of `g-signin`.

### Setting up Facebook Authentication
Similar to the Google authentication, Facebook requires you to register the app on their developers page.
`https://developers.facebook.com/`
Upon registration, you should have an App ID and an App Secret, which can be inserted into the `fb_client_secrets.json` file. The `login.html` file also needs to include the App ID. It should be placed as a string value for `appID` in the final `<script>` element.

### Launching the Server
The application is run by executing the python file `application.py`. It will be hosted at the domain you provided in earlier steps.

## Using the Item Catalog
Categories and Items can be created by any logged in user. Users can only edit or delete Categories or Items that they themselves have created. Currently, there is no administrator profile. To reset the Catalog entirely, simply delete the `catalog.db` file and rerun `database_setup.py`.

## Acknowledgments
Much of the code handling the OAuth2 authentication was adapted from the Udacity FSND lessons on this subject. This includes the login handlers in 'application.py' and parts of 'login.html'. There are also some similarities between the Flask code of this project and that of previous lessons on the Restaurant Menu App. Some of HTML code for the Bootstrap dropdowns and cards is fairly close to what is provided in the Bootstrap documentation. The images used in `populate_db.py` are from Wikipedia and should have attributions to the original artists if used on a live website.
