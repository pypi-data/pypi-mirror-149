#! python3
# -*- coding: utf-8 -*-

"""A Python interface to CryptoSys PKI <https://www.cryptosys.net/pki/>."""

# cryptosyspki.py
# $Date: 2022-05-02 06:01:00 $

# ************************** LICENSE *****************************************
# Copyright (C) 2016-22 David Ireland, DI Management Services Pty Limited.
# <www.di-mgt.com.au> <www.cryptosys.net>
# This code is provided 'as-is' without any express or implied warranty.
# Free license is hereby granted to use this code as part of an application
# provided this license notice is left intact. You are *not* licensed to
# share any of this code in any form of mass distribution, including, but not
# limited to, reposting on other web sites or in any source code repository.
# ****************************************************************************

# Requires `CryptoSys PKI` to be installed on your system,
# available from <https://www.cryptosys.net/pki/>.


from ctypes import windll, create_string_buffer, c_char_p, c_void_p, c_int

__version__ = "20.4.0.0000"
# History:
# [20.4.0] Updated to match core library version 20.4.
# [20.3.0] Updated to match core library version 20.3. Added "pki." prefix for imports.
# [20.1.0] Updated to match core library version 20.1.
# [20.0.0] Updated to match core library version 20.0.
# [12.4.0] Updated to match core lbrary version 12.4.
# [12.3.0] Updated to match core lbrary version 12.3.
# [12.2.0] Updated to match core library version 12.2 and converted to Python 3.
# [12.1.0] Updated to match core library version 12.1.
# [11.3.0] Updated to match core library version 11.3.
# [11.2.0] Changed Rng.bytes() to Rng.bytestring(). Substantial update to documentation.
# [0.1.2] Fixed utf8_check_to_string() so it returns "KeyError" instead of raising an exception
# [0.1.1] Added sphinx-compatible comments to public constants


# OUR EXPORTED CLASSES
__all__ = (
    'PKIError',
    'Asn1', 'Cipher', 'Cms', 'Compr', 'Cnv', 'Ecc', 'Gen', 'Hash', 'Hmac', 'Ocsp',
    'Pbe', 'Pem', 'Pfx', 'Pwd', 'Rng', 'Rsa', 'Sig', 'Smime', 'Wipe', 'X509'
)

# Our global DLL object for CryptoSys PKI
_dipki = windll.diCrPKI

# Global constants
_INTMAX = 2147483647
_INTMIN = -2147483648


def _isanint(v):
    try: v = int(v)
    except: pass
    return isinstance(v, int)


class PKIError(Exception):
    """Raised when a call to a core PKI library function returns an error, or some obviously wrong parameter is detected."""

    def __init__(self, value):
        """."""
        self.value = value

    def __str__(self):
        """Behave differently if value is an integer or not."""
        if (_isanint(self.value)):
            n = int(self.value)
            s1 = "ERROR CODE %d: %s" % (n, Gen.error_lookup(n))
        else:
            s1 = "ERROR: %s" % (self.value)
        se = Gen.last_error()
        return "%s%s" % (s1, ": " + se if se else "")


