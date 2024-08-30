import random
import string
import time


class IDGenerator:
    def generate_custom_id(self, prefix):
        timestamp = str(int(time.time()))
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"{prefix}-{timestamp}-{random_chars}"
