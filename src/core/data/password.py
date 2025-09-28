import bcrypt


def get_password_hash(password: str):
    salt = bcrypt.gensalt()
    password_enc = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password=password_enc, salt=salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password_enc: str) -> bool:
    plain_password_enc = plain_password.encode("utf-8")
    hashed_password_enc = hashed_password_enc.encode("utf-8")
    return bcrypt.checkpw(
        password=plain_password_enc, hashed_password=hashed_password_enc
    )
