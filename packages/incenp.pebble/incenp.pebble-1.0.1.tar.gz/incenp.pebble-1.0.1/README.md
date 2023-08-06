Pebble - Command-line Passman client
====================================

Pebble is a command-line client for the
[Passman](https://github.com/nextcloud/passman) password manager.

It supports read and write access to Passman vaults: it can list,
show, create, modify or delete entries in a vault. It cannot,
however, create or delete the vaults themselves.


Configuration
-------------
Pebble requires a configuration file describing the vault(s) to use. The
configuration file uses the [INI
syntax](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure)
and is expected to be at `$XDG_CONFIG_HOME/pebble/config` by default;
another location may be specified using the `-c` option.

A vault is described in the configuration file by a section like in the
following example:

```
[default]
host: host.example.com
user: alice
password: mypassword
vault: MyVault
```

The file may contain several sections, one for each different vault.
Use the `-s` option to specify the name of the section to use (and thus,
which vault to connect to). By default, a section named `default` will
be used.

Inside a vault section, the `password` field may be omitted, in which
case the password will be asked interactively. Note: This is the
Nextcloud password, *not* the vault’s password! The vault password is
*always* asked interactively.


Use
---
With at least one vault configured, Pebble may then be used through the
`pbl` command and its subcommands. Current available subcommands are:

* `list` to list credentials in the vault;
* `show` to display a credential’s details;
* `new` to add a new credential;
* `edit` to modify a credential;
* `delete` to remove a credential from the vault;
* `export` to dump all credentials to a file;
* `conf` to create or edit the configuration file;
* `refresh` to forcefully refresh the local cache;
* `clear` to empty the local cache.

In addition, calling `pbl` without any subcommand will start an
interactive shell in which subcommands can be invoked successively
without quitting the program.

Calling `pbl` with the `-h` option will display the general help;
calling a given subcommand with the `-h` option will display the help
for that subcommand.

The program will interactively for the vault passphrase when it is
needed to decrypt or encrypt a credential.


Copying
-------
Pebble is distributed under the terms of the GNU General Public License,
version 3 or higher. The full license is included in the [COPYING
file](COPYING) of the source distribution.

Pebble include codes that was originally distributed under a 3-clause
BSD license. The original copyright notice and license can be found in
the header of any file of the source distribution containing such code.


Homepage and repository
-----------------------

The project is located at <https://incenp.org/dvlpt/pebble.html> with
the manual at <https://incenp.org/dvlpt/pebble/index.html>. The source
code is available in a Git repository at
<https://git.incenp.org/damien/pebble>.
