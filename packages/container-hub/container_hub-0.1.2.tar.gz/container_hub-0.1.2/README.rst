=============
container-hub
=============


.. image:: https://img.shields.io/pypi/v/container-hub.svg
        :target: https://pypi.python.org/pypi/container-hub

.. image:: https://github.com/nens/container-hub/workflows/Python%20application/badge.svg?branch=master
     :target: https://github.com/nens/container-hub/actions?query=branch%3Amaster
.. image:: https://pyup.io/repos/github/nens/container-hub/shield.svg
     :target: https://pyup.io/repos/github/nens/container-hub/
     :alt: Updates


Container Hub
-------------

Spiritual successor of the machine manager. Main purpose is starting
and stopping threedi simulation containers.


Usage
-----

The container hub solely exposes two functions, ``up()`` and ``down()`` in backend classes. 
A backend class can be imported via the `get_backend`` helper function

    from container_hub import get_backend
    backend = get_backend(settings) # settings is either simple-settings/Django settings or similar object.

Based on provided settings this gives you a carrier backend,
either from the ``container_hub.carriers.marathon.backend`` or the
``container_hub.carriers.docker.backend``.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
