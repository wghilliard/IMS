# {
#     "classes": [{
#         "name": "MATH",
#         "number": "1301"
#     }, {
#         "name": "CSE",
#         "number": "1301"
#     }],
#     "commute": {
#         "workToSchool": "20",
#         "homeToSchool": "30",
#         "workToHome": "60"
#     },
#     "sleep": "8",
#     "block_outs": [{
#         "name": "work",
#         "location": "work",
#         "start_time": {
#             "hour": "08",
#             "minute": "30"
#         },
#         "end_time": {
#             "hour": "12",
#             "minute": "30"
#         },
#         "repetition": {
#             "mon": False,
#             "tues": False,
#             "weds": False,
#             "thurs": False,
#             "fri": False,
#             "sat": False,
#             "sun": False
#         }
#     }, {
#         "name": "lol",
#         "location": "home",
#         "start_time": {
#             "hour": "17",
#             "minute": "30"
#         },
#         "end_time": {
#             "hour": "20",
#             "minute": "30"
#         }
#         "repetition": {
#             "mon": False,
#             "tues": False,
#             "weds": False,
#             "thurs": False,
#             "fri": False,
#             "sat": False,
#             "sun": False
#         }
#     }]
# }
# // Types: ["work", "class", "commute", "sleep", "study", "other"]

from user import User
from app.models import Generator, Section
# from scheduler import Scheduler


def compile_schedules(commute, sleep, study, blocks, gen_id):
    gen_object = Generator.objects(pk=gen_id).first()
    full_classes = gen_object.sections

    sections_dict = dict()
    for course in full_classes:
        for thing in course:
            sections_dict[thing] = [Section.objects(pk=section).first() for section in course[thing]]

    print sections_dict



    return
