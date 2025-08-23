
from factory import django, faker

from .models import User

class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = faker.Faker('user_name')
    email = faker.Faker("email")
    first_name = faker.Faker('first_name')
    last_name = faker.Faker("last_name")
    password = faker.Faker("password", length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    
    
    
    