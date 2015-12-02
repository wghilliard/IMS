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


def compile_schedules(data, gen_id):
    import json
    gen_object = Generator.objects(pk=gen_id).first()
    full_classes = gen_object.sections

    sections_dict = dict()
    for course in full_classes:
        for thing in course:
            section_list = [Section.objects(pk=section).first().to_mongo().to_dict() for section in course[thing]]
            for item in section_list:
                item['_id'] = str(item['_id'])
            sections_dict[thing] = section_list

    print(sections_dict)
    data['sections'] = sections_dict
    with open('tmp/in/{0}.JSON'.format(gen_id), 'w') as outfile:
        json.dump(data, outfile)

    return


# def filter_one(sections_dict, block_outs_w_sleep):
#     for course in sections_dict:
#         for section in course:
#             for block in block_outs_w_sleep:
#                 for day in block.repetition:
#                     if block.repetition[day] == section.repetition[day]:
#                         # if
#                         pass
#
#     return
#
#
# def check_no_conflicts(block_one, block_two):
#     pass


# def add_in_sleep(sleep, block_outs):
#     print "IN ADD IN SLEEP"
#
#     print sleep
#     print block_outs
#
#     sleep_block = {
#         "name": "sleep",
#         "location": "home",
#         "start_time": {
#             "hour": "00",
#             "minute": "00"
#         },
#         "end_time": {
#             "hour": str(sleep),
#             "minute": "00"
#         },
#         "repetition": {
#             "mon": "true",
#             "tues": "true",
#             "weds": "true",
#             "thurs": "true",
#             "fri": "true",
#             "sat": "true",
#             "sun": "true"
#         }
#     }
#
#     block_outs.append(sleep_block)
#     return block_outs
