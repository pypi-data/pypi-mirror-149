# ##################################################################
#
# Copyright 2022 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: pt186002@teradata.com
# Secondary Owner:
#
# This file has definitions for TDApiClient and other related classes
# This classes help users to use Teradata with SageMaker.
# ##################################################################

import logging
import glob
import importlib
import random
import shutil
import string
import tempfile
import os

import boto3
import sagemaker as sg
import pandas as pd
from teradataml import DataFrame, get_connection
from teradataml.common.exceptions import TeradataMlException

from tdapiclient.common.constants import TDApiClientConstants
from tdapiclient.common.exceptions import TDApiClientException
from tdapiclient.common.messagecodes import ErrorInfoCodes, MessageCodes
from tdapiclient.common.messages import Messages
from tdapiclient.common import logger as tdsglog
from tdapiclient.utils.validators import _Validators

logger = tdsglog._get_logger()


def create_tdapi_context(type, bucket_name, **options):
    """
    DESCRIPTION:
        Function creates an TDAPI Context to be used for executing TDApiClient
        functions.

        NOTE:
            Before using the module, the following environment variables should to
            be created.
            1. AWS_ACCESS_KEY_ID
            2. AWS_SECRET_ACCESS_KEY
            3. AWS_REGION
            4. AWS_SESSION_TOKEN
            5. AWS_DEFAULT_REGION

            AWS_ACCESS_KEY_ID:
                Required Environment Variable.
                Specifies AWS Access Key ID.
                Types: str

            AWS_SECRET_ACCESS_KEY:
                Required Environment Variable.
                Specifies AWS Secret Access Key.
                Types: str

            AWS_REGION:
                Required Environment Variable.
                Specifies AWS Region. If defined,
                this environment variable overrides the values in the
                environment variable AWS_DEFAULT_REGION.
                Types: str

            AWS_SESSION_TOKEN:
                Optional Environment Variable.
                Specifies AWS Session Token.
                Types: str

            AWS_DEFAULT_REGION:
                Optional Environment Variable.
                Specifies Default AWS Region.
                Types: str

            EXAMPLES:
                For Linux or macOS:
                    export AWS_REGION="us-west-2"
                    export AWS_ACCESS_KEY_ID="aws_access_key_id"
                    export AWS_SECRET_ACCESS_KEY="aws_secret_access_key"
                    export AWS_SESSION_TOKEN="aws_session_token"

                For Windows Command Prompt:
                    set AWS_ACCESS_KEY_ID=aws_access_key_id
                    set AWS_SECRET_ACCESS_KEY=aws_secret_access_key
                    set AWS_REGION=us-west-2
                    set AWS_SESSION_TOKEN=aws_session_token

                For PowerShell:
                    $Env:AWS_ACCESS_KEY_ID="aws_access_key_id"
                    $Env:AWS_SECRET_ACCESS_KEY="aws_secret_access_key"
                    $Env:AWS_REGION="us-west-2"
                    $Env:AWS_SESSION_TOKEN="aws_session_token"

    PARAMETERS:
        type:
            Required Argument.
            Specifies cloud type of TDAPI context (example: "aws").
            Types: Str

        bucket_name:
            Required Argument.
            Specifies S3 bucket name.
            Note: Give just the bucket name without leading /s3 or
                  s3:// and s3.amazonaws.com at the back.
            Types: Str

    RETURNS:
        Instance of TDAPI Context class.

    RAISES:
        TDApiClientException

    EXAMPLES:
        from tdapiclient import create_tdapi_context, TDApiClient
        context = create_tdapi_context("s3_bucket")
    """

    # Below matrix is list of list, where in each row contains following elements:
    # Let's take an example of following, just to get an idea:
    #   [element1, element2, element3, element4, element5, element6]
    #   e.g.
    #       ["join", join, True, (str), True, concat_join_permitted_values]

    #   1. element1 --> Argument Name, a string. ["join" in above example.]
    #   2. element2 --> Argument itself. [join]
    #   3. element3 --> Specifies a flag that mentions argument is optional or not.
    #                   False, means required and True means optional.
    #   4. element4 --> Tuple of accepted types. (str) in above example.
    #   5. element5 --> True, means validate for empty value. Error will be raised, if empty values is passed.
    #                   If not specified, means same as specifying False.
    #   6. element6 --> A list of permitted values, an argument can accept.
    #                   If not specified, it is as good as passing None. If a list is passed, validation will be
    #                   performed for permitted values.

    awu_matrix = []
    awu_matrix.append(["bucket_name", bucket_name, False, (str), True])
    awu_matrix.append(["type", type, False, (str), True])
    # Validate argument types
    _Validators._validate_function_arguments(awu_matrix)

    if type.lower() != "aws":
        err_msg = Messages.get_message(
            MessageCodes.UNSUPPORTED_CLOUD_TYPE_FOUND, type)
        error_code = ErrorInfoCodes.UNSUPPORTED_CLOUD_TYPE_FOUND
        raise TDApiClientException(err_msg, error_code)


    if "log_level" in options:
        log_level = options["log_level"].lower()
        if log_level == "debug":
            logger.setLevel(logging.DEBUG)
        elif log_level == "info":
            logger.setLevel(logging.INFO)
        elif log_level == "warn":
            logger.setLevel(logging.WARN)
        elif log_level == "error":
            logger.setLevel(logging.ERROR)
        else:
            err_msg = Messages.get_message(
                MessageCodes.INVALID_ARG_VALUE, log_level, "log_level",
                "debug or info or warn or error")
            error_code = ErrorInfoCodes.INVALID_ARG_VALUE
            raise TDApiClientException(err_msg, error_code)
    else:
        if len(options) >= 1:
            err_msg = Messages.get_message(
                MessageCodes.INVALID_KWARG_VALUE, "create_tdapi_context",
                "log_value=warn or error or debug or info")
            error_code = ErrorInfoCodes.INVALID_KWARG_VALUE
            raise TDApiClientException(err_msg, error_code)

    return _TDApiContext(bucket_name)


