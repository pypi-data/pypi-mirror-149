# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gds_template_pack']

package_data = \
{'': ['*'],
 'gds_template_pack': ['templates/gds/accordion/*',
                       'templates/gds/back-link/*',
                       'templates/gds/breadcrumbs/*',
                       'templates/gds/button/*',
                       'templates/gds/character-count/*',
                       'templates/gds/checkboxes/*',
                       'templates/gds/cookie-banner/*',
                       'templates/gds/date-input/*',
                       'templates/gds/details/*',
                       'templates/gds/error-summary/*',
                       'templates/gds/fieldset/*',
                       'templates/gds/file-upload/*',
                       'templates/gds/footer/*',
                       'templates/gds/header/*',
                       'templates/gds/inset-text/*',
                       'templates/gds/notification-banner/*',
                       'templates/gds/panel/*',
                       'templates/gds/phase-banner/*',
                       'templates/gds/radios/*',
                       'templates/gds/select/*',
                       'templates/gds/skip-link/*',
                       'templates/gds/summary-list/*',
                       'templates/gds/table/*',
                       'templates/gds/tabs/*',
                       'templates/gds/tag/*',
                       'templates/gds/text-input/*',
                       'templates/gds/textarea/*',
                       'templates/gds/warning-text/*']}

setup_kwargs = {
    'name': 'gds-template-pack',
    'version': '0.1.1',
    'description': 'A GOV.UK design system template pack for Django Pattern Library.',
    'long_description': '# GDS template pack\n\nThis is a [django-pattern-library](https://github.com/torchbox/django-pattern-library) template pack for the \n[GOV.UK design system](https://design-system.service.gov.uk/components/).\n\n## Quickstart\n\nThis is a minimal how-to for installation and usage. \n\nInstall using your package manager of choice. e.g. with pip:\n\n```\npip install gds-template-pack\n```\n\nAdd to installed apps and add a section to the [django-pattern-library](https://github.com/torchbox/django-pattern-library) settings:\n\n```python\n# settings.py\n\nINSTALLED_APPS = [\n    # ...\n    "pattern_library",\n    "gds_template_pack",\n]\n\n# django-pattern-library\nPATTERN_LIBRARY = {\n    "SECTIONS": (\n        ("gds", ("gds",)),\n        # ...\n    ),\n    # ...\n}\n```\n\n### Usage\n\nOnce installed and configured, you can reference the various templates as you would do with any Django app. e.g.\nto use the back-link component: `{% include "gds/back-link/back-link.html" with link_url="https://example.com" link_text="Back" %})`\n\n## Development\n\nYou\'ll need Python 3.8 or above and [Poetry](https://python-poetry.org/docs/#installation) installed.\n\n## Setup\n\nInstall the Python dependencies using Poetry:\n\n```sh\npoetry install\n```\n\nBy default, this will create a virtual environment in `./.venv/` and install the dependencies there.\nIf this doesn\'t happen, check your settings against [the documentation](https://python-poetry.org/docs/configuration/#virtualenvscreate).\n\nThen start the Django development server and browse the template pack at [http://localhost:8000/](http://127.0.0.1:8000/):\n\n```\npoetry run dev_app/manage.py runserver 8000\n```\n\n## Frontend Development\n\nTo set up the frontend development environment, first run the above commands to start the django server. Then, run the following commands in a separate terminal window.\n\n```sh\nfnm use\nnpm install\nnpm run start\n```\n\nIf you haven\'t installed `fnm` yet, you can install it with `brew install fnm` on macOS / Linux. Further install instructions are [on the fnm repository](https://github.com/Schniz/fnm), or alternatively you can use `nvm use` instead.\n\nNavigate to [http://localhost:3000](http://127.0.0.1:3000/) to see the project running.\n\nRun `npm run dev` to tell WebPack to watch for SCSS and JS changes without adding livereload to your browser. The files will recompile automatically, but you\'ll need to manually [refresh your webpage](http://127.0.0.1:8000/) to see changes take effect.\n\n### GOV UK Frontend CSS, JS and assets\n\nThis repo installs the GOV UK frontend styling and JavaScript via NPM. Where custom components are added to this repo, their styles and JavaScript are found in the `static-src` directory.\n\nTo add the GOV UK NPM package separately to your project, this can be done using the following instructions:\n\n- Install the `govuk-frontend` package: `npm install govuk-frontend --save`\n- Follow [the documentation](https://frontend.design-system.service.gov.uk/get-started/#get-started) on how to get the CSS, JS, fonts and images working\n\n### Custom Components\n\nWe\'ve added custom styles and JavaScript for some of the components in this pattern library, as they aren\'t officially supported by GDS yet.\n\nGOV UK assets are stored in the root folder (under `assets/`) as this is where webpack will look for them when compiling the GOV UK node module SCSS. `govuk.js` is a separate JS file with all the official components JavaScript; it is loaded this way following the [GOV get started advice](https://frontend.design-system.service.gov.uk/get-started/#get-started).\n\nAdd any new SCSS or JS files to the `static-src/` directory under `dev_app/`. The `static` folder must remain under `dev_app` as this is where Django will look for static files. Static file loading is only suitable for development purposes - this repository is not suitable as a base for production ready sites.\n',
    'author': 'Ben Dickinson',
    'author_email': 'ben.dickinson@torchbox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
