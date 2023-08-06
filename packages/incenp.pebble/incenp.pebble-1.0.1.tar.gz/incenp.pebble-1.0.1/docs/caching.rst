*******
Caching
*******

Pebble keeps a local cache of a vault contents within the
``$XDG_DATA_HOME/pebble`` directory. This cache allows Pebble to be used
locally without a network connection (for read operations only).

When Pebble is invoked, it checks the age of the cache (as indicated by
the cache file’s last modification time). If the cache is older than the
value indicated by the ``max_age`` setting in the :ref:`configuration
file <vault-sections>`, or if the cache file does not exists, Pebble
will then download the vault contents from the server. Otherwise it will
read the contents from the cache.

All later read operations (listing or showing credentials) will be done
using the cache, without any network access.

.. note::

   The cache will never contain decrypted credentials.

Write operations (adding, editing, or deleting a credential), however,
will always be performed by contacting the server directly, the local
cache being updated afterwards. Therefore, such operations cannot be
done while offline.

Independently of the ``max_age`` setting, the cache can be forcefully
refreshed by calling Pebble with the ``-f`` or ``--refresh`` option.
Conversely, the ``--no-refresh`` option may be used to prevent
refreshing the cache even if it is older than the ``max_age`` value
(refresh will still occur if the cache does not actually exist).

The cache can also be forcefully refreshed or cleared using the
``refresh`` or ``clear`` commands, respectively.

Local caching for a vault can be completely disabled by setting the
``nocache`` key to ``true`` in the :ref:`configuration file
<vault-sections>`. In that case, the vault contents will only be kept in
memory and never written to disk, which implies that the contents will
have to be downloaded from the server upon each invocation.
