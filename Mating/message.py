class Message:

    def __init__(self, message=None):
        self.message = message or ''

    def __str__(self):
        return self.message


class PersonalMessage(Message):

    def __init__(self, hash_code, message):
        Message.__init__(self, message)
        self.hash_code = hash_code


class GenomeMessage(PersonalMessage):

    def __init__(self, hash_code, filename):
        with open(filename, 'r') as genome_file:
            genome = genome_file.read()
            if self.validate_genome(genome):
                self.message = genome
            else:
                raise ValueError('Malformed genome file')
        PersonalMessage.__init__(self, hash_code, self.message)

    def validate_genome(genome):
        return True  # TODO: Change
