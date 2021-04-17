# Supremumweb


## Development environment
If you wish to run this website locally, do the following:

### Setup
0. Install python3 and git.
1. Download this git repository.
2. Run `setup.sh` (Linux, OS X) or `setup.bat` (Windows).
    - This creates a virtual environment (venv) and installs the necessary python packages.

### Start
After you have everything set up, run the following commands on the command line each time you want to start the server locally:
0. Run `source venv/bin/activate` (Linux, OS X) or `venv\Scripts\activate.bat` (Windows).
    - This activates the virtual environment we created in the setup.
    - It can be deactivated by running `source venv/bin/deactivate` (Linux, OS X) or `venv\Scripts\deactivate.bat` (Windows).
1. Execute `python3 wsgi.py`
    - This starts the development server.
2. Open `http://localhost:5000/` on your web browser to view the website.

### Automatic reload
This development server has been setup in such a way that when changing and saving a python file (`.py`), the server automatically restarts. Simply (force-)refresh your browser to view the update version: `ctrl+shift+r` (Windows, Linux) or `cmd+shift+r` (OS X).
This also works when updating a `.css` file. 

When you have updated an `.html` file, you have to restart the 

## Documentation
The documentation for this repository is continued in the `app` folder.