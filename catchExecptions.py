def catch_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in function {func.__name__} in file {func.__file__}: {e}")
            return None  
    return wrapper