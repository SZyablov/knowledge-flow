from datetime import datetime

class ProviderNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

# Функция для подсчёта 
def sync_stopwatch(description="unknown"):

    def inner(func):

        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = func(*args, **kwargs)
            end = datetime.now()
            print(f'==> Total time spent ({description}): {(end-start).total_seconds():.2f}s')
            return result
        
        return wrapper
    
    return inner

def stopwatch(description="unknown"):

    def inner(func):

        async def wrapper(*args, **kwargs):
            start = datetime.now()
            result = await func(*args, **kwargs)
            end = datetime.now()
            print(f'==> Total time spent ({description}): {(end-start).total_seconds():.2f}s')
            return result
        
        return wrapper
    
    return inner