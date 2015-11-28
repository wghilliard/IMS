from mongoengine import Document, StringField, DictField, DateTimeField, ListField, IntField, UUIDField


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
