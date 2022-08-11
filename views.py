from pepperoni_framework.templator import render


class Index:
	def __call__(self, request):
		return '200 OK', render('index.html', data=request.get('data', None))


class About:
	def __call__(self, request):
		return '200 OK', render('about.html')


class Login:
	def __call__(self, request):
		return '200 OK', render('login.html')


class Contact:
	def __call__(self, request):
		return '200 OK', render('contact.html')
