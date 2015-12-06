from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from models import Section, Generator, Schedule, User
import datetime
import re, json, os
from selenium.common.exceptions import NoSuchFrameException
from uuid import uuid4
from __init__ import worker
from pymongo.errors import PyMongoError


@worker.task(name='tasks.parse')
def parse(gen_id, loaded_data):
    gen_object = Generator.objects(pk=gen_id).first()
    section_list = list()
    class_list = gen_object.classes
    for thing in class_list:
        section_objects = Section.objects(class_number=thing['number'], department=thing['name'])
        # print section_objects
        if section_objects:
            section_list.append({thing['name'] + "_" + thing['number']: [section.id for section in section_objects]})
        else:
            holder = scrape(thing['name'], thing['number'])
            # print holder
            if len(holder) == 0:
                gen_object.status['fetch'] = 'failed'
                gen_object.error = "Could not fetch {0} {1}.".format(thing['name'], thing['number'])
                gen_object.save()
                return
            section_list.append({thing['name'] + "_" + thing['number']: holder})

    gen_object.sections = section_list
    gen_object.status['fetch'] = 'complete'
    gen_object.save()

    compile_schedules(gen_object.id, loaded_data)
    save_output(gen_object.id)
    return


@worker.task(name='tasks.save_output')
def save_output(gen_id):
    with open('scheduler_final/tmp/out/{0}.JSON'.format(gen_id), 'r') as infile:
        in_data = json.load(infile)

    # os.remove('scheduler_final/tmp/out/{0}.JSON'.format(gen_id))
    # os.remove('scheduler_final/tmp/in/{0}.JSON'.format(gen_id))

    gen_object = Generator.objects(pk=gen_id).first()

    sched_list = list()
    try:
        if in_data['status'] != 'complete':
            gen_object.status['compile'] = in_data['status']
            gen_object.error = in_data['error']
        else:
            for schedule in in_data['schedules']:
                # print schedule
                sched_id = Schedule(**schedule).save().id
                sched_list.append(sched_id)
            user = User.objects(pk=gen_object.owner).first()
            user.schedules = user.schedules + sched_list
            user.save()
            gen_object.status['compile'] = 'complete'

    except KeyError as e:
        print e
        gen_object.status['compile'] = 'failed'
        gen_object.error = 'UKNOWN'

    except PyMongoError as e:
        gen_object.status['compile'] = 'failed'
        gen_object.error = 'UKNOWN'

        print e

    finally:
        gen_object.save()
        # print sched_list


@worker.task(name='tasks.compile_schedules')
def compile_schedules(gen_id, data):
    gen_object = Generator.objects(pk=gen_id).first()
    full_classes = gen_object.sections
    new_data = data_sans(data)
    sections_dict = dict()
    for course in full_classes:
        for thing in course:
            section_list = [Section.objects(pk=section).first().to_mongo().to_dict() for section in course[thing]]
            for item in section_list:
                item['_id'] = str(item['_id'])

            sections_dict[thing] = section_list

    new_data['sections'] = sections_dict
    with open('scheduler_final/tmp/in/{0}.JSON'.format(gen_id), 'w') as outfile:
        json.dump(new_data, outfile)

    os.system("cd scheduler_final; java -cp json-simple-1.1.1.jar:. Scheduler " + str(gen_id) + ".JSON; cd ..")
    return


@worker.task(name='tasks.data_sans')
def data_sans(data):
    data['sleep'] = "{0}".format(data['sleep'])
    # print data
    for item in data['commute']:
        data['commute'][item] = "{0}".format(data['commute'][item])
    holder = data['block_outs']
    out_list = list()
    for block in holder:
        # print "block ", block['sTime'][11:13]
        # print "block2", block['sTime'][14:16]
        block['start_time'] = {
            "hour": "{0}".format(block['sTime'][11:13]),
            "minute": "{0}".format(block['sTime'][14:16])
        }
        block['end_time'] = {
            "hour": "{0}".format(block['eTime'][11:13]),
            "minute": "{0}".format(block['eTime'][14:16])
        }
        out_list.append(block)
    data['block_outs'] = out_list
    # print "out", data
    return data


