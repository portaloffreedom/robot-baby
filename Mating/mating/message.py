import codecs

MESSAGE_INTERVAL_SEC = 0.5


class Message:

    def __init__(self, message=None):
        self.message = message or ''

    def __str__(self):
        return self.message


class PersonalMessage(Message):
    """ PersonalMessage sends a hash_code along with the message itself, in
        order to be able to identify individuals (or one's self).
    """
    def __init__(self, hash_code, message):
        Message.__init__(self, message)
        self.hash_code = hash_code


class GenomeMessage(PersonalMessage):
    """ Class that reads a genome from a .genome file and uses it as a message
        string.
    """
    def __init__(self, hash_code, filename):
        def validate_genome(genome):
            """ Checks if the genome is in the correct format
                (i.e syntax errors in the .genome file).
                Returns true if it is, false otherwise.
            """
            if genome:
                return True  # TODO: Implement

        with codecs.open(filename, 'r', 'utf-8') as genome_file:
            genome = genome_file.read()
            if validate_genome(genome):
                self.message = genome
            else:
                raise ValueError('Malformed genome file')
        PersonalMessage.__init__(self, hash_code, self.message)
