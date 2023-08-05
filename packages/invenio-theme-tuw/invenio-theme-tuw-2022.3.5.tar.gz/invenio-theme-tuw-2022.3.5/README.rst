..
    Copyright (C) 2020 - 2021 TU Wien.

    Invenio-Theme-TUW is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

===================
 Invenio-Theme-TUW
===================

This module provides templates and assets to bring a TU Wien look and feel to InvenioRDM.


Installation
------------

After installing Invenio-Theme-TUW via `pip`, Invenio's assets have to be updated:

.. code-block:: console

   $ pip install invenio-theme-tuw
   $ invenio-cli assets update

Also, theming-related configuration items (e.g. `THEME_LOGO`) have to be removed from `invenio.cfg` to prevent them
from overriding the values set in `Invenio-Theme-TUW`.


Components
----------

* `views.py`: provides a `Blueprint` that registers both the `static/` and `templates/` folders to be usable by Invenio
* `webpack.py`: registers the front-end assets (in the `assets/` folder) to webpack
* `config.py`: overrides several configuration items related to theming Invenio

