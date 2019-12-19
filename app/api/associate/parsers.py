from flask_restful import reqparse

# 添加参数
name_parse = reqparse.RequestParser()
name_parse.add_argument('word', type=str, required=True, help='word')