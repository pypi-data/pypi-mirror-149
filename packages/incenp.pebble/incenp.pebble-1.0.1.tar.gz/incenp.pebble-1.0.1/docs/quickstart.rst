***************
Getting Started
***************

Prerequisites
=============

You need to have Pebble :doc:`installed <install>` with the ``pbl``
program available from the command line.

You also need an account on a Nextcloud instance with the Passman
application installed, and at least one Passman vault created.


Creating a configuration file
=============================

Pebble requires a configuration file describing the vault(s) to use and
cannot function properly without one. By default, Pebble will look for a
file named ``config`` under the directory ``$XDG_CONFIG_HOME/pebble``.

A simple configuration file may look like the following:

.. code-block:: ini

    [default]
    host: cloud.example.org
    user: alice
    password: XXXXXX
    vault: MyVault

where ``cloud.example.org`` is the Nextcloud or Owncloud server,
``alice`` is the username of an account on that server, ``XXXXXX`` the
corresponding password, and ``MyVault`` the name of a Passman’s vault.


.. _assisted-config:

Assisted configuration
======================

Starting from version 0.4.3, Pebble can create a minimal configuration
on its own. If no configuration file exists, the program will
interactively ask for the server’s hostname and the account’s login and
password:

.. code-block:: console

   $ pbl
   Hostname: cloud.example.org
   Username: alice
   Password: XXXXXX

If :ref:`keyring support <keyring-support>` is available, Pebble will
try to get the password from the user’s keyring before asking the user
for it.

If there are several vaults associated with the account, you will in
addition be presented with a list of those vaults and asked to choose
the one to use:

.. code-block:: console

   Vault (MyVault, MyOtherVault): MyVault


Listing, searching and viewing credentials
==========================================

Use the ``list`` command to print the labels for all credentials
stored in the vault:

.. code-block:: console

   $ pbl list
   example.com
   social.example.org
   bank.example

Called with one or more parameters, the command will only print
credentials whose label matches one of the specified pattern(s):

.. code-block:: console

   $ pbl list bank
   bank.example

Add the ``-i`` option to also print the credential’s unique identifier.
This identifier will be needed to edit or delete the credential.

.. code-block:: console

   $ pbl list -i
   29:example.com
   30:social.example.org
   31:bank.example

To print the actual contents of a credential, use the ``show`` command.
The command will either print all available credentials (if called
without any argument), all the credentials matching the specified
pattern(s), or the one credential with the unique identifier specified
with the ``-i`` option.

You will be asked for the vault’s passphrase to decrypt the encrypted
fields.

.. code-block:: console

   $ pbl show bank
   Passphrase for vault MyVault on alice@cloud.example.org:
   +---- bank.example (31) -----
   | URL: https://bank.example/
   | Email: alice@example.org
   | Password: 123456
   +----


Adding, editing, and deleting credentials
=========================================

Use the ``new`` command to create a new credential and add it to the
vault. The command will fire your favorite editor (as specified in the
``$EDITOR`` environment variable) in which you will be able to set the
contents of the credentials to add. Once you are done, save your
modifications and quit the editor.

To edit an existing credential, use the ``edit`` command with a single
argument representing the unique identifier of the credential to edit
(as displayed by ``list -i``). Again, your editor will be started and
loaded with a textual representation of the credential for you to edit.
The modified credential is sent to the server when you quit the editor
after saving your modifications.

When you are in the editor, if you wish to cancel adding a new
credential or modifying an existing credential, simply quit the editor
without saving anything.

To delete a credential, use the ``del`` command with a single argument
representing the unique identifier of the credential to delete.