@worker.task(name='tasks.scrape')
def scrape(class_dept, class_number):
    driver = webdriver.Firefox()
    driver.get(
        'https://sis-portal-prod.uta.edu/psp/AEPPRD/EMPLOYEE/PSFT_ACS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?pslnkid=UTA_PS_CLASS_SCHEDULE_LINK&PORTALPARAM_PTCNAV=UTA_PS_CLASS_SCHEDULE&EOPP.SCNode=EMPL&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=ADMN_CATALOGS_AND_CLASSES&EOPP.SCLabel=Catalogs%20and%20Classes&EOPP.SCPTcname=&FolderPath=PORTAL_ROOT_OBJECT.PORTAL_BASE_DATA.CO_NAVIGATION_COLLECTIONS.ADMN_CATALOGS_AND_CLASSES.ADMN_S200910131407282926114688&IsFolder=false')
    # sleep(5)
    while True:
        try:
            driver.switch_to.frame('ptifrmtgtframe')
            break
        except NoSuchFrameException:
            pass
        except Exception as e:
            print type(e)
            print e

    driver.find_element_by_name('SSR_CLSRCH_WRK_SUBJECT$0').send_keys(class_dept)

    driver.find_element_by_name('SSR_CLSRCH_WRK_CATALOG_NBR$1').click()
    try:
        driver.find_element_by_id('SUBJECT_TBL_DESCR$0')
    except Exception as e:
        print e
        print type(e)
    sleep(3)
    driver.find_element_by_name('SSR_CLSRCH_WRK_CATALOG_NBR$1').send_keys(class_number)
    driver.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()
    sleep(2)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    driver.close()

    soup = BeautifulSoup(html, "html.parser")
    # print soup.prettify()

    section_list = list()
    for i in range(0, 20):
        try:
            soup.find(id='MTG_CLASSNAME${0}'.format(i)).get_text()
            section_list.append(dict())
            # print '##############'
            section_list[i]['section_number'] = soup.find(id='MTG_CLASSNAME${0}'.format(i)).get_text()
            section_list[i]['unformatted_day_time'] = soup.find(id='MTG_DAYTIME${0}'.format(i)).get_text()
            section_list[i]['room'] = soup.find(id='MTG_ROOM${0}'.format(i)).get_text()
            section_list[i]['instructor'] = soup.find(id='MTG_INSTR${0}'.format(i)).get_text()
            # print '##############'

        except Exception as e:
            # print e
            pass

    for section in section_list:
        if section['unformatted_day_time'] == 'TBA':
            continue
        process_array = section['unformatted_day_time'].split()

        # print process_array

        repetition = {
            'mon': False,
            'tues': False,
            'weds': False,
            'thurs': False,
            'fri': False,
            'sat': False,
            'sun': False
        }

        day_split = re.findall('[A-Z][^A-Z]*', process_array[0])

        for day in day_split:
            if 'Mo' in day:
                repetition['mon'] = True
            elif 'Tu' in day:
                repetition['tues'] = True
            elif 'We' in day:
                repetition['weds'] = True
            elif 'Th' in day:
                repetition['thurs'] = True
            elif 'Fr' in day:
                repetition['fri'] = True
            else:
                repetition['sat'] = True

        # for thing in process_array:
        start_time = process_array[1]
        # print process_array
        if 'PM' in start_time[-2:]:
            hour = int(start_time[:-5])
            if hour == 24:
                hour = 0
            elif hour != 12:
                hour += 12

            minute = int(start_time[-4:-2])

            f_start_time = datetime.time(hour, minute)

        else:
            f_start_time = datetime.time(int(start_time[:-5]), int(start_time[-4:-2]))

        end_time = process_array[3]
        if 'PM' in start_time[-2:]:
            f_end_time = datetime.time(int(end_time[:-5]) + 12, int(end_time[-4:-2]))
        elif 'AM' in start_time[-2:]:
            f_end_time = datetime.time(int(end_time[:-5]), int(end_time[-4:-2]))
        # print "start_time {0}".format(f_start_time)
        # print "end_time {0}".format(f_end_time)

        section['start_time'] = dict()
        section['end_time'] = dict()

        section['end_time']['minute'] = f_end_time.minute
        section['end_time']['hour'] = f_end_time.hour

        section['start_time']['minute'] = f_start_time.minute
        section['start_time']['hour'] = f_start_time.hour

        section['class_number'] = class_number
        section['department'] = class_dept
        section['repetition'] = repetition
        # section['uuid'] = uuid
        # print section

    # print 'building objects'
    # for section in section_list:
    #     print section
    r_list = list()
    for section in section_list:
        if section is not None and section.get('start_time'):
            try:
                # print section
                r_list.append(Section(**section).save().id)
            except Exception as e:
                print e
    #
    # for section in Section.objects():
    #     print section

    return [str(section) for section in r_list]
