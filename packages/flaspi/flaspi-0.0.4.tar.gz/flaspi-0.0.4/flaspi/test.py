
# flask api tool [flaspi]

import sys
import flask
from ezpip import load_develop
# flask api tool [flaspi]
flaspi = load_develop("flaspi", "../", develop_flag = True)

# create flask app
app = flask.Flask(__name__)

# function for api
def greeting_func(request_obj):
	name = request_obj["name"]
	response_obj = {
		"message": "Hello, %s!!"%name
	}
	return response_obj

# create post api [flaspi]
flaspi.post_api("/greeting", greeting_func, app = app)

# run server
app.run(host = "0.0.0.0", port = "80", debug = False)

# api call example
# curl http://localhost:80/greeting -X POST -H "Content-Type: application/json" --data '{"name": "Hoge"}'
