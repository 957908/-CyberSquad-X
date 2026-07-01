import hashlib

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def verify_password(
    plain,
    hashed
):
    return (
        hashlib.sha256(
            plain.encode()
        ).hexdigest()
        == hashed
    )