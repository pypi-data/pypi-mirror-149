Revision History
-----------------

20.4.0 (2022-05-02)
^^^^^^^^^^^^^^^^^^^

* Changes to match main core CryptoSys PKI DLL module version 20.4.

20.3.0 (2022-01-05)
^^^^^^^^^^^^^^^^^^^

* Changes to match main core CryptoSys PKI DLL module version 20.3.

20.0.0 (2020-10-19)
^^^^^^^^^^^^^^^^^^^

* Changes to match main core CryptoSys PKI DLL module version 20.0.

12.4.0 (2020-05-13)
^^^^^^^^^^^^^^^^^^^

* Changes to match main core CryptoSys PKI DLL module version 12.4.

12.3.0 (2020-03-09)
^^^^^^^^^^^^^^^^^^^

* Changes to match main core CryptoSys PKI DLL module version 12.3.

12.2.0 (2019-12-27)
^^^^^^^^^^^^^^^^^^^

* Updated for Python 3.
* Changes to match main core module version 12.2.
* Added new methods ``Cms.*_bytes()`` to handle byte arrays specifically.
* The existing ``Cms.*_string()`` methods now handle full UTF-8-encoded strings.
* Removed ``Cnv.utf8_to_latin1()`` and ``Cnv.utf8_from_latin1()`` - not relevant with Python 3.
* Added ``Hash.hex_from_string()`` and ``Hmac.hex_from_string()`` methods to handle UTF-8 string types.


12.1.0 (2018-12-16)
^^^^^^^^^^^^^^^^^^^

* Changes to match main core module versions 12.0 and 12.1.
* Added support for RSA-PSS in RSA signatures, CMS signed-data objects and X.509 certificates.
* Added support for RSA-OAEP in RSA encryption and CMS enveloped-data objects.
* Added support for ECDSA in X.509 certificates.
* Added support for ZLIB compression.
* Added support for AES-GCM authenticated encryption.
* Added functions to read certificate strings from P7 chain files and PFX files.
* Added option for quicker single pass in ``Wipe.file()``.
* Changed parameter in ``Cms.make_sigdata_*()`` functions from ``Cms.HashAlg`` type to ``Cms.SigAlg``.


11.3.0 (2017-10-31)
^^^^^^^^^^^^^^^^^^^

* Changes to match main core module (11.3).

11.2.0 (2017-08-11)
^^^^^^^^^^^^^^^^^^^

* Synchronized cryptosyspki.py version number with main core module (11.2).
* Substantial changes to inline documentation.
* Renamed ``Rng.bytes`` to ``Rng.bytestring`` to avoid clashes with Python built-in function.
* Changed optional parameters in ``X509.cert_path_is_valid()`` and ``X509.get_cert_count_from_p7()``.


0.1.1 (2016-08-27)
^^^^^^^^^^^^^^^^^^

* Minor changes.


0.1.0 (2016-05-25)
^^^^^^^^^^^^^^^^^^

* First release of cryptosyspki.py v0.1.0.
