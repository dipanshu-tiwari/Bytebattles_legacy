from .models import Verdict

def checkExtension(extension):
    allowed_extension = ['c', 'cpp', 'py', 'java']
    for ext in allowed_extension:
        if ext == extension:
            return True
    return False