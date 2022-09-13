import copy
from behavioral import ConsoleWriter, Subject
from unit_of_work import DomainObject
import sqlite3

from patterns.data_mappers import StudentMapper


class User:
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, name):
        self.courses = []
        super(Student, self).__init__(name)


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type, name):
        return cls.types[type](name)


class CoursePrototype:
    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super(Course, self).__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class OfflineCourse(Course):
    pass


class OnlineCourse(Course):
    pass


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class CourseFactory:
    types = {
        'offlinecourse': OfflineCourse,
        'onlinecourse': OnlineCourse,
    }

    @classmethod
    def create(cls, type, name, category):
        return cls.types[type](name, category)


class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type, name):
        return UserFactory.create(type, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'category with id={id} does not exists')

    @staticmethod
    def create_course(type, name, category):
        return CourseFactory.create(type, name, category)

    def get_course_by_name(self, name) -> Course | None:
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student_by_name(self, name) -> Student | None:
        for item in self.students:
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


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super(Singleton, cls).__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        else:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):
    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'logger ::: {text}'
        self.writer.write(text)


connection = sqlite3.connect('patterns.sqlite')


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
