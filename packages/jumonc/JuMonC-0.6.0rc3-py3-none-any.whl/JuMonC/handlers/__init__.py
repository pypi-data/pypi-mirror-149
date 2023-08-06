"""
The handlers package of JuMonC provides the handlers to interact with JuMonC using the REST-API.

The REST API is documented with openapi, and rendered well by gitlab on:
https://gitlab.jsc.fz-juelich.de/witzler1/jumonc/-/blob/CI_fixes/doc/REST_API/openapi.yaml
"""

import logging

from flask import jsonify, make_response, Response


from JuMonC.handlers.base import RESTAPI
from JuMonC._version import __version__
from JuMonC.tasks import taskID, taskSwitcher
from JuMonC.authentication import scopes
from JuMonC.authentication.check import check_auth


logger = logging.getLogger(__name__)


@RESTAPI.route("/ping", methods=["GET"])
def ping() -> str:
    return "PONG.\n"


@RESTAPI.route("/stop")
@check_auth(scopes["full"])
def stopJuMonC() -> Response:
    
    
    taskSwitcher.taskSwitcher().addTask([taskID.finalize])
    
    return make_response(jsonify("Stopping server and shutting down JuMonC\n"), 200)


@RESTAPI.route("/version", methods=["GET"])
def version() -> Response:
    response_body = {"JuMonC_version": __version__}
    return make_response(jsonify(response_body), 200)


@RESTAPI.route("/all_links", methods=["GET"])
@check_auth(scopes["full"])
def allLinks() -> Response:
    return make_response(jsonify(RESTAPI.url_map), 200)