def remove_tdapi_context(tdapi_context):
    """
    DESCRIPTION:
        Function removes a specified TDAPI Context. It also removes any S3
        folder created during operations of TDApiClient.

    PARAMETERS:
        tdapi_context:
            Required Argument.
            Specifies the TDAPI Context which needs to be removed.
            Types: TDAPI Context class

    RETURNS:
        None

    RAISES:
        TDApiClientException

    EXAMPLES:
        from tdapiclient import create_tdapi_context, remove_tdapi_contex
        context = create_tdapi_context("s3_bucket")
        remove_tdapi_contex(context)
    """
    awu_matrix = []
    awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
    # Validate argument types
    _Validators._validate_function_arguments(awu_matrix)

    try:
        _remove_s3_folders(tdapi_context, tdapi_context._s3_prefixes)
        tdapi_context._access_id = None
        tdapi_context._access_key = None
        tdapi_context._session_token = None
        tdapi_context._bucket_name = None
    except Exception as ex:
        msg = Messages.get_message(MessageCodes.TDSG_S3_ERROR, str(ex))
        error_code = ErrorInfoCodes.TDSG_S3_ERROR
        raise TDApiClientException(msg, error_code) from ex


def _remove_s3_folders(tdapi_context, s3_prefix_list):
    """
    DESCRIPTION:
        A private method to remove S3 folders using credentials provided
        in TDAPI Context.

    PARAMETERS:
        tdapi_context:
            Required Argument.
            Specifies the TDAPI Context which holds the AWS credentials.
            Types: TDAPI Context Class

        s3_prefix_list:
            Required Argument.
            Specifies the list of s3 prefixes to be deleted.
            Note:
                These prefixes are searched in the bucket specified by the
                tdapi_context.
            Types: List of s3 prefixes of type Str

    RETURNS:
        None

    RAISES:
        AWS service exceptions or botocore.exception

    EXAMPLES:
        from tdapiclient import create_tdapi_context, remove_tdapi_contex
        context = create_tdapi_context("s3_bucket")
        s3_prefix_list = ["test-s3-path/"]
        _remove_s3_folders(context, s3_prefix_list)
    """
    awu_matrix = []
    awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
    awu_matrix.append(["s3_prefix_list", s3_prefix_list, False, (list), True])
    # Validate argument types
    _Validators._validate_function_arguments(awu_matrix)

    s3 = boto3.resource("s3", aws_access_key_id=tdapi_context._access_id,
                        aws_secret_access_key=tdapi_context._access_key,
                        aws_session_token=tdapi_context._session_token,
                        region_name=tdapi_context._aws_region)

    bucket_name = tdapi_context._bucket_name

    # Convert /s3/pp.amazon.com to pp
    if bucket_name.endswith("/"):
        bucket_name = bucket_name[:-1]
    bucket_name = bucket_name.split("/")[-1]
    bucket_name = bucket_name.split(".")[0]

    bucket = s3.Bucket(bucket_name)
    for s3_prefix in s3_prefix_list:
        bucket.objects.filter(Prefix=s3_prefix).delete()


