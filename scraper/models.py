from mongoengine import Document, StringField, DictField, DateTimeField, ObjectIdField, BooleanField, ListField, \
    ReferenceField, IntField, UUIDField
from name_generator import gen_name
import datetime


class User(Document):
    meta = {'collection': 'users'}
    username = StringField(max_length=20, unique=True)
    nickname = StringField()
    password = StringField()
    email = StringField()
    authenticated = BooleanField(default=False)
    ip_log = ListField(StringField())
    schedules = ListField(ObjectIdField())

    @property
    def is_valid(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<USER %r>' % (self.username)


# class Schedule(Document):
#     meta = {'collection': 'schedules'}
#     creation_date = DateTimeField()
#     modified_date = DateTimeField()
#     name = StringField()
#     valid = BooleanField()
#     blocks = ListField(ListField(ListField(DictField())))
#     sections = ListField(ReferenceField(Document))
#
#     def save(self, *args, **kwargs):
#         if not self.creation_date:
#             self.creation_date = datetime.datetime.now()
#         self.modified_date = datetime.datetime.now()
#         if not self.name:
#             self.name = gen_name()
#         return super(Schedule, self).save(*args, **kwargs)
#
#     @property
#     def is_valid(self):
#         return self.valid
#
#     def __repr__(self):
#         return '<SCHEDULE %r>' % (self.name)


class Section(Document):
    meta = {'collection': 'sections'}
    class_number = IntField()
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


class Schedule(Document):
    meta = {'collection': 'schedules'}
    creation_date = DateTimeField()
    modified_date = DateTimeField()
    name = StringField()
    valid = BooleanField()
    sections = ListField(ObjectIdField())

    monday = ListField(DictField())
    tuesday = ListField(DictField())
    wednesday = ListField(DictField())
    thursday = ListField(DictField())
    friday = ListField(DictField())
    saturday = ListField(DictField())
    sunday = ListField(DictField())

    def save(self, *args, **kwargs):
        if not self.valid:
            self.valid = True
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        if not self.name:
            self.name = gen_name()
        return super(Schedule, self).save(*args, **kwargs)
