# -----------------------------------------------------------------------------
#
# This file is the copyrighted property of Tableau Software and is protected
# by registered patents and other applicable U.S. and international laws and
# regulations.
#
# Unlicensed use of the contents of this file is prohibited. Please refer to
# the NOTICES.txt file for further details.
#
# -----------------------------------------------------------------------------


class Endpoint:
    """
    A network endpoint to which a connection can be established. Use :any:`HyperProcess.endpoint` to get the
    endpoint to connect to the Hyper process.
    """

    def __init__(self, connection_descriptor: str, user_agent: str):
        self.__descriptor = connection_descriptor
        self.__user_agent = user_agent

    @property
    def connection_descriptor(self) -> str:
        """ The string representation of the endpoint. """
        return self.__descriptor

    @property
    def user_agent(self) -> str:
        """ The user agent. """
        return self.__user_agent

    def __str__(self):
        return self.__descriptor

    def __repr__(self):
        return f'Endpoint({repr(self.__descriptor)}, {repr(self.user_agent)})'
