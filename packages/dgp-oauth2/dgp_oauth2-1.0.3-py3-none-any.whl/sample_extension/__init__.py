def on_new_user(user_info={}):
    user_info['id'] = 'new-user'


def on_user_login(user_info={}):
    user_info['id'] = 'user-login'


def on_user_logout(user_info={}):
    user_info['id'] = 'user-logout'
