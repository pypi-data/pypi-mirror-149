import logging

from flask import jsonify, make_response, Response

from typing import Dict, List, Union


from JuMonC.handlers.base import api_version_path, check_version, RESTAPI
from JuMonC.authentication import scopes
from JuMonC.authentication.check import check_auth


logger = logging.getLogger(__name__)

links: List[Dict[str, Union[str, Dict[str, str]]]] = []

gpu_path = "/gpu"

@RESTAPI.route(api_version_path + gpu_path, methods=["GET"])
@check_version
@check_auth(scopes["see_links"])
def returnGPULinks(version: int) -> Response:
    logging.debug("Accessed /v%i/gpu/", version)
    return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)

def registerRestApiPaths(version: int) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    return {
        "link": "/v" + str(version) + gpu_path,
        "isOptional": False,
        "description": "Gather information concerning the GPU",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }