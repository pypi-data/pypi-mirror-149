# ##################################################################
#
# Copyright 2022 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: pt186002@teradata.com
# Secondary Owner:
#
# This file defines exceptions related to tdapiclient library
# ##################################################################

class TDApiClientException(Exception):
    """
    TDApiClient exception class
    All public functions and methods should only raise TDApiClientException so
    that application code need only catch TDApiClientException.

    Internal functions should let other exceptions from the driver bubble up.
    If internal functions would like to do something in a try: except: block
    like logging, then it should use the form.
        try:
            # do something useful
        except:
            logger.log ("log something useful")
            # re-raise the error so that it is caught by the
            # calling public function.
            raise

    If TDApiClientException was the result of another exception, then the
    attribute __cause__ will be set with the root cause exception.
    """
    def __init__(self, msg, code=1000):
        """
        DESCRIPTION:
            Initializer for TDApiClientException. Call the parent class
            initializer and set the code.

        PARAMETERS:
            msg:
                Required Argument.
                The error message, should be a standard message from
                messages._getMessage().

            code:
                Optional Argument.
                The code, should be from MessageCodes like
                ErrorInfoCodes.SG_CLASS_NOT_FOUND.
                Default Value: 1000

        RETURNS:
            A TDApiClientException with the error message and code.

        RAISES:
            None.

        EXAMPLES:
            if key not in columnnames:
                raise TDApiClientException(message._getMessage(
                    MessageCodes.SG_CLASS_NOT_FOUND),
                    ErrorInfoCodes.SG_CLASS_NOT_FOUND)
        """
        super(TDApiClientException, self).__init__(msg)
        self.code = code
