def checkPassword(password: str):
    if password.count(' ') > 0:
        return False, 'Password can\'t contain spaces'
    elif len(password) < 8 or len(password) > 20:
        return False, 'Password\'s size should be between 8 and 20'
    else:
        return True, 'Registered successfully'