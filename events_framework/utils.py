class AbstractEvents:
    CHOICES = []

    @classmethod
    def as_choices(cls):
        return [(type_name, label) for type_name, label in cls.CHOICES]
