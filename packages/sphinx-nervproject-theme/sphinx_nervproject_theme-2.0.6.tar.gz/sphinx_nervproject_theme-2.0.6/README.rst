Sphinx NervProject Theme
========================

A modern responsive theme for python's `Sphinx <http://www.sphinx-doc.org>`_ documentation generator based on
sphinx_press_theme and ablog.

This theme is based on `VuePress <https://vuepress.vuejs.org/>`_.
It uses `Vue.js <https://vuejs.org/>`_ and LessCSS managed by
`webpack <https://webpack.js.org>`_ through `vue-cli <https://cli.vuejs.org/>`_.


Usage
~~~~~

On Sphinx project's `conf.py`: set the theme name to `nervproject`.

.. code:: python

   html_theme = "nervproject"

See details on `Sphinx theming docs <http://www.sphinx-doc.org/en/master/theming.html#using-a-theme>`_.

Development
~~~~~~~~~~~

To rebuild web assets:

.. code:: bash

   npm run build

Install theme locally with `pip install -e .`.

`docs` folder contains theme's own documentantion.

.. code:: bash

   cd docs
   make clean; make html

Compatibility
~~~~~~~~~~~~~

This theme needs CSS vars enabled in the browser, so
it doesn't work on IE. Four color variations are
available :

- light low contrast (default) ;
- light high contrast ;
- dark low contrast ;
- dark high contrast.

The good one is used based on prefers-contrast and
prefers-color-scheme media queries. This is automatically
done by a compatible browser. If not, the default theme
is used. Some browsers need manual configuration like
Chromium on Linux (a flag to enable for all websites).

Example
~~~~~~~

See the `Nerv Project's web site <https://www.nerv-project.eu>`_
