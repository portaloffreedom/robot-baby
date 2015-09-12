class Message:

    def __init__(self, hash_code, message):
        self.hash_code = hash_code
        self.message = message

    def __str__(self):
        return self.message
