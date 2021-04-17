# Repository structure
This folder is the heart of the application, which (current) consists of three modules: `home`, `infima` and `supremum`. 

## Module contents
A module comprises (at least) the following files:
- `__init__.py`
    - In this file the blueprint of the module is defined an all components of the module are loaded.
- `routes.py`
    - In this file, all "routes" are defined and are closely related to the website's urls. 
    Take for example the url `http://supremum.gewis.nl/infima/submit_infimum`, whose route is `/infima/submit_infimum`. 
    In the `routes.py` file, this route is defined, and it is indicated what code should be run when this page is accessed.
    - Note: observe that in infima's `routes.py` only the route `/submit_infimum` is defined, without the `/infima` prefix.
    This is due to the `url_prefix` provided to the infima-module. 
    See [Registering a module](##-Registering-a-module) for more information on `url_prefix`es.
- `templates/`
    - This folder contains all `.html` files that are served by this module.
- `static/`
    - This folder contains among others all figures and `.css` files that are served by this module.

## Registering a module
When you have created your own module, you still have to register it to the application. 
This is done in the `register_blueprint` function inside `__init__.py`.
First import the blueprint of your module and add it to `app` in the designated function.
If you wish all routes of this module to start with a certain prefix, specify this as `url_prefix` when registering the blueprint.
Hereafter, you do not have to repeat this prefix in the `routes.py` of the module.