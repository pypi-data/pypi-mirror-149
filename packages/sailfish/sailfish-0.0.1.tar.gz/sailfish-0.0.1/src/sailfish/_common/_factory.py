"""A generic base factory class
"""


class BaseFactory:
    """A base factory class.
    """

    # Internal registry for keeping track of available things to build.
    registry = {}

    @classmethod
    def register(cls, name):
        """Adds cls to the registry under name.

        Args:
            name: name of the model class.
        """
        def inner_wrapper(new_class):
            cls.registry[name] = new_class
            return new_class

        return inner_wrapper

    @classmethod
    def create(cls, name, **kwargs):
        """Factory command to build.

        Args:
            name: the name of the widget to build.
            kwargs: the configuration parameters for the build.

        Returns:
        """
        if name not in cls.registry:
            raise LookupError("\"{}\" not found in registry.".format(name))

        to_del = []
        config = {}
        for key in kwargs:
            if key.endswith("config"):
                if not kwargs[key] is None:
                    config.update(kwargs[key])
                to_del.append(key)

        for key in to_del:
            del kwargs[key]

        return cls.registry[name](**kwargs, **config)
