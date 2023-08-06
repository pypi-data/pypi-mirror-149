# GDS template pack

This is a [django-pattern-library](https://github.com/torchbox/django-pattern-library) template pack for the 
[GOV.UK design system](https://design-system.service.gov.uk/components/).

## Quickstart

This is a minimal how-to for installation and usage. 

Install using your package manager of choice. e.g. with pip:

```
pip install gds-template-pack
```

Add to installed apps and add a section to the [django-pattern-library](https://github.com/torchbox/django-pattern-library) settings:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    "pattern_library",
    "gds_template_pack",
]

# django-pattern-library
PATTERN_LIBRARY = {
    "SECTIONS": (
        ("gds", ("gds",)),
        # ...
    ),
    # ...
}
```

### Usage

Once installed and configured, you can reference the various templates as you would do with any Django app. e.g.
to use the back-link component: `{% include "gds/back-link/back-link.html" with link_url="https://example.com" link_text="Back" %})`

## Development

You'll need Python 3.8 or above and [Poetry](https://python-poetry.org/docs/#installation) installed.

## Setup

Install the Python dependencies using Poetry:

```sh
poetry install
```

By default, this will create a virtual environment in `./.venv/` and install the dependencies there.
If this doesn't happen, check your settings against [the documentation](https://python-poetry.org/docs/configuration/#virtualenvscreate).

Then start the Django development server and browse the template pack at [http://localhost:8000/](http://127.0.0.1:8000/):

```
poetry run dev_app/manage.py runserver 8000
```

## Frontend Development

To set up the frontend development environment, first run the above commands to start the django server. Then, run the following commands in a separate terminal window.

```sh
fnm use
npm install
npm run start
```

If you haven't installed `fnm` yet, you can install it with `brew install fnm` on macOS / Linux. Further install instructions are [on the fnm repository](https://github.com/Schniz/fnm), or alternatively you can use `nvm use` instead.

Navigate to [http://localhost:3000](http://127.0.0.1:3000/) to see the project running.

Run `npm run dev` to tell WebPack to watch for SCSS and JS changes without adding livereload to your browser. The files will recompile automatically, but you'll need to manually [refresh your webpage](http://127.0.0.1:8000/) to see changes take effect.

### GOV UK Frontend CSS, JS and assets

This repo installs the GOV UK frontend styling and JavaScript via NPM. Where custom components are added to this repo, their styles and JavaScript are found in the `static-src` directory.

To add the GOV UK NPM package separately to your project, this can be done using the following instructions:

- Install the `govuk-frontend` package: `npm install govuk-frontend --save`
- Follow [the documentation](https://frontend.design-system.service.gov.uk/get-started/#get-started) on how to get the CSS, JS, fonts and images working

### Custom Components

We've added custom styles and JavaScript for some of the components in this pattern library, as they aren't officially supported by GDS yet.

GOV UK assets are stored in the root folder (under `assets/`) as this is where webpack will look for them when compiling the GOV UK node module SCSS. `govuk.js` is a separate JS file with all the official components JavaScript; it is loaded this way following the [GOV get started advice](https://frontend.design-system.service.gov.uk/get-started/#get-started).

Add any new SCSS or JS files to the `static-src/` directory under `dev_app/`. The `static` folder must remain under `dev_app` as this is where Django will look for static files. Static file loading is only suitable for development purposes - this repository is not suitable as a base for production ready sites.
