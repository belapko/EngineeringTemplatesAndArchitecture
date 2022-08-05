from datetime import date
from views import Index, About


def secret_front(request):
	request['data'] = date.today()
	print(request)


def other_front(request):
	request['key'] = 'key'
	print('-' * 50, 'other front')
	print(request)


fronts = [secret_front, other_front]

routes = {
	'/': Index(),
	'/about/': About(),
}
