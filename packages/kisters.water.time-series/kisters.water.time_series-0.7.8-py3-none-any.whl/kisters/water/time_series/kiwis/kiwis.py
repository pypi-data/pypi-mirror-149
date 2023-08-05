import logging
from typing import Union

import pandas as pd
import requests

from kisters.water.time_series.kiwis._support.auth.basic_auth import Auth, BasicAuth


class KiWISError(Exception):
    pass


class KiWIS(object):
    """
    KiWIS class provides access to the KISTERS Web Interoperability Solution, it mimics the
    different requests supported by KiWIS as methods. This class follows camelCase convention
    for the methods which are requests in KiWIS to match with KiWIS documentation.
    """

    def __init__(
        self,
        kiwis_uri,
        datasource,
        user: str = None,
        password: str = None,
        create_pandas=True,
        kilogger=None,
        logger=None,
    ):
        if kilogger:
            self.__logger = kilogger.get_logger("debug", self.__class__.__name__)
        elif logger:
            self.__logger = logger
        else:
            self.__logger = logging.getLogger(self.__class__.__name__)
            self.__logger.setLevel(logging.DEBUG)
        if user is not None and password is not None:
            self.__auth: Auth = BasicAuth(user, password)
        else:
            self.__auth = None
        self.__kiwis_uri = kiwis_uri
        self.__not_params = ["self", "locals_", "args", "kwargs"]
        self.__graph_functions = ["getGraph", "getStationGraph"]
        self.__data_source = datasource
        self.__create_pandas = create_pandas
        self.__request = requests.Session()
        self.__request_info = self.make_request("getRequestInfo", {"format": "json"}).json()[0]["Requests"]
        self.__additional_params = ["format", "returnfields"]

        return

    def _pre_request_check(self, params, request_name):
        self.__logger.info("Checking params for validity")
        for (param_key, param_value) in params.items():
            # removing underscores at the end of param name (for example from_)
            if param_key[-1] == "_":
                params.pop(param_key)
                param_key = param_key[:-1]
                params[param_key] = param_value

        self._check_params(params, request_name)
        self._check_format(params["format"], request_name)
        if "Dateformats" in self.__request_info[request_name] and params.get("dateformat", False):
            self._check_date_format(params["dateformat"], request_name)
        if params.get("returnfields", False):
            self._check_return_fields(params["returnfields"], request_name)
        return params

    def _check_params(self, parameters, request_name):
        for param in parameters:
            # checking if all given params are in requestInfo
            if (
                param not in self.__request_info[request_name]["QueryFields"]["Content"]
                and param not in self.__request_info[request_name]["Optionalfields"]["Content"]
                and param not in self.__additional_params
            ):
                self.__logger.warning(
                    "Param '%s' not in requestInfo for %s. It might be faulty to provide it. Please refer to "
                    "%s?service=kisters&type=queryServices&request=getRequestInfo"
                    % (param, request_name, self.__kiwis_uri)
                )

    def _check_format(self, format, request_name):
        """checking if format is in requestInfo"""
        if format not in self.__request_info[request_name]["Formats"]["Content"]:
            self.__logger.warning(
                "Format '%s' not in requestInfo for %s. Please refer to "
                "%s?service=kisters&type=queryServices&request=getRequestInfo"
                % (format, request_name, self.__kiwis_uri)
            )

    def _check_date_format(self, date_formats, request_name):
        """checking if date_formats are correct"""
        date_formats = date_formats.split(",")
        for dateformat in [
            x for x in date_formats if x not in self.__request_info[request_name]["Dateformats"]["Content"]
        ]:
            self.__logger.warning(
                "Dateformat '%s' not in requestInfo for %s. Please refer to "
                "%s?service=kisters&type=queryServices&request=getRequestInfo"
                % (dateformat, request_name, self.__kiwis_uri)
            )

    def _check_return_fields(self, return_fields, request_name):
        """checking if return_fields are correct"""
        return_fields = return_fields.split(",")
        return_fields_info = self.__request_info[request_name]["Returnfields"]["Content"]
        for return_field in [x for x in return_fields if x not in return_fields_info]:
            if (
                not return_field.startswith("ts_clientvalue")
                or "ts_clientvalue##" not in return_fields_info
            ):
                self.__logger.warning(
                    "Returnfield '%s' not in requestInfo for %s. Please refer to "
                    "%s?service=kisters&type=queryServices&request=getRequestInfo"
                    % (return_field, request_name, self.__kiwis_uri)
                )

    def make_request(self, request_name, request_data) -> Union[requests.Response, pd.DataFrame]:
        request_data.update(
            {
                "service": "kisters",
                "type": "queryServices",
                "datasource": self.__data_source,
                "request": request_name,
            }
        )
        headers = {"Authentication": self.__auth.auth_header()} if self.__auth is not None else None
        req = self.__request.get(self.__kiwis_uri, params=request_data, headers=headers)

        self.__logger.info("Making request %s" % request_name)
        self.__logger.debug(req.url)

        if (
            (request_data["format"] == "objson" or request_data["format"] == "dajson")
            and self.__create_pandas
            and request_name not in self.__graph_functions
        ):
            req_json = req.json()
            if type(req_json) is dict and "type" in req_json.keys() and req_json["type"] == "error":
                raise KiWISError(
                    'KIWIS returned an error:\n\tCode: {0}\n\tMessage: "{1}"'.format(
                        req_json["code"], req_json["message"]
                    )
                )
            return pd.DataFrame(req_json)
        else:
            if req.status_code != 200:
                raise KiWISError(
                    "KiWIS returned an Error:\n\tCode:\t%i\n\tMessage:\t%s" % (req.status_code, req.content)
                )
            return req

    def getStationList(
        self,
        format="objson",
        stationgroup_id=None,
        site_no=None,
        site_id=None,
        station_no=None,
        station_id=None,
        station_uuid=None,
        returnfields=None,
        catchment_no=None,
        catchment_name=None,
        site_uuid=None,
        site_name=None,
        parametertype_id=None,
        stationparameter_name=None,
        object_type=None,
        object_type_shortname=None,
        bbox=None,
        csvdiv=None,
        crs=None,
        ca_site_returnfields=None,
        ca_sta_returnfields=None,
        jsoncallback=None,
        downloadaszip=None,
        downloadfilename=None,
        flatten=None,
        addlinks=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getStationList")
        kiwis_result = self.make_request("getStationList", res)
        return kiwis_result

    def getTimeseriesList(
        self,
        format="objson",
        timeseriesgroup_id=None,
        returnfields=None,
        station_no=None,
        station_id=None,
        ts_id=None,
        ts_path=None,
        ts_name=None,
        station_name=None,
        ts_shortname=None,
        ts_type_id=None,
        parametertype_id=None,
        parametertype_name=None,
        stationparameter_name=None,
        stationparameter_no=None,
        ts_unitname=None,
        csvdiv=None,
        dateformat=None,
        timezone=None,
        jsoncallback=None,
        downloadaszip=None,
        downloadfilename=None,
        ca_site_returnfields=None,
        ca_sta_returnfields=None,
        ca_par_returnfields=None,
        ca_ts_returnfields=None,
        addlinks=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getTimeseriesList")
        kiwis_result = self.make_request("getTimeseriesList", res)
        return kiwis_result

    def getTimeseriesEnsembleValues(self, format="json", **kwargs):
        kwargs.update(format=format)
        res = self._pre_request_check(kwargs, "getTimeseriesEnsembleValues")
        kiwis_result = self.make_request("getTimeseriesEnsembleValues", res)
        return kiwis_result

    def getTimeseriesValues(
        self,
        format="dajson",
        ts_id=None,
        timeseriesgroup_id=None,
        from_=None,
        to=None,
        ts_path=None,
        returnfields=None,
        period=None,
        csvdiv=None,
        metadata=None,
        md_returnfields=None,
        custattr_returnfields=None,
        ca_site_returnfields=None,
        ca_sta_returnfields=None,
        ca_par_returnfields=None,
        ca_ts_returnfields=None,
        dateformat=None,
        timezone=None,
        crs=None,
        valueorder=None,
        useprecision=None,
        valuelocale=None,
        jsoncallback=None,
        downloadaszip=None,
        downloadfilename=None,
        getensembletimestampsonly=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getTimeseriesValues")
        kiwis_result = self.make_request("getTimeseriesValues", res)
        return kiwis_result

    def getTimeseriesValueLayer(
        self,
        format="objson",
        ts_id=None,
        timeseriesgroup_id=None,
        returnfields=None,
        bbox=None,
        stationparameter_no=None,
        ts_shortname=None,
        date=None,
        valuecolumn=None,
        site_no=None,
        csvdiv=None,
        metadata=None,
        md_returnfields=None,
        custattr_returnfields=None,
        ca_sta_returnfields=None,
        ca_par_returnfields=None,
        ca_ts_returnfields=None,
        dateformat=None,
        timezone=None,
        crs=None,
        orderby=None,
        orderdir=None,
        invalidperiod=None,
        invalidvalue=None,
        showemptytimeseries=None,
        hidetsid=None,
        useprecision=None,
        valuelocale=None,
        jsoncallback=None,
        downloadaszip=None,
        downloadfilename=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getTimeseriesValueLayer")
        kiwis_result = self.make_request("getTimeseriesValueLayer", res)
        return kiwis_result

    def getSiteList(
        self,
        format="objson",
        returnfields=None,
        site_no=None,
        site_id=None,
        site_uuid=None,
        site_name=None,
        parametertype_id=None,
        parametertype_name=None,
        stationparameter_name=None,
        bbox=None,
        csvdiv=None,
        crs=None,
        custattr_returnfields=None,
        ca_site_returnfields=None,
        jsoncallback=None,
        downloadaszip=None,
        downloadfilename=None,
        addlinks=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getSiteList")
        kiwis_result = self.make_request("getSiteList", res)
        return kiwis_result

    def getParameterList(
        self,
        format="objson",
        station_no=None,
        station_id=None,
        returnfields=None,
        station_name=None,
        site_no=None,
        site_name=None,
        stationparameter_id=None,
        stationparameter_name=None,
        stationparameter_no=None,
        stationparameter_longname=None,
        parametertype_id=None,
        parametertype_name=None,
        parametertype_longname=None,
        csvdiv=None,
        jsoncallback=None,
        ca_par_returnfields=None,
        downloadaszip=None,
        downloadfilename=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(
            locals2_,
            "getParameterList",
        )
        kiwis_result = self.make_request("getParameterList", res)
        return kiwis_result

    def getParameterTypeList(
        self,
        format="objson",
        returnfields=None,
        parametertype_id=None,
        parametertype_name=None,
        csvdiv=None,
        jsoncallback=None,
        downloadaszip=None,
        downloadfilename=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getParameterTypeList")
        kiwis_result = self.make_request("getParameterTypeList", res)
        return kiwis_result

    def getTimeseriesTypeList(
        self,
        format="objson",
        returnfields=None,
        ts_type_id=None,
        ts_shortname=None,
        ts_name=None,
        csvdiv=None,
        jsoncallback=None,
        downloadaszip=None,
        downloadfilename=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getTimeseriesTypeList")
        kiwis_result = self.make_request("getTimeseriesTypeList", res)
        return kiwis_result

    def getGroupList(
        self,
        format="objson",
        group_name=None,
        returnfields=None,
        group_type=None,
        supergroup_name=None,
        csvdiv=None,
        jsoncallback=None,
        downloadaszip=None,
        downloadfilename=None,
        ca_group_returnfields=None,
        addlinks=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getGroupList")
        kiwis_result = self.make_request("getGroupList", res)
        return kiwis_result

    def getGraph(
        self,
        format="png",
        ts_id=None,
        ext_ts_id=None,
        from_=None,
        to=None,
        period=None,
        width=None,
        height=None,
        template=None,
        showgroups=None,
        overlayinterval=None,
        overlayslices=None,
        renderer=None,
        timezone=None,
        downloadaszip=None,
        downloadfilename=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getGraph")
        kiwis_result = self.make_request("getGraph", res)
        return kiwis_result

    def getStationGraph(
        self,
        format="png",
        station_id=None,
        from_=None,
        to=None,
        period=None,
        width=None,
        height=None,
        template=None,
        showgroups=None,
        overlayinterval=None,
        overlayslices=None,
        timezone=None,
        downloadaszip=None,
        downloadfilename=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getStationGraph")
        kiwis_result = self.make_request("getStationGraph", res)
        return kiwis_result

    def getGraphTemplateList(self, format="tabjson", csvdiv=None, jsoncallback=None, **kwargs):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getGraphTemplateList")
        kiwis_result = self.make_request("getGraphTemplateList", res)

    def getWqmSampleValuesAsTimeseriesByFilter(
        self,
        format="dajson",
        parametertype_shortname=None,
        site_no=None,
        catchment_name=None,
        sh_=None,
        from_=None,
        to=None,
        period=None,
        csvdiv=None,
        downloadaszip=None,
        downloadfilename=None,
        dateformat=None,
        timezone=None,
        metadata=None,
        md_returnfields=None,
        valueorder=None,
        valuelocale=None,
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getWqmSampleValuesAsTimeseriesByFilter")
        kiwis_result = self.make_request("getWqmSampleValuesAsTimeseriesByFilter", res)
        return kiwis_result

    def getReleaseStateClasses(
        self,
        format="objson",
        **kwargs,
    ):
        locals_ = locals()

        # I don't know why locals get updated, however this dict comprehension creates a new dict that will not update
        locals2_ = {
            argname: arg
            for (argname, arg) in locals_.items()
            if argname not in self.__not_params and arg is not None
        }
        for key, value in kwargs.items():
            locals2_[key] = value
        locals_ = None
        res = self._pre_request_check(locals2_, "getReleaseStateClasses")
        kiwis_result = self.make_request("getReleaseStateClasses", res)
        return kiwis_result