class _TDApiContext:
    """
    This is a class for holding TDAPI Context information. This is used while
    creating TDApiClient object.
    """

    def __init__(self, bucket_name):
        """
        DESCRIPTION:
            An initializer for _TDApiContext.

        PARAMETERS:
            bucket_name:
                Required Argument.
                Specifies S3 bucket name.
                Note: Give just the bucket name without leading /s3 or
                s3:// and s3.amazonaws.com at the back.
                Types: Str

        RETURNS:
            Instance of TDAPI Context class.

        RAISES:
            None

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            context = _TDApiContext("s3_bucket")
        """
        awu_matrix = []
        awu_matrix.append(["bucket_name", bucket_name, False, (str), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if "AWS_REGION" in os.environ:
            self._aws_region = os.environ["AWS_REGION"]
        else:
            self._aws_region = os.environ["AWS_DEFAULT_REGION"]

        self._bucket_name = "/s3/{}.s3.amazonaws.com/".format(bucket_name)
        logger.debug("Generated bucket name in write_nos format is {}".format(
            bucket_name))
        if "AWS_ACCESS_KEY_ID" in os.environ:
            self._access_id = os.environ["AWS_ACCESS_KEY_ID"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AWS_ACCESS_KEY_ID")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        if "AWS_SECRET_ACCESS_KEY" in os.environ:
            self._access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
        else:
            errMsg = Messages.get_message(
                MessageCodes.ENVIRONMENT_VARIABLE_NOT_FOUND, "AWS_SECRET_ACCESS_KEY")
            error_code = ErrorInfoCodes.ENVIRONMENT_VARIABLE_NOT_FOUND
            raise TDApiClientException(errMsg, error_code)

        self._session_token = "" # Default value for session token
        if "AWS_SESSION_TOKEN" in os.environ:
            self._session_token = os.environ["AWS_SESSION_TOKEN"]

        self._s3_prefixes = []


class TDPredictor:
    """
    This is a wrapper over SageMaker.Predictor class. It allows for
    integration with Teradata at the time of scoring using predict method.
    """

    def __init__(self, sage_obj, tdapi_context):
        """
        DESCRIPTION:
            Initliazer for TDPredictor.

        PARAMETERS:
            sage_obj:
                Required Argument.
                Specifies instance of SageMaker predictor class.
                Types: SageMaker predictor Object

            tdapi_context:
                Required Argument.
                Specifies TDAPI Context object holding aws credentials
                information.
                Types: _TDApiContext object

        RETURNS:
            A TDPredictor instance.

        RAISES:
            None

        EXAMPLES:
            # This class is created by the library in following
            # type of operation.

            from tdapiclient import create_tdapi_context, TDApiClient
            from teradataml import DataFrame
            context = create_tdapi_context("s3_bucket")
            tdapiclient = TDApiClient(context)
            # SKlearn takes all parameters that AWS SageMaker Library requires
            skLearnObject = tdapiclient.SKLearn()
            df = DataFrame(tableName='t')
            skLearnObject.fit(df)
            predictor = skLearnObject.deploy(instance_type="ml.m5.large",
                            initial_instance_count=1)
            # predictor will be of type TDPredictor
        """
        awu_matrix = []
        awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
        awu_matrix.append(["sage_obj", sage_obj, False, (object), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        self.sageObj = sage_obj
        self._tdapi_context: _TDApiContext = tdapi_context

    @classmethod
    def from_predictor(cls, sagemaker_predictor_obj, tdapi_context):
        """
        DESCRIPTION:
            This method creates TDPredictor from the sagemaker predictor
            object to allow for prediction using teradataml DataFrame and
            SageMaker endpoint represented by this predictor object.

        PARAMETERS:
            sagemaker_predictor_obj:
                Required Argument.
                Specifies the instance of SageMaker predictor class.
                Types: SageMaker predictor Object

            tdapi_context:
                Required Argument.
                Specifies the TDAPI Context object holding aws credentials
                information.
                Types: _TDApiContext object

        RETURNS:
            A TDPredictor instance.

        RAISES:
            None

        EXAMPLES:
            from tdapiclient import TDPredictor, create_tdapi_context
            import sagemaker
            from sagemaker.xgboost.estimator import XGBoost
            from sagemaker.session import s3_input, Session

            # Initialize hyperparameters
            hyperparameters = {
                    "max_depth":"5",
                    "eta":"0.2",
                    "gamma":"4",
                    "min_child_weight":"6",
                    "subsample":"0.7",
                    "verbosity":"1",
                    "objective":"reg:linear",
                    "num_round":"50"}

            # Set an output path where the trained model will be saved
            bucket = sagemaker.Session().default_bucket()
            prefix = 'DEMO-xgboost-as-a-framework'
            output_path = 's3://{}/{}/{}/output'.format(bucket, prefix,
              'abalone-xgb-framework')

            # Construct a SageMaker XGBoost estimator
            # Specify the entry_point to your xgboost training script
            estimator = XGBoost(entry_point = "your_xgboost_abalone_script.py",
                                framework_version='1.0-1',
                                hyperparameters=hyperparameters,
                                role=sagemaker.get_execution_role(),
                                train_instance_count=1,
                                train_instance_type='ml.m5.2xlarge',
                                output_path=output_path)

            # Define the data type and paths to the training and validation
            # datasets
            content_type = "libsvm"
            train_input = s3_input("s3://{}/{}/{}/".format(bucket, prefix,
              'train'), content_type=content_type)
            validation_input = s3_input("s3://{}/{}/{}/".format(bucket,
                 prefix, 'validation'), content_type=content_type)

            # Execute the XGBoost training job
            estimator.fit({'train': train_input,
                   'validation': validation_input})
            sagemaker_predictor = estimator.deploy()
            context = create_tdapi_context("aws_region", "s3_bucket" "access_id",
                                          "access_key", "session_token_if_any")

            tdsg_predictor = TDPredictor.from_predictor(
                sagemaker_predictor, context)

        """
        awu_matrix = []
        awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
        awu_matrix.append(["sagemaker_predictor_obj", sagemaker_predictor_obj, False, (object), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        return TDPredictor(sagemaker_predictor_obj, tdapi_context)

    def predict(self, input: DataFrame, mode, **options):
        """
        DESCRIPTION:
            This method performs prediction using teradataml DataFrame and
            SageMaker endpoint represented by this predictor object.

        PARAMETERS:
            input:
                Required Argument.
                Specifies the teradataml DataFrame where input for scoring
                comes from.
                Types: teradataml DataFrame

            mode:
                Required Argument.
                Specifies the mode for scoring.
                Permitted Values:
                    * 'UDF': Score in database using a Teradata UDF.
                             Faster scoring with the data from Teradata.
                    * 'CLIENT': Score at client using a library. Data will be
                                pulled from Teradata and serialized for
                                scoring at client.
                Default Value: 'UDF'
                Types: Str

            options:
                Optional Argument.
                Specifies the predict method with the following key-value
                arguments:
                udf_name: Specifies the UDF name used to invoke predict with
                          UDF mode.
                          Default Value: tapidb.API_Request
                content_type: Specifies content type required for
                              SageMaker endpoint present in the predictor.
                              Default Value: csv
                key_start_index: Specifies the index in DataFrame columns to
                                 be the key for scoring starts.
                                 Default Value: 0
                Types: kwarg

        RETURNS:
            A teradataml DataFrame, when mode is set to 'UDF'; otherwise
            an array or JSON.

        RAISES:
            None

        EXAMPLES:
            from tdapiclient import create_tdapi_context, TDApiClient
            from teradataml import DataFrame
            context = create_tdapi_context("s3_bucket")
            tdapiclient = TDApiClient(context)
            # SKlearn takes all parameters that AWS SageMaker Library requires
            skLearnObject = tdapiclient.SKLearn()
            df = DataFrame(tableName='t')
            skLearnObject.fit(df)
            predictor = skLearnObject.deploy(instance_type="ml.m5.large",
                            initial_instance_count=1)
            df = DataFrame(tableName='inputTable')
            outputDF = predictor.predict(df, mode='UDF', content_type='csv')
        """
        options = {k.lower(): v for k, v in options.items()}
        self._set_default_options(options)
        if mode.lower() == "client":
            return self._run_prediction_at_client(input, options)
        elif mode.lower() == "udf":
            return self._run_udf(input, options)
        else:
            errMsg = Messages.get_message(
                MessageCodes.INVALID_ARG_VALUE, mode, "mode", "client or udf")
            error_code = ErrorInfoCodes.INVALID_ARG_VALUE
            raise TDApiClientException(errMsg, error_code)

    def _set_default_options(self, options: dict):
        """
        DESCRIPTION:
            A private method for getting default options for predict API.

        PARAMETERS:
            options:
                Required Argument.
                Specifies options given by User.
                Types: dict

        RETURNS:
            None
            It fills the input options with default option parameters.

        RAISES:
            None

        EXAMPLE:
            options = {}
            self.__fillDefaultOptions(options)
        """
        awu_matrix = []
        awu_matrix.append(["options", options, False, (dict), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        
        if "udf_name" not in options:
            options["udf_name"] = "tapidb.API_Request"
        if "content_type" not in options:
            options["content_type"] = "csv"
        if "key_start_index" not in options:
            options["key_start_index"] = 0

    def _run_prediction_at_client(self, data: DataFrame, options):
        """
        DESCRIPTION:
            A private method for runing predict operation at the client side.

        PARAMETERS:
            data:
                Required Argument.
                Specifies input teradataml dataframe which holds input data
                for scoring.
                Types: teradataml DataFrame

            options:
                Required Argument.
                Specifies options dictionary which holds user given or default
                options for predict API.
                Types: dict

        RETURNS:
            It returns array or json as per SageMaker model.

        RAISES:
            SagemakerException

        EXAMPLE:
            options = {}
            self._set_default_options(options)
            inputDataFrame = DataFrame(tableName='customer_data')
            output = self._run_prediction_at_client(inputDataFrame, options)
        """
        awu_matrix = []
        awu_matrix.append(["options", options, False, (dict), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        
        content_type = options["content_type"].lower()
        pdf = data.to_pandas()
        if content_type == "json":
            row_data = pdf.to_json(orient="values")
            return (self.sageObj.predict(row_data))
        elif content_type == "csv":
            row_data = pdf.to_csv(index=False, header=False)
            return (self.sageObj.predict(row_data))
        else:
            errMsg = Messages.get_message(
                MessageCodes.INVALID_ARG_VALUE, content_type, "content_type",
                "json or csv")
            error_code = ErrorInfoCodes.INVALID_ARG_VALUE
            raise TDApiClientException(errMsg, error_code)

    def _run_udf(self, data: DataFrame, options: dict):
        """
        DESCRIPTION:
            A private method for runing predict operation inside DB using UDF.

        PARAMETERS:
            data:
                Required Argument.
                Specifies input teradataml dataframe which holds input data
                for scoring.
                Types: teradataml DataFrame
            options:
                Required Argument.
                Specifies options dictionary which holds user given or default
                options for predict API.
                Types: dict

        RETURNS:
            It returns teradataml DataFrame object containing output column
            for prediction.

        RAISES:
            TeradataMlException
            TDApiClientException

        EXAMPLE:
            options = {}
            self._set_default_options(options)
            inputDataFrame = DataFrame(tableName='customer_data')
            output = self._runUDF(inputDataFrame, options)
        """
        awu_matrix = []
        awu_matrix.append(["options", options, False, (dict), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
        
        input_query = None
        try:
            input_query = data.show_query(True)
        except TeradataMlException as tdml_ex:
            msg = Messages.get_message(MessageCodes.TDML_OPERATION_ERROR,
                                       "show_query")
            error_code = ErrorInfoCodes.TDML_OPERATION_ERROR
            raise TDApiClientException(msg, error_code) from tdml_ex
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.TDSG_RUNTIME_ERROR)
            error_code = ErrorInfoCodes.TDSG_RUNTIME_ERROR
            raise TDApiClientException(msg, error_code) from ex
        session_token_str = ""
        token_str = self._tdapi_context._session_token
        if len(token_str) > 0:
            session_token_str = ", Session_Token : {}".format(token_str)

        auth_info_fmt_str = ('{{ "Access_ID": "{}", "Access_Key": ' +
                             '"{}", "Region" : "{}", {} }}')
        auth_info = auth_info_fmt_str.format(self._tdapi_context._access_id,
                                             self._tdapi_context._access_key,
                                             self._tdapi_context._aws_region,
                                             session_token_str)
        udf_query = ("SELECT * FROM {}( ON ({}) USING AUTHORIZATION('{}')" +
                     " API_TYPE('aws-sagemaker') ENDPOINT('{}') " +
                     " CONTENT_TYPE('{}') KEY_START_INDEX('{}')) " +
                     "as \"DT\" ")

        content_type = options["content_type"]
        key_start_index = options["key_start_index"]
        function_name = options["udf_name"]

        logger.debug("content_type is {}".format(content_type))
        logger.debug("key_start_index is {}".format(key_start_index))
        logger.debug("function_name is {}".format(function_name))

        udf_query = udf_query.format(function_name, input_query,
                                     auth_info, self.sageObj.endpoint_name,
                                     content_type, key_start_index)
        try:
            queryDf = DataFrame(query=udf_query)
            return queryDf
        except TeradataMlException as tdml_ex:
            msg = Messages.get_message(MessageCodes.TDML_OPERATION_ERROR,
                                       "DataFrame")
            error_code = ErrorInfoCodes.TDML_OPERATION_ERROR
            raise TDApiClientException(msg, error_code) from tdml_ex
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.TDSG_RUNTIME_ERROR)
            error_code = ErrorInfoCodes.TDSG_RUNTIME_ERROR
            raise TDApiClientException(msg, error_code) from ex

    def __getattr__(self, name):
        def __sg_method_invoker(*c, **kwargs):
            return atrribute_instance(*c, **kwargs)

        atrribute_instance = getattr(self.sageObj, name)
        if callable(atrribute_instance):
            return __sg_method_invoker
        return atrribute_instance


class _TDApiClientObjectWrapper:
    """
        This class is a wrapper over SageMaker Estimator class, which provides
        a way for integration between estimator class and Teradata
        in following ways:
        1. For fit method, user can specify teradataml DataFrame objects to
           specify input for training.
        2. For deploy method, it returns predictor object which provides option
           for in-db prediction.
    """

    def __init__(self, sageObj, tdapi_context) -> None:
        """
        DESCRIPTION:
            Initializer for _TDApiClientObjectWrapper.

        PARAMETERS:
            sageObj:
                Required Argument.
                Specifies instance of SageMaker estimator class.
                Types: SageMaker Estimator instance

            tdapi_context:
                Required Argument.
                Specifies instance of TDAPI Context class.
                Types: TDAPI Context

        RETURNS:
            A _TDApiClientObjectWrapper instance.

        RAISES:
            None

        EXAMPLES:
            # This class is created by the library in following
            # type of operation.

            context = create_tdapi_context("s3_bucket")
            tdapiclient = TDApiClient(context)
            # SKlearn takes all parameters that AWS SageMaker Library requires
            skLearnObject = tdapiclient.SKLearn()
            # skLearnObject will be of type _TDApiClientObjectWrapper

        """
        awu_matrix = []
        awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
        awu_matrix.append(["sageObj", sageObj, False, (object), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        self.sageObj = sageObj
        self._tdapi_context: _TDApiContext = tdapi_context

    def fit(self, inputs, content_type='csv', **sg_kw_args):
        """
        DESCRIPTION:
            Execute SageMaker.fit method using the teradataml DataFrame as
            source for training.

        PARAMETERS:
            inputs:
                Required Argument.
                Specifies a teradataml Dataframe or S3 path as a string.
                Types: Can be one of the following
                       1. Single object of teradataml DataFrame
                       2. String
                       3. Dict of string to object of teradataml Dataframe

            content_type:
                Optional Argument.
                Specifies content type for inputs.
                Default Value: CSV
                Types: Str

            **sg_args:
                Optional Argument.
                Specifies any additional argument required for SageMaker.fit.
                These parameters are directly supplied to SageMaker.fit method.
                Types: Multiple

        RETURNS:
            SageMaker.fit's return value.

        EXAMPLES:
            from tdapiclient import create_tdapi_context,TDApiClient
            context = create_tdapi_context("s3_bucket")
            tdapiclient = TDApiClient(context)
            # SKlearn takes all parameters that AWS SageMaker Library requires
            skLearnObject = tdapiclient.SKLearn()
            train = DataFrame(tableName='train_data')
            test = DataFrame(tableName='test_data')
            skLearnObject.fit(inputs={'train': train, 'test': test},
                              content_type='csv', wait=False)

        RAISES:
            TeradataMlException
            TDApiClientException
        """
        awu_matrix = []
        awu_matrix.append(["content_type", content_type, True, (str), False])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)


        updated_inputs = inputs
        if isinstance(inputs, dict):
            for inputName, object in inputs.items():
                if isinstance(object, DataFrame):
                    newObj = self.__get_s3_address_for_df(object, content_type)
                    inputs[inputName] = newObj
        if isinstance(inputs, DataFrame):
            updated_inputs = self.__get_s3_address_for_df(inputs,
                                                          content_type)
        logger.info("Updated input is : {}".format(updated_inputs))
        method_instance = getattr(self.sageObj, self.fit.__name__)
        try:
            return method_instance(updated_inputs, **sg_kw_args)
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.TDSG_RUNTIME_ERROR)
            error_code = ErrorInfoCodes.TDSG_RUNTIME_ERROR
            raise TDApiClientException(msg, error_code) from ex

    def __get_s3_address_for_df(self, input: DataFrame, content_type):
        """
        DESCRIPTION:
            Private method to convert the teradataml DataFrame to S3 path using
            Write_NOS functionality and conversion to the specified content
            type.

        PARAMETERS:
            input:
                Required Argument.
                Specifies the teradataml DataFrame which needs to be exported
                to S3.
                Types: teradataml DataFrame

            content_type:
                Required Argument.
                Specifies the content type for DataFrame content when it is
                exported to S3.
                Types: str

        RETURNS:
            Returns S3 path information.

        EXAMPLES:
            train = DataFrame(tableName='train_data')
            s3Path = self.__get_s3_address_for_df(train, 'csv')

        RAISES:
            TeradataMlException
            TDApiClientException
        """
        awu_matrix = []
        awu_matrix.append(["content_type", content_type, False, (str), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)


        s3_address_details = self._export_df_to_s3(input, content_type)
        s3BucketName = self._tdapi_context._bucket_name
        if s3_address_details[5]:
            return self._convert_format_and_upload_data(s3BucketName,
                                                        s3_address_details[2],
                                                        s3_address_details[4],
                                                        content_type)
        else:
            return s3_address_details[0]

    #  TODO: Replace this with teradataml call when support for write_nos is
    #  there in teradataml
    def _export_df_to_s3(self, input_data_frame: DataFrame, content_type):
        """
        DESCRIPTION:
            Private method for exporting input data frame to S3 using Write_NOS
            functionality.

        PARAMETERS:
            input_data_frame:
                Required Argument.
                Specifies teradataml DataFrame which needs to be exported
                to S3.
                Types: teradataml DataFrame

            content_type:
                Required Argument.
                Specifies content_type for teradataml DataFrame content
                when it is exported to S3.
                Types: str

        RETURNS:
            Returns a tuple of 6 values, with details as follows
            [0] -> S3 Address
            [1] -> S3 Bucket Name
            [2] -> S3 Folder Name
            [3] -> Requestd content type
            [4] -> Current Content type
            [5] -> Conversion needed

        EXAMPLES:
            from teradataml.dataframe import DataFrame

            train = DataFrame(tableName='train_data')
            s3AddressInfo = self._export_df_to_s3(train, 'csv')
            print(s3AddressInfo[0])
        RAISES:
            TeradataMlException
        """
        awu_matrix = []
        awu_matrix.append(["content_type", content_type, False, (str), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        input_query = None
        try:
            input_query = input_data_frame.show_query(True)
        except TeradataMlException as tdml_ex:
            msg = Messages.get_message(MessageCodes.TDML_OPERATION_ERROR,
                                       "show_query")
            error_code = ErrorInfoCodes.TDML_OPERATION_ERROR
            raise TDApiClientException(msg, error_code) from tdml_ex
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.TDSG_RUNTIME_ERROR)
            error_code = ErrorInfoCodes.TDSG_RUNTIME_ERROR
            raise TDApiClientException(msg, error_code) from ex
        requested_content_type = content_type
        conversion_needed = False
        if content_type == "json":
            content_type = "parquet"
            conversion_needed = True
        if content_type == "csv":
            content_type = "parquet"
            conversion_needed = True
        s3_address = self._tdapi_context._bucket_name
        if s3_address[-1] != '/':
            s3_address += "/"
        s3_address += "{}/"
        s3_folder_name = 'tdsg-{}'.format(
            ''.join(random.choices(string.ascii_lowercase, k=10)))
        self._tdapi_context._s3_prefixes.append(s3_folder_name + "/")
        s3_address = s3_address.format(''.join(s3_folder_name))
        storedAs = content_type
        session_token_str = ""
        token_str = self._tdapi_context._session_token
        msg = "Using '{}' folder under s3 bucket '{}' for write_nos."
        logger.debug(msg.format(s3_folder_name,
                                self._tdapi_context._bucket_name))
        if len(token_str) > 0:
            session_token_str = ", Session_Token : {}".format(token_str)
        auth_info_str = '{{ "Access_ID": "{}", "Access_Key": "{}" {} }}'
        auth_info = auth_info_str.format(self._tdapi_context._access_id,
                                         self._tdapi_context._access_key,
                                         session_token_str)
        write_nos_query = ("SELECT * FROM WRITE_NOS(ON ({}) USING " +
                           "LOCATION('{}') " +
                           "AUTHORIZATION('{}') STOREDAS('{}')) AS d")
        write_nos_query = write_nos_query.format(input_query, s3_address,
                                                 auth_info, storedAs)
        td_connection = get_connection()
        try:
            result = td_connection.execute(write_nos_query)
            for row in result:
                pass
            address = s3_address
            address = address.replace('/s3/', 's3://')
            return (address, self._tdapi_context._bucket_name, s3_folder_name,
                    requested_content_type, content_type, conversion_needed)
        except Exception as ex:
            msg = Messages.get_message(MessageCodes.TDSG_RUNTIME_ERROR)
            error_code = ErrorInfoCodes.TDSG_RUNTIME_ERROR
            raise TDApiClientException(msg, error_code) from ex

    def _convert_format_and_upload_data(self, bucket_name, folder_name,
                                        original_format, requested_format):
        """
        DESCRIPTION:
            Private method for converting format of files in S3 path and
            uploading converted data to new S3 folder.

        PARAMETERS:
            bucket_name:
                Required Argument.
                Specifies S3 bucket name where input data/files can be found.
                Types: str

            folder_name:
                Required Argument.
                Specifies S3 folder name where files can be found.
                This function will read all files in this folder and convert
                them to requested_format.
                Types: str

            original_format:
                Required Argument.
                Specifies original format for the content in S3 folder.
                Types: str

            requested_format:
                Required Argument.
                Specifies new format required for the content in S3 folder.
                Types: str

        RETURNS:
            Returns a S3 path where files can be found in the requested_format.

        EXAMPLES:
            newS3Path =
                self._convert_format_and_upload_data('s3-test-bucket',
                         'table-data', 'paraquet',   'csv' )
            print(newS3Path)

        RAISES:
            TDApiClientException - INVALID_ARG_VALUE
        """
        awu_matrix = []
        awu_matrix.append(["bucket_name", bucket_name, False, (str), True])
        awu_matrix.append(["folder_name", folder_name, False, (str), True])
        awu_matrix.append(["original_format", original_format, False, (str), True])
        awu_matrix.append(["requested_format", requested_format, False, (str), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if bucket_name.endswith("/"):
            bucket_name = bucket_name[:-1]
        # Convert /s3/pp.amazon.com to pp
        bucket_name = bucket_name.split("/")[-1]
        bucket_name = bucket_name.split(".")[0]
        if original_format == "parquet":
            if requested_format not in ["csv", "json"]:
                error_code = ErrorInfoCodes.INVALID_ARG_VALUE
                msg = Messages.get_message(
                    MessageCodes.INVALID_ARG_VALUE, requested_format,
                    'requested_format', 'csv or json')
                raise TDApiClientException(msg, error_code)

            s3 = boto3.resource(
                "s3",
                aws_access_key_id=self._tdapi_context._access_id,
                aws_secret_access_key=self._tdapi_context._access_key,
                aws_session_token=self._tdapi_context._session_token,
                region_name=self._tdapi_context._aws_region)

            bucket = s3.Bucket(bucket_name)
            dirpath = tempfile.mkdtemp()
            s3_obj = bucket.objects
            for file in s3_obj.filter(Prefix=folder_name + "/"):
                s3_key_path = file.key
                input_file_name = s3_key_path.split("/")[-1]
                output_file_name = "{}.{}"
                output_file_name = "{}.{}".format(
                    input_file_name.split(".")[0],
                    requested_format)
                bucket.download_file(s3_key_path,
                                     "{}/{}".format(dirpath, input_file_name))
                df = pd.read_parquet("{}/{}".format(dirpath, input_file_name))
                if requested_format == "csv":
                    df.to_csv("{}/{}".format(dirpath, output_file_name))
                else:
                    df.to_json("{}/{}".format(dirpath, output_file_name))
            new_dir_path = "{}/*.{}".format(dirpath, requested_format)
            list_of_new_formatted_files = glob.glob(new_dir_path)
            new_folder_name = folder_name + "-" + requested_format
            self._tdapi_context._s3_prefixes.append(new_folder_name + "/")
            s3 = boto3.resource(
                's3',
                aws_access_key_id=self._tdapi_context._access_id,
                aws_secret_access_key=self._tdapi_context._access_key,
                aws_session_token=self._tdapi_context._session_token,
                region_name=self._tdapi_context._aws_region)
            for file in list_of_new_formatted_files:
                s3FileName = "{}/{}".format(new_folder_name,
                                            file.split("/")[-1])
                s3.Bucket(bucket_name).upload_file(file, s3FileName)
            shutil.rmtree(dirpath)  # Delete tmp directory
            # After conversion, we no longer need s3 folder with content
            # in earlier format, Delete that folder
            folder_name = folder_name + "/"
            s3_prefix_for_write_nos_op = folder_name
            # Also remove it from s3 prefix list
            self._tdapi_context._s3_prefixes = list(
                filter(lambda a: a != folder_name,
                       self._tdapi_context._s3_prefixes))
            _remove_s3_folders(self._tdapi_context, [s3_prefix_for_write_nos_op])
            return "s3://{}/{}".format(bucket_name, new_folder_name)
        error_code = ErrorInfoCodes.INVALID_ARG_VALUE
        msg = Messages.get_message(
            MessageCodes.INVALID_ARG_VALUE, original_format, 'original_format',
            "parquet")
        raise TDApiClientException(msg, error_code)

    def deploy(self, *sagemaker_p_args, **sagemaker_kw_args):
        """
        DESCRIPTION:
            Execute SageMaker.deploy method of AWS SageMaker estimator class
            to allow integration with Teradata at the time of scoring.

        PARAMETERS:
            sagemaker_p_args:
                Required Argument.
                Specifies all posititonal parameters required for original
                SageMaker.deploy method.
                Types: Multiple

            sagemaker_kw_args:
                Required Argument.
                Specifies all kwarg parameters required for original
                SageMaker.deploy method.
                Types: Multiple

        RETURNS:
            Returns an instance of TDPredictor.

        EXAMPLES:
            predictor =
                td_apiclient.deploy(instance_type="ml.c5.large",
                                    initial_instance_count=1)

        RAISES:
            TDApiClientException - SG_DEPLOY_ERROR
        """
        try:
            method_instance = getattr(self.sageObj, self.deploy.__name__)
            predictor_object = method_instance(*sagemaker_p_args,
                                               **sagemaker_kw_args)
            return TDPredictor(predictor_object, self._tdapi_context)
        except Exception as ex:
            error_code = ErrorInfoCodes.SG_DEPLOY_ERROR
            msg = Messages.get_message(MessageCodes.SG_DEPLOY_ERROR, ex)
            raise TDApiClientException(msg, error_code) from ex

    def __getattr__(self, name):
        def __sg_method_invoker(*c, **kwargs):
            return atrribute_instance(*c, **kwargs)

        atrribute_instance = getattr(self.sageObj, name)
        if callable(atrribute_instance):
            return __sg_method_invoker
        return atrribute_instance


class TDApiClient:
    """
    TDApiClient class is used to create SageMaker estimator class which in turn
    can be used to create SageMaker predictor. SageMaker estimator class
    can take input data from teradataml DataFrame for training the model. And
    SageMaker predictor can use Teradata tables or queries (using teradataml
    DataFrame) for scoring.
    """

    def __init__(self, tdapi_context):
        """
        DESCRIPTION:
            Initializer for TDApiClient.

        PARAMETERS:
            tdapi_context:
                Required Argument.
                Specifies an instance of TDAPI Context created using
                create_tdapi_context to be used with TDApiClient.
                Types: TDAPI Context

       RETURNS:
            Returns an instance of TDApiClient.

        EXAMPLES:
            from TDApiClient import create_tdapi_context, TDApiClient
            context = create_tdapi_context("s3_bucket")
            TDApiClient = TDApiClient(context)

        RAISES:
            None
        """   
        awu_matrix = []
        awu_matrix.append(["tdapi_context", tdapi_context, False, (_TDApiContext), True])
        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)
       
        self._tdapi_context: _TDApiContext = tdapi_context

    def __getattr__(self, name):
        def __sgClassFinder(*c,  **kwargs):
            sagemaker_module_list = TDApiClientConstants.SG_MODULE_LIST.value
            for module in sagemaker_module_list:
                lib_object = importlib.import_module(module)
                try:
                    logger.debug(
                        "Searching for '{}' class in module '{}'.".format(
                            name, module))
                    class_instance = getattr(lib_object, name)
                    logger.debug("Found '{}' class in module '{}'.".format(
                        name, module))
                except Exception:
                    continue
                set_sg_session = False
                if "sagemaker_session" in kwargs:
                    if kwargs["sagemaker_session"] is None:
                        set_sg_session = True
                else:
                    set_sg_session = True

                if set_sg_session:
                    session = boto3.Session(
                        aws_access_key_id=self._tdapi_context._access_id,
                        aws_secret_access_key=self._tdapi_context._access_key,
                        aws_session_token=self._tdapi_context._session_token,
                        region_name=self._tdapi_context._aws_region)
                    sagemaker_session = sg.Session(boto_session=session)
                    kwargs["sagemaker_session"] = sagemaker_session
                    logger.debug("Created new sagemaker_session object " +
                                 "and passed it to '{}''s constructor.".format(
                                     name))
                sg_object = class_instance(*c, **kwargs)
                return _TDApiClientObjectWrapper(sg_object, self._tdapi_context)
            error_code = ErrorInfoCodes.SG_CLASS_NOT_FOUND
            msg = Messages.get_message(MessageCodes.SG_CLASS_NOT_FOUND, name)
            raise TDApiClientException(msg, error_code)
        return __sgClassFinder
