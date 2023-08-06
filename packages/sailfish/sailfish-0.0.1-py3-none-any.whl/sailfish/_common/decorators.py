"""Black Magic decorators.
"""
import functools


def singleton(cls):
    """Make a class a Singleton class (only one instance).
    Args:
        cls: class to make a singleton.
    Returns:
        decorator wrapper class.
    """
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton


def signature(name=None, variable_names=None):
    """Add signature function to the class.
    Args:
        name: name to include in the signature.
        variable_names: names of the variables to include in the signature.
    Returns:
        decorator wrapper function.
    """
    def decorator(cls):
        """Add signature function to the class.
        Args:
            cls: the class to modify.
        Returns:
            modified class.
        """
        nonlocal name, variable_names

        if not variable_names:
            variable_names = []
        if not name:
            name = cls.__name__

        def _signature(self):
            """Signature function.
            Returns:
                A string that represents the instance.
            """
            values = [name] + [str(self.__dict__[var_name]) for var_name in variable_names]
            return "_".join(values)

        setattr(cls, "signature", _signature)

        return cls

    return decorator
