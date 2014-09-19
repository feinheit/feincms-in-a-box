.. _setup:

=====
Setup
=====

After following all the steps outlined in :ref:`prerequisites`, you're now
ready to generate the first project. Run the following command inside a
Terminal of your choice::

    cookiecutter https://github.com/feinheit/cookiecutter-box

You'll be asked a few questions:

- ``nice_name``: Some nice, descriptive name. This variable will be used to
  fill in the initial ``<title>``, among other things.
- ``project_name`` (Defaults to ``box``): The name of the main Python module.
  If you have no differing preferences, just keep ``box``.
- ``domain``: The final domain for this project. This value is also slugified
  and used as default database and repository name, so choose well.
- ``server``: The server this project will be deployed to. Currently
  cookiecutter-box has many assumptions about server layout, deployment will
  probably not work out-of-the-box if you have a different setup (which you
  will most probably have).

Next, ``fab setup_local`` will be executed automatically. The setup step should
complete successfully, if it does not please report it as a bug!
