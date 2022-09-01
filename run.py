from pepperoni_framework.main import Pepperoni
from urls import routes, fronts
from wsgiref.simple_server import make_server

application = Pepperoni(routes, fronts)

with make_server('', 8000, application) as httpd:
	print(f'Server started at {httpd.server_address}')
	httpd.serve_forever()