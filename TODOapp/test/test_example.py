import pytest

def test_equal_or_not_equal():
    assert 3 == 3

def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)


def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, year: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year

@pytest.fixture
def default_employee():
    return Student('John', 'Doe', major='Computer Science', year=3)

def test_person_initialization(default_employee):
    assert default_employee.first_name == 'John', 'First name should be John'
    assert default_employee.last_name == 'Doe', 'Last name should be Doe'
    assert default_employee.major == 'Computer Science', 'Major should be Computer Science'
    assert default_employee.year == 3
