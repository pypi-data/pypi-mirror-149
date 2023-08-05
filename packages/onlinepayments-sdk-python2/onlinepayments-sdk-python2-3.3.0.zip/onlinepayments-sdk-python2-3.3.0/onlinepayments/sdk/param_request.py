from abc import ABCMeta, abstractmethod


class ParamRequest(object):
    """
    Represents a set of request parameters.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_request_parameters(self):
        """
        :return: list[:class:`onlinepayments.sdk.RequestParam`] representing the HTTP request parameters
        """
