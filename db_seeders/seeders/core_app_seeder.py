
from core.factories import UserFactory


def run(data=200):
    UserFactory.create_batch(data)
    
        