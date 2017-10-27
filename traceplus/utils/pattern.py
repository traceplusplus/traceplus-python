# This file is copy from https://github.com/tylerlaberge/PyPattyrn with MIT License

from traceplus.packages import six
from abc import abstractmethod, ABCMeta

class Singleton(type):
    """
    Singleton Metaclass.
    Enforces any object using this metaclass to only create a single instance.
    - External Usage documentation: U{https://github.com/tylerlaberge/PyPattyrn#singleton-pattern}
    - External Singleton Pattern documentation: U{https://en.wikipedia.org/wiki/Singleton_pattern}
    """
    __instance = None

    def __call__(cls, *args, **kwargs):
        """
        Override the __call__ method to make sure only one instance is created.
        """
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args, **kwargs)

        return cls.__instance

class Factory(six.with_metaclass(ABCMeta, object)):
    """
    Factory Interface.
    All Factories should inherit this class and overwrite the create method.
    - External Usage documentation: U{https://github.com/tylerlaberge/PyPattyrn#factory-pattern}
    - External Factory Pattern documentation: U{https://en.wikipedia.org/wiki/Factory_method_pattern}
    """
    @abstractmethod
    def create(self, **kwargs):
        """
        Abstract create method.
        Concrete implementations should return a new instance of the object the factory class is responsible for.
        @param kwargs: Arguments for object creation.
        @return: A new instance of the object the factory is responsible for.
        """
        pass
