import os
import re
import sys


from tdapiclient.common.constants import TDApiClientConstants
from tdapiclient.common.exceptions import TDApiClientException
from tdapiclient.common.messagecodes import ErrorInfoCodes, MessageCodes
from tdapiclient.common.messages import Messages

from teradataml.utils.validators import _Validators as tdmlval
from teradataml.common.exceptions import TeradataMlException

class _Validators:

    @staticmethod
    def _validate_function_arguments(arg_list, skip_empty_check = None):
        """
        Method to verify that the input arguments are of valid data type except for
        argument of DataFrameType.
        PARAMETERS:
            arg_list:
                Required Argument.
                Specifies a list of arguments, expected types are mentioned as type or tuple.
                       argInfoMatrix = []
                       argInfoMatrix.append(["data", data, False, (DataFrame)])
                       argInfoMatrix.append(["centers", centers, True, (int, list)])
                       argInfoMatrix.append(["threshold", threshold, True, (float)])
                Types: List of Lists
            skip_empty_check:
                Optional Argument.
                Specifies column name and values for which to skip check.
                Types: Dictionary specifying column name to values mapping.
                Default Value: None
        RAISES:
            Error if arguments are not of valid datatype
        EXAMPLES:
            _Validators._validate_function_arguments(arg_list)
        """
        try:
            tdmlval._validate_function_arguments(arg_list)

        except TypeError as ex:
            if str(ex).find("First") >= 0:
                err_msg = Messages.get_message(MessageCodes.ARG_INF_MATRIX_TYPE, "First", "str")
                error_code = ErrorInfoCodes.ARG_INF_MATRIX_TYPE
                raise TDApiClientException(err_msg, error_code)
            
            elif str(ex).find("Third") >= 0:
                err_msg = Messages.get_message(MessageCodes.ARG_INF_MATRIX_TYPE, "Third", "bool")
                error_code = ErrorInfoCodes.ARG_INF_MATRIX_TYPE
                raise TDApiClientException(err_msg, error_code)
            
            elif str(ex).find("Fourth") >= 0:
                err_msg = Messages.get_message(MessageCodes.ARG_INF_MATRIX_TYPE, "Fourth", "'tuple of types' or 'type' type")
                error_code = ErrorInfoCodes.ARG_INF_MATRIX_TYPE
                raise TDApiClientException(err_msg, error_code)

            elif str(ex).find("Fifth") >= 0:
                err_msg = Messages.get_message(MessageCodes.ARG_INF_MATRIX_TYPE, "Fifth", "bool")
                error_code = ErrorInfoCodes.ARG_INF_MATRIX_TYPE
                raise TDApiClientException(err_msg, error_code)
            
            else:
                names_list = str(ex).split()
                invalid_arg_names = names_list[6]
                start = invalid_arg_names.index('[')
                end = invalid_arg_names.index(']')
                invalid_arg_names = invalid_arg_names[start:end+1]

                types = names_list[9].split(".")
                invalid_arg_types = types[0]
                err_msg = Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, invalid_arg_names, invalid_arg_types)
                error_code = ErrorInfoCodes.UNSUPPORTED_DATATYPE
                raise TDApiClientException(err_msg, error_code)          

        except ValueError as ex:
            err_list = str(ex).split()
            arg_name = eval(err_list[2])
            err_msg = Messages.get_message(MessageCodes.ARG_EMPTY, arg_name)
            error_code = ErrorInfoCodes.ARG_EMPTY
            raise TDApiClientException(err_msg, error_code)

        except TeradataMlException as ex:
            args_list = str(ex).split()
            miss_args = eval(args_list[5])
            err_msg = Messages.get_message(MessageCodes.MISSING_ARGS, miss_args)
            error_code = ErrorInfoCodes.MISSING_ARGS
            raise TDApiClientException(err_msg, error_code)