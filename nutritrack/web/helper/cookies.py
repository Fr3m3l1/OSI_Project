from streamlit_cookies_controller import CookieController

# Centralized cookie controller
controller = CookieController()

# Cookie handling functions
def set_cookie(name, value, expires=3600):
    controller.set(name, value, max_age=expires)

def get_cookie(name):
    return controller.get(name)

def delete_cookie(name):
    controller.remove(name)