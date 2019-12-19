from flask import jsonify
from ..exceptions import ResourceNotExistError
from ..exceptions import ResourceAlreadyExistsError
from ..exceptions import ResourceStatusError
from . import bp


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@bp.errorhandler(ValueError)
def validation_error(e):
    return bad_request(e.args[0])


@bp.errorhandler(ResourceNotExistError)
def resource_not_exist_error(e):
    response = jsonify({'error': 'Gone', 'message': e.args[0], 'code': 410})
    response.status_code = 200
    return response


@bp.errorhandler(ResourceAlreadyExistsError)
def resource_already_exists_error(e):
    response = jsonify({'error': 'Conflict', 'message': e.args[0], 'code': 409})
    response.status_code = 200
    return response


@bp.errorhandler(ResourceStatusError)
def resource_status_error(e):
    response = jsonify({'error': 'Conflict', 'message': e.args[0], 'code': 409})
    response.status_code = 200
    return response
