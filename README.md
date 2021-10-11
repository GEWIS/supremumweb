# Supremumweb
This repository contains the repository of the supremum.gewis.nl website.

In this README, we treat the following subjects in order:
1. The application stack.
2. The repository structure.
3. Development basics.
4. Deployment basics.
5. Administration details.
## Stack
For our stack, we use three key technologies.
- **Docker**. `Docker` is what 'contains' our application.
It provides a convenient way for us to develop the website we want, upload
it and host it at the GEWIS server, without the CBC having to worry about our
implementation details. In our docker container, we run two applications.
- **Flask**: `Flask` is the framework with which we have created out website.
It contains a built in (development) server, which we also (ab)use for hosting
the website in the docker container.
- **Nginx**: `Nginx` acts as the "glue" between the outside worlds and our
`Flask` application. It takes the requests from the 'outside world'
(i.e. people requesting our page on the internet) and either forwards the
request to the Flask application, or handles it by itself. Shortly stated, it
handles static requests (large files, .css files) itself, and let's the Flask
application deal with the HTML.


## Repository structure.
The website is contained in the `app` folder and consists of four modules:
- **home**. The `home` module contains the majority of the website: essentially
everything any (non-administrator) user interacts with.
- **admin**. The `admin` module contains the administration pages and accompanying files.
- **auth**. As the name suggests, the `auth`(orization) module is responsible for logging
people in and out from the application.
- **api**. Lastly, our website provides a (small) `api` through which other webpages
can access content that our website provides. The primary example here are the random
infima that are displayed on all other pages of the GEWIS website; these are (indirectly)
requested from our website.

Have a look at the `__init.py__` file in the `app` folder to see how the modules
have been configured.

Most modules consist of the following folders/files:
- **`__init__.py`**. In `Flask`, these modules are called `Blueprint`s. In the
`init.py` file, these blueprints are defined.
- **`routes.py`**. This files specifies the routes (urls) that can be requested
by a user and performs the steps necessary to provide the page to the user.
- **`models.py`**. This file specifies the database objects that are used to
retrieve the right data from the right location.
- **`/static`**. The static folder contains, as the name suggests, the static files
of the module. These are mostly `.css` files and images, but any (future) `.js` files
should also be placed here.
- **`/templates`**. The templates folder contains the `html` templates that are
filled in by the flask application (<- server side rendered) and subsequently
provided to the user.

For more details on how to work with Flask, you are encouraged to look for the
official [documentation](https://flask.palletsprojects.com/en/2.0.x/) or a
[tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

## Development
### Setting up the repository locally.
In order to run the repository locally, perform the following steps.
1. Clone the repository.
2. Open the repository via the command line and setup a virtual environment.
- [Linux] Execute `setup.sh`
- [Windows] Execute `setup.bat`

### Edit the repository locally.
1. Activate the virtual environment.
- [Linux] Execute `source venv/bin/activate`
- [Windows] Execute `venv/Scripts/activate.bat`
2. Activate the development server.
- [Linux] Execute `python3 serve.py`
- [Windows] Execute `python serve.py`

At this moment, you should be able to edit away to your hearts content. For most files
(with the exception of the `.env` and `config.py` files) holds that if you save them
after editing, the development server will automatically restart, which means that a
simple reload of the page will provide you with your update in place. Please note,
this does not apply for `.css` files: for these you will have to perform a **force** reload:
`ctrl + shift + r`. Happy editing!

### Environment variables
There is some information that we need to run your application that we DONT
want to end up in the GIT repository. Think of api-keys, database username/password
and the likes. To still be able to use there values, we make use of environment variables.
We store these in the `.env` file at the root of the repository. As you can see, this file
is absent by default. However, we do provide an `.env.example` file, which you should copy and save as `.env` file. After this, you can fill in your database credentials / other 
secrets to your hearts content and these variables are automatically read when the
application is run. To see how/which variables are processed, see the `config.py` file.
Note: by default, you have to restart the development server before any changes to the 
`.env` file take effect.

## Deployment
As mentioned, we use `Docker` to contain our application and deploy it on the
GEWIS server.
At the time of writing, CBC provides the supremum with two stacks:
- **supremum_live** which provides the `supremum.gewis.nl` website.
- **supremumtest** which provides the `supremum.test.gewis.nl` website.

You can access the configuration of these containers over on `docker.gewis.nl`.
If you cannot login, or do not have access to the stacks, you should get in contact
with the CBC to get this sorted.

### Pushing your version to the GEWIS server.
Let's quickly discuss how to get the changed repository on the GEWIS server.
1. Make sure all the files in your local repository are the way that you want
them to end up in the server image.
Although the `Dockerfile` specifies how the docker image is created from your local
files, it does so based on the current files in your directory, not the last
committed version.
_Note: if you know of a better method to approach this, feel free to rewrite the documentation on this._
2. Set the correct port in the `extra_nginx.conf` file. If you are creating a version for the test-server, set it to `9500`; for the live server set it to `9501`.
WARNING: This is super important, otherwise the server won't operate properly.
_Note: feel free to change the docker install to circumvent this issue._
3. Create the image.
- [Linux]: ```sudo docker build . -t supremum.docker-registry.gewis.nl/site:v{tag}```,
where you replace `{tag}` with the version number of your image.
- [Windows]: this command is not known. We advise you to use WSL and use the above command.
4. Push the image to the GEWIS server.
- [Linux]: ```sudo docker push supremum.docker-registry.gewis.nl/site:v{tag}```
- [Windows]: this command is not known. We advise you to use WSL and use the above command.
It might be that (during the first time) you are asked for your credentials in order to push
to the GEWIS server. We advise you to have a look at the Docker documentation on this
process and login with your `docker.gewis.nl` credentials.

### Changing the version on the server.
To start using the image on the server, head on over to `docker.gewis.nl` and open the
appropriate stack in the `stacks` overview. Once there, open the `editor` tab and
under `flask -> image` change the version number to the appropriate version.
Hereafter, push the `update the stack` button and within a couple seconds your new
version is live.

WARNING: at the time of writing, the database used by the test server and the live
server are identical. If you wish to test something related to the database,
head over to `mysql.gewis.nl` and create a new database to test on.

### The Data
The Supremum website stores quite some data. The most notable being
- Infima
- Supremum pdfs.

As these are very asimilar, we employ two different methods to store these.
- **Persistent volume**. We store the Supremum pdfs as files in a persistent volume
on the docker.gewis server. It is not really possible to directly access this
volume via `docker.gewis.nl`. Instead, you can only update these files via the
administration panel on the website itself.
- **Database**. The database contains the infima and the paths to where the suprema
are stored in the persistent volume. The interface for the database is accessible via
`mysql.gewis.nl`. You should be able to log in with the same credentials as those
for `docker.gewis.nl`. If you don't have credentials or do not have access to the
databases, get in contact with CBC.


## Administration
Below, we provide some basic information on some administrational tasks that one
might wish to perform.

### Add/remove a user as admin
Sadly, this is not yet possible on the `supremum.gewis.nl` website itself.
Instead, we have to change a value in the database to make someone an admin (or not).
1. Head over to `mysql.gewis.nl` and log in.
2. Open the `supremum_website` database.
3. Edit/add the entry with the desired GEWIS-id and set them to admin (1) or not (0).
