import json
import re
from collections import defaultdict

import pymysql
from flask_restful import Resource
from flask import current_app, jsonify
from app.utils.mongo_util import MongoJDAli
from ..parsers import name_parse


class SchoolName(Resource):
	"""实体名称消歧联想"""

	def get(self):
		di = dict()
		args = ""
		try:
			client = MongoJDAli().client()
			school_name_associate = client.applet_test.school_name_associate
			args = name_parse.parse_args()
			current_app.logger.info(f'request data: {args}')
			word = args.word
			word = word.lower()
			dic = dict()
			# print(word)
			# lic.append(cluster_company_api(word))

			for c in school_name_associate.find({"origin_name": {"$regex": word, '$options': 'i'}}):
				dic[c['pure_name']] = c['score']
			# print(lic)

			for c in school_name_associate.find({"py_name": {"$regex": word, '$options': 'i'}}):
				dic[c['pure_name']] = c['score']
			# print(lic)

			for c in school_name_associate.find({"pure_name": {"$regex": word, '$options': 'i'}}):
				dic[c['pure_name']] = c['score']
			# print(lic)

			lic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
			lic = [a[0] for a in lic[:10]]
			ret = school_name_associate.find_one({'origin_name': word})
			if ret:
				pure_name = ret['pure_name']
				print(pure_name)
				if pure_name not in lic:
					lic.insert(0, pure_name)
				else:
					lic = [i for i in lic if i != pure_name]
					lic.insert(0, pure_name)
			di['status'] = 200
			di['data'] = lic
			client.close()
		except Exception as e:
			di['message'] = "error: " + str(e) + "|||args:" + str(args)
			di['status'] = 500
			di['data'] = []

		return jsonify(di)

	def post(self):
		return self.get()


class CompanyName(Resource):
	def get(self):
		di = dict()
		try:
			mysql_di = eval(current_app.config['MYSQL_URI'])
			conn = pymysql.connect(host=mysql_di['host'], user=mysql_di['user'], passwd=mysql_di['passwd'],
			                       db=mysql_di['db'], port=mysql_di['port'],
			                       charset='utf8')
			cursor = conn.cursor()

			args = name_parse.parse_args()
			current_app.logger.info(f'request data: {args}')
			word = args.word
			lic = list()
			# print(word)
			# lic.append(cluster_company_api(word))
			sql = "select * from com_name where origin_com_name like '%{}%' limit 10".format(word)
			# sql = "select * from com_name where instr(origin_com_name,'{}')>0  limit 10".format(word)
			cursor.execute(sql)
			data = cursor.fetchall()
			if data:
				for c in data:
					lic.append(c[0])
			# print(lic)
			sql2 = "select * from com_name where new_com_name like '{}' limit 10".format(word)
			# sql2 = "select * from com_name where instr(new_com_name,'{}')>0  limit 10".format(word)
			cursor.execute(sql2)
			data2 = cursor.fetchall()
			if data2:
				for c in data:
					lic.append(c[0])
			# print(lic)
			lic = list(set(lic))[:10]
			di['status'] = 200
			di['data'] = lic
			cursor.close()  # 关闭游标
			conn.close()
		except Exception as e:
			di['error'] = "error: " + str(e)
			di['status'] = 500
			di['data'] = []
		return jsonify(di)

	def post(self):
		return self.get()
