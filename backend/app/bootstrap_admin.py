"""Create the first administrator interactively; never use preset credentials."""
from getpass import getpass
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Role, User
from app.security import hash_password

def main():
    email = input("Administrator email: ").strip().lower()
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise SystemExit("A valid email address is required.")
    password = getpass("New password (minimum 14 characters): ")
    if len(password) < 14:
        raise SystemExit("Password must contain at least 14 characters.")
    confirmation = getpass("Confirm password: ")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")
    with SessionLocal.begin() as db:
        if db.scalar(select(User.id).limit(1)):
            raise SystemExit("An account already exists. Use the approved account recovery process.")
        role = db.scalar(select(Role).where(Role.name == "Super Administrator"))
        if role is None:
            role = Role(name="Super Administrator")
            db.add(role)
            db.flush()
        db.add(User(email=email, password_hash=hash_password(password), roles=[role]))
    print("Initial administrator created. No credential has been printed or stored in source control.")

if __name__ == "__main__":
    main()
