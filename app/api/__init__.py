from flask import Blueprint
from flask_restful import Api

from .associate.resources.name import SchoolName, CompanyName

bp = Blueprint('api', __name__, url_prefix='')
api = Api(bp, catch_all_404s=True)

api.add_resource(SchoolName, '/api/name/school_name/', '/school_name/')

api.add_resource(CompanyName, '/api/name/com_name/', '/com_name/')
