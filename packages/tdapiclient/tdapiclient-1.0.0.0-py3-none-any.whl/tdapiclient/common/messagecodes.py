# ##################################################################
#
# Copyright 2022 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: pt186002@teradata.com
# Secondary Owner:
#
# # This file defines error and info messages
# ##################################################################


from enum import Enum


class ErrorInfoCodes(Enum):
    SG_CLASS_NOT_FOUND = "TDSG_1000"
    CONV_NOT_SUPPORTED = "TDSG_1001"
    INVALID_ARG_VALUE = "TDSG_1003"
    SG_DEPLOY_ERROR = "TDSG_1004"
    TDML_OPERATION_ERROR = "TDSG_1005"
    TDSG_RUNTIME_ERROR = "TDSG_1006"
    TDSG_S3_ERROR = "TDSG_1007"
    INVALID_KWARG_VALUE = "TDSG_1003"
    ENVIRONMENT_VARIABLE_NOT_FOUND = "TDSG_1008"
    MANDATORY_KW_ARGS_NOT_FOUND = "TDSG_1009"
    UNSUPPORTED_CLOUD_TYPE_FOUND = "TDSG_1010"
    ARG_EMPTY = 'TDSG_1009'
    MISSING_ARGS = 'TDSG_1010'
    UNSUPPORTED_DATATYPE = 'TDSG_1011'
    ARG_INF_MATRIX_TYPE = 'TDSG_1012'

class MessageCodes(Enum):
    """
    MessageCodes contains all the messages that are displayed to the user
    which are informational or raised when an exception/error occurs.
    Add messages to the class whenever a message need to be displayed
    to the user.
    """
    SG_CLASS_NOT_FOUND = "Unable to find class {} in sagemaker module list."
    INVALID_ARG_VALUE = ("Invalid value(s) '{}' passed to argument '{}', " +
                         "should be: {}.")
    SG_DEPLOY_ERROR = "Error while running sagemaker.deploy : {}."
    TDML_OPERATION_ERROR = "Error while teradataml operation : {}."
    TDSG_RUNTIME_ERROR = "Generic error at runtime."
    TDSG_S3_ERROR = "Error during AWS S3 operation : {}"
    INVALID_KWARG_VALUE = (
        "Invalid key value arguments passed to {}, Valid option(s): {}")
    ENVIRONMENT_VARIABLE_NOT_FOUND = ("Mandatory environment variable '{}' not found.")
    MANDATORY_KW_ARGS_NOT_FOUND = "Mandatory KW argument {} not found"
    UNSUPPORTED_CLOUD_TYPE_FOUND = "Unsupported cloud type given : {}"
    ARG_EMPTY = "Argument '{}' should not be empty string."
    MISSING_ARGS = "Following required arguments are missing: {}."
    UNSUPPORTED_DATATYPE = "Invalid type(s) passed to argument '{}', should be: {}."
    ARG_INF_MATRIX_TYPE = "{} element in argument information matrix should be: {}."
