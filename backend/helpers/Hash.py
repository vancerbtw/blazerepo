import hashlib, binascii, os


class Hash:
    def hash_password(self, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        hashed = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                     salt, 100000)
        hashed = binascii.hexlify(hashed)
        return (salt + hashed).decode('ascii')

    def verify_password(self, stored_pass, inputed):
        """Verify a stored password against one provided by user"""
        salt = stored_pass[:64]
        stored_pass = stored_pass[64:]
        hashed = hashlib.pbkdf2_hmac('sha512',
                                     inputed.encode('utf-8'),
                                     salt.encode('ascii'),
                                     100000)
        hashed = binascii.hexlify(hash).decode('ascii')
        return hash == stored_pass
