from abc import ABC, abstractmethod


class SignatureService(ABC):

    @classmethod
    @abstractmethod
    def verify(cls, **kwargs):
        """
        Verify payment signature.
        """
        raise NotImplementedError