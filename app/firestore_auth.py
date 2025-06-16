import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("./cred/dragon-forge-cred.json")
    firebase_admin.initialize_app(cred)

def create_user(email, password, display_name):
    """Create a new user with the given email, password y display_name."""
    user = auth.create_user(
        email=email,
        password=password,
        display_name=display_name
    )
    return user.uid

def delete_user(uid):
    """Delete a user with the given UID."""
    try:
        auth.delete_user(uid)
        print(f"Usuario eliminado con éxito: {uid}")
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")

def get_user(uid):
    """Get user information by UID."""
    try:
        user = auth.get_user(uid)
        return user
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return None
    
def get_user_by_email(email):
    """Get user information by email."""
    try:
        user = auth.get_user_by_email(email)
        return user
    except Exception as e:
        print(f"Error al obtener usuario por email: {e}")
        return None

# Obtener datos del usuario
def get_user_data(uid):
    """Get user data by UID."""
    try:
        user = auth.get_user(uid)
        return {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
            "email_verified": user.email_verified,
            "disabled": user.disabled
        }
    except Exception as e:
        print(f"Error al obtener datos del usuario: {e}")
        return None


# print(create_user("fer@gmail.com", "12345678"))
# user = auth.get_user("fhmELcEXhgQME9T9FOPeohEv2gr1")
# user2 = auth.get_user_by_email("fer@gmail.com")
# print(user.EmailIdentifier)
# print(user2.email)

# for user in auth.list_users().iterate_all():
#     print('User: ' + user.uid)

# print(get_user_data("fhmELcEXhgQME9T9FOPeohEv2gr1"))