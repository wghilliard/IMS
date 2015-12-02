from mongoengine import Document, StringField, DictField, DateTimeField, ListField, IntField, UUIDField, \
    ObjectIdField, ReferenceField


class Section(Document):
    meta = {'collection': 'sections'}
    class_number = StringField()
    department = StringField()
    section_number = StringField(unique=True)
    room = StringField()
    instructor = StringField()
    unformatted_day_time = StringField()
    start_time = DictField()
    end_time = DictField()
    repetition = DictField()
    uuid = UUIDField()


class Generator(Document):
    meta = {'collection': 'generators'}
    owner = ObjectIdField()
    classes = ListField(DictField())
    tag_uuid = UUIDField()
    sections = ListField(DictField())
    block_outs = ListField(DictField())
    status = DictField()
    error = StringField()

    def fetch_sections(self):
        pass
