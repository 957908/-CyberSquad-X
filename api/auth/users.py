from api.auth.password import hash_password

users = {
    "admin": {
        "password":
            hash_password(
                "admin123"
            ),
        "role":
            "admin"
    },

    "analyst": {
        "password":
            hash_password(
                "analyst123"
            ),
        "role":
            "analyst"
    },

    "viewer": {
        "password":
            hash_password(
                "viewer123"
            ),
        "role":
            "viewer"
    }
}