class Asn1:
    """Utilities to analyze ASN.1 files."""

    class Opts():
        """Bitwise flags for text_dump()."""
        NOCOMMENTS = 0x100000  #: Hide the comments
        ADDLEVELS  = 0x800000  #: Show level numbers

    @staticmethod
    def type(asn1file):
        """Describe the type of ASN.1 data.

        Args:
            asn1file (str): Filename of ASN.1 formatted data file to be analyzed (or a string containing its base64 or PEM representation)

        Returns:
            string: String containing the name of the type of ASN.1 data or the empty string if not found. Possible return values::

                "EC PRIVATE KEY"
                "OCSP REQUEST"
                "OCSP RESPONSE"
                "PKCS1 RSA PRIVATE KEY"
                "PKCS1 RSA PUBLIC KEY"
                "PKCS10 CERTIFICATE REQUEST"
                "PKCS12 PFX"
                "PKCS7 CERTIFICATE CHAIN"
                "PKCS7/CMS COMPRESSED DATA"
                "PKCS7/CMS DATA"
                "PKCS7/CMS ENVELOPED DATA"
                "PKCS7/CMS SIGNED DATA"
                "PKCS8 ENCRYPTED PRIVATE KEY"
                "PKCS8 PRIVATE KEY INFO"
                "PUBLIC KEY INFO"
                "X509 CERTIFICATE"
                "X509 CRL"
        """
        nc = _dipki.ASN1_Type(None, 0, asn1file.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ASN1_Type(buf, nc, asn1file.encode(), 0)
        return buf.value.decode()

    @staticmethod
    def text_dump(outputfile, asn1file, opts=0):
        """Dump details of an ASN.1 formatted data file to a text file.

         Args:
             outputfile (str): Filename of text file to be created
             asn1file (str): Filename of ASN.1 formatted data file to be analyzed (or a string containing its base64 representation)
             opts (Asn1.Opts): Option flags.

         Returns:
             int: Zero if successful.
         """
        n = _dipki.ASN1_TextDump(outputfile.encode(), asn1file.encode(), opts)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def text_dump_tostring(asn1file, opts=0):
        """Dump details of an ASN.1 formatted data file to a string.

        Args:
            asn1file (str): Filename of ASN.1 formatted data file to be analyzed (or a string containing its base64 or PEM representation)
            opts (Asn1.Opts): Option flags.

        Returns:
            string: String containing ASN.1 formatted data.
        """
        nc = _dipki.ASN1_TextDumpToString(None, 0, asn1file.encode(), b"", opts)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ASN1_TextDumpToString(buf, nc, asn1file.encode(), b"", opts)
        return buf.value.decode()


class Cipher:
    """Generic block cipher functions."""
    # CONSTANTS
    class Alg:
        """Block cipher algorithms."""
        TDEA   = 0x10  #: Triple DES (3DES, des-ede3)
        AES128 = 0x20  #: AES-128
        AES192 = 0x30  #: AES-192
        AES256 = 0x40  #: AES-256

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class Mode:
        """Block cipher modes."""
        ECB = 0      #: Electronic Code Book mode (default)
        CBC = 0x100  #: Cipher Block Chaining mode
        OFB = 0x200  #: Output Feedback mode
        CFB = 0x300  #: Cipher Feedback mode
        CTR = 0x400  #: Counter mode

    class Pad:
        """Block cipher padding options."""
        DEFAULT = 0             #: Use default padding
        NOPAD        = 0x10000  #: No padding is added
        PKCS5        = 0x20000  #: Padding scheme in PKCS#5/#7
        ONEANDZEROES = 0x30000  #: Pad with 0x80 followed by as many zero bytes necessary to fill the block
        ANSIX923     = 0x40000  #: Padding scheme in ANSI X9.23
        W3C          = 0x50000  #: Padding scheme in W3C XMLENC

    class AeadAlg:
        """Authenticated encryption algorithm."""
        AES_128_GCM = 0x520  #: Use the AEAD_AES_128_GCM authenticated encryption algorithm from RFC 5116.
        AES_192_GCM = 0x530  #: Use the AES-192-GCM authenticated encryption algorithm in the same manner as RFC 5116.
        AES_256_GCM = 0x540  #: Use the AEAD_AES_256_GCM authenticated encryption algorithm from RFC 5116.

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class Opts:
        """Advanced options."""
        DEFAULT = 0  #: Use default options
        PREFIXIV = 0x1000  #: Prepend the IV before the ciphertext in the output (ignored for ECB mode)

    # Internal lookup
    _blocksize = {Alg.TDEA: 8, Alg.AES128: 16, Alg.AES192: 16, Alg.AES256: 16}
    _keysize = {Alg.TDEA: 24, Alg.AES128: 16, Alg.AES192: 24, Alg.AES256: 32}

    @staticmethod
    def blockbytes(alg):
        """Return the block size in bytes for a given cipher algorithm.

        Args:
            alg (Cipher.Alg): Cipher algorithm

        Returns:
            int: Block size in bytes
        """
        return Cipher._blocksize[alg]

    @staticmethod
    def keybytes(alg):
        """Return the key size in bytes for a given cipher algorithm.

        Args:
            alg (Cipher.Alg): Cipher algorithm

        Returns:
            int: Key size in bytes
        """
        return Cipher._keysize[alg]

    @staticmethod
    def encrypt(data, key, iv=None, algmodepad='', alg=None, mode=Mode.ECB, pad=Pad.DEFAULT, opts=Opts.DEFAULT):
        """Encrypt data.

        Args:
            data (bytes): Input data to be encrypted
            key (bytes): Key of exact length for block cipher algorithm
            iv (bytes): Initialization Vector (IV) of exactly the block size (see :py:func:`Cipher.blockbytes`) or ``None`` for ECB mode
            algmodepad (str): String containing the block cipher algorithm, mode and padding, e.g. ``"Aes128/CBC/OneAndZeroes"``
            alg (Cipher.Alg): Cipher algorithm. Ignored if ``algmodepad`` is set, otherwise required.
            mode (Cipher.Mode): Cipher mode. Ignored if ``algmodepad`` is set.
            pad (Cipher.Pad): Padding method to use. Ignored if ``algmodepad`` is set.
            opts (Cipher.Opts): Advanced options. Use Cipher.Opts.PREFIXIV to prepend the IV to the output.

        Returns:
            bytes: Ciphertext or empty array on error.
        """
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = alg | mode | pad
        else:
            noptions = 0
        noptions |= opts
        ivlen = 0
        if iv is None:
            iv = b''
        else:
            ivlen = len(iv)
        n = _dipki.CIPHER_EncryptBytes(None, 0, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, algmodepad.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_EncryptBytes(buf, n, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, algmodepad.encode(), noptions)
        return bytes(buf.raw)

    @staticmethod
    def decrypt(data, key, iv=None, algmodepad='', alg=None, mode=Mode.ECB, pad=Pad.DEFAULT, opts=Opts.DEFAULT):
        """Decrypt data.

        Args:
            data (bytes): Input data to be decrypted
            key (bytes): Key of exact length for block cipher algorithm
            iv (bytes): Initialization Vector (IV) of exactly the block size (see :py:func:`Cipher.blockbytes`) or ``None`` for ECB mode
            algmodepad (str): String containing the block cipher algorithm, mode and padding, e.g. ``"Aes128/CBC/OneAndZeroes"``
            alg (Cipher.Alg): Cipher algorithm. Ignored if ``algmodepad`` is set, otherwise required.
            mode (Cipher.Mode): Cipher mode. Ignored if ``algmodepad`` is set.
            pad (Cipher.Pad): Padding method to use. Ignored if ``algmodepad`` is set.
            opts (Cipher.Opts): Advanced options. Use Cipher.Opts.PREFIXIV to expect the IV to be prepended at the start of the input.

        Returns:
            bytes: Plaintext in byte array or empty array on error.
        """
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = alg | mode | pad
        else:
            noptions = 0
        noptions |= opts
        ivlen = 0
        if iv is None:
            iv = b''
        else:
            ivlen = len(iv)
        dlen = len(data)
        buf = create_string_buffer(dlen)
        n = _dipki.CIPHER_DecryptBytes2(buf, dlen, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, algmodepad.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        # Shorten output if necessary
        return bytes(buf.raw)[:n]

    @staticmethod
    def encrypt_hex(datahex, keyhex, ivhex='', algmodepad='', alg=None, mode=Mode.ECB, pad=Pad.DEFAULT, opts=Opts.DEFAULT):
        """Encrypt data hex-encoded data using hex-encoded parameters.

        Args:
            datahex (str): Input data to be encrypted encoded in hexadecimal.
            keyhex (str): Hex-encoded key of exact length for block cipher algorithm.
            ivhex (str): Hex-encoded Initialization Vector (IV) of exactly the block size (see :py:func:`Cipher.blockbytes`) or ``None`` for ECB mode.
            algmodepad (str): String containing the block cipher algorithm, mode and padding, e.g. ``"Aes128/CBC/OneAndZeroes"``.
            alg (Cipher.Alg): Cipher algorithm. Ignored if ``algmodepad`` is set, otherwise required.
            mode (Cipher.Mode): Cipher mode. Ignored if ``algmodepad`` is set.
            pad (Cipher.Pad): Padding method to use. Ignored if ``algmodepad`` is set.
            opts (Cipher.Opts): Advanced options. Use Cipher.Opts.PREFIXIV to prepend the IV to the output.

        Returns:
            str: Hex-encoded ciphertext or empty array on error.
        """
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = alg | mode | pad
        else:
            noptions = 0
        noptions |= opts
        if ivhex is None:
            ivhex = ''
        n = _dipki.CIPHER_EncryptHex(None, 0, datahex.encode(), keyhex.encode(), ivhex.encode(), algmodepad.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n + 1)
        n = _dipki.CIPHER_EncryptHex(buf, n, datahex.encode(), keyhex.encode(), ivhex.encode(), algmodepad.encode(), noptions)
        return (buf.raw.decode())[:n]

    @staticmethod
    def decrypt_hex(datahex, keyhex, ivhex='', algmodepad='', alg=None, mode=Mode.ECB, pad=Pad.DEFAULT, opts=Opts.DEFAULT):
        """Decrypt hex-encoded data using hex-encoded parameters.

        Args:
            datahex (str): Input data to be decrypted encoded in hexadecimal.
            keyhex (str): Hex-encoded key of exact length for block cipher algorithm
            ivhex (str): Hex-encoded Initialization Vector (IV) of exactly the block size (see :py:func:`Cipher.blockbytes`) or ``None`` for ECB mode
            algmodepad (str): String containing the block cipher algorithm, mode and padding, e.g. ``"Aes128/CBC/OneAndZeroes"``
            alg (Cipher.Alg): Cipher algorithm. Ignored if ``algmodepad`` is set, otherwise required.
            mode (Cipher.Mode): Cipher mode. Ignored if ``algmodepad`` is set.
            pad (Cipher.Pad): Padding method to use. Ignored if ``algmodepad`` is set.
            opts (Cipher.Opts): Advanced options. Use Cipher.Opts.PREFIXIV to expect the IV to be prepended at the start of the input.

        Returns:
            str: Hex-encoded plaintext in byte array or empty array on error.
        """
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = alg | mode | pad
            algmodepad = ''
        else:
            noptions = 0
        noptions |= opts
        if ivhex is None:
            ivhex = ''
        n = _dipki.CIPHER_DecryptHex(None, 0, datahex.encode(), keyhex.encode(), ivhex.encode(), algmodepad.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return ''
        buf = create_string_buffer(n + 1)
        n = _dipki.CIPHER_DecryptHex(buf, n, datahex.encode(), keyhex.encode(), ivhex.encode(), algmodepad.encode(), noptions)
        # Shorten output if necessary
        return (buf.raw.decode())[:n]

    @staticmethod
    def encrypt_block(data, key, iv=None, alg=Alg.TDEA, mode=Mode.ECB):
        """Encrypt a block of data. Must be an exact multiple of block length.

        Args:
            data (bytes): Input data to be encrypted
            key (bytes): Key of exact length for block cipher algorithm
            iv (bytes): Initialization Vector (IV) of exactly the block size (see :py:func:`Cipher.blockbytes`) or ``None`` for ECB mode
            alg (Cipher.Alg): Cipher algorithm
            mode (Cipher.Mode): Cipher mode

        Returns:
            bytes: Ciphertext in byte array or empty array on error.
            Output is always the same length as the input.
        """
        noptions = alg | mode | Cipher.Pad.NOPAD
        ivlen = 0
        if iv is None:
            iv = b''
        else:
            ivlen = len(iv)
        # Output is always the same length as the input
        n = len(data)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_EncryptBytes(buf, n, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, None, noptions)
        if (n < 0): raise PKIError(-n)
        return bytearray(buf.raw)

    @staticmethod
    def decrypt_block(data, key, iv=None, alg=Alg.TDEA, mode=Mode.ECB):
        """Decrypt a block of data. Must be an exact multiple of block length.

        Args:
            data (bytes): Input data to be decrypted
            key (bytes): Key of exact length for block cipher algorithm
            iv (bytes): Initialization Vector (IV) of exactly the block size (see :py:func:`Cipher.blockbytes`) or ``None`` for ECB mode
            alg (Cipher.Alg): Cipher algorithm
            mode (Cipher.Mode): Cipher mode

        Returns:
            bytes: Plaintext in byte array or empty array on error.
            Output is always the same length as the input.
        """
        noptions = alg | mode | Cipher.Pad.NOPAD
        ivlen = 0
        if iv is None:
            iv = b''
        else:
            ivlen = len(iv)
        # Output is always the same length as the input
        n = len(data)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_DecryptBytes(buf, n, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, None, noptions)
        if (n < 0): raise PKIError(-n)
        return bytearray(buf.raw)

    @staticmethod
    def file_encrypt(fileout, filein, key, iv, algmodepad='', alg=None, mode=Mode.ECB, pad=Pad.DEFAULT, opts=Opts.DEFAULT):
        """Encrypt a file.

        Args:
            fileout (str): Name of output file to be created or overwritten
            filein (str): Name of input file
            key (bytes): Key of of exact length for block cipher algorithm
            iv (bytes): Initialization Vector (IV) of exactly the block size (see :py:func:`Cipher.blockbytes`) or ``None`` for ECB mode
            algmodepad (str): String containing the block cipher algorithm, mode and padding, e.g. ``"Aes128/CBC/OneAndZeroes"``
            alg (Cipher.Alg): Cipher algorithm. Ignored if ``algmodepad`` is set, otherwise required.
            mode (Cipher.Mode): Cipher mode. Ignored if ``algmodepad`` is set.
            pad (Cipher.Pad): Padding method to use. Ignored if ``algmodepad`` is set.
            opts (Cipher.Opts): Advanced options

        Returns:
            int: 0 if successful.

        Note:
            ``fileout`` and ``filein`` must *not* be the same.
        """
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = alg | mode | pad
        else:
            noptions = 0
        if (opts != 0):
            noptions |= opts
        ivlen = 0
        if iv is None:
            iv = b''
        else:
            ivlen = len(iv)
        n = _dipki.CIPHER_FileEncrypt(fileout.encode(), filein.encode(), bytes(key), len(key), bytes(iv), ivlen, algmodepad.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def file_decrypt(fileout, filein, key, iv, algmodepad=None, alg=None, mode=Mode.ECB, pad=Pad.DEFAULT, opts=Opts.DEFAULT):
        """Decrypt a file.

        Args:
            fileout (str): Name of output file to be created or overwritten
            filein (str): Name of input file
            key (bytes): Key of of exact length for block cipher algorithm
            iv (bytes): Initialization Vector (IV) of exactly the block size (see :py:func:`Cipher.blockbytes`) or ``None`` for ECB mode
            algmodepad (str): String containing the block cipher algorithm, mode and padding, e.g. ``"Aes128/CBC/OneAndZeroes"``
            alg (Cipher.Alg): Cipher algorithm. Ignored if ``algmodepad`` is set, otherwise required.
            mode (Cipher.Mode): Cipher mode. Ignored if ``algmodepad`` is set.
            pad (Cipher.Pad): Padding method to use. Ignored if ``algmodepad`` is set.
            opts (Cipher.Opts): Advanced options

        Returns:
            int: 0 if successful.

        Note:
            ``fileout`` and ``filein`` must *not* be the same.
        """
        if (algmodepad is None or len(algmodepad) == 0):
            if (alg is None): raise PKIError("Cipher algorithm must be specified")
            noptions = alg | mode | pad
        else:
            noptions = 0
        if (opts != 0):
            noptions |= opts
        ivlen = 0
        if iv is None:
            iv = b''
        else:
            ivlen = len(iv)
        n = _dipki.CIPHER_FileDecrypt(fileout.encode(), filein.encode(), bytes(key), len(key), bytes(iv), ivlen, algmodepad.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def key_wrap(data, kek, alg):
        """Wrap (encrypt) key material with a key-encryption key.

        Args:
            data (bytes): Key material to be wrapped
            kek (bytes): Key encryption key
            alg (Cipher.Alg): Block cipher to use for wrapping

        Returns:
            bytes: Wrapped key.
        """
        n = _dipki.CIPHER_KeyWrap(None, 0, bytes(data), len(data), bytes(kek), len(kek), alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_KeyWrap(buf, n, bytes(data), len(data), bytes(kek), len(kek), alg)
        return bytes(buf.raw)[:n]

    @staticmethod
    def key_unwrap(data, kek, alg):
        """Unwrap (decrypt) key material with a key-encryption key.

        Args:
            data (bytes): Wrapped key
            kek (bytes): Key encryption key
            alg (Cipher.Alg): Block cipher to use for wrapping

        Returns:
            bytes: Unwrapped key material.
        """
        n = _dipki.CIPHER_KeyUnwrap(None, 0, bytes(data), len(data), bytes(kek), len(kek), alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_KeyUnwrap(buf, n, bytes(data), len(data), bytes(kek), len(kek), alg)
        return bytes(buf.raw)[:n]

    @staticmethod
    def pad(data, alg, pad=Pad.PKCS5):
        # HINT: Repeat signature as first line of docstring to get "pad=Pad.PKCS5" not "pad=131072"
        # http://www.sphinx-doc.org/en/stable/ext/autodoc.html#confval-autodoc_docstring_signature
        """pad(data, alg, pad=Pad.PKCS5)
        Pad byte array to correct length for ECB and CBC encryption.

        Args:
            data (bytes): data to be padded
            alg (Cipher.Alg): Block cipher being used
            pad (Cipher.Pad): Padding method to use.

        Returns:
            bytes: padded data in byte array.
        """
        blklen = Cipher._blocksize[alg]
        n = _dipki.PAD_BytesBlock(None, 0, bytes(data), len(data), blklen, pad)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.PAD_BytesBlock(buf, n, bytes(data), len(data), blklen, pad)
        return bytes(buf.raw)[:n]

    @staticmethod
    def pad_hex(datahex, alg, pad=Pad.PKCS5):
        """pad_hex(datahex, alg, pad=Pad.PKCS5)
        Pad hex-encoded string to correct length for ECB and CBC encryption.

        Args:
            datahex (str): hex-encoded data to be padded
            alg (Cipher.Alg): Block cipher being used
            pad (Cipher.Pad): Padding method to use.

        Returns:
            string: padded data in hex-encoded string.
        """
        blklen = Cipher._blocksize[alg]
        n = _dipki.PAD_HexBlock(None, 0, datahex.encode(), blklen, pad)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.PAD_HexBlock(buf, n, datahex.encode(), blklen, pad)
        return (buf.raw.decode())[:n]

    @staticmethod
    def unpad(data, alg, pad=Pad.PKCS5):
        """unpad(data, alg, pad=Pad.PKCS5)
        Remove padding from an encryption block.

        Args:
            data (bytes): padded data
            alg (Cipher.Alg): Block cipher being used
            pad (Cipher.Pad): Padding method to use.

        Returns:
            bytes: Unpadded data in byte array.

        Note:
            Unless ``pad`` is ``NoPad``, the
            unpadded output is *always* shorter than the padded input.
            An error is indicated by returning the *original* data. Check its length.
        """
        blklen = Cipher._blocksize[alg]
        n = len(data)
        buf = create_string_buffer(n)
        n = _dipki.PAD_UnpadBytes(buf, n, bytes(data), len(data), blklen, pad)
        return bytes(buf.raw)[:n]

    @staticmethod
    def unpad_hex(datahex, alg, pad=Pad.PKCS5):
        """unpad_hex(datahex, alg, pad=Pad.PKCS5)
        Remove the padding from a hex-encoded encryption block.

        Args:
            datahex (str): hex-encoded padded data
            alg (Cipher.Alg): Block cipher being used
            pad (Cipher.Pad): Padding method to use.

        Returns:
            string: Unpadded data in hex-encoded string or unchanged data on error.

        Note:
            Unless ``pad`` is ``NoPad``, the
            unpadded output is *always* shorter than the padded input.
            An error is indicated by returning the *original* data. Check its length.
        """
        blklen = Cipher._blocksize[alg]
        n = len(datahex)
        buf = create_string_buffer(n)
        n = _dipki.PAD_UnpadHex(buf, n, datahex.encode(), blklen, pad)
        return (buf.raw.decode())[:n]

    @staticmethod
    def encrypt_aead(data, key, iv, aeadalg, aad=None, opts=Opts.DEFAULT):
        """Encrypt data using the AES-GCM authenticated encryption algorithm.

        Args:
            data (bytes): Input data to be encrypted.
            key (bytes): Key of exact length for algorithm (16, 24 or 32 bytes).
            iv (bytes): Initialization Vector (IV) (aka nonce) exactly 12 bytes long (required).
            aeadalg (Cipher.AeadAlg): Authenticated encryption algorithm.
            aad (bytes): Additional authenticated data (optional).
            opts (Cipher.Opts): Advanced options. Use :py:class:`Cipher.Opts.PREFIXIV` to prepend the 12-byte IV to the output.

        Returns:
            bytes: Ciphertext with tag appended in a byte array.
        """
        noptions = aeadalg | opts
        if iv is None:
            ivlen = 0
            iv = b''
        else:
            ivlen = len(iv)
        if aad is None:
            aadlen = 0
            aad = b''
        else:
            aadlen = len(aad)
        n = _dipki.CIPHER_EncryptAEAD(None, 0, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, bytes(aad), aadlen, noptions)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_EncryptAEAD(buf, n, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, bytes(aad), aadlen, noptions)
        return bytearray(buf.raw)[:n]

    @staticmethod
    def decrypt_aead(data, key, iv, aeadalg, aad=None, opts=Opts.DEFAULT):
        """Decrypt data using the AES-GCM authenticated encryption algorithm.

        Args:
            data (bytes): Input data to be decrypted.
            key (bytes): Key of exact length for algorithm (16, 24 or 32 bytes).
            iv (bytes): Initialization Vector (IV) (aka nonce) exactly 12 bytes long. Set as `None` if prepended to input.
            aeadalg (Cipher.AeadAlg): Authenticated encryption algorithm.
            aad (bytes): Additional authenticated data (optional).
            opts (Cipher.Opts): Advanced options. Use :py:class:`Cipher.Opts.PREFIXIV` to expect the 12-byte IV to be prepended the input.

        Returns:
            bytes: Plaintext in a byte array.
        """
        noptions = aeadalg | opts
        if iv is None:
            ivlen = 0
            iv = b''
        else:
            ivlen = len(iv)
        if aad is None:
            aadlen = 0
            aad = b''
        else:
            aadlen = len(aad)
        n = _dipki.CIPHER_DecryptAEAD(None, 0, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, bytes(aad), aadlen, noptions)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.CIPHER_DecryptAEAD(buf, n, bytes(data), len(data), bytes(key), len(key), bytes(iv), ivlen, bytes(aad), aadlen, noptions)
        return bytearray(buf.raw)[:n]


class Compr:
    """Compression utilities."""

    @staticmethod
    def compress(data):
        """Compress data using zlib compression.

        Args:
             data (bytes): Data to be compressed.

        Returns:
             bytes: Compressed data.
        """
        n = _dipki.COMPR_Compress(None, 0, bytes(data), len(data), 0)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.COMPR_Compress(buf, n, bytes(data), len(data), 0)
        return bytes(buf.raw)[:n]

    @staticmethod
    def uncompress(data):
        """Uncompress data using zlib compression.

        Args:
             data (bytes): Compressed data to be uncompressed.

        Returns:
             bytes: Uncompressed data.
        """
        n = _dipki.COMPR_Uncompress(None, 0, bytes(data), len(data), 0)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.COMPR_Uncompress(buf, n, bytes(data), len(data), 0)
        return bytes(buf.raw)[:n]


class Cms:
    """Create, read and analyze Cryptographic Message Syntax (CMS) objects."""

    class SigDataOpts:
        """Advanced options for CMS signed-data objects."""
        DEFAULT = 0  #: Use default options
        FORMAT_BASE64     = 0x10000  #: Format output in base64 [default=binary]
        EXCLUDE_CERTS      = 0x0100  #: Exclude X.509 certs from output.
        EXCLUDE_DATA       = 0x0200  #: Exclude data from output.
        CERTS_ONLY         = 0x0400  #: Create a "certs-only" PKCS#7 certficate chain.
        NO_OUTER        = 0x2000000  #: Create a "naked" SignedData object with no outerContentInfo as per PKCS#7 v1.6
        ALT_ALGID       = 0x4000000  #: Use alternative (non-standard) signature algorithm identifiers
        BIGFILE         = 0x8000000  #: Use to speed up the processing of large files.
        PSEUDOSIG        = 0x100000  #: Create/sign a "pseudo" SignedData object with dummy placeholder signature.
        MGF1SHA1         = 0x800000  #: RSA-PSS only. Force the MGF hash function to be SHA-1 [default = same as signature hash algorithm]
        SALTLEN_ZERO     = 0x400000  #: RSA-PSS only. Set the salt length to be zero [default = same length as the output of the hash function]
        INCLUDE_ATTRS      = 0x0800  #: Include Signed Attributes content-type and message-digest plus any more added using the ``ADD_`` options.
        ADD_SIGNTIME       = 0x1000  #: Add signing time to signed attributes (requires ``INCLUDE_ATTRS``).
        ADD_SMIMECAP       = 0x2000  #: Add S/MIME capabilities to signed attributes (requires ``INCLUDE_ATTRS``).
        ADD_SIGNINGCERT    = 0x4000  #: Add ESS Signing Certificate Attribute to the signed attributes (requires ``INCLUDE_ATTRS``).
        ADD_ALGPROTECT     = 0x8000  #: add an Algorithm Identifier Protection Attribute to the signed attributes (requires ``INCLUDE_ATTRS``).

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class EnvDataOpts:
        """Advanced options for CMS enveloped-data objects."""
        DEFAULT = 0  #: Use default options
        FORMAT_BASE64     = 0x10000  #: Format output in base64 [default=binary]
        ALT_ALGID       = 0x4000000  #: Use alternative (non-standard) encryption algorithm identifiers
        BIGFILE         = 0x8000000  #: Use to speed up the processing of large files.
        MGF1SHA1         = 0x800000  #: RSA-OAEP only. Force the MGF hash function to be SHA-1 [default = same as signature hash algorithm]

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class ComprDataOpts:
        """Advanced options for CMS compressed-data objects."""
        DEFAULT = 0  #: Use default options
        NO_INFLATE      = 0x1000000  #: Extract the compressed data as is without inflation

    class KeyEncrAlg:
        """Key encryption algorithm  for CMS enveloped-data objects."""
        DEFAULT = 0        #: Default (``rsaEncryption``)
        RSA_PKCS1V1_5 = 0  #: RSAES-PKCS-v1_5 (``rsaEncryption``)
        RSA_OAEP = 0x8000  #: RSAES-OAEP

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class SigAlg:
        """Signature algorithm  for CMS signed-data objects."""
        DEFAULT    = 0x0  #: Use default signature algorithm (``rsa-sha1``/``sha1WithRSAEncryption``)
        RSA_SHA1   = 0x0  #: Sign with sha1WithRSAEncryption (rsa-sha1) [default]
        RSA_SHA224 = 0x6  #: Sign with sha224WithRSAEncryption (rsa-sha224)
        RSA_SHA256 = 0x3  #: Sign with sha256WithRSAEncryption (rsa-sha256) [minimum recommended]
        RSA_SHA384 = 0x4  #: Sign with sha384WithRSAEncryption (rsa-sha384)
        RSA_SHA512 = 0x5  #: Sign with sha512WithRSAEncryption (rsa-sha512) signature algorithm
        RSA_MD5    = 0x1  #: Sign with md5WithRSAEncryption (rsa-md5) signature algorithm [legacy applications only]
        RSA_PSS_SHA1   = 0xB0   #: Sign with RSA-PSS using SHA-1
        RSA_PSS_SHA224 = 0xB6   #: Sign with RSA-PSS using SHA-224
        RSA_PSS_SHA256 = 0xB3   #: Sign with RSA-PSS using SHA-256
        RSA_PSS_SHA384 = 0xB4   #: Sign with RSA-PSS using SHA-384
        RSA_PSS_SHA512 = 0xB5   #: Sign with RSA-PSS using SHA-512
        ECDSA_SHA1   = 0x10  #: Sign with ecdsaWithSHA1
        ECDSA_SHA224 = 0x20  #: Sign with ecdsaWithSHA224
        ECDSA_SHA256 = 0x30  #: Sign with ecdsaWithSHA256
        ECDSA_SHA384 = 0x40  #: Sign with ecdsaWithSHA384
        ECDSA_SHA512 = 0x50  #: Sign with ecdsaWithSHA512
        ED25519      = 0xC0  #: Sign with Ed25519

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    # Local constants
    _BIGFILE = 0x8000000  # Speed up processing of large files (binary-to-binary only)
    _PSEUDOSIG = 0x100000

    @staticmethod
    def make_envdata(outputfile, inputfile, certlist, cipheralg=0, keyencralg=KeyEncrAlg.DEFAULT, hashalg=0, opts=EnvDataOpts.DEFAULT, bigfile=False):
        """Create a CMS enveloped-data object for one or more recipients using their x.509 certificates
        [file --> file].

        Args:
            outputfile (str): Output file to be created
            inputfile (str): Input data file
            certlist (str): List of X509 certificate filename(s), separated by semi-colons
            cipheralg (Cipher.Alg): Content encryption algorithm [default=Triple DES]
            keyencralg (Cms.KeyEncrAlg): Key encryption algorithm [default=rsaEncryption]
            hashalg (Hash.Alg): RSA-OAEP only: Encoding hash algorithm [default=SHA-1]
            opts (Cms.EnvDataOpts): Advanced options. Set as zero for defaults.
            bigfile (bool): Set True for faster handling of a large input file.

        Returns:
            int: Number of successful recipients or a negative error code.
        """
        noptions = opts | cipheralg | keyencralg | hashalg | (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_MakeEnvData(outputfile.encode(), inputfile.encode(), certlist.encode(), None, 0, noptions)
        # Careful: returns +ve number of recipients or a -ve error code
        if (n < 0): raise PKIError(-n)
        return n    # Number of recipients

    @staticmethod
    def make_envdata_from_string(outputfile, inputdata, certlist, cipheralg=0, keyencralg=KeyEncrAlg.DEFAULT, hashalg=0, opts=EnvDataOpts.DEFAULT):
        """Create a CMS enveloped-data object for one or more recipients using their x.509 certificates
        [string --> file].

        Same as :py:func:`Cms.make_envdata` except the input is from a UTF-8 string instead of a file.

        Args:
            outputfile (str): Output file to be created
            inputdata (str): Input data text
            certlist (str): List of X509 certificate filename(s), separated by semi-colons
            cipheralg (Cipher.Alg): Content encryption algorithm [default=Triple DES]
            keyencralg (Cms.KeyEncrAlg): Key encryption algorithm [default=rsaEncryption]
            hashalg (Hash.Alg): RSA-OAEP only: Encoding hash algorithm [default=SHA-1]
            opts (Cms.EnvDataOpts): Option flags. Set as zero for defaults.

        Returns:
            int: Number of successful recipients or negative error code.
        """
        noptions = opts | cipheralg | keyencralg | hashalg
        n = _dipki.CMS_MakeEnvDataFromString(outputfile.encode(), inputdata.encode(), certlist.encode(), None, 0, noptions)
        # Careful: returns +ve number of recipients or a -ve error code
        if (n < 0): raise PKIError(-n)
        return n    # Number of recipients

    @staticmethod
    def make_envdata_from_bytes(outputfile, inputdata, certlist, cipheralg=0, keyencralg=KeyEncrAlg.DEFAULT, hashalg=0, opts=EnvDataOpts.DEFAULT):
        """Create a CMS enveloped-data object for one or more recipients using their x.509 certificates
        [bytes --> file].

        Same as :py:func:`Cms.make_envdata` except the input is from a byte array instead of a file.

        Args:
            outputfile (str): Output file to be created
            inputdata (bytes): Input data
            certlist (str): List of X509 certificate filename(s), separated by semi-colons
            cipheralg (Cipher.Alg): Content encryption algorithm [default=Triple DES]
            keyencralg (Cms.KeyEncrAlg): Key encryption algorithm [default=rsaEncryption]
            hashalg (Hash.Alg): RSA-OAEP only: Encoding hash algorithm [default=SHA-1]
            opts (Cms.EnvDataOpts): Option flags. Set as zero for defaults.

        Returns:
            int: Number of successful recipients or negative error code.
        """
        noptions = opts | cipheralg | keyencralg | hashalg
        n = _dipki.CMS_MakeEnvDataFromBytes(outputfile.encode(), bytes(inputdata), len(inputdata), certlist.encode(), None, 0, noptions)
        # Careful: returns +ve number of recipients or a -ve error code
        if (n < 0): raise PKIError(-n)
        return n    # Number of recipients

    @staticmethod
    def read_envdata_to_file(outputfile, inputfile, prikeystr, certfile="", bigfile=False):
        """Read and decrypt CMS enveloped-data object using the recipient's private key.
        [file --> file]

        Args:
            outputfile (str): Name of output file to be created
            inputfile (str): File that contains the CMS-enveloped data
            prikeystr (str): Internal representation of private key
            certfile (str): (optional) specifies the filename of the recipient's X.509 certificate
            bigfile (bool): Set True for faster handling of a large input file.

        Returns:
            int: Zero if successful.
        """
        noptions = (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_ReadEnvData(outputfile.encode(), inputfile.encode(), certfile.encode(), prikeystr.encode(), noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def read_envdata_to_string(inputfile, prikeystr, certfile=""):
        """Read and decrypt CMS enveloped-data object using the recipient's private key
        [file --> string] (expects output to be UTF-8-encoded text).

        Args:
            inputfile (str): File that contains the CMS-enveloped data
            prikeystr (str): Internal representation of private key
            certfile (str): (optional) specifies the filename of the recipient's X.509 certificate

        Returns:
            str: Message text.
        """
        nc = _dipki.CMS_ReadEnvDataToString(None, 0, inputfile.encode(), certfile.encode(), prikeystr.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CMS_ReadEnvDataToString(buf, nc, inputfile.encode(), certfile.encode(), prikeystr.encode(), 0)
        return buf.value.decode()

    @staticmethod
    def read_envdata_to_bytes(inputfile, prikeystr, certfile=""):
        """Read and decrypt CMS enveloped-data object using the recipient's private key
        [file --> bytes].

        Args:
            inputfile (str): File that contains the CMS-enveloped data
            prikeystr (str): Internal representation of private key
            certfile (str): (optional) specifies the filename of the recipient's X.509 certificate

        Returns:
            bytes: Message data.
        """
        nc = _dipki.CMS_ReadEnvDataToBytes(None, 0, inputfile.encode(), certfile.encode(), prikeystr.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CMS_ReadEnvDataToBytes(buf, nc, inputfile.encode(), certfile.encode(), prikeystr.encode(), 0)
        return buf.value

    @staticmethod
    def make_sigdata(outputfile, inputfile, certlist, prikeystr, sigalg=SigAlg.DEFAULT, opts=SigDataOpts.DEFAULT, bigfile=False):
        """Create a CMS signed-data object from a data file using user's private key
        [file --> file].

        Args:
            outputfile (str): name of output file to be created
            inputfile (str): name of file containing message data to be signed
            certlist (str): containing the filename of the signer's
                certificate and (optionally) a list of other certificates
                to be included in the output, separated by semi-colons(;)
            prikeystr (str): Internal representation of private key for the sender
            sigalg (Cms.SigAlg): Signature algorithm [default=rsa-sha1]
            opts (Cms.SigDataOpts): Advanced option flags.
            bigfile (bool): Set True for faster handling of a large input file.

        Returns:
            int: Zero if successful.
        """
        noptions = opts | sigalg | (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_MakeSigData(outputfile.encode(), inputfile.encode(), certlist.encode(), prikeystr.encode(), noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_sigdata_from_string(outputfile, inputstr, certlist, prikeystr, sigalg=SigAlg.DEFAULT, opts=SigDataOpts.DEFAULT):
        """Create a CMS signed-data object from a string using user's private key
        [string --> file].

        Args:
            outputfile (str): name of output file to be created
            inputstr (str): string containing message data to be signed
            certlist (str): containing the filename of the signer's
                certificate and (optionally) a list of other certificates
                to be included in the output, separated by semi-colons(;)
            prikeystr (str): Internal representation of private key for the sender
            sigalg (Cms.SigAlg): Signature algorithm [default=rsa-sha1]
            opts (Cms.SigDataOpts): Advanced option flags.

        Returns:
            int: Zero if successful.
        """
        noptions = opts | sigalg
        data = inputstr.encode()
        n = _dipki.CMS_MakeSigDataFromBytes(outputfile.encode(), data, len(data), certlist.encode(), prikeystr.encode(), noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_sigdata_from_bytes(outputfile, inputdata, certlist, prikeystr, sigalg=SigAlg.DEFAULT, opts=SigDataOpts.DEFAULT):
        """Create a CMS signed-data object from data using user's private key
        [bytes --> file].

        Args:
            outputfile (str): name of output file to be created
            inputdata (bytes): message data to be signed
            certlist (str): containing the filename of the signer's
                certificate and (optionally) a list of other certificates
                to be included in the output, separated by semi-colons(;)
            prikeystr (str): Internal representation of private key for the sender
            sigalg (Cms.SigAlg): Signature algorithm [default=rsa-sha1]
            opts (Cms.SigDataOpts): Advanced option flags.

        Returns:
            int: Zero if successful.
        """
        noptions = opts | sigalg
        n = _dipki.CMS_MakeSigDataFromBytes(outputfile.encode(), bytes(inputdata), len(inputdata), certlist.encode(), prikeystr.encode(), noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_sigdata_from_sigvalue(outputfile, sigvalue, data, certlist, sigalg=SigAlg.DEFAULT, opts=SigDataOpts.DEFAULT):
        """Create a CMS object of type SignedData using a pre-computed signature value
        [bytes --> file].

        Args:
            outputfile (str): name of output file to be created
            sigvalue (bytes): signature value
            data (bytes): string containing content data that has been signed
            certlist (str): containing the filename of the signer's
                certificate and (optionally) a list of other certificates
                to be included in the output, separated by semi-colons(;)
            sigalg (Cms.SigAlg): Signature algorithm [default=rsa-sha1]. RSA-PKCS1V1_5 only.
            opts (Cms.SigDataOpts): Advanced option flags.

        Returns:
            int: Zero if successful.

        Remarks:
            Only RSASSA-PKCS1V1_5 is supported. Using RSA-PSS will raise an exception.
        """
        noptions = opts | sigalg
        n = _dipki.CMS_MakeSigDataFromSigValue(outputfile.encode(), bytes(sigvalue), len(sigvalue), bytes(data), len(data), certlist.encode(), noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_sigdata_from_pseudo(outputfile, inputfile, sigvalue, opts=SigDataOpts.DEFAULT):
        """Create a SignedData object from a "pseudo" object.
        Args:
            outputfile (str): name of output file to be created
            inputfile (str): input "pseudo" file with dummy placeholder.
            sigvalue (bytes): Signature value computed by external service.
            opts (Cms.SigDataOpts): Advanced option flags.

        Returns:
            int: Zero if successful.

        Remarks:
            RSASSA-PKCS1V1_5 only.
        """
        noptions = opts | Cms._PSEUDOSIG
        n = _dipki.CMS_MakeSigDataFromSigValue(outputfile.encode(), bytes(sigvalue), len(sigvalue), None, 0, inputfile.encode(), noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_detached_sig(outputfile, hexdigest, certlist, prikeystr, sigalg=SigAlg.DEFAULT, opts=SigDataOpts.DEFAULT):
        """Create a "detached signature" CMS signed-data object from a message digest of the content
        [hexdigest --> file].

        Args:
            outputfile (str): name of output file to be created
            hexdigest (str): string containing message digest in hex format
            certlist (str): containing the filename of the signer's
                certificate and (optionally) a list of other certificates
                to be included in the output, separated by semi-colons(;)
            prikeystr (str): Internal representation of private key for the sender
            sigalg (Cms.SigAlg): Signature algorithm [default=rsa-sha1]
            opts (Cms.SigDataOpts): Advanced option flags.

        Returns:
            int: Zero if successful.
        """
        noptions = opts | sigalg
        n = _dipki.CMS_MakeDetachedSig(outputfile.encode(), hexdigest.encode(), certlist.encode(), prikeystr.encode(), noptions)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def read_sigdata_to_file(outputfile, inputfile, bigfile=False):
        """Read the content from a CMS signed-data object file
        [file --> file].

        Args:
            outputfile (str): file to receive content
            inputfile (str): file containing CMS signed-data object
            bigfile (bool): Set True for faster handling of a large input file.


        Returns:
            int: If successful, a positive number indicating the number of bytes in the content.
        """
        noptions = (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_ReadSigData(outputfile.encode(), inputfile.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        return 0

    @staticmethod
    def read_sigdata_to_string(inputfile):
        """Read the content from a CMS signed-data object file directly into a string
        [file --> string] (expects output to be UTF-8-encoded text).

        Args:
            inputfile (str): file containing CMS signed-data object.

        Returns:
            str: String containing the content.
        """
        nc = _dipki.CMS_ReadSigDataToString(None, 0, inputfile.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CMS_ReadSigDataToString(buf, nc, inputfile.encode(), 0)
        return buf.value.decode()

    @staticmethod
    def read_sigdata_to_bytes(inputfile):
        """Read the content from a CMS signed-data object file into bytes.
        [file --> bytes]

        Args:
            inputfile (str): file containing CMS signed-data object.

        Returns:
            bytes: Content data.
        """
        nc = _dipki.CMS_ReadSigDataToBytes(None, 0, inputfile.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CMS_ReadSigDataToBytes(buf, nc, inputfile.encode(), 0)
        return buf.value

    @staticmethod
    def verify_sigdata(sigdatafile, certfile="", hexdigest="", bigfile=False):
        """Verify the signature and content of a signed-data CMS object file.

        Args:
            sigdatafile (str): file containing CMS signed-data object
            certfile (str): an (optional) X.509 certificate file of the signer
            hexdigest (str): (optional) digest of eContent to be verified (use for "detached-signature" form)
            bigfile (bool): Set True for faster handling of a large input file.

        Returns:
            bool: True if successfully verified or False if signature is invalid.

        Raises:
            PKIError: If file is missing or corrupt, or parameters are bad, etc.
        """
        noptions = (Cms._BIGFILE if bigfile else 0)
        n = _dipki.CMS_VerifySigData(sigdatafile.encode(), certfile.encode(), hexdigest.encode(), noptions)
        # Catch straightforward invalid signature error
        _SIGNATURE_ERROR = -22
        if (n == _SIGNATURE_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc)
        if (n < 0): raise PKIError(-n)
        return True

    @staticmethod
    def query_sigdata(cmsfile, query):
        """Query a CMS signed-data object file for selected information. May return an integer or a string.

        Args:
            cmsfile (str): file containing CMS signed-data object
            query (str): Query string (case insensitive). Valid queries are:

                * ``"version"`` -- signedData version (sdVer) value, e.g. ``1``.
                * ``"eContentType"`` -- ContentType of the EncapsulatedContentInfo, e.g. "data".
                * ``"HASeContent"`` -- ``1`` if eContent is present; ``0`` if not.
                * ``"CountOfCertificates"`` -- Number of certificates included in the data.
                * ``"CountOfSignerInfos"`` -- Number of SignerInfos included in the data.
                * ``"signerInfoVersion"`` -- signerInfo version (siVer) value.
                * ``"digestAlgorithm"`` -- digestAlgorithm, e.g. "sha1".
                * ``"signatureAlgorithm"`` -- signatureAlgorithm, e.g. "rsaEncryption".
                * ``"signatureValue"`` -- Signature value encoded in hex.
                * ``"HASsignedAttributes"`` -- ``1`` if signedAttributes (authenticatedAttributes) are present; ``0`` if not.
                * ``"DigestOfSignedAttrs"`` -- Computed digest over signed attributes, if present, using digestAlgorithm.
                * ``"DigestOfeContent"`` -- Computed digest over eContent, if present, using digestAlgorithm.
                * ``"signingTime"`` -- Date on which the certificate validity period begins in format "2005-12-31 23:30:59".
                * ``"messageDigest"`` -- messageDigest attribute in hexadecimal format, if present.
                * ``"pssParams"`` -- parameters used for RSA-PSS (if applicable).
                * ``"HASsigningCertificate"`` -- ``1`` if an ESS signingCertificate is present; ``0`` if not.
                * ``"signingCertHash"`` -- certHash value of ESS signing certificate, if present, encoded in hex.
                * ``"HASalgorithmProtection"`` -- ``1`` if a cmsAlgorithmProtection attribute is present; ``0`` if not.

                By default, the function queries the first signerInfo in the file.
                To query the Nth signerInfo append ``"/N"`` to the query string,
                e.g. ``"signerInfoVersion/2"`` to find the version number of the second signerInfo in the file.

        Returns:
            Result of query if found or an empty string if not found.

        """
        _QUERY_GETTYPE = 0x100000
        _QUERY_STRING = 2
        # Find what type of result to expect: number or string (or error)
        n = _dipki.CMS_QuerySigData(None, 0, cmsfile.encode(), query.encode(), _QUERY_GETTYPE)
        if (n < 0): raise PKIError(-n)
        if (_QUERY_STRING == n):
            nc = _dipki.CMS_QuerySigData(None, 0, cmsfile.encode(), query.encode(), 0)
            if (nc < 0): raise PKIError(-nc)
            buf = create_string_buffer(nc + 1)
            nc = _dipki.CMS_QuerySigData(buf, nc, cmsfile.encode(), query.encode(), 0)
            return buf.value.decode()
        else:
            n = _dipki.CMS_QuerySigData(None, 0, cmsfile.encode(), query.encode(), 0)
            return n

    @staticmethod
    def query_envdata(cmsfile, query):
        """Query a CMS enveloped-data object file for selected information. May return an integer or a string.

        Args:
            cmsfile (str): file containing CMS enveloped-data object
            query (str): Query string (case insensitive). Valid queries are:

                * ``"version"`` -- envelopedData CMSVersion value, e.g. ``0``.
                * ``"recipientInfoVersion"`` -- recipientInfo version (riVer) value.
                * ``"countOfRecipientInfos"`` -- Number of RecipientInfos included in the data.
                * ``"recipientIssuerName"`` -- Distinguished Name of recipient's certificate issuer.
                * ``"recipientSerialNumber"`` -- serialNumber of recipient's certificate in hex format
                * ``"contentEncryptionAlgorithm"`` -- contentEncryptionAlgorithm, e.g. "des-EDE3-CBC".
                * ``"sizeofEncryptedContent"`` -- Size (in bytes) of the EncryptedContent.
                * ``"encryptedContent"`` -- EncryptedContent encoded in hex.
                * ``"iv"`` -- Initialization vector encoded in hex.
                * ``"keyEncryptionAlgorithm"`` -- keyEncryptionAlgorithm, e.g. "rsaEncryption".
                * ``"keyEncryptionFlags"`` -- Bit flags used for the key encryption algorithm.
                * ``"sizeofEncryptedKey"`` -- Size (in bytes) of the EncryptedKey.
                * ``"encryptedKey"`` -- EncryptedKey value encoded in hex.
                * ``"oaepParams"`` -- Parameters used for RSA-OAEP (if applicable).

                By default, the function queries the first recipientInfo in the file.
                To query the Nth recipientInfo append ``"/N"`` to the query string,
                e.g. ``"recipientInfoVersion/2"`` to find the version number of the second recipientInfo in the file.

        Returns:
            Result of query if found or an empty string if not found.
        """
        _QUERY_GETTYPE = 0x100000
        _QUERY_STRING = 2
        # Find what type of result to expect: number or string (or error)
        n = _dipki.CMS_QueryEnvData(None, 0, cmsfile.encode(), query.encode(), _QUERY_GETTYPE)
        if (n < 0): raise PKIError(-n)
        if (_QUERY_STRING == n):
            nc = _dipki.CMS_QueryEnvData(None, 0, cmsfile.encode(), query.encode(), 0)
            if (nc < 0): raise PKIError(-nc)
            buf = create_string_buffer(nc + 1)
            nc = _dipki.CMS_QueryEnvData(buf, nc, cmsfile.encode(), query.encode(), 0)
            return buf.value.decode()
        else:
            n = _dipki.CMS_QueryEnvData(None, 0, cmsfile.encode(), query.encode(), 0)
            return n

    @staticmethod
    def make_comprdata(outputfile, inputfile):
        """Create a new CMS compressed-data file (.p7z) from an existing input file.
        [binary file --> binary file]

        Args:
            outputfile (str): Output file to be created
            inputfile (str): Input data file

        Returns:
            int: Zero if successful.
        """
        n = _dipki.CMS_MakeComprData(outputfile.encode(), inputfile.encode(), 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def read_comprdata(outputfile, inputfile, opts=ComprDataOpts.DEFAULT):
        """Read and extract the decompressed contents of a CMS compressed-data file
        [binary file --> binary file].

        Args:
            outputfile (str): Output file to be created
            inputfile (str): Input data file
            opts (Cms.ComprDataOpts): Options [default=inflate contents]

        Returns:
            int: If successful the return value is the number of bytes in the output file.
        """
        n = _dipki.CMS_ReadComprData(outputfile.encode(), inputfile.encode(), opts)
        if (n < 0): raise PKIError(-n)
        return n


class Cnv:
    """Character conversion routines."""

    # CONSTANTS
    class EndianNess:
        """Byte order for integer/byte array conversions."""
        BIG_ENDIAN    = 0x0  #: Big-endian order (default)
        LITTLE_ENDIAN = 0x1  #: Little-endian order

    @staticmethod
    def tohex(data):
        """
        Encode binary data as a hexadecimal string.

        Args:
            data (bytes): binary data to be encoded.

        Returns:
            str: Hex-encoded string.
            Letters [A-F] are in uppercase. Use ``s.lower()`` for lowercase.
        Examples:
            >>> Cnv.tohex(b"abc\xe9")
            '616263E9'
            >>> Cnv.tohex(bytearray([0xde, 0xad, 0xbe, 0xef])).lower()
            'deadbeef'
        """
        nbytes = len(data)
        if (nbytes == 0): return ""
        nc = _dipki.CNV_HexStrFromBytes(None, 0, bytes(data), nbytes)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CNV_HexStrFromBytes(buf, nc, bytes(data), nbytes)
        return buf.value.decode()[:nc]

    @staticmethod
    def fromhex(s):
        """Decode a hexadecimal-encoded string into a byte array.

        Args:
            s (str): Hex-encoded string

        Returns:
            bytes: Binary data in byte array.

        Note:
            Whitespace and ASCII punctuation characters in the input are ignored,
            but other non-hex characters, e.g. ``[G-Zg-z]``, will cause an error.

        Examples:
            >>> Cnv.fromhex("61:62:63")
            'abc'

        """
        n = _dipki.CNV_BytesFromHexStr(None, 0, s.encode())
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes()
        buf = create_string_buffer(n)
        n = _dipki.CNV_BytesFromHexStr(buf, n, s.encode())
        return bytes(buf.raw)[:n]

    @staticmethod
    def tobase64(data):
        """Encode binary data as a base64 string.

        Args:
            data (bytes): binary data to be encoded.

        Returns:
            str: Base64-encoded string.

        Example:
            >>> Cnv.tobase64(Cnv.fromhex('fedcba9876543210'))
            '/ty6mHZUMhA='
        """
        nbytes = len(data)
        if (nbytes == 0): return ""
        nc = _dipki.CNV_B64StrFromBytes(None, 0, bytes(data), nbytes)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CNV_B64StrFromBytes(buf, nc, bytes(data), nbytes)
        return buf.value.decode()[:nc]

    @staticmethod
    def frombase64(s):
        """Decode a base64-encoded string into a byte array.

        Args:
            s (str): Base64-encoded data

        Returns:
            bytes: Binary data in byte array.

        Remarks:
            Whitespace characters are ignored,
            but other non-base64 characters will cause an error.
        """
        n = _dipki.CNV_BytesFromB64Str(None, 0, s.encode())
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.CNV_BytesFromB64Str(buf, n, s.encode())
        return bytes(buf.raw)[:n]

    @staticmethod
    def tobase58(data):
        """Encode binary data as a base58 string.

        Uses the "Bitcoin" scheme of base58 encoding
        where the leading character '1' is reserved for representing
        an entire leading zero byte.

        Args:
            data (bytes): binary data

        Returns:
            str: Base58-encoded string.

        Example:
            >>> Cnv.tobase58(Cnv.fromhex("00010966776006953D5567439E5E39F86A0D273BEED61967F6"))
            '16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM'

        """
        nbytes = len(data)
        if (nbytes == 0): return ""
        nc = _dipki.CNV_Base58FromBytes(None, 0, bytes(data), nbytes)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.CNV_Base58FromBytes(buf, nc, bytes(data), nbytes)
        return buf.value.decode()[:nc]

    @staticmethod
    def frombase58(s):
        """Decode a base58-encoded string into a byte array.

        Uses the "Bitcoin" scheme of base58 encoding
        where the leading character '1' is reserved for representing
        an entire leading zero byte.

        Args:
            s (str): Base58-encoded data

        Returns:
            bytes: Binary data in byte array.
        """
        n = _dipki.CNV_Base58ToBytes(None, 0, s.encode())
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.CNV_Base58ToBytes(buf, n, s.encode())
        return bytes(buf.raw)[:n]

    @staticmethod
    def reverse_bytes(data):
        """Reverse the order of a byte array.

        Args:
            data (bytes): Input data to be reversed

        Returns:
            bytes: Byte array in reverse order.

        Examples:
            >>> Cnv.tohex(Cnv.reverse_bytes(Cnv.fromhex("DEADBEEF01")))
            '01EFBEADDE'
        """
        n = len(data)
        buf = create_string_buffer(n)
        _dipki.CNV_ReverseBytes(buf, data, n)
        return bytes(buf.raw)

    @staticmethod
    def num_from_bytes(data, endn=EndianNess.BIG_ENDIAN):
        """num_from_bytes(data, endn=EndianNess.BIG_ENDIAN)
        Convert the leftmost four bytes of an array to a 32-bit integer.

        An array shorter than 4 bytes will be padded on the right with zeros.

        Args:
            data (bytes): Byte array to be converted
            endn (EndianNess): Byte order

        Returns:
            int: Integer value.

        Examples:
            >>> hex(Cnv.num_from_bytes(Cnv.fromhex("DEADBEEF")))
            '0xdeadbeefL'
            >>> hex(Cnv.num_from_bytes(Cnv.fromhex("DEADBEEF"), Cnv.EndianNess.LITTLE_ENDIAN))
            '0xefbeaddeL'
        """
        n = _dipki.CNV_NumFromBytes(data, len(data), endn)
        # Force number to be a positive 32-bit integer
        return n & 0xFFFFFFFF

    @staticmethod
    def num_to_bytes(num, endn=EndianNess.BIG_ENDIAN):
        """num_to_bytes(num, endn=EndianNess.BIG_ENDIAN)
        Convert a 32-bit integer to an array of 4 bytes.

        Args:
            num (int): Integer to be converted
            endn (EndianNess): Byte order

        Returns:
            bytes: Byte array containing representation of integer in given order.
        """
        n = 4
        buf = create_string_buffer(n)
        n = _dipki.CNV_NumToBytes(buf, n, (num & 0xFFFFFFFF), endn)
        return bytes(buf.raw)

    # UTF-8 STUFF...
    @staticmethod
    def utf8_check(data):
        """Check if a byte array or string contains valid UTF-8 characters. Returns integer code.

        Args:
            data (bytes): input byte array to check

        Returns:
            int: Integer code indicating nature of encoded characters:

            * ``0`` -- Not valid UTF-8
            * ``1`` -- Valid UTF-8, all characters are 7-bit ASCII
            * ``2`` -- Valid UTF-8, contains at least one multi-byte character equivalent to 8-bit ANSI
            * ``3`` -- Valid UTF-8, contains at least one multi-byte character that cannot be represented in a single-byte character set
        """
        n = _dipki.CNV_CheckUTF8Bytes(bytes(data), len(data))
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def utf8_check_file(filename):
        """Check if a file contains valid UTF-8 characters. Returns integer code.

        Args:
            filename (str): name of file to check

        Returns:
            int: Integer code indicating nature of encoded characters:

            * ``0`` -- Not valid UTF-8
            * ``1`` -- Valid UTF-8, all characters are 7-bit ASCII
            * ``2`` -- Valid UTF-8, contains at least one multi-byte character equivalent to 8-bit ANSI
            * ``3`` -- Valid UTF-8, contains at least one multi-byte character that cannot be represented in a single-byte character set
        """
        n = _dipki.CNV_CheckUTF8File(filename.encode())
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def utf8_check_to_string(n):
        """Return a string describing an integer code returned by :py:func:`Cnv.utf8_check` and :py:func:`Cnv.utf8_check_file`.

        Examples:
            >>> Cnv.utf8_check_to_string(Cnv.utf8_check("abc".encode()))
            'Valid UTF-8, all characters are 7-bit ASCII'

        """
        d = {
            0: 'Not valid UTF-8',
            1: 'Valid UTF-8, all characters are 7-bit ASCII',
            2: 'Valid UTF-8, contains at least one multi-byte character equivalent to 8-bit ANSI',
            3: 'Valid UTF-8, contains at least one multi-byte character that cannot be represented in a single-byte character set'
        }
        if n not in d: return "KeyError"
        return d[n]

    # Python 3: removed Cnv.utf8_to_latin1 and Cnv.utf8_from_latin1
    # def utf8_to_latin1(b):
    # def utf8_from_latin1(s):


class Ecc:
    """Manage keys for elliptic curve cryptography."""

    class CurveName:
        """Supported curve names."""
        SECP192R1 = "secp192r1"    #: P-192
        SECP224R1 = "secp224r1"    #: P-224
        SECP256R1 = "secp256r1"    #: P-256
        SECP384R1 = "secp384r1"    #: P-384
        SECP521R1 = "secp521r1"    #: P-521
        SECP256K1 = "secp256k1"    #: "Bitcoin" curve
        # Alternative synonyms
        P_192 = "P-192"     #: secp192r1
        P_224 = "P-224"     #: secp224r1
        P_256 = "P-256"     #: secp256r1
        P_384 = "P-384"     #: secp384r1
        P_521 = "P-521"     #: secp521r1
        # Yet more alternatives
        PRIME192V1 = "prime192v1"   #: P-192
        PRIME256V1 = "prime256v1"   #: P-256
        # Safe curves
        X25519 = "X25519"       #: Safe curve for ECDH
        ED25519 = "Ed25519"     #: safe curve for EdDSA
        # Brainpool curves from RFC5639
        BRAINPOOLP256R1 = "brainpoolP256r1" #: ECC Brainpool 256-bit curve
        BRAINPOOLP384R1 = "brainpoolP384r1" #: ECC Brainpool 384-bit curve
        BRAINPOOLP512R1 = "brainpoolP512r1" #: ECC Brainpool 512-bit curve

    class PbeScheme:
        """Password-based encryption scheme to encrypt the private key file."""
        DEFAULT = 0    #: ``pbeWithSHAAnd3-KeyTripleDES-CBC`` from PKCS#12
        PBKDF2_DESEDE3 = 0x1010  #: PBKDF2 using ``des-EDE3-CBC``
        PBKDF2_AES128  = 0x1020  #: PBKDF2 using ``aes128-CBC``
        PBKDF2_AES192  = 0x1030  #: PBKDF2 using ``aes192-CBC``
        PBKDF2_AES256  = 0x1040  #: PBKDF2 using ``aes256-CBC``

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class KeyType:
        """Key type for unencrypted key file.

        Default is ``SubjectPublicKeyInfo`` for an EC public key or ``ECPrivateKey`` for an EC private key.
        """
        DEFAULT = 0  #: Default type: ``SubjectPublicKeyInfo`` for an EC public key or ``ECPrivateKey`` for an EC private key.
        PKCS8 = 0x40000  #: Save private key in PKCS#8 ``PrivateKeyInfo`` format (ignored for a public key).
        PRIVATE_KEY = 0x0  #:
        PUBLIC_KEY = 0x1

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class Format:
        """Format for saved key file."""
        DEFAULT = 0  #: Binary
        BINARY  = 0  #: Binary (default)
        PEM = 0x10000  #: PEM-encoded format

    @staticmethod
    def make_keys(pubkeyfile, prikeyfile, curvename, password, pbescheme=0, params='', fileformat=0):
        """Generate a new EC public/private key pair and save as two key files.

        Args:
            pubkeyfile (str): name of public key file to be created.
            prikeyfile (str): name of encrypted private key file to be created.
            curvename (Ecc.CurveName): name of elliptic curve.
            password (str): password to be used for the encrypted key file.
            pbescheme (Ecc.PbeScheme): Password-based encryption scheme to encrypt private key
                [default = ``pbeWithSHAAnd3-KeyTripleDES-CBC``]
            params (str): Optional parameters.
                A set of attribute "name=value" pairs separated by a semicolon ";" .

                count=<integer>
                    To set the iteration count used in the PBKDF2 method,
                    e.g. ``"count=5000;"`` [default=2048].

                prf=<hmac-name>
                    To change the HMAC algorithm used in the PBKDF2 method,
                    e.g. ``"prf=hmacwithSHA256;"``. Valid values are (case insensitive):

                        * ``hmacwithSHA1`` (default)
                        * ``hmacwithSHA224``
                        * ``hmacwithSHA256``
                        * ``hmacwithSHA384``
                        * ``hmacwithSHA512``

                rngseed=<string>
                    To add some user-supplied entropy for the key generation process,
                    e.g. ``"rngseed=NaCl;"``.

            fileformat (Ecc.Format): Format to save file [default = DER binary]

        Returns:
            int: Zero if successful.

        Example:
            >>> # Make default key pair using P-192 curve
            >>> Ecc.make_keys("mykey.pub", "mykey.p8", Ecc.CurveName.P_192, "password")
            0
            >>> # Make key pair using P-384 with advanced options
            >>> Ecc.make_keys("mypubkey384.pem", "myprikey384.pem", Ecc.CurveName.P_384, "password", Ecc.PbeScheme.PBKDF2_AES128, "count=3999;prf=hmacWithSha256", Ecc.Format.PEM)
            0

        """
        noptions = pbescheme | fileformat
        n = _dipki.ECC_MakeKeys(pubkeyfile.encode(), prikeyfile.encode(), str(curvename).encode(), password.encode(), params.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def read_private_key(keyfileorstr, password=""):
        """Read from a file or string containing an EC private key into an "internal" private key string.

        Args:
            keyfileorstr (str): Name of file or a PEM string containing the key
            password (str): Password for private key, if encrypted.

        Returns:
            str: Ephemeral internal representation of the private key

        Example:
            >>> intprikey = Ecc.read_private_key("mykey.p8", "password")
            >>> Ecc.query_key(intprikey, 'curveName')
            'secp192r1'
        """
        nc = _dipki.ECC_ReadPrivateKey(None, 0, keyfileorstr.encode(), password.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ECC_ReadPrivateKey(buf, nc, keyfileorstr.encode(), password.encode(), 0)
        return (buf.value.decode())[:nc]

    @staticmethod
    def read_public_key(keyfileorstr):
        """Read from a file or string containing an EC public key into an "internal" public key string.

        Args:
            keyfileorstr (str): Name of file or a PEM string containing the key

        Returns:
            str: Ephemeral internal representation of the public key.

        Example:
            >>> intpubkey = Ecc.read_public_key("mykey.pub")
            >>> Ecc.query_key(intpubkey, 'isPrivate')
            0
        """
        nc = _dipki.ECC_ReadPublicKey(None, 0, keyfileorstr.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ECC_ReadPublicKey(buf, nc, keyfileorstr.encode(), 0)
        return buf.value.decode()[:nc]

    @staticmethod
    def read_key_by_curve(keyhex, curvename, ispublic=False):
        """Return an internal key string of an EC key from its hexadecimal representation.

        Args:
            keyhex (str): hexadecimal representation of the key, private or public
            curvename (Ecc.CurveName): name of the elliptic curve
            ispublic (bool): ``True`` if key is a public key, ``False`` if a private key. Required for safe curve keys,
                otherwise ignored.

        Returns:
            str: The key in ephemeral "internal" representation, or the empty string on error

            For NIST/SEC curves, an EC private key ``w`` is represented as ``HEX(w)``
            and a public key ``(x,y)`` in the uncompressed X9.63 form ``04||HEX(x)||HEX(y)``.
            The key type is detected automatically and the ``ispublic`` argument is ignored.

            For the safe curves, X25519 and Ed25519, both private and public keys are expected as the
            hexadecimal representation of a 32-byte value in little-endian format.
            The ``ispublic`` argument *must* be used to must specify whether the key is a private or public key.
        """
        _PRIVATE_KEY = 0x0
        _PUBLIC_KEY = 0x1
        noptions = _PUBLIC_KEY if ispublic else _PRIVATE_KEY
        nc = _dipki.ECC_ReadKeyByCurve(None, 0, keyhex.encode(), str(curvename).encode(), noptions)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ECC_ReadKeyByCurve(buf, nc, keyhex.encode(), str(curvename).encode(), noptions)
        return buf.value.decode()[:nc]

    @staticmethod
    def query_key(intkeystr, query):
        """Query an EC key string for selected information. May return an integer or a string.

        Args:
            intkeystr (str): containing the key as an internal key string
            query (str): Query string (case insensitive). Valid queries are:

                * ``"curveName"`` -- Name of the curve.
                * ``"keyBits"`` -- Number of bits in the key.
                * ``"isPrivate"`` -- ``1`` if key is a private key; ``0`` if not.
                * ``"privateKey"`` -- Value of the private key in hex format.
                * ``"publicKey"`` -- Value of the public key in hex format.

        Returns:
            Result of query if found or an empty string if not found.
        """
        _QUERY_GETTYPE = 0x100000
        _QUERY_STRING = 2
        # Find what type of result to expect: number or string (or error)
        n = _dipki.ECC_QueryKey(None, 0, intkeystr.encode(), query.encode(), _QUERY_GETTYPE)
        if (n < 0): raise PKIError(-n)
        if (_QUERY_STRING == n):
            nc = _dipki.ECC_QueryKey(None, 0, intkeystr.encode(), query.encode(), 0)
            if (nc < 0): raise PKIError(-nc)
            buf = create_string_buffer(nc + 1)
            nc = _dipki.ECC_QueryKey(buf, nc, intkeystr.encode(), query.encode(), 0)
            return buf.value.decode()
        else:
            n = _dipki.ECC_QueryKey(None, 0, intkeystr.encode(), query.encode(), 0)
            return n

    @staticmethod
    def save_key(outputfile, intkeystr, keytype=0, fileformat=0):
        """Save an internal EC key string (public or private) to an unencrypted key file.

        Args:
            outputfile (str): Name of key file to be created
            intkeystr (str): the private or public EC key as an internal key string
            keytype (Ecc.KeyType): Key structure for private key (ignored for public)
            fileformat (Ecc.Format): Format to save file [default = DER binary]

        Returns:
            int: Zero if successful.
        """
        noptions = keytype | fileformat
        n = _dipki.ECC_SaveKey(outputfile.encode(), intkeystr.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def save_enc_key(outputfile, intkeystr, password, pbescheme=0, params='', fileformat=0):
        """Save an internal EC private key string to an encrypted private key file.

        Args:
            outputfile (str): Name of key file to be created
            intkeystr (str): the private EC key as an internal key string
            password (str): Password for private key, if encrypted.
            pbescheme (Ecc.PbeScheme): Encryption scheme to encrypt private key [default = ``pbeWithSHAAnd3-KeyTripleDES-CBC``]
            params (str): Optional parameters.
                A set of attribute name=value pairs separated by a semicolon ``;``.

                count=<integer>:
                    To set the iteration count used in the PBKDF2 method,
                    e.g. ``"count=5000;"`` [default=2048].

                prf=<hmac-name>
                    To change the HMAC algorithm used in the PBKDF2 method,
                    e.g. ``"prf=hmacwithSHA256;"``. Valid values are (case insensitive):

                        * ``hmacwithSHA1`` (default)
                        * ``hmacwithSHA224``
                        * ``hmacwithSHA256``
                        * ``hmacwithSHA384``
                        * ``hmacwithSHA512``

            fileformat (Ecc.Format): Format to save file [default = DER binary]

        Returns:
            int: Zero if successful.
        """
        noptions = pbescheme | fileformat
        n = _dipki.ECC_SaveEncKey(outputfile.encode(), intkeystr.encode(), password.encode(), params.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def publickey_from_private(intkeystr):
        """Return an internal EC public key string from an internal EC private key string.

        Args:
            intkeystr (str): the private key as an internal key string

        Returns:
            str: The public key in ephemeral "internal" representation, or the empty string on error.

        Examples:
            >>> # Specify an EC private key in base58 form
            >>> keyb58 = "6ACCbmy9qwiFcuVgvxNNwMPfoghobzznWrLs3v7t3RmN"
            >>> curvename = "secp256k1"
            >>> # Read in to an internal key
            >>> intpristr = Ecc.read_key_by_curve(Cnv.tohex(Cnv.frombase58(keyb58)), curvename)
            >>> # Extract public key from private key
            >>> intpubstr = Ecc.publickey_from_private(intpristr)
            >>> Ecc.query_key(intpristr, 'publicKey')
            '04654bacc2fc7a3bde0f8eb95dc5aac9ba1df732255cf7f2eb7e1e8e6edbb1f4188ff3752ac4bdf1e3a31a488747745dddcbabd33a10c3b52d737c092851da13c0'
            >>> # These should be the same
            >>> Ecc.key_hashcode(intpubstr)
            'BA36523B'
            >>> Ecc.key_hashcode(intpristr)
            'BA36523B'

        """
        nc = _dipki.ECC_PublicKeyFromPrivate(None, 0, intkeystr.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.ECC_PublicKeyFromPrivate(buf, nc, intkeystr.encode(), 0)
        return buf.value.decode()[:nc]

    @staticmethod
    def key_hashcode(intkeystr):
        """Compute the hash code of an "internal" ECC public or private key string.

        Should be the same for a matching private and public key.

        Args:
            intkeystr (str): Internal key string.

        Returns:
            int: A 32-bit hash code for the key, or zero on error.
        """
        n = _dipki.ECC_KeyHashCode(intkeystr.encode())
        if (n == 0): raise PKIError('key_hashcode failed: key string probably invalid')
        # Make sure we format negative values _correctly_ as unsigned
        return format(n & 0xFFFFFFFF, "08X")

    @staticmethod
    def dh_shared_secret(intprikeystr, intpubkeystr):
        """Compute EC Diffie-Hellman shared secret.

        Args:
            intprikeystr (str): Our own private key in *internal string form.
            intpubkeystr (str): Other party's public key in *internal* string form.

        Returns:
            bytes: Diffie-Hellman shared secret.
        """
        n = _dipki.ECC_DHSharedSecret(None, 0, intprikeystr.encode(), intpubkeystr.encode(), 0)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        _dipki.ECC_DHSharedSecret(buf, n, intprikeystr.encode(), intpubkeystr.encode(), 0)
        return bytearray(buf.raw)


class Gen:
    """General info about the core DLL and errors returned by it."""

    @staticmethod
    def version():
        """Return the release version of the core CryptoSys PKI DLL as an integer value."""
        return _dipki.PKI_Version(0, 0)

    @staticmethod
    def compile_time():
        """Return date and time the core CryptoSys PKI DLL was last compiled."""
        nchars = _dipki.PKI_CompileTime(None, 0)
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_CompileTime(buf, nchars)
        return buf.value.decode()

    @staticmethod
    def module_name():
        """Return full path name of the current process's DLL module."""
        nchars = _dipki.PKI_ModuleName(None, 0, 0)
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_ModuleName(buf, nchars, 0)
        return buf.value.decode()

    @staticmethod
    def module_info():
        """Get additional information about the core DLL module."""
        nchars = _dipki.PKI_ModuleInfo(None, 0, 0)
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_ModuleInfo(buf, nchars, 0)
        return buf.value.decode()

    @staticmethod
    def core_platform():
        """Return the platform the core DLL was compiled for ('Win32' or 'X64')."""
        nchars = 5
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_Platform(buf, nchars)
        return buf.value.decode()[:nchars]

    @staticmethod
    def licence_type():
        """Return licence type: "D"=Developer "T"=Trial."""
        n = _dipki.PKI_LicenceType(0)
        return chr(n)

    @staticmethod
    def last_error():
        """Return the last error message set by the toolkit, if any."""
        nchars = _dipki.PKI_LastError(None, 0)
        buf = create_string_buffer(nchars + 1)
        nchars = _dipki.PKI_LastError(buf, nchars)
        return buf.value.decode()

    @staticmethod
    def error_lookup(n):
        """Return a description of an error code.

        Args:
            n (int): Code number

        Returns:
            string: Corresponding error message
        """
        nchars = _dipki.PKI_ErrorLookup(None, 0, c_int(n))
        buf = create_string_buffer(nchars + 1)
        _dipki.PKI_ErrorLookup(buf, nchars, c_int(n))
        return buf.value.decode()

    @staticmethod
    def error_code():
        """Return the error code of the *first* error that occurred when calling the last function."""
        return _dipki.PKI_ErrorCode()


class Hash:
    """Compute message digest hash values."""

    # CONSTANTS
    class Alg:
        """Hash algorithms."""
        SHA1   = 0  #: SHA-1 (default)
        SHA224 = 6  #: SHA-224
        SHA256 = 3  #: SHA-256
        SHA384 = 4  #: SHA-384
        SHA512 = 5  #: SHA-512
        MD5    = 1  #: MD5 (as per RFC 1321)
        RMD160 = 7  #: RIPEMD-160
        BTC160 = 8  #: RIPEMD-160 hash of a SHA-256 hash (``RIPEMD160(SHA256(m))``)

        def __or__(self, other):
            return self | other

    @staticmethod
    def data(data, alg=Alg.SHA1):
        """data(data, alg=Alg.SHA1)
        Compute message digest as a byte array from bytes data.

        Args:
            data (bytes): Message data
            alg (Hash.Alg): Hash algorithm to be used

        Returns:
            bytes: Message digest in byte array.
        """
        n = _dipki.HASH_Bytes(None, 0, bytes(data), len(data), alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        _dipki.HASH_Bytes(buf, n, bytes(data), len(data), alg)
        return bytearray(buf.raw)

    @staticmethod
    def file(filename, alg=Alg.SHA1):
        """file(filename, alg=Alg.SHA1)
        Compute message digest as a byte array from data in a file.

        Args:
            filename (str): Name of file containing message data
            alg (Hash.Alg): Hash algorithm to be used

        Returns:
            bytes: Message digest in byte array.
        """
        n = _dipki.HASH_File(None, 0, filename.encode(), alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        _dipki.HASH_File(buf, n, filename.encode(), alg)
        return bytearray(buf.raw)

    @staticmethod
    def hex_from_data(data, alg=Alg.SHA1):
        """hex_from_data(data, alg=Alg.SHA1)
        Compute message digest in hexadecimal format from bytes data.

        Args:
            data (bytes): Message data in byte array.
            alg (Hash.Alg): Hash algorithm to be used.

        Returns:
            string: Message digest in hex-encoded format.

        Examples:
            >>> Hash.hex_from_data(b'abc')
            'a9993e364706816aba3e25717850c26c9cd0d89d'
            >>> Hash.hex_from_data(b'abc', Hash.Alg.SHA256)
            'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
        """
        nc = _dipki.HASH_HexFromBytes(None, 0, bytes(data), len(data), alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        _dipki.HASH_HexFromBytes(buf, nc, bytes(data), len(data), alg)
        return buf.value.decode()

    @staticmethod
    def hex_from_string(s, alg=Alg.SHA1):
        """hex_from_string(s, alg=Alg.SHA1)
        Compute message digest in hexadecimal format from a string.

        Args:
            s (str): Message data in UTF-8 string.
            alg (Hash.Alg): Hash algorithm to be used.

        Returns:
            str: Message digest in hex-encoded format.

        Examples:
            >>> Hash.hex_from_string('abc', Hash.Alg.SHA256)
            'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
            >>> Hash.hex_from_string('Olá mundo')  # UTF-8
            'f6c2fc0dd7f1131d8cb5ac7420d77a4c28ac1aa0'
        """
        return Hash.hex_from_data(s.encode(), alg)

    @staticmethod
    def hex_from_file(filename, alg=Alg.SHA1):
        """hex_from_file(filename, alg=Alg.SHA1)
        Compute message digest in hexadecimal format from data in a file.

        Args:
            filename (str): Name of file containing message data
            alg (Hash.Alg): Hash algorithm to be used

        Returns:
            str: Message digest in hex-encoded format
        """
        nc = _dipki.HASH_HexFromFile(None, 0, filename.encode(), alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        _dipki.HASH_HexFromFile(buf, nc, filename.encode(), alg)
        return buf.value.decode()

    @staticmethod
    def hex_from_hex(datahex, alg=Alg.SHA1):
        """hex_from_hex(datahex, alg=Alg.SHA1)
        Compute message digest in hexadecimal format from data in a hexadecimal-encoded string.

        Args:
            datahex (str): Message data in hex-encoded format
            alg (Hash.Alg): Hash algorithm to be used

        Returns:
            str: Message digest in hex-encoded format.

        Examples:
            >>> Hash.hex_from_hex('616263')  # HEX('abc')
            'a9993e364706816aba3e25717850c26c9cd0d89d'
        """
        nc = _dipki.HASH_HexFromHex(None, 0, datahex.encode(), alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        _dipki.HASH_HexFromHex(buf, nc, datahex.encode(), alg)
        return buf.value.decode()

    @staticmethod
    def double(data, alg=Alg.SHA1):
        """double(data, alg=Alg.SHA1)
        Create a double hash - hash of hash - as a byte array from bytes data.

        Args:
            data (bytes): Message data in byte array
            alg (Hash.Alg): Hash algorithm to be used

        Returns:
            bytes: Message digest ``HASH(HASH(m))`` in byte format

        """
        _HASH_DOUBLE = 0x20000
        n = _dipki.HASH_Bytes(None, 0, bytes(data), len(data), alg | _HASH_DOUBLE)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        _dipki.HASH_Bytes(buf, n, bytes(data), len(data), alg | _HASH_DOUBLE)
        return bytearray(buf.raw)


class Hmac:
    """Compute keyed-hash based message authentication code (HMAC) values."""

    # CONSTANTS
    class Alg:
        """HMAC algorithms."""
        SHA1   = 0  #: HMAC-SHA-1 (default)
        SHA224 = 6  #: HMAC-SHA-224
        SHA256 = 3  #: HMAC-SHA-256
        SHA384 = 4  #: HMAC-SHA-384
        SHA512 = 5  #: HMAC-SHA-512
        MD5    = 1  #: HMAC-MD5

    @staticmethod
    def data(data, key, alg=Alg.SHA1):
        """data(data, key, alg=Alg.SHA1)
        Compute a keyed-hash based message authentication code (HMAC) as a byte array from bytes data.

        Args:
            data (bytes): Message to be signed in byte array.
            key (bytes): Key in byte array.
            alg (Hmac.Alg): Hash algorithm to be used.

        Returns:
            bytes: HMAC in byte format
        """
        n = _dipki.HMAC_Bytes(None, 0, bytes(data), len(data), bytes(key), len(key), alg)
        if (n < 0): raise PKIError(-n)
        buf = create_string_buffer(n)
        n = _dipki.HMAC_Bytes(buf, n, bytes(data), len(data), bytes(key), len(key), alg)
        return bytearray(buf.raw)

    @staticmethod
    def hex_from_data(data, key, alg=Alg.SHA1):
        """hex_from_data(data, key, alg=Alg.SHA1)
        Compute a keyed-hash based message authentication code (HMAC) in hexadecimal format from bytes data.

        Args:
            data (bytes): Message to be signed in byte array.
            key (bytes): Key in byte array.
            alg (Hmac.Alg): Hash algorithm to be used.

        Returns:
            str: HMAC in hex-encoded format.

        Examples:
            >>> Hmac.hex_from_data(b"Hi There", Cnv.fromhex("0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b"))
            'b617318655057264e28bc0b6fb378c8ef146be00'

        """
        nc = _dipki.HMAC_HexFromBytes(None, 0, bytes(data), len(data), bytes(key), len(key), alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.HMAC_HexFromBytes(buf, nc, bytes(data), len(data), bytes(key), len(key), alg)
        return buf.value.decode()

    @staticmethod
    def hex_from_string(s, key, alg=Alg.SHA1):
        """hex_from_string(s, key, alg=Alg.SHA1)
        Compute a keyed-hash based message authentication code (HMAC) in hexadecimal format from string data.

        Args:
            s (str): Message data in UTF-8 string.
            key (bytes): Key in byte array.
            alg (Hmac.Alg): Hash algorithm to be used.

        Returns:
            str: Message digest in hex-encoded format.

        """
        return Hmac.hex_from_data(s.encode(), key, alg)

    @staticmethod
    def hex_from_hex(datahex, keyhex, alg=Alg.SHA1):
        """hex_from_hex(datahex, keyhex, alg=Alg.SHA1)
        Compute a keyed-hash based message authentication code (HMAC) in hex format from data in hex-encoded strings.

        Args:
            datahex (str): Message to be signed in hex-encoded format.
            keyhex (str): Key in hex-encoded format.
            alg (Hmac.Alg): Hash algorithm to be used.

        Returns:
            str: HMAC in hex-encoded format.

        Examples:
            >>> # HEX('Hi There') = 4869205468657265
            >>> Hmac.hex_from_hex("4869205468657265", "0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b")
            'b617318655057264e28bc0b6fb378c8ef146be00'

        """
        nc = _dipki.HMAC_HexFromHex(None, 0, datahex.encode(), keyhex.encode(), alg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.HMAC_HexFromHex(buf, nc, datahex.encode(), keyhex.encode(), alg)
        return buf.value.decode()


class Ocsp:
    """Online Certificate Status Protocol (OCSP) routines."""

    class HashAlg:
        """Hash algorithms."""
        SHA1   = 0  #: SHA-1 (default)
        SHA224 = 6  #: SHA-224
        SHA256 = 3  #: SHA-256
        SHA384 = 4  #: SHA-384
        SHA512 = 5  #: SHA-512
        MD5    = 1  #: MD5 (as per RFC 1321)

    @staticmethod
    def make_request(issuercert, certfile_or_serialnumber, hashalg=0):
        """Create an Online Certification Status Protocol (OCSP) request as a base64 string.

        Args:
            issuercert (str): name of issuer's X.509 certificate file (or base64 representation)
            certfile_or_serialnumber (str): either the name of X.509 certificate file to be checked or its serial number in hexadecimal format preceded by #x.

                The certificate to be checked can either be specified directly as a filename
                or as a serialNumber in hexadecimal format preceded by "#x", e.g. "#x01deadbeef".
                If the latter format is used, it must be in hexadecimal format,
                so the serial number decimal 10 would be passed as "#x0a".

            hashalg (Hash.Alg): Hash algorithm to be used [default = SHA-1]

        Returns:
            str: A base64 string suitable for an OCSP request to an Online Certificate Status Manager or an empty string on error.

        Note:
            It is an error (``NO_MATCH_ERROR``) if the issuer's name of the certificate to be checked
            does not match the subject name of the issuer's certificate.

        """
        nc = _dipki.OCSP_MakeRequest(None, 0, issuercert.encode(), certfile_or_serialnumber.encode(), b"", hashalg)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.OCSP_MakeRequest(buf, nc, issuercert.encode(), certfile_or_serialnumber.encode(), b"", hashalg)
        return buf.value.decode()

    @staticmethod
    def read_response(responsefile, issuercert=""):
        """Read a response to an Online Certification Status Protocol (OCSP) request and outputs the main results in text form.

        Args:
            responsefile (str): name of the file containing the response data in BER format.
            issuercert (str): (optional) name of issuer's X.509 certificate file (or its base64 representation).

                If provided, it will be used to check the signature on the OCSP reponse and and an error
                will result if the signature is not valid.

                **CAUTION:** For some CAs (e.g. VeriSign) the key used to sign the OCSP response is not the same as
                the key in the issuer's certificate, so specifying the issuer's certificate in this case will result
                in a signature error. If you can separately obtain the certificate used to sign the OCSP response,
                then specify this as the ``issuercert``; otherwise leave as the empty string ``""``.

        Returns:
            str: A text string outlining the main results in the response data or an empty string on error.

        Note:
            A revoked certificate will still result in a "Successful response", so check the CertStatus.

        """
        nc = _dipki.OCSP_ReadResponse(None, 0, responsefile.encode(), issuercert.encode(), b"", 0)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.OCSP_ReadResponse(buf, nc, responsefile.encode(), issuercert.encode(), b"", 0)
        return buf.value.decode()


class Pbe:
    """Password-based encryption."""

    class PrfAlg:
        """PRF algorithms."""
        HMAC_SHA1   = 0  #: HMAC-SHA-1 (default)
        HMAC_SHA224 = 6  #: HMAC-SHA-224
        HMAC_SHA256 = 3  #: HMAC-SHA-256
        HMAC_SHA384 = 4  #: HMAC-SHA-384
        HMAC_SHA512 = 5  #: HMAC-SHA-512

    @staticmethod
    def kdf2(dklen, password, salt, count, prfalg=0):
        """Derive a key of any length from a password using the PBKDF2 algorithm.

        Args:
            dklen (int): Required length of key in bytes
            password (str): Password
            salt (bytes): Salt in byte array
            count (int): Iteration count
            prfalg (PrfAlg): Algorithm to use in PRF [default = HMAC-SHA-1]

        Returns:
            bytes: Derived key in byte array.

        Examples:
            >>> Cnv.tohex(Pbe.kdf2(24, 'password', Cnv.fromhex('78578E5A5D63CB06'), 2048))
            'BFDE6BE94DF7E11DD409BCE20A0255EC327CB936FFE93643'

        """
        if (dklen <= 0 or dklen > _INTMAX): raise PKIError('dklen out of range')
        buf = create_string_buffer(dklen)
        n = _dipki.PBE_Kdf2(buf, dklen, password.encode(), len(password.encode()), bytes(salt), len(salt), count, prfalg)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return bytes(buf.raw)


class Pem:
    """PEM file conversion routines."""

    class EOL:
        """Line ending options."""
        DEFAULT = 0  #: Windows CR-LF line endings (default)
        WINDOWS = 0  #: Windows CR-LF line endings
        UNIX = 0x20000  #: Unix/SSL LF line endings

    @staticmethod
    def from_binfile(outputfile, filein, header, linelen=64, eol=EOL.DEFAULT):
        """Create a PEM file from a binary file.

        Args:
            outputfile (str): Name of PEM file to create
            filein (str): Name of input binary file.
                *Any* input file is accepted and treated as binary data.
                No checks are made that the header matches the data.
            header (str): Header to be used. Leave empty to omit the PEM header and footer.
            linelen (int): Maximum length of a line in the resulting PEM file [default = 64 characters]
            eol (EOL): Line ending option [default = Windows CR-LF endings]

        Returns:
            int: Zero if successful.
        """
        n = _dipki.PEM_FileFromBinFileEx(outputfile.encode(), filein.encode(), header.encode(), linelen, eol)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def to_binfile(outputfile, filein):
        """Convert the contents of a PEM file into a binary file.

        Args:
            outputfile (str): Name of binary file to create.
            filein (str): Name of input PEM file

        Returns:
            int: Zero if successful.
        """
        n = _dipki.PEM_FileToBinFile(outputfile.encode(), filein.encode())
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n


class Pfx:
    """PKCS-12 (PFX) file utilties."""

    class Opts:
        """Bitwise options for creating a PFX file."""
        STRONG_CERT = 0x1000000  #: Encrypt the certificate with "stronger" Triple DES (default is "weak" 40-bit RC2).
        PLAIN_CERT = 0x2000000  #: Store the certificate in unencrypted form (default is encrypted with 40-bit RC2)
        CLONE_KEY  = 0x4000000  #: Store the private key in the exact form of the pkcs-8 input file (default is to re-encrypt with Triple DES)
        ALT_FORMAT =  0x100000  #: Create a PFX file with the exact peculiarities used by Microsoft (default is OpenSSL)
        FORMAT_PEM =   0x10000  #: Create the output file in PEM format (default is DER-encoded binary)

    @staticmethod
    def make_file(outputfile, certlist, prikeyfile="", password="", friendlyname="", opts=0):
        """Create a PFX (PKCS-12) file from an X.509 certificate and (optional) encrypted private key file.

        Args:
            outputfile (str): name of output file to be created
            certlist (str): filename of the subject's X.509 certificate (required)
            prikeyfile (str): filename of the subject's encrypted private key in pkcs-8 format (optional)
            password (str): password for private key file and new PFX file
            friendlyname (str): friendly name identification for the subject (optional)
            opts (Pfx.Opts): Specialist options

        Returns:
            int: Zero if successful.
        """
        n = _dipki.PFX_MakeFile(outputfile.encode(), certlist.encode(), prikeyfile.encode(), password.encode(), friendlyname.encode(), opts)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def sig_is_valid(pfxfile, password):
        """Determine if the MacData signature is valid in a pkcs-12 file.

        Args:
            pfxfile (str): Name of PKCS-12 file to be checked
            password (str): password for file

        Returns:
            bool: True if signature is OK.
        """
        _INVALID   = -1
        n = _dipki.PFX_VerifySig(pfxfile.encode(), password.encode(), 0)
        if (0 == n):
            isvalid = True
        elif (_INVALID == n):
            isvalid = False
        else:
            raise PKIError(-n if n < 0 else n)
        return isvalid


class Pwd:
    """Password dialog utility."""

    @staticmethod
    def prompt(caption="", prompt=""):
        """Return a password entered into a dialog box.

        Args:
            caption (str): Caption for dialog window
            prompt (str): Wording for prompt

        Returns:
            str: String containing password or Empty string if user cancels
        """
        _MAXPWDLEN = 512
        nc = _MAXPWDLEN
        buf = create_string_buffer(nc + 1)
        n = _dipki.PWD_PromptEx(buf, nc, caption.encode(), prompt.encode(), 0)
        if (n <= 0):
            return ""
        return buf.value.decode()


class Rng:
    """Random Number Generator to NIST SP800-90."""

    # FIELDS
    SEED_BYTES = 64  #: Size in bytes of seed file
    RNG_GUID_CHARS = 36  #: Length of GUID string

    @staticmethod
    def bytestring(n):
        """Generate an array of n random bytes.

        Args:
            n (int): Required number of random bytes.

        Returns:
            bytes: Array of random bytes.
        """
        if (n < 0 or n > _INTMAX): raise PKIError('n out of range')
        buf = create_string_buffer(n)
        n = _dipki.RNG_Bytes(buf, n, None, 0)
        return bytes(buf.raw)

    @staticmethod
    def number(lower, upper):
        """Generate a random integer in a given range.

        Args:
            lower (int): lower value of range
            upper (int): upper value of range

        Returns:
            int: Random integer x: ``lower <= x <= upper``
        """
        if (lower < _INTMIN) or (lower > _INTMAX): raise PKIError('out of range')
        if (upper < _INTMIN) or (upper > _INTMAX): raise PKIError('out of range')
        n = _dipki.RNG_Number(lower, upper)
        return n

    @staticmethod
    def octet():
        """Generate a single random octet (byte).

        Returns:
            int: Single byte value randomly chosen between 0 and 255
        """
        n = _dipki.RNG_Number(0, 255)
        return n

    @staticmethod
    def initialize(seedfilename):
        """Initialize the RNG generator using a seed file.

        Use a seed file to increase the entropy for the current session.
        Initialization is recommended but not mandatory.
        The seed file is automatically updated by this procedure.

        Args:
            seedfilename (str): Full path name of seed file.
                If the seed file does not exist, it will be created.

        Returns:
            int: Zero if successful.
        """
        n = _dipki.RNG_Initialize(seedfilename.encode(), 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def update_seedfile(seedfilename):
        """Update the RNG seed file with more entropy.

        Args:
            seedfilename (str): Full path name of seed file.
                The seed file must exist and be writable.

        Returns:
            int: Zero if successful.
        """
        n = _dipki.RNG_UpdateSeedFile(seedfilename.encode(), 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def guid():
        """Generate a random 36-character Global Unique IDentifier (GUID) string according to [RFC4122].

        Returns:
            str: String of the form "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" where 'x' is a hexadecimal digit ``[0-9a-f]``.
        """
        n = Rng.RNG_GUID_CHARS
        buf = create_string_buffer(n + 1)
        n = _dipki.RNG_Guid(buf, n, 0)
        return buf.value.decode()


class Rsa:
    """RSA encryption and key management."""
    # CONSTANTS
    class PbeScheme:
        """Password-based encryption scheme to encrypt the private key file."""
        DEFAULT = 0    #: ``pbeWithSHAAnd3-KeyTripleDES-CBC`` from PKCS#12
        PBKDF2_DESEDE3 = 0x1010  #: PBKDF2 using ``des-EDE3-CBC``
        PBKDF2_AES128  = 0x1020  #: PBKDF2 using ``aes128-CBC``
        PBKDF2_AES192  = 0x1030  #: PBKDF2 using ``aes192-CBC``
        PBKDF2_AES256  = 0x1040  #: PBKDF2 using ``aes256-CBC``

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class PublicExponent:
        """Choice for public exponent (e)."""
        RSAEXP_EQ_3     = 0  #: Set exponent equal to 3 (F0)
        RSAEXP_EQ_5     = 1  #: Set exponent equal to 5 (F1)
        RSAEXP_EQ_17    = 2  #: Set exponent equal to 17 (F2)
        RSAEXP_EQ_257   = 3  #: Set exponent equal to 257 (F3)
        RSAEXP_EQ_65537 = 4  #: Set exponent equal to 65537 (F4)

    class Format:
        """Format for saved RSA key."""
        DEFAULT = 0  #: Default
        BINARY  = 0  #: Binary DER-encoded (default)
        PEM = 0x10000  #: PEM-encoded
        SSL = 0x20000  #: PEM-encoded compatible with OpenSSL

    class XmlOptions:
        """Bitwise flags when converting between RSA key and XML."""
        RSAKEYVALUE = 0x0001  #: Create in .NET-compatible RSAKeyValue format (to_xml only)
        EXCLPRIVATE = 0x0010  #: Exclude private key even if present
        REQPRIVATE  = 0x0020  #: Require the private key to exist in the XML input or fail (from_xml only)
        HEXBINARY   = 0x0100  #: Create XML using non-standard hexadecimal encoding (to_xml only)

    class HashAlg:
        """Hash algorithm for RSA signatures."""
        SHA1   = 0  #: SHA-1 (default)
        SHA224 = 6  #: SHA-224
        SHA256 = 3  #: SHA-256
        SHA384 = 4  #: SHA-384
        SHA512 = 5  #: SHA-512
        MD5    = 1  #: MD5 (as per RFC 1321)

    class EME:
        """Encoding method for encryption."""
        PKCSV1_5  = 0x00  #: EME-PKCS1-v1_5 encoding method (default)
        OAEP = 0x10  #: EME-OAEP encoding method

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class AdvOpts:
        """Advanced options."""
        DEFAULT = 0  #: Default
        MGF1_SHA1 = 0x800000  #: RSA-OAEP only: Force the MGF hash function to be SHA-1 (default = same as encoding set by Rsa.HashAlg)

    @staticmethod
    def make_keys(pubkeyfile, prikeyfile, nbits, exponent, password, pbes=0, params='', fileformat=0):
        """Generate a new RSA public/private key pair.

        Args:
            pubkeyfile (str): Output filename for public key
            prikeyfile (str): Output filename for (encrypted) private key
            nbits (int): Required key modulus size in bits (min 96)
            exponent (PublicExponent): Exponent (Fermat Prime)
            password (str): Password string for encrypted private key
            pbes (Rsa.PbeScheme): Encryption scheme to encrypt private key.
            params (str): Optional parameters.
                A set of attribute "name=value" pairs separated by a semicolon ";" .

                count=<integer>
                    To set the iteration count used in the PBKDF2 method,
                    e.g. ``"count=5000;"`` [default=2048].

                prf=<hmac-name>
                    To change the HMAC algorithm used in the PBKDF2 method,
                    e.g. ``"prf=hmacwithSHA256;"``. Valid values are (case insensitive):

                        * ``hmacwithSHA1`` (default)
                        * ``hmacwithSHA224``
                        * ``hmacwithSHA256``
                        * ``hmacwithSHA384``
                        * ``hmacwithSHA512``

                rngseed=<string>
                    To add some user-supplied entropy for the key generation process,
                    e.g. ``"rngseed=NaCl;"``.

            fileformat (Rsa.Format): Format to save file [default = DER binary]

        Returns:
            int: Zero if successful.
        """
                    
        noptions = pbes | fileformat
        n = _dipki.RSA_MakeKeysXtd(pubkeyfile.encode(), prikeyfile.encode(), password.encode(), nbits, exponent, params.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def key_bits(keystr):
        """Return number of significant bits in RSA key modulus.

        Args:
            keystr (str): Internal key string (private or public).

        Returns:
            int: Number of significant bits in key.
        """
        n = _dipki.RSA_KeyBits(keystr.encode())
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def key_bytes(keystr):
        """Return number of bytes (octets) in RSA key modulus.

        Args:
            keystr (str): Internal key string (private or public).

        Returns:
            int: Number of bytes in key.
        """
        n = _dipki.RSA_KeyBytes(keystr.encode())
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def key_hashcode(keystr):
        """Compute the hash code of an "internal" RSA public or private key string.

        Should be the same for a matching private and public key.

        Args:
            keystr (str): Internal key string.

        Returns:
            str: A 32-bit hash code for the key encoded in hex.
        """
        n = _dipki.RSA_KeyHashCode(keystr.encode())
        if (n == 0): raise PKIError('key_hashcode failed: key string probably invalid')
        # Make sure we format negative values _correctly_ as unsigned
        return format(n & 0xFFFFFFFF, "08X")

    @staticmethod
    def key_isprivate(keystr):
        """Determine if keystring is a private key.

        Args:
            keystr (str): Internal key string.

        Returns:
            bool: True if the key string contains a valid RSA private key,
            or False if a valid RSA public key.

        Raises:
            PKIError: If keystring is invalid.
        """
        n = _dipki.RSA_CheckKey(keystr.encode(), 0)
        if (n < 0): raise PKIError(-n)
        return (n == 0)

    @staticmethod
    def key_value(keystr, fieldname):
        """Extract a base64-encoded RSA key value from internal key string.

        The output is a continuous string of base64 characters
        suitable for a ``<RSAKeyValue>`` node in an XML-DSIG document.

        Args:
            keystr (str): Public or private key in internal string format
            fieldname (str): Name of field to be extracted: ``"Modulus"`` or ``"Exponent"``

        Returns:
            str: Value encoded in base64 or an empty string on error
        """
        nc = _dipki.RSA_KeyValue(None, 0, keystr.encode(), fieldname.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_KeyValue(buf, nc, keystr.encode(), fieldname.encode(), 0)
        return buf.value.decode()

    @staticmethod
    def key_match(prikeystr, pubkeystr):
        """Determine if a pair of "internal" RSA private and public key strings are matched.

        Args:
            prikeystr (str): Internal RSA private key string
            pubkeystr (str): Internal RSA public key string

        Returns:
            bool: True if the keystrings are valid and matched, or
            False if the keystrings are valid but not matched.

        Raises:
            PKIError: If a key string is invalid.
        """
        _NO_MATCH_ERROR = -21
        n = _dipki.RSA_KeyMatch(prikeystr.encode(), pubkeystr.encode())
        if (n == 0):
            return True
        elif (n == _NO_MATCH_ERROR):
            return False
        else:
            raise PKIError(-n if n < 0 else n)

    @staticmethod
    def publickey_from_private(intkeystr):
        """Return an internal RSA public key string from an internal RSA private key string.

        Args:
            intkeystr (str): Private key in "internal" format

        Returns:
            str: Internal representation of the public key.
        """
        nc = _dipki.RSA_PublicKeyFromPrivate(None, 0, intkeystr.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_PublicKeyFromPrivate(buf, nc, intkeystr.encode(), 0)
        return (buf.value.decode())[:nc]

    @staticmethod
    def to_xmlstring(keystr, opts=0, prefix=''):
        """Return an XML string representation of an RSA internal key string.

        Args:
            keystr (str): Internal key string
            opts (XmlOptions): Option flags.
            prefix (str): Prefix to add to elements, e.g. ``"ds"`` or ``"ds:"``.

        Returns:
            string: XML string or empty string on error
        """
        nc = _dipki.RSA_ToXMLStringEx(None, 0, keystr.encode(), prefix.encode(), opts)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_ToXMLStringEx(buf, nc, keystr.encode(), prefix.encode(), opts)
        return (buf.value.decode())[:nc]

    @staticmethod
    def from_xmlstring(xmlstr, opts=0):
        """Return an RSA key string in internal format from an XML string.

        Creates an internal private key string if the XML contains private key parameters,
        otherwise an internal public key string.

        Args:
            xmlstr (str): The XML string to use to reconstruct the RSA key.
            opts (XmlOptions): Option flags.

        Returns:
            str: Key string in internal format or empty string on error.
        """
        nc = _dipki.RSA_FromXMLString(None, 0, xmlstr.encode(), opts)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_FromXMLString(buf, nc, xmlstr.encode(), opts)
        return (buf.value.decode())[:nc]

    @staticmethod
    def read_private_key(keyfileorstr, password=""):
        """Return an internal private key string from a file or string containing an RSA private key.

        Args:
            keyfileorstr (str): Either the name of file containing the private key or
                a string containing the key in PEM format or XML format.
            password (str): password for key file, if encrypted.

        Returns:
            str: Private key string in internal format.
        """
        nc = _dipki.RSA_ReadAnyPrivateKey(None, 0, keyfileorstr.encode(), password.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_ReadAnyPrivateKey(buf, nc, keyfileorstr.encode(), password.encode(), 0)
        return (buf.value.decode())[:nc]

    @staticmethod
    def read_public_key(keyfileorstr):
        """Return an internal public key string from a file or string containing an RSA public key.

        Args:
            keyfileorstr (str): Either the name of file containing the public key or
                a string containing the key in PEM format or XML format.

        Returns:
            str: Public key string in internal format.
        """
        nc = _dipki.RSA_ReadAnyPublicKey(None, 0, keyfileorstr.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.RSA_ReadAnyPublicKey(buf, nc, keyfileorstr.encode(), 0)
        return (buf.value.decode())[:nc]

    @staticmethod
    def save_key(outputfile, keystr, fileformat=0):
        """Save an internal RSA key string (public or private) to an unencrypted key file.

        Args:
            outputfile (str): Name of file to create
            keystr (str): Key string (public or private) in internal format
            fileformat (Rsa.Format): File format [default = DER-encoded binary file]

        Returns:
            int: Zero if successful.
        """
        # TODO: at some stage add this to core C library. For now we do in parts.
        if (Rsa.key_isprivate(keystr)):
            n = _dipki.RSA_SavePrivateKeyInfo(outputfile.encode(), keystr.encode(), fileformat)
        else:
            n = _dipki.RSA_SavePublicKey(outputfile.encode(), keystr.encode(), fileformat)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def save_enc_key(outputfile, intkeystr, password, pbescheme=0, count=2048, params='', fileformat=0):
        """Save an internal RSA private key string to an encrypted private key file.

        Args:
            outputfile (str): Name of file to create
            intkeystr (str): Private key in internal format
            password (str): Password to encrypt key file.
            pbescheme (Rsa.PbeScheme): Encryption scheme to encrypt private key.
            count (int): Iteration count to be used when encrypting file (ignored as of [v20.3] - use ``count=nnn`` in ``params``).
            params (str): Optional parameters.
                A set of attribute "name=value" pairs separated by a semicolon ";" .

                count=<integer>
                    To set the iteration count used in the PBKDF2 method,
                    e.g. ``"count=5000;"`` [default=2048].

                prf=<hmac-name>
                    To change the HMAC algorithm used in the PBKDF2 method,
                    e.g. ``"prf=hmacwithSHA256;"``. Valid values are (case insensitive):

                        * ``hmacwithSHA1`` (default)
                        * ``hmacwithSHA224``
                        * ``hmacwithSHA256``
                        * ``hmacwithSHA384``
                        * ``hmacwithSHA512``

            fileformat (Rsa.Format): File format [default = DER-encoded binary file]

        Returns:
             int: Zero if successful.
        """
                                                                                   
        noptions = pbescheme | fileformat
        n = _dipki.RSA_SaveEncKey(outputfile.encode(), intkeystr.encode(), password.encode(), params.encode(), noptions)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def get_privatekey_from_pfx(outputfile, pfxfile):
        """Extract an encrypted private key from a PKCS-12 PKCS8ShroudedKeyBag,
        saving the output directly as a new file.

        The first pkcs-12-pkcs-8ShroudedKeyBag found in the PFX file will be extracted and saved directly as a
        BER-encoded EncryptedPrivateKeyInfo file. No decryption or other conversion is carried out.

        Args:
            outputfile (str): Name of file to create.
            pfxfile (str): Name of PFX (.p12) file.

        Returns:
             int: If successful, it returns the number of bytes written to the output file.
        """
        n = _dipki.RSA_GetPrivateKeyFromPFX(outputfile.encode(), pfxfile.encode(), 0)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def raw_private(block, prikeystr):
        """Return RSA transformation of block using private key.

        Args:
            block (bytes): Data (*must* be same byte length as key modulus).
            prikeystr (str): Private key in internal string format.

        Returns:
            bytes: Transformed data.
        """
        nd = len(block)
        buf = create_string_buffer(block, nd)
        n = _dipki.RSA_RawPrivate(buf, nd, prikeystr.encode(), 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return bytes(buf.raw)

    @staticmethod
    def raw_public(block, pubkeystr):
        """Return RSA transformation of block using public key.

        Args:
            block (bytes): Data (*must* be same byte length as key modulus).
            pubkeystr (str): Public key in internal string format.

        Returns:
            bytes: Transformed data.
        """
        nd = len(block)
        buf = create_string_buffer(block, nd)
        n = _dipki.RSA_RawPublic(buf, nd, pubkeystr.encode(), 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return bytes(buf.raw)

    @staticmethod
    def encode_msg_for_signature(keybytes, message, hashalg=HashAlg.SHA1, digest_only=False):
        """Create an encoded message for signature (EMSA-PKCS1-v1_5 only).

        Args:
            keybytes (int): Number of bytes in the key
            message (bytes): Message to be encoded (or digest value if `digest_only=True`)
            hashalg (Rsa.HashAlg): Message digest algorithm to use [default = SHA-1]
            digest_only (bool): Set True to pass the message digest value instead of the message itself.

        Returns:
            bytes: Encoded block.
        """
        _EMSIG_PKCSV1_5 = 0x20
        _DIGESTONLY = 0x1000
        noptions = _EMSIG_PKCSV1_5 | hashalg
        if digest_only: noptions |= _DIGESTONLY
        n = keybytes
        buf = create_string_buffer(n)
        n = _dipki.RSA_EncodeMsg(buf, n, bytes(message), len(message), noptions)
        if (n < 0): raise PKIError(-n)
        # success == 0
        return bytes(buf.raw)

    @staticmethod
    def decode_digest_for_signature(data, full_digestinfo=False):
        """Extract digest (or digestinfo) from an EMSA-PKCS1-v1_5-encoded block.

        Args:
            data (bytes): Encoded message for signature.
            full_digestinfo (bool): If True, extract the full ``DigestInfo``;
                otherwise just extract the message digest itself.

        Returns:
            bytes: Decoded data.
        """
        _EMSIG_PKCSV1_5 = 0x20
        _DIGINFO = 0x2000
        noptions = (_EMSIG_PKCSV1_5 | _DIGINFO) if full_digestinfo else _EMSIG_PKCSV1_5
        n = _dipki.RSA_DecodeMsg(None, 0, bytes(data), len(data), noptions)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.RSA_DecodeMsg(buf, n, bytes(data), len(data), noptions)
        return bytes(buf.raw)[:n]

    @staticmethod
    def encode_msg_for_encryption(keybytes, message, method=EME.PKCSV1_5):
        """Create an encoded message for encryption (EME).

        Args:
            keybytes (int): Number of bytes in the key.
            message (bytes): Message to be encoded.
            method (Rsa.EME): Encoding method to use [default = EME.PKCSV1_5].

        Returns:
            bytes: Encoded block.
        """
        nb = keybytes
        buf = create_string_buffer(nb)
        n = _dipki.RSA_EncodeMsg(buf, nb, bytes(message), len(message), method)
        if (n < 0): raise PKIError(-n)
        # success == 0
        return bytes(buf.raw)

    @staticmethod
    def decode_msg_for_encryption(data, method=EME.PKCSV1_5):
        """Extract message from a PKCS#1 EME-encoded block.

        Args:
            data (bytes): Encoded block.
            method (Rsa.EME): Encoding method used [default = EME.PKCSV1_5].

        Returns:
            bytes: Decoded message.
        """
        n = _dipki.RSA_DecodeMsg(None, 0, bytes(data), len(data), method)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.RSA_DecodeMsg(buf, n, bytes(data), len(data), method)
        return bytes(buf.raw)[:n]

    @staticmethod
    def encrypt(data, pubkeyfileorstring, method=EME.PKCSV1_5, hashalg=HashAlg.SHA1, advopts=AdvOpts.DEFAULT, params=""):
        """Encrypt a short message using RSA encryption.

        Args:
            data (bytes): Data to be encrypted (*must* be at least 11 bytes shorter than the key modulus size).
            pubkeyfileorstring (str): Name of the public key file or X.509 certificate, or a string containing the
                key or certificate in PEM format, or a valid internal public key string.
            method (Rsa.EME): Encoding method to use [default = EME.PKCSV1_5].
            hashalg (Rsa.HashAlg) : Hash function for EME-OAEP encoding, otherwise ignored.
            advopts (Rsa.AdvOpts) : Advanced options for EME-OAEP only.
            params (str): For specialist use.

        Returns:
            bytes: Encrypted data.
        """
        opts = method | hashalg | advopts
        n = _dipki.RSA_Encrypt(None, 0, bytes(data), len(data), pubkeyfileorstring.encode(), params.encode(), opts)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.RSA_Encrypt(buf, n, bytes(data), len(data), pubkeyfileorstring.encode(), params.encode(), opts)
        return bytes(buf.raw)[:n]

    @staticmethod
    def decrypt(data, prikeyfileorstring, password="", method=EME.PKCSV1_5, hashalg=HashAlg.SHA1, advopts=AdvOpts.DEFAULT):
        """Decrypt a message encrypted using RSA encryption.

        Args:
            data (bytes): Data to be decrypted (*must* be exactly the same length as the key modulus size).
            prikeyfileorstring (str): Name of the private key file, or a string containing the key in PEM format, or a valid internal private key string.
            password (str): Password for encrypted private key, or "" if password is not required.
            method (Rsa.EME): Encoding method used [default = EME.PKCSV1_5].
            hashalg (Rsa.HashAlg) : Hash function for EME-OAEP encoding, otherwise ignored.
            advopts (Rsa.AdvOpts) : Advanced options for EME-OAEP only.

        Returns:
            bytes: Decrypted data.
        """
        opts = method | hashalg | advopts
        n = _dipki.RSA_Decrypt(None, 0, bytes(data), len(data), prikeyfileorstring.encode(), password.encode(), b"", opts)
        if (n < 0): raise PKIError(-n)
        if (n == 0): return bytes("")
        buf = create_string_buffer(n)
        n = _dipki.RSA_Decrypt(buf, n, bytes(data), len(data), prikeyfileorstring.encode(), password.encode(), b"", opts)
        return bytes(buf.raw)[:n]


class Sig:
    """Create and verify digital signatures."""

    class Alg:
        """Signature algorithm to use."""
        DEFAULT = ""  #: Use default signature algorithm (``rsa-sha1``/``sha1WithRSAEncryption``)
        RSA_SHA1 = "sha1WithRSAEncryption"  #: Use sha1WithRSAEncryption (rsa-sha1) signature algorithm [default]
        RSA_SHA224 = "sha224WithRSAEncryption"  #: Use sha224WithRSAEncryption (rsa-sha224) signature algorithm
        RSA_SHA256 = "sha256WithRSAEncryption"  #: Use sha256WithRSAEncryption (rsa-sha256) signature algorithm [minimum recommended]
        RSA_SHA384 = "sha384WithRSAEncryption"  #: Use sha384WithRSAEncryption (rsa-sha384) signature algorithm
        RSA_SHA512 = "sha512WithRSAEncryption"  #: Use sha512WithRSAEncryption (rsa-sha512) signature algorithm
        RSA_MD5 = "md5WithRSAEncryption"  #: Use md5WithRSAEncryption (rsa-md5) signature algorithm [ legacy applications only]
        ECDSA_SHA1 = "ecdsaWithSHA1"      #: Use ecdsaWithSHA1 (ecdsa-sha1) signature algorithm
        ECDSA_SHA224 = "ecdsaWithSHA224"  #: Use ecdsaWithSHA224 (ecdsa-sha224) signature algorithm
        ECDSA_SHA256 = "ecdsaWithSHA256"  #: Use ecdsaWithSHA256 (ecdsa-sha256) signature algorithm
        ECDSA_SHA384 = "ecdsaWithSHA384"  #: Use ecdsaWithSHA384 (ecdsa-sha384) signature algorithm
        ECDSA_SHA512 = "ecdsaWithSHA512"  #: Use ecdsaWithSHA512 (ecdsa-sha512) signature algorithm
        RSA_PSS_SHA1 = "RSA-PSS-SHA1"      #: Use RSA-PSS signature algorithm with SHA-1
        RSA_PSS_SHA224 = "RSA-PSS-SHA224"  #: Use RSA-PSS signature algorithm with SHA-224
        RSA_PSS_SHA256 = "RSA-PSS-SHA256"  #: Use RSA-PSS signature algorithm with SHA-256
        RSA_PSS_SHA384 = "RSA-PSS-SHA384"  #: Use RSA-PSS signature algorithm with SHA-384
        RSA_PSS_SHA512 = "RSA-PSS-SHA512"  #: Use RSA-PSS signature algorithm with SHA-512
        ED25519 = "Ed25519"  #: Use Ed25519, the Edwards-curve Digital Signature Algorithm (EdDSA) as per [RFC8032]

    class Opts:
        """Options for ECDSA and RSA-PSS signatures."""
        DEFAULT = 0  #: Use default options for signature.
        DETERMINISTIC = 0x2000  #: ECDSA only: Use the deterministic digital signature generation procedure of [RFC6979] for ECDSA signature [default=random k]
        # Note ASN1DER value changed from 0x200000 to 0x4000 in [v12.0]
        ASN1DER = 0x4000  #: ECDSA only: Form ECDSA signature value as a DER-encoded ASN.1 structure [default= ``r||s``].
        PSS_SALTLEN_HLEN = 0x000000  #: RSA-PSS only: Set the salt length to hLen, the length of the output of the hash function [default].
        PSS_SALTLEN_MAX = 0x200000   #: RSA-PSS only: Set the salt length to the maximum possible (like OpenSSL).
        PSS_SALTLEN_20 = 0x300000    #: RSA-PSS only: Set the salt length to be exactly 20 bytes regardless of the hash algorithm.
        PSS_SALTLEN_ZERO = 0x400000  #: RSA-PSS only: Set the salt length to be zero.
        MGF1SHA1 = 0x800000  #: RSA-PSS only: Force the MGF hash function to be SHA-1 [default = same as signature hash algorithm].

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" options.
            return self | other

    class VerifyOpts:
        """Specialist options for verifying a signature."""
        DEFAULT = 0  #: Use default options.
        MGF1SHA1 = 0x800000  #: RSA-PSS only: Force the MGF hash function to be SHA-1 [default = same as signature hash algorithm].

    class Encoding:
        """Encodings for signature output."""
        DEFAULT = 0  #: Default encoding (base64)
        BASE64 = 0   #: Base64 encoding (default)
        HEX       = 0x30000  #: Hexadecimal encoding
        BASE64URL = 0x40000  #: URL-safe base64 encoding as in section 5 of [RFC4648]

    @staticmethod
    def sign_data(data, keyfile, password, alg, opts=Opts.DEFAULT, encoding=Encoding.DEFAULT):
        """Compute a signature value over data in a byte array.

        Args:
            data (bytes): input data to be signed
            keyfile (str): Name of private key file
                (or a string containing the key in PEM format, or an internal private key)
            password (str): Password for the private key, if encrypted
            alg (Sig.Alg): Signature algorithm to be used.
            opts (Sig.Opts): Options for ECDSA signatures.
            encoding (Sig.Encoding): Optional encodings for output.

        Returns:
            str: The encoded signature value.
            By default, a continuous string of base64 characters suitable for the
            ``<SignatureValue>`` of an XML-DSIG document.
        """
        noptions = opts | encoding
        nc = _dipki.SIG_SignData(None, 0, bytes(data), len(data), keyfile.encode(), password.encode(), str(alg).encode(), noptions)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.SIG_SignData(buf, nc, bytes(data), len(data), keyfile.encode(), password.encode(), str(alg).encode(), noptions)
        return buf.value.decode()

    @staticmethod
    def sign_digest(digest, keyfile, password, alg, opts=Opts.DEFAULT, encoding=Encoding.DEFAULT):
        """Compute a signature value over a message digest value.

        Args:
            digest (bytes): digest value in a byte array
            keyfile (str): Name of private key file
                (or a string containing the key in PEM format, or an internal private key)
            password (str): Password for the private key, if encrypted
            alg (Sig.Alg): Signature algorithm to be used.
            opts (Sig.Opts): Options for ECDSA signatures.
            encoding (Sig.Encoding): Optional encodings for output.

        Returns:
            str: The encoded signature value.
        """
        _USEDIGEST = 0x1000
        noptions = opts | encoding | _USEDIGEST
        nc = _dipki.SIG_SignData(None, 0, bytes(digest), len(digest), keyfile.encode(), password.encode(), str(alg).encode(), noptions)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.SIG_SignData(buf, nc, bytes(digest), len(digest), keyfile.encode(), password.encode(), str(alg).encode(), noptions)
        return buf.value.decode()

    @staticmethod
    def sign_file(datafile, keyfile, password, alg, opts=Opts.DEFAULT, encoding=Encoding.DEFAULT):
        """Compute a signature value over binary data in a file.

        Args:
            datafile (str): Name of input file containing data to be signed.
            keyfile (str): Name of private key file
                (or a string containing the key in PEM format, or an internal private key)
            password (str): Password for the private key, if encrypted
            alg (Sig.Alg): Signature algorithm to be used.
            opts (Sig.Opts): Options for ECDSA signatures.
            encoding (Sig.Encoding): Optional encodings for output.

        Returns:
            str: The encoded signature value.
        """
        noptions = opts | encoding
        nc = _dipki.SIG_SignFile(None, 0, datafile.encode(), keyfile.encode(), password.encode(), str(alg).encode(), noptions)
        if (nc < 0): raise PKIError(-nc)
        if (nc == 0): return ""
        buf = create_string_buffer(nc + 1)
        nc = _dipki.SIG_SignFile(buf, nc, datafile.encode(), keyfile.encode(), password.encode(), str(alg).encode(), noptions)
        return buf.value.decode()

    @staticmethod
    def data_is_verified(sig, data, certorkey, alg, verifyopts=VerifyOpts.DEFAULT):
        """Verify a signature value over data in a byte array.

        Args:
            sig (str): Containing the encoded signature value
            data (bytes): Containing the input data to be verified
            certorkey (str): Specifying the X.509 certificate or public key file name
                (or a string containing the certificate or key in PEM format or base64 representation,
                or an internal key string).
            alg (Sig.Alg): Signature algorithm to be used
            verifyopts (Sig.VerifyOpts): Advanced options for RSA-PSS only.

        Returns:
            bool: True if the signature is valid, False if invalid.

        Raises:
            PKIError: If parameters or formats are bad, or if file is missing.

        Remarks:
            A signature value is considered valid if it can be decrypted by the public key
            in ``certorkey`` and the digest value of the data matches the original digest
            of the data in the signature.
            Public keys in X.509 certificates are currently not supported for ECDSA signatures;
            only public key files or their string representations.
            Any supported encodings of the signature value are detected automatically.
        """
        n = _dipki.SIG_VerifyData(sig.encode(), bytes(data), len(data), certorkey.encode(), str(alg).encode(), verifyopts)
        # Catch straightforward invalid signature error
        _SIGNATURE_ERROR = -22  # Changed in v11.3
        if (n == _SIGNATURE_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc)
        if (n < 0): raise PKIError(-n)
        return True

    @staticmethod
    def digest_is_verified(sig, digest, certorkey, alg, verifyopts=VerifyOpts.DEFAULT):
        """Verify a signature value over a message digest value of data .

        Args:
            sig (str): Containing the encoded signature value
            digest (bytes): Byte array containing the message digest value of the data to be verified
            certorkey (str): Specifying the X.509 certificate or public key file name
                (or a string containing the certificate or key in PEM format or base64 representation,
                or an internal key string).
            alg (Sig.Alg): Signature algorithm to be used
            verifyopts (Sig.VerifyOpts): Advanced options for RSA-PSS only.

        Returns:
            bool: True if the signature is valid, False if invalid.

        Raises:
            PKIError: If parameters or formats are bad, or if file is missing.
        """
        _USEDIGEST = 0x1000
        n = _dipki.SIG_VerifyData(sig.encode(), bytes(digest), len(digest), certorkey.encode(), str(alg).encode(), _USEDIGEST | verifyopts)
        # Catch straightforward invalid signature error
        _SIGNATURE_ERROR = -22  # Changed in v11.3
        if (n == _SIGNATURE_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc)
        if (n < 0): raise PKIError(-n)
        return True

    @staticmethod
    def file_is_verified(sig, datafile, certorkey, alg, verifyopts=VerifyOpts.DEFAULT):
        """Verify a signature value over data in a file.

        Args:
            sig (str): Containing the encoded signature value
            datafile (str): Name of file containing data to be verified.
            certorkey (str): Specifying the X.509 certificate or public key file name
                (or a string containing the certificate or key in PEM format or base64 representation,
                or an internal key string).
            alg (Sig.Alg): Signature algorithm to be used
            verifyopts (Sig.VerifyOpts): Advanced options for RSA-PSS only.

        Returns:
            bool: True if the signature is valid, False if invalid.

        Raises:
            PKIError: If parameters or formats are bad, or if file is missing.
        """
        n = _dipki.SIG_VerifyFile(sig.encode(), datafile.encode(), certorkey.encode(), str(alg).encode(), verifyopts)
        # Catch straightforward invalid signature error
        _SIGNATURE_ERROR = -22  # Changed in v11.3
        if (n == _SIGNATURE_ERROR): return False
        # Raise error for other errors (bad params, missing file, etc)
        if (n < 0): raise PKIError(-n)
        return True


class Smime:
    """S/MIME entity utilities."""

    class Opts():
        """Options for S/MIME methods."""
        ENCODE_BASE64 = 0x10000  #: Encode output in base64
        ENCODE_BINARY = 0x20000  #: Encode body in binary encoding
        ADDX = 0x100000  #: Add an "x-" to the content subtype (for compatibility with legacy applications)

    @staticmethod
    def wrap(outputfile, inputfile, opts=0):
        """Wrap a CMS object in an S/MIME entity.

        Args:
            outputfile (str): Output file to be created
            inputfile (str): Input file containing CMS object.
                Expected to be a binary CMS object of type enveloped-data,
                signed-data or compressed-data; otherwise it is an error.
                The type of input file is detected automatically.
            opts (Smime.Opts): Options.

        Returns:
            int: A positive number giving the size of the output file in bytes.
        """
        n = _dipki.SMIME_Wrap(outputfile.encode(), inputfile.encode(), b"", opts)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def extract(outputfile, inputfile, opts=0):
        """Extract the body from an S/MIME entity.

        This is designed to extract the body from an S/MIME entity with a content type of
        ``application/pkcs7-mime`` with base64 or binary transfer encoding.
        In practice, it will extract the body from almost any type of S/MIME (or MIME) file,
        except one with quoted-printable transfer encoding.

        Args:
            outputfile (str): Name of output file to be created
            inputfile (str): Name of input file containing S/MIME entity
            opts (Smime.Opts): Options.
                By default the output is encoded in binary.
                Use `Opts.ENCODE_BASE64` to encode the output in base64.

        Returns:
            int: A positive number giving the size of the output file in bytes.
        """
        n = _dipki.SMIME_Extract(outputfile.encode(), inputfile.encode(), opts)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def query(filename, query):
        """Query an S/MIME entity for selected information.

        Args:
            filename (str): Name of file containing S/MIME entity.
            query (str): Query string (case insensitive). Valid queries are:

                * ``"content-type"`` -- Value of Content-Type, e.g. "application/pkcs7-mime".
                * ``"smime-type"`` -- Value of smime-type parameter of Content-Type, e.g. "enveloped-data".
                * ``"encoding"`` -- Value of Content-Transfer-Encoding, e.g. "base64".
                * ``"name"`` -- Value of name parameter of Content-Type, e.g. "smime.p7m".
                * ``"filename"`` -- Value of filename parameter of Content-Disposition, e.g. "smime.p7m".

        Returns:
            Result of query if found or an empty string if not found.
        """
        nc = _dipki.SMIME_Query(None, 0, filename.encode(), query.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.SMIME_Query(buf, nc, filename.encode(), query.encode(), 0)
        return buf.value.decode()


class Wipe:
    """Wipe data securely."""
    class Options:
        """Wipe options."""
        DEFAULT = 0x0    #: Default options (DOD 7-pass).
        DOD7PASS  = 0x0  #: DOD 7-pass (default).
        SIMPLE    = 0x1  #: Overwrite with single pass of zero bytes (quicker but less secure).

    @staticmethod
    def file(filename, opts=Options.DEFAULT):
        """Securely wipe and delete a file.

        Args:
            filename (str): Name of file to be wiped.
            opts (Wipe.Options): Options.
        """
        n = _dipki.WIPE_File(filename.encode(), opts)
        if (n != 0): raise PKIError(-n if n < 0 else n)

    @staticmethod
    def data(data):
        """Zeroize data in memory.

        Args:
            data (bytes): data to be wiped.
        """
        n = _dipki.WIPE_Data(bytes(data), len(data))
        if (n != 0): raise PKIError(-n if n < 0 else n)


class X509:
    """Create and manage X.509 certificates."""
    # CONSTANTS
    class KeyUsageFlags:
        """Bitwise flags for key usage in certificate."""
        NONE = 0    #: None
        DIGITALSIGNATURE  = 0x0001  #: Set the ``digitalSignature`` bit
        NONREPUDIATION    = 0x0002  #: Set the ``nonRepudiation`` (``contentCommitment``) bit
        KEYENCIPHERMENT   = 0x0004  #: Set the ``keyEncipherment`` bit
        DATAENCIPHERMENT  = 0x0008  #: Set the ``dataEncipherment`` bit
        KEYAGREEMENT      = 0x0010  #: Set the ``keyAgreement`` bit
        KEYCERTSIGN       = 0x0020  #: Set the ``keyCertSign`` bit
        CRLSIGN           = 0x0040  #: Set the ``cRLSign`` bit
        ENCIPHERONLY      = 0x0080  #: Set the ``encipherOnly`` bit
        DECIPHERONLY      = 0x0100  #: Set the ``decipherOnly`` bit

    class Opts:
        """
        Various option flags used by some methods of this class.
        Combine using 'bitwise or' operator ``|``.
        Ignored if not applicable for the particular method.
        Check manual for details.
        """
        FORMAT_PEM     = 0x10000  #: Create in PEM-encoded format (default for CSR)
        FORMAT_BIN     = 0x20000  #: Create in binary format (default for X.509 cert and CRL)
        REQ_KLUDGE    = 0x100000  #: Create a request with the "kludge" that omits the strictly mandatory attributes completely [default = include attributes with zero-length field]
        NO_TIMECHECK  = 0x200000  #: Avoid checking if the certificates are valid now (default = check validity dates against system clock)
        # LATIN1        = 0x400000  #: Re-encode Unicode or UTF-8 string as Latin-1, if possible [REDUNDANT?]
        UTF8          = 0x800000  #: Encode distinguished name as UTF8String [default = PrintableString]
        AUTHKEYID    = 0x1000000  #: Add the issuer's KeyIdentifier, if present, as an AuthorityKeyIdentifer [default = do not add]
        NO_BASIC     = 0x2000000  #: Disable the BasicConstraints extension [default = include]
        CA_TRUE      = 0x4000000  #: Set the BasicConstraints subject type to be a CA [default = End Entity]
        VERSION1     = 0x8000000  #: Create a Version 1 certificate, i.e. no extensions [default = Version 3]
        LDAP            = 0x1000  #: Output distinguished name in LDAP string representation
        DECIMAL         = 0x8000  #: Output serial number in decimal format [default = hex]
        DETERMINISTIC   = 0x2000  #: Use the deterministic signature generation procedure of [RFC6979] for an ECDSA signature.
        SALTLEN_ZERO    =  0x300  #: Use a zero-length salt in an RSA-PSS signature.

        def __or__(self, other):
            # Define this to avoid warnings when we try to "or" opts with another class.
            return self | other

    class SigAlg:
        """Signature algorithm to use for signatures."""
        RSA_SHA1   = 0x0  #: Sign with sha1WithRSAEncryption (rsa-sha1) [default]
        RSA_SHA224 = 0x6  #: Sign with sha224WithRSAEncryption (rsa-sha224)
        RSA_SHA256 = 0x3  #: Sign with sha256WithRSAEncryption (rsa-sha256) [minimum recommended]
        RSA_SHA384 = 0x4  #: Sign with sha384WithRSAEncryption (rsa-sha384)
        RSA_SHA512 = 0x5  #: Sign with sha512WithRSAEncryption (rsa-sha512) signature algorithm
        RSA_MD5    = 0x1  #: Sign with md5WithRSAEncryption (rsa-md5) signature algorithm [legacy applications only]
        RSA_PSS_SHA1   = 0xB0   #: Sign with RSA-PSS using SHA-1
        RSA_PSS_SHA224 = 0xB6   #: Sign with RSA-PSS using SHA-224
        RSA_PSS_SHA256 = 0xB3   #: Sign with RSA-PSS using SHA-256
        RSA_PSS_SHA384 = 0xB4   #: Sign with RSA-PSS using SHA-384
        RSA_PSS_SHA512 = 0xB5   #: Sign with RSA-PSS using SHA-512
        ECDSA_SHA1   = 0x10  #: Sign with ecdsaWithSHA1
        ECDSA_SHA224 = 0x20  #: Sign with ecdsaWithSHA224
        ECDSA_SHA256 = 0x30  #: Sign with ecdsaWithSHA256
        ECDSA_SHA384 = 0x40  #: Sign with ecdsaWithSHA384
        ECDSA_SHA512 = 0x50  #: Sign with ecdsaWithSHA512
        ED25519      = 0xC0  #: Sign with Ed25519

    class HashAlg:
        """Digest algorithms for hashes."""
        SHA1   = 0  #: SHA-1 (default)
        SHA224 = 6  #: SHA-224
        SHA256 = 3  #: SHA-256
        SHA384 = 4  #: SHA-384
        SHA512 = 5  #: SHA-512
        MD5    = 1  #: MD5 (as per RFC 1321)

    @staticmethod
    def make_cert(newcertfile, issuercert, subject_pubkeyfile, issuer_prikeyfile, password, certnum, yearsvalid, distname, extns="", keyusage=0, sigalg=0, opts=0):
        """Create an X.509 certificate using subject's public key and issuer's private key.

        Args:
            newcertfile (str): Name of file to be created.
            issuercert (str): Name of issuer's certificate file.
            subject_pubkeyfile (str): File containing subject's public key data, or a string containing its PEM textual representation.
            issuer_prikeyfile (str): File containing issuer's private key data, or a string containing its PEM textual representation.
            password (str): Password for issuer's private key.
            certnum (int): Serial number for new certificate.
            yearsvalid (int): Number of years to be valid.
            distname (str): Distinguished name string. See
                `Distinguished Names <https://www.cryptosys.net/pki/manpki/pki_distnames.html>`_ in the main manual.
            extns (str): Extensions: a list of attribute-value pairs separated by semicolons (;).
                See `X.509 Extensions Parameter <https://www.cryptosys.net/pki/manpki/pki_x509extensions.html>`_
                in the main manual.
            keyusage (X509.KeyUsageFlags): Key usage options.
            sigalg (X509.SigAlg): Signature algorithm to use when signing.
            opts (X509.Opts): Option flags.

        Returns:
            int: Zero if successful.
        """
        # Note order of params is different from C version (password is not optional)
        n = _dipki.X509_MakeCert(
            newcertfile.encode(), issuercert.encode(), subject_pubkeyfile.encode(),
            issuer_prikeyfile.encode(), certnum, yearsvalid, distname.encode(), extns.encode(), keyusage,
            password.encode(), opts | sigalg)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_cert_self(newcertfile, prikeyfile, password, certnum, yearsvalid, distname, extns="", keyusage=0, sigalg=0, opts=0):
        """Create a self-signed X.509 certificate.

        Args:
            newcertfile (str): Name of file to be created.
            prikeyfile (str): File containing issuer's private key data, or a string containing its PEM textual representation.
            password (str): Password for issuer's private key.
            certnum (int): Serial number for new certificate.
            yearsvalid (int): Number of years to be valid.
            distname (str): Distinguished name string. See
                `Distinguished Names <https://www.cryptosys.net/pki/manpki/pki_distnames.html>`_ in the main manual.
            extns (str): Extensions: a list of attribute-value pairs separated by semicolons (;).
                See `X.509 Extensions Parameter <https://www.cryptosys.net/pki/manpki/pki_x509extensions.html>`_
                in the main manual.
            keyusage (X509.KeyUsageFlags): Key usage options.
            sigalg (X509.SigAlg): Signature algorithm to use when signing.
            opts (X509.Opts): Option flags.

        Returns:
            int: Zero if successful.
        """
        # Note order of params is different from C version (password is not optional)
        n = _dipki.X509_MakeCertSelf(
            newcertfile.encode(), prikeyfile.encode(), certnum, yearsvalid, distname.encode(),
            extns.encode(), keyusage, password.encode(), opts | sigalg)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def cert_request(newcsrfile, prikeyfile, password, distname, extns="", sigalg=0, opts=0):
        """Create a PKCS #10 certificate signing request (CSR).

        Args:
            newcsrfile (str): Name of file to be created.
            prikeyfile (str): File containing issuer's private key data, or a string containing its PEM textual representation.
            password (str): Password for issuer's private key.
            distname (str): Distinguished name string. See
                `Distinguished Names <https://www.cryptosys.net/pki/manpki/pki_distnames.html>`_ in the main manual.
            extns (str): Extensions: a list of attribute-value pairs separated by a semicolon (;)
                to be included in an ``extensionRequest`` field.
                See `X.509 Extensions Parameter <https://www.cryptosys.net/pki/manpki/pki_x509extensions.html>`_
                in the main manual.
            sigalg (X509.SigAlg): Signature algorithm to use when signing.
            opts (X509.Opts): Option flags.

        Returns:
            int: Zero if successful.
        """
        # Note order of params is different from C version (password is not optional)
        n = _dipki.X509_CertRequest(newcsrfile.encode(), prikeyfile.encode(), distname.encode(), extns.encode(), password.encode(), opts | sigalg)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def make_crl(newcrlfile, issuercert, prikeyfile, password, revokedcertlist="", extns="", sigalg=0, opts=0):
        r"""Create an X.509 Certificate Revocation List (CRL). Version 1 only.

        Args:
            newcrlfile (str): name of new CRL file to be created.
            issuercert (str): name of issuer's X.509 certificate file (or its base64 representation).
            prikeyfile (str): name of issuer's encrypted private key file, or a string containing its PEM textual representation.
            password (str): password for Issuer's encrypted private key file.
            revokedcertlist (str): list of revoked certificates in format.
                ``serialNumber,revocationDate; ...`` or the empty string ``""``
                for no revoked certificates. See the Remarks section below for more details
            extns (str): Extensions: a list of attribute-value pairs separated by a semicolon (;).
                Valid attribute-value pairs are:

                * ``lastUpdate``\=<iso-date-string>
                * ``nextUpdate``\=<iso-date-string>

            sigalg (X509.SigAlg): Signature algorithm to use when signing.
            opts (X509.Opts): Option flags.


        Returns:
            int: Zero if successful.

        Remarks:
            This creates a version 1 CRL file with no extensions or cRLReason's.
            The parameter ``revokedCertList`` must be in the form
            ``serialNumber,revocationDate;serialNumber,revocationDate; ...``.
            The serialNumber must either be a positive decimal integer (e.g. ``123``)
            or the number in hex format preceded by #x (e.g. ``#x0102deadbeef``).
            The revocation date must be in ISO date format (e.g. ``2009-12-31T12:59:59Z``).
            For example::

                "1,2007-12-31; 2, 2009-12-31T12:59:59Z; 66000,2066-01-01; #x0102deadbeef,2010-02-28T01:01:59"

            By default, the ``lastUpdate`` time in the CRL is set to the time given by the system clock,
            and ``nextUpdate`` time is left empty.
            You can specify your own times using the ``lastUpdate`` and ``nextUpdate`` attributes
            in the extensions parameter.
            Times, if specified, must be in ISO 8601 format and are always interpreted as GMT times whether or not you add a "Z".
        """
        n = _dipki.X509_MakeCRL(newcrlfile.encode(), issuercert.encode(), prikeyfile.encode(), password.encode(), revokedcertlist.encode(), extns.encode(), opts | sigalg)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def text_dump(outputfile, certfile, opts=0):
        """Dump details of X.509 certificate (or CRL or CSR) to a text file.

        Args:
            outputfile (str): Filename of text file to be created.
            certfile (str): Filename of certificate file (or its base64 representation).
            opts (X509.Opts): Option flags for output formatting, e.g. ``X509.Opts.Ldap``.

        Returns:
            int: Zero if successful.
        """
        n = _dipki.X509_TextDump(outputfile.encode(), certfile.encode(), 0)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def text_dump_tostring(certfile, opts=0):
        """Dump details of X.509 certificate (or CRL or CSR) to a string.

        Args:
            certfile (str): Filename of certificate file (or its base64 representation).
            opts (X509.Opts): Option flags for output formatting, e.g. ``X509.Opts.Ldap``.

        Returns:
            str: Result of text dump.
        """
        nc = _dipki.X509_TextDumpToString(None, 0, certfile.encode(), opts)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.X509_TextDumpToString(buf, nc, certfile.encode(), opts)
        return buf.value.decode()

    @staticmethod
    def query_cert(filename, query, opts=0):
        """Query an X.509 certificate file for selected information. May return an integer or a string.

        Args:
            filename (str): Name of file to be queried (or its base64 representation).
            query (str): Query string (case insensitive). Valid queries are:

                * ``"version"`` -- X.509 version number, e.g. ``3``.
                * ``"serialNumber"`` -- Serial number in hex-encoded format.
                * ``"signatureAlgorithm"`` -- Signature algorithm used, e.g. "sha1WithRSAEncryption".
                * ``"sigAlgId"`` -- ID of signature algorithm used. See :py:class:`X509.SigAlg`.
                * ``"signatureValue"`` -- Signature value in hex-encoded format.
                * ``"notBefore"`` -- Date on which the certificate validity period begins in ISO format yyyy-mm-ddThh:nn:ssZ
                * ``"notAfter"`` -- Date on which the certificate validity period ends in ISO format yyyy-mm-ddThh:nn:ssZ
                * ``"issuerName"`` -- Distinguished name (DN) of entity who has signed and issued the certificate.
                * ``"subjectName"`` -- Distinguished name (DN) of the subject.
                * ``"subjectPublicKeyAlgorithm"`` -- Algorithm used in subject's public key, e.g. "dsa".
                * ``"subjectKeyIdentifier"`` -- The subject key identifier extension, if present, in hex-encoded format.
                * ``"authorityKeyIdentifier"`` -- The authority key identifier extension, if present, in hex-encoded format.
                * ``"rfc822Name"`` -- Internet mail address contained in a subjectAltName extension, if present.
                * ``"isCA"`` -- Returns ``1`` -- if the subject type is a CA, otherwise returns ``0``.
                * ``"keyUsageString"`` -- keyUsage flags in text format, e.g. "digitalSignature,nonRepudiation".
                * ``"extKeyUsageString"`` -- extKeyUsage purposes in text format, e.g. "codeSigning,timeStamping".
                * ``"cRLDistributionPointsURI"`` -- First URI found in cRLDistributionPoints, if any.
                * ``"authorityInfoAccessURI"`` -- First URI found in authorityInfoAccess, if any.
                * ``"subjectAltName"`` -- Subject alternative name extension, if present.
                * ``"hashAlgorithm"`` -- Hash algorithm used in signature, e.g. "sha256".
                * ``"pssParams"`` -- Parameters used for RSA-PSS (if applicable).

            opts (X509.Opts): Option flags for output formatting, e.g. ``X509.Opts.Ldap``.

        Returns:
            Result of query or an empty string if query not found.
        """
        _QUERY_GETTYPE = 0x100000
        _QUERY_STRING = 2
        # Find what type of result to expect: number or string (or error)
        n = _dipki.X509_QueryCert(None, 0, filename.encode(), query.encode(), _QUERY_GETTYPE)
        if (n < 0): raise PKIError(-n)
        if (_QUERY_STRING == n):
            nc = _dipki.X509_QueryCert(None, 0, filename.encode(), query.encode(), opts)
            if (nc < 0): raise PKIError(-nc)
            buf = create_string_buffer(nc + 1)
            nc = _dipki.X509_QueryCert(buf, nc, filename.encode(), query.encode(), opts)
            return buf.value.decode()
        else:
            n = _dipki.X509_QueryCert(None, 0, filename.encode(), query.encode(), opts)
            return n

    @staticmethod
    def read_string_from_file(certfilename):
        """Create a base64 string representation of an X.509 certificate.

        Args:
            certfilename (str): Filename of certificate file (or its base64 representation).

        Returns:
            str: String in continuous base64 format.
        """
        nc = _dipki.X509_ReadStringFromFile(None, 0, certfilename.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.X509_ReadStringFromFile(buf, nc, certfilename.encode(), 0)
        return buf.value.decode()

    @staticmethod
    def save_file_from_string(newcertfile, certstring, in_pem_format=False):
        """Create an X.509 certificate file from its base64 string representation.

        Args:
            newcertfile (str): Name of new certificate file to be created.
            certstring (str): String containing certificate data in base64 format.
            in_pem_format (bool): True to save in base64 PEM format, or False to save in binary DER format.
                A PEM format file starts with ``-----BEGIN CERTIFICATE-----``.

        Returns:
            int: Zero if successful.
        """
        fileformat = X509.Opts.FORMAT_PEM if in_pem_format else 0
        n = _dipki.X509_SaveFileFromString(newcertfile.encode(), certstring.encode(), fileformat)
        if (n != 0): raise PKIError(-n if n < 0 else n)
        return n

    @staticmethod
    def key_usage_flags(certfile):
        """Return a bitfield containing the keyUsage flags for an X.509 certificate.

        Args:
            certfile (str): Filename of certificate file (or its base64 representation).

        Returns:
            int: A positive integer containing the ``keyUsage`` flags as a bitfield,
            or 0 if no ``keyUsage`` flags are set.
            See :py:class:`X509.KeyUsageFlags` for values.
        """
        n = _dipki.X509_KeyUsageFlags(certfile.encode())
        if (n < 0): raise PKIError(-n)
        return n & 0xFFFFFFFF

    @staticmethod
    def cert_thumb(certfilename, hashalg=0):
        """Return the thumbprint (message digest hash) of an X.509 certificate.

        Args:
            certfilename (str): Filename of certificate file (or its base64 representation).
            hashalg (X509.HashAlg): Message digest algorithm to use.

        Returns:
            string: String containing the message digest in hexadecimal format
        """
        nc = _dipki.X509_CertThumb(certfilename.encode(), None, 0, hashalg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.X509_CertThumb(certfilename.encode(), buf, nc, hashalg)
        return buf.value.decode()

    @staticmethod
    def cert_hashissuersn(certfilename, hashalg=0):
        """Return the hash of the issuer and serial number.

        This should give a unique identifier for any certificate.

        Args:
            certfilename (str): Filename of certificate file (or its base64 representation).
            hashalg (X509.HashAlg): Message digest algorithm to use.

        Returns:
            string: String containing the message digest in hexadecimal format.
        """
        nc = _dipki.X509_HashIssuerAndSN(certfilename.encode(), None, 0, hashalg)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.X509_HashIssuerAndSN(certfilename.encode(), buf, nc, hashalg)
        return buf.value.decode()

    @staticmethod
    def cert_is_valid_now(certfile):
        """Verify that an X.509 certificate is currently valid as per system clock.

        Args:
            certfile (str): Filename of certificate file (or its base64 representation).

        Returns:
            bool: True if certificate is currently valid, False if certificate has expired or is not yet valid.
        """

        _VALID_NOW = 0
        _EXPIRED   = +16    # Changed in v11.3
        n = _dipki.X509_CertIsValidNow(certfile.encode(), 0)
        if (_VALID_NOW == n):
            isvalid = True
        elif (_EXPIRED == n):
            isvalid = False
        else:
            raise PKIError(-n if n < 0 else n)
        return isvalid

    @staticmethod
    def cert_is_revoked(certfile, crlfile, crl_issuercert="", isodate=""):
        """Check whether an X.509 certificate has been revoked in a given Certificate Revocation List (CRL).

        Args:
            certfile (str): name of X.509 certificate to be checked (or base64 representation).
            crlfile (str): name of CRL file, or a string containing its PEM textual representation.
            crl_issuercert (str): (optional) name of X.509 certificate file for the entity that issued the CRL
                (or its base64 representation). If given, the signature of the CRL will be checked
                against the key in the issuer's certificate and
                a `SIGNATURE_ERROR` will result if the signature is invalid.
                Leave empty to omit this check.
            isodate (str): (optional) date in ISO format (``yyyy-mm-dd[Thh[:nn:ss]][Z]``) on or after
                you wish to check for revocation. Leave empty ""  for any date.
                The time must be in GMT (UTC, Zulu time).

        Returns:
            bool: True if the certificate has been revoked, False if not found in the revoked list.

        """
        _REVOKED = 42   # Changed in v11.3
        n = _dipki.X509_CheckCertInCRL(certfile.encode(), crlfile.encode(), crl_issuercert.encode(), isodate.encode(), 0)
        if (n < 0): raise PKIError(-n)
        return (_REVOKED == n)

    @staticmethod
    def cert_is_verified(certfile, issuercert):
        """Verify that an X.509 certificate has been signed by its issuer.

        This can also be used to verify that an X.509 Certificate Revocation List (CRL)
        or PKCS#10 Certification Signing Request (CSR) has been signed by the owner of the issuer's certificate.

        Args:
            certfile (str): Filename of certificate (or CRL or CSR) to verify, or a string containing its PEM textual representation.
            issuercert (str): Filename of purported issuer's certificate.

        Returns:
            bool: True if the certificate's signature is verified, or False if the verification fails.
        """

        # Legacy anomaly with *positive* error code
        _SUCCESS = 0
        _FAILURE = 22   # Changed in v11.3
        n = _dipki.X509_VerifyCert(certfile.encode(), issuercert.encode(), 0)
        if (_SUCCESS == n):
            isvalid = True
        elif (_FAILURE == n):
            isvalid = False
        else:
            raise PKIError(-n if n < 0 else n)
        return isvalid

    @staticmethod
    def cert_path_is_valid(certlist, trustedcert="", no_timecheck=False):
        """Validate a certificate path.

        Args:
            certlist (str): either a list of certificate names separated by a semicolon
                or the name of a PKCS-7 "certs-only" file containing the certificates to be validated.
            trustedcert (str): name of the trusted certificate (or base64 representation).
            no_timecheck (bool): Set True to avoid checking if the certificates are valid now,
                otherwise check each certificate's validity dates against system clock.

        Returns:
            bool: True if the certification path is valid, or False if path is invalid.
        """
        _SUCCESS = 0
        _INVALID = +43  # Changed in v11.3
        flags = X509.Opts.NO_TIMECHECK if no_timecheck else 0
        n = _dipki.X509_ValidatePath(certlist.encode(), trustedcert.encode(), flags)
        if (_SUCCESS == n):
            isvalid = True
        elif (_INVALID == n):
            isvalid = False
        else:
            raise PKIError(-n if n < 0 else n)
        return isvalid

    @staticmethod
    def get_cert_count_from_p7(p7file):
        """Return number of certificates in a PKCS-7 "certs-only" certificate chain file.

        Args:
            p7file (str): Name of the PKCS-7 "certs-only" file, or a string containing its PEM textual representation.

        Returns:
            int: Number of X.509 certificates found.
        """
        n = _dipki.X509_GetCertCountInP7Chain(p7file.encode(), 0)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def get_cert_from_p7(outfile, p7file, index=1):
        """Extract an X.509 certificate from a PKCS-7 "certs-only" certificate chain file,
        saving the output directly as a new file.

        Args:
            outfile (str): Name of output file to be created.
            p7file (str): Name of the PKCS-7 "certs-only" file, or a string containing its PEM textual representation.
            index (int): specifying which certificate (1,2,...) in the chain to extract.

        Returns:
            int: If successful, it returns the number of bytes written to the output file.
        """
        if (index <= 0): raise PKIError("Invalid index: " + str(index))
        n = _dipki.X509_GetCertFromP7Chain(outfile.encode(), p7file.encode(), index, 0)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def get_cert_from_pfx(outfile, pfxfile, password):
        """Extract an X.509 certificate from a PKCS-12 PFX/.p12 file, saving the output directly as a new file.

        This will attempt to find a matching certificate for any private key,
        otherwise it will save the first pkcs-12-certBag found in the PFX file containing a x509Certificate.
        Only weak 40-bit RC2 encryption is supported for the certificate.

        Args:
            outfile (str): Name of output file to be created.
            pfxfile (str): Name of the PKCS-12 file, or a string containing its PEM textual representation.
            password (str): Password or "" if not encrypted.

        Returns:
            int: If successful, it returns the number of bytes written to the output file.
        """
        n = _dipki.X509_GetCertFromPFX(outfile.encode(), pfxfile.encode(), password.encode(), 0)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def get_p7chain_from_pfx(outfile, pfxfile, password):
        """Extract all X.509 certificates from a PKCS-12 PFX/.p12 file,
        saving the output directly as a new PKCS-7 "certs-only" certificate chain file.

        Args:
            outfile (str): Name of output file to be created.
            pfxfile (str): Name of the PKCS-12 file, or a string containing its PEM textual representation.
            password (str): Password or "" if not encrypted.
                Only weak 40-bit RC2 encryption is supported for the certificate.

        Returns:
            int: If successful, it returns the number of bytes written to the output file.
        """
        _PKI_PFX_P7CHAIN = 0x0400
        n = _dipki.X509_GetCertFromPFX(outfile.encode(), pfxfile.encode(), password.encode(), _PKI_PFX_P7CHAIN)
        if (n < 0): raise PKIError(-n)
        return n

    @staticmethod
    def read_cert_string_from_p7chain(inputfile, index):
        """Reads an X.509 certificate into a base64 string from PKCS-7 "certs-only" data.

        Args:
            inputfile (str): Name of PKCS-7 "certs-only" file, or a string containing its PEM textual representation.
            index (int): Specifying which certificate (1,2,...) in the chain to extract.

        Returns:
            str: String in continuous base64 format, or an empty string on error.

        Remarks:
            To find the number of certificates in the P7 chain, use :py:class:`X509.get_cert_count_from_p7`.
        """
        if (index <= 0): raise PKIError("Invalid index: " + str(index))
        nc = _dipki.X509_ReadCertStringFromP7Chain(None, 0, inputfile.encode(), index, 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.X509_ReadCertStringFromP7Chain(buf, nc, inputfile.encode(), index, 0)
        return buf.value.decode()

    @staticmethod
    def read_cert_string_from_pfx(inputfile, password):
        """Read an X.509 certificate into a base64 string from PKCS-12 PFX/.p12 data.

        Args:
            inputfile (str): Name of PKCS-12 file, or a string containing its PEM textual representation.
            password (str): Password for PFX or "" if certificate is not encrypted.

        Returns:
            str: String in continuous base64 format, or an empty string on error.
        """
        nc = _dipki.X509_ReadCertStringFromPFX(None, 0, inputfile.encode(), password.encode(), 0)
        if (nc < 0): raise PKIError(-nc)
        buf = create_string_buffer(nc + 1)
        nc = _dipki.X509_ReadCertStringFromPFX(buf, nc, inputfile.encode(), password.encode(), 0)
        return buf.value.decode()


class _NotUsed:
    """Dummy for parsing."""
    pass


# PROTOTYPES (derived from diCrPKI.h)
# If wrong argument type is passed, these will raise an `ArgumentError` exception
#     ArgumentError: argument 1: <type 'exceptions.TypeError'>: wrong type
_dipki.PKI_Version.argtypes = [c_void_p, c_void_p]
_dipki.PKI_LicenceType.argtypes = [c_int]
_dipki.PKI_LastError.argtypes = [c_char_p, c_int]
_dipki.PKI_ErrorCode.argtypes = []
_dipki.PKI_ErrorLookup.argtypes = [c_char_p, c_int, c_int]
_dipki.PKI_CompileTime.argtypes = [c_char_p, c_int]
_dipki.PKI_Platform.argtypes = [c_char_p, c_int]
_dipki.PKI_ModuleName.argtypes = [c_char_p, c_int, c_int]
_dipki.PKI_ModuleInfo.argtypes = [c_char_p, c_int, c_int]
_dipki.PKI_PowerUpTests.argtypes = [c_int]
_dipki.CMS_MakeEnvData.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_int]
_dipki.CMS_MakeEnvDataFromString.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_int]
_dipki.CMS_MakeEnvDataFromBytes.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_int, c_int]
_dipki.CMS_ReadEnvData.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_ReadEnvDataToString.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_ReadEnvDataToBytes.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_MakeSigData.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_MakeSigDataFromString.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_MakeSigDataFromBytes.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.CMS_MakeSigDataFromSigValue.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.CMS_MakeDetachedSig.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_ReadSigData.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CMS_ReadSigDataToString.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CMS_ReadSigDataToBytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CMS_GetSigDataDigest.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.CMS_VerifySigData.argtypes = [c_char_p, c_char_p, c_char_p, c_int]
_dipki.CMS_QuerySigData.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.CMS_QueryEnvData.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.CMS_MakeComprData.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CMS_ReadComprData.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RSA_MakeKeysXtd.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int, c_char_p, c_int]
_dipki.RSA_ReadEncPrivateKey.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_ReadPrivateKeyInfo.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_GetPrivateKeyFromPFX.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RSA_ReadPublicKey.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_GetPublicKeyFromCert.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_SavePublicKey.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RSA_SavePrivateKeyInfo.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RSA_SaveEncKey.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.RSA_SaveEncPrivateKey.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_KeyBits.argtypes = [c_char_p]
_dipki.RSA_KeyBytes.argtypes = [c_char_p]
_dipki.RSA_ToXMLStringEx.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_FromXMLString.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_CheckKey.argtypes = [c_char_p, c_int]
_dipki.RSA_KeyHashCode.argtypes = [c_char_p]
_dipki.RSA_KeyMatch.argtypes = [c_char_p, c_char_p]
_dipki.RSA_ReadPrivateKeyFromPFX.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_PublicKeyFromPrivate.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_ReadAnyPrivateKey.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_ReadAnyPublicKey.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_KeyValue.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_RawPublic.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_RawPrivate.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RSA_EncodeMsg.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.RSA_DecodeMsg.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.RSA_Encrypt.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.RSA_Decrypt.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.ECC_MakeKeys.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.ECC_ReadKeyByCurve.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.ECC_ReadPrivateKey.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.ECC_ReadPublicKey.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.ECC_SaveEncKey.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.ECC_SaveKey.argtypes = [c_char_p, c_char_p, c_int]
_dipki.ECC_PublicKeyFromPrivate.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.ECC_QueryKey.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.ECC_KeyHashCode.argtypes = [c_char_p]
_dipki.ECC_DHSharedSecret.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.PFX_MakeFile.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.PFX_VerifySig.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_MakeCert.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_int, c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.X509_MakeCertSelf.argtypes = [c_char_p, c_char_p, c_int, c_int, c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.X509_CertRequest.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.X509_VerifyCert.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_CertThumb.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_CertIsValidNow.argtypes = [c_char_p, c_int]
_dipki.X509_CertIssuedOn.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_CertExpiresOn.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_CertSerialNumber.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_HashIssuerAndSN.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_CertIssuerName.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.X509_CertSubjectName.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int]
_dipki.X509_GetCertFromP7Chain.argtypes = [c_char_p, c_char_p, c_int, c_int]
_dipki.X509_GetCertCountInP7Chain.argtypes = [c_char_p, c_int]
_dipki.X509_GetCertFromPFX.argtypes = [c_char_p, c_char_p, c_char_p, c_int]
_dipki.X509_KeyUsageFlags.argtypes = [c_char_p]
_dipki.X509_QueryCert.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.X509_ReadStringFromFile.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.X509_SaveFileFromString.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_TextDump.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_TextDumpToString.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.X509_ValidatePath.argtypes = [c_char_p, c_char_p, c_int]
_dipki.X509_MakeCRL.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.X509_CheckCertInCRL.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.X509_ReadCertStringFromP7Chain.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.X509_ReadCertStringFromPFX.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.OCSP_MakeRequest.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.OCSP_ReadResponse.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.TDEA_HexMode.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p]
_dipki.TDEA_B64Mode.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p]
_dipki.TDEA_BytesMode.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p]
_dipki.TDEA_File.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_char_p]
_dipki.CIPHER_Bytes.argtypes = [c_int, c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_File.argtypes = [c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_Hex.argtypes = [c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_KeyWrap.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.CIPHER_KeyUnwrap.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.CIPHER_EncryptBytes.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.CIPHER_DecryptBytes.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.CIPHER_EncryptHex.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_DecryptHex.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.CIPHER_FileEncrypt.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.CIPHER_FileDecrypt.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int]
_dipki.CIPHER_EncryptAEAD.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.CIPHER_DecryptAEAD.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.HASH_Bytes.argtypes = [c_char_p, c_int, c_void_p, c_int, c_int]
_dipki.HASH_File.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.HASH_HexFromBytes.argtypes = [c_char_p, c_int, c_void_p, c_int, c_int]
_dipki.HASH_HexFromFile.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.HASH_HexFromHex.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.HMAC_Bytes.argtypes = [c_char_p, c_int, c_void_p, c_int, c_void_p, c_int, c_int]
_dipki.HMAC_HexFromBytes.argtypes = [c_char_p, c_int, c_void_p, c_int, c_void_p, c_int, c_int]
_dipki.HMAC_HexFromHex.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.CNV_B64StrFromBytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CNV_BytesFromB64Str.argtypes = [c_char_p, c_int, c_char_p]
_dipki.CNV_B64Filter.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CNV_HexStrFromBytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CNV_BytesFromHexStr.argtypes = [c_char_p, c_int, c_char_p]
_dipki.CNV_HexFilter.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CNV_Base58FromBytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CNV_Base58ToBytes.argtypes = [c_char_p, c_int, c_char_p]
# Removed in v12.2: Latin-1/UTF-8 conversions not relevant for Python 3:
# _dipki.CNV_UTF8FromLatin1.argtypes = [c_char_p, c_int, c_char_p]
# _dipki.CNV_Latin1FromUTF8.argtypes = [c_char_p, c_int, c_char_p]
# _dipki.CNV_UTF8BytesFromLatin1.argtypes = [c_char_p, c_int, c_char_p]
# _dipki.CNV_Latin1FromUTF8Bytes.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.CNV_CheckUTF8.argtypes = [c_char_p]
_dipki.CNV_CheckUTF8Bytes.argtypes = [c_char_p, c_int]
_dipki.CNV_CheckUTF8File.argtypes = [c_char_p]
_dipki.CNV_ByteEncoding.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.CNV_ReverseBytes.argtypes = [c_char_p, c_char_p, c_int]
_dipki.CNV_NumToBytes.argtypes = [c_char_p, c_int, c_int, c_int]
_dipki.CNV_NumFromBytes.argtypes = [c_char_p, c_int, c_int]
_dipki.PEM_FileFromBinFile.argtypes = [c_char_p, c_char_p, c_char_p, c_int]
_dipki.PEM_FileFromBinFileEx.argtypes = [c_char_p, c_char_p, c_char_p, c_int, c_int]
_dipki.PEM_FileToBinFile.argtypes = [c_char_p, c_char_p]
_dipki.RNG_Bytes.argtypes = [c_char_p, c_int, c_void_p, c_int]
_dipki.RNG_Number.argtypes = [c_int, c_int]
_dipki.RNG_BytesWithPrompt.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.RNG_Initialize.argtypes = [c_char_p, c_int]
_dipki.RNG_MakeSeedFile.argtypes = [c_char_p, c_char_p, c_int]
_dipki.RNG_UpdateSeedFile.argtypes = [c_char_p, c_int]
_dipki.RNG_Test.argtypes = [c_char_p, c_int]
_dipki.RNG_Guid.argtypes = [c_char_p, c_int, c_int]
_dipki.PAD_BytesBlock.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int, c_int]
_dipki.PAD_UnpadBytes.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int, c_int]
_dipki.PAD_HexBlock.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.PAD_UnpadHex.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.WIPE_File.argtypes = [c_char_p, c_int]
_dipki.WIPE_Data.argtypes = [c_void_p, c_int]
_dipki.PWD_Prompt.argtypes = [c_char_p, c_int, c_char_p]
_dipki.PWD_PromptEx.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.PBE_Kdf2.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_int, c_int]
_dipki.PBE_Kdf2Hex.argtypes = [c_char_p, c_int, c_int, c_char_p, c_char_p, c_int, c_int]
_dipki.ASN1_TextDump.argtypes = [c_char_p, c_char_p, c_int]
_dipki.ASN1_TextDumpToString.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.ASN1_Type.argtypes = [c_char_p, c_int, c_char_p, c_int]
_dipki.SIG_SignData.argtypes = [c_char_p, c_int, c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_int]
_dipki.SIG_SignFile.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.SIG_VerifyData.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.SIG_VerifyFile.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_int]
_dipki.SMIME_Wrap.argtypes = [c_char_p, c_char_p, c_char_p, c_int]
_dipki.SMIME_Extract.argtypes = [c_char_p, c_char_p, c_int]
_dipki.SMIME_Query.argtypes = [c_char_p, c_int, c_char_p, c_char_p, c_int]
_dipki.COMPR_Compress.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
_dipki.COMPR_Uncompress.argtypes = [c_char_p, c_int, c_char_p, c_int, c_int]
