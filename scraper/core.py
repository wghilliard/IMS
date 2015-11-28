from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from models import Section
import datetime
import re
from selenium.common.exceptions import NoSuchFrameException
from uuid import uuid4
from __init__ import worker
driver = webdriver.Firefox()


@worker.task(name='tasks.parse')
def parse(class_list):
    section_list = list()
    print class_list

    for thing in class_list:
        print thing[0]
        print thing[1]
        section_list.append(scrape(thing[0], thing[1], uuid4()))


    # while len(section_list) != len(result_list):
    #     for item in result_list:
    #         if item.ready():
    #             section_list.append(item.get())

    return


@worker.task(name='tasks.scrape')
def scrape(classDept, classNumber, uuid):
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

    driver.find_element_by_name('SSR_CLSRCH_WRK_SUBJECT$0').send_keys(classDept)

    driver.find_element_by_name('SSR_CLSRCH_WRK_CATALOG_NBR$1').click()
    try:
        driver.find_element_by_id('SUBJECT_TBL_DESCR$0')
    except Exception as e:
        print e
        print type(e)
    sleep(3)
    driver.find_element_by_name('SSR_CLSRCH_WRK_CATALOG_NBR$1').send_keys(classNumber)
    driver.find_element_by_name('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()
    sleep(2)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    # driver.close()

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

        section['class_number'] = classNumber
        section['department'] = classDept
        section['repetition'] = repetition
        section['uuid'] = uuid
        # print section

    # print 'building objects'
    # for section in section_list:
    #     print section
    r_list = list()
    for section in section_list:
        if section is not None:
            try:
                # print section
                r_list.append(Section(**section).save().id)
            except Exception as e:
                print e
    #
    # for section in Section.objects():
    #     print section

    return [str(section) for section in r_list]
