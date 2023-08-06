def end_point(beautiful_console):
    def wrapper(*args, **kwargs):
        if "get_input" in kwargs or "get_input" in args:
            if "get_input" in kwargs and kwargs["get_input"] is True or "get_input" in args:
                try:
                    text = input(beautiful_console(*args, **kwargs))
                    print("\u001b[0m")
                except KeyboardInterrupt:
                    print("\u001b[0m")
                    exit()
                return text
            else:
                raise AttributeError("\"get_input\" value must be boolean")      
        else:
            return beautiful_console(*args, **kwargs)
    return wrapper
