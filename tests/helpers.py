import random
import string

def generate_unique_email():
    return f"test_{''.join(random.choices(string.ascii_lowercase, k=7))}@examlpe.com"