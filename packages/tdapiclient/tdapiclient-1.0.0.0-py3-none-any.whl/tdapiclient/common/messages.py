# ##################################################################
#
# Copyright 2022 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: pt186002@teradata.com
# Secondary Owner:
#
# This file defines error and info messages and method for getting the
# error message
# ##################################################################


from tdapiclient.common.messagecodes import ErrorInfoCodes
from tdapiclient.common.messagecodes import MessageCodes


class Messages():
    """
    Contains a dictionary mapping messages with error codes.
    Add new error and message codes in __messages dictionary whenever codes are
    added in messagecodes.py file.
    """
    __messages = {}
    __standard_message = "[Teradata][tdapiclient]"

    __messages = {
        MessageCodes.SG_CLASS_NOT_FOUND: ErrorInfoCodes.SG_CLASS_NOT_FOUND,
        MessageCodes.INVALID_ARG_VALUE: ErrorInfoCodes.INVALID_ARG_VALUE,
        MessageCodes.SG_DEPLOY_ERROR: ErrorInfoCodes.SG_DEPLOY_ERROR,
        MessageCodes.TDML_OPERATION_ERROR: ErrorInfoCodes.TDML_OPERATION_ERROR,
        MessageCodes.TDSG_RUNTIME_ERROR: ErrorInfoCodes.TDSG_RUNTIME_ERROR,
        MessageCodes.INVALID_KWARG_VALUE: ErrorInfoCodes.INVALID_KWARG_VALUE,
        MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND: ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND,
        MessageCodes.MANDATORY_KW_ARGS_NOT_FOUND : ErrorInfoCodes.MANDATORY_KW_ARGS_NOT_FOUND,
        MessageCodes.UNSUPPORTED_CLOUD_TYPE_FOUND : ErrorInfoCodes.UNSUPPORTED_CLOUD_TYPE_FOUND,
        MessageCodes.ARG_EMPTY: ErrorInfoCodes.ARG_EMPTY,
        MessageCodes.MISSING_ARGS: ErrorInfoCodes.MISSING_ARGS,
        MessageCodes.UNSUPPORTED_DATATYPE: ErrorInfoCodes.UNSUPPORTED_DATATYPE,
        MessageCodes.ARG_INF_MATRIX_TYPE: ErrorInfoCodes.ARG_INF_MATRIX_TYPE
    }

    @staticmethod
    def get_message(messagecode, *variables, **kwargs):
        """
        DESCRIPTION:
            Generate a message associated with standard message and error code.

        PARAMETERS:
            messagecode:
                Required Argument.
                Message to be returned to the user when needed to be raised
                based on the associated MessageCode.

            variables:
                Optional Argument.
                List of arguments to mention if any missing arguments.
                Default Value: Empty list

            kwargs:
                Optional Argument.
                Dictionary of keyword arguments for displaying the key and its
                desired value.
                Default Value: Empty dict

        RETURNS:
            Message with standard Python message and message code.

        RAISES:
            None.

        EXAMPLES:
            from tdsagemaker.common.messagecodes import MessageCodes
            from tdsagemaker.common.messages import Messages

            raise TDSagemmakerException(
                Messages.get_message(MessageCodes.SG_CLASS_NOT_FOUND,
                "testSgClass"), ErrorInfoCodes.SG_CLASS_NOT_FOUND)
        """
        error_code = Messages.__messages[messagecode]
        message = "{}({}) {}".format(
            Messages.__standard_message, error_code.value, messagecode.value)
        if len(variables) != 0:
            message = message.format(*variables)
        if len(kwargs) != 0:
            message = "{} {}".format(message, kwargs)

        return message
