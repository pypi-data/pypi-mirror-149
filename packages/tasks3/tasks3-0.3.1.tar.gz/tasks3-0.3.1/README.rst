======
tasks3
======


.. image:: https://img.shields.io/pypi/v/tasks3.svg
        :target: https://pypi.python.org/pypi/tasks3

.. image:: https://github.com/hXtreme/tasks3/actions/workflows/tox-test.yml/badge.svg
        :target: https://github.com/hXtreme/tasks3/actions/workflows/tox-test.yml

.. image:: https://readthedocs.org/projects/tasks3/badge/?version=latest
        :target: https://tasks3.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/hXtreme/tasks3/shield.svg
     :target: https://pyup.io/repos/github/hXtreme/tasks3/
     :alt: Updates



A commandline tool to create and manage tasks and todos.


* Free software: GNU General Public License v3
* Documentation: https://tasks3.readthedocs.io.


Features
--------

* Easily create tasks from the commandline and deledate them to folders.

Create a task in a specific folder with default settings.

.. code-block:: bash

        tasks3 task add --title "Think of a cool name" \
            --folder "~/Documents/story" \
            --yes
        Added Task:
        [e1c100] Think of a cool name (⏰⏰    ) (🚨🚨  )
          [path: ~/Documents/story]

Create a task in a current folder with custom settings and description.

.. code-block:: bash

        tasks3 task add --title "Try new model" \
            --urgency 4 --importance 3 \
            --description "Try:\n - model with 3 layers.\n - model with 4 layers." \
            --yes
        Added Task:
        [a0a5f4] Try new model (⏰⏰⏰⏰) (🚨🚨🚨 )
            Try:
             - model with 3 layers.
             - model with 4 layers.

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
