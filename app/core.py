from models import Generator, Section
import json


def compile_schedules(data, gen_id):
    gen_object = Generator.objects(pk=gen_id).first()
    full_classes = gen_object.sections

    sections_dict = dict()
    for course in full_classes:
        for thing in course:
            section_list = [Section.objects(pk=section).first().to_mongo().to_dict() for section in course[thing]]
            for item in section_list:
                item['_id'] = str(item['_id'])
            sections_dict[thing] = section_list

    data['sections'] = sections_dict
    with open('tmp/in/{0}.JSON'.format(gen_id), 'w') as outfile:
        json.dump(data, outfile)

    return
