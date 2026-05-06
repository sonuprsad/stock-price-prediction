import pandas as pd
import hashlib

USER_FILE = "users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        users = pd.read_csv(USER_FILE)
    except:
        users = pd.DataFrame(columns=["username","password"])

    if username in users['username'].values:
        return False

    users.loc[len(users)] = [username, hash_password(password)]
    users.to_csv(USER_FILE, index=False)
    return True

def login_user(username, password):
    try:
        users = pd.read_csv(USER_FILE)
    except:
        return False

    if username in users['username'].values:
        stored = users[users['username']==username]['password'].values[0]
        return stored == hash_password(password)

    return False