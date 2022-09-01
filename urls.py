from datetime import date
from views import Index, About, Login, Contact, CoursesList, CreateCourse, CreateCategory, CategoryList, CopyCourse


def secret_front(request):
	request['data'] = date.today()


def other_front(request):
	request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
	'/': Index(),
	'/about/': About(),
	'/login/': Login(),
	'/contact/': Contact(),
	'/courses-list/': CoursesList(),
	'/create-course/': CreateCourse(),
	'/create-category/': CreateCategory(),
	'/category-list/': CategoryList(),
	'/copy-course/': CopyCourse(),
}
