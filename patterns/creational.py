import copy


class User:
	pass


class Teacher(User):
	pass


class UserFactory:
	types = {
		'user': User,
		'teacher': Teacher,
	}

	@classmethod
	def create(cls, type):
		return cls.types[type]()


class CoursePrototype:
	def clone(self):
		return copy.deepcopy(self)


class Course(CoursePrototype):
	def __init__(self, name, category, duration):
		self.name = name
		self.category = category
		self.duration = duration
		self.category.courses.append(self)


class OnlineCourse(Course):
	pass


class OfflineCourse(Course):
	pass


class CourseFactory:
	types = {
		'online': OnlineCourse,
		'offline': OfflineCourse,
	}

	@classmethod
	def create(cls, type, name, category, duration):
		return cls.types[type](name, category, duration)


class Category:
	auto_id = 0

	def __init__(self, name, category, duration):
		self.id = Category.auto_id
		Category.auto_id += 1
		self.name = name
		self.category = category
		self.duration = duration
		self.courses = []

	def course_count(self):
		result = len(self.courses)
		if self.category:
			result += self.category.course_count()
		return result


class Engine:
	def __init__(self):
		self.teachers = []
		self.users = []
		self.courses = []
		self.categories = []

	@staticmethod
	def create_user(type):
		return UserFactory.create(type)

	@staticmethod
	def create_category(name, duration, category=None):
		return Category(name, category, duration)

	def find_category_by_id(self, id):
		for item in self.categories:
			print('item', item.id)
			if item.id == id:
				return item
		raise Exception(f'Нет категории с таким id: {id}')

	@staticmethod
	def create_course(type, name, category, duration):
		return CourseFactory.create(type, name, category, duration)

	def get_course(self, name):
		for item in self.courses:
			if item.name == name:
				return item
		return None

	@staticmethod
	def decode_value(data):
		new_data = {}
		for key, str_value in data.items():
			while '%' in str_value:
				idx = str_value.index('%')
				hex_part = str_value[idx: idx + 3]
				str_value = str_value.replace(hex_part, bytes.fromhex(hex_part[1:]).decode('utf-8'))
			new_data[key] = str_value
		return new_data


class SingletonByName(type):
	def __init__(cls, name, bases, attrs, **kwargs):
		super(SingletonByName, cls).__init__(name, bases, attrs)
		cls.__instance = {}

	def __call__(cls, *args, **kwargs):
		name = None
		if args:
			name = args[0]
		if kwargs:
			name = kwargs['name']
		if name in cls.__instance:
			return cls.__instance[name]
		else:
			cls.__instance[name] = super().__call__(*args, **kwargs)
			return cls.__instance[name]

class Logger(metaclass=SingletonByName):

	def __init__(self, name):
		self.name = name

	@staticmethod
	def log(text):
		print('log: ', text)