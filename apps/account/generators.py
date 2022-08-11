import os
import random

from . import anonymous

def generate_anonymous_name():
    names = anonymous.ret_names()
    return names[random.randint(0, len(names))]


def generate_random_string_number(length=5):
    return "".join([ str(random.randint(0, 9)) for i in range(length)])

def generate_anonymous_username():
    return generate_anonymous_name() + generate_random_string_number()