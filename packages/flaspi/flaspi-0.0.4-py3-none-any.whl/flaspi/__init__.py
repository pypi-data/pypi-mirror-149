
# flask api tool [flaspi]

import sys
import json
import flask
import random
import requests

# create post api [flaspi]
def post_api(path, api_func, app):
	# 登録対象の関数
	def temporary_func():
		# リクエストをjson形式で受け取り
		request_obj = flask.request.json
		# 処理の実行
		response_obj = api_func(request_obj)
		# 返却されたオブジェクトをjson形式にして返す
		try:
			response_json = json.dumps(response_obj, ensure_ascii = False, indent = 2)
			return response_json
		except:
			# jsonフォーマットに則っていない場合
			return "invalid_response_json_format", 500
	# flaskの仕様により、同名の関数を登録できないので、関数の内部の名前をランダムなものに変更
	rand_str = str(random.random()).replace("0.", "")
	temporary_func.__name__ = 'rand_func_name_%s'%rand_str
	# 関数の登録 (関数名を毎回変えるため、デコレータをバラして書いている)
	app.route(path, methods = ["post"])(temporary_func)

# call post api [flaspi]
def call_post_api(path, data):
	res = requests.post(path, json = data)
	# レスポンスの分解
	status_code = res.status_code
	if status_code == 200:
		json_obj = json.loads(res.text)
	else:
		json_obj = res.text
	return status_code, json_obj
