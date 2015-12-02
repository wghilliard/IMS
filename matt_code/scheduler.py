# #
# # * To change this license header, choose License Headers in Project Properties.
# # * To change this template file, choose Tools | Templates
# # * and open the template in the editor.
# #
# # *
# # *
# # * @author Matthew
# #
#
# from user import User
#
# class Scheduler(object):
#     # *
#     # * @param args the command line arguments
#     #
#     def main(args):
#
#         # Test Case 1
#         dog1 = User(10, 10, 10, 6, 0, 30, 43)
#         dog1.addCourse("CSE 1315")
#         print(dog1.getNotification())
#         dog1.addCourse("MATH 3330")
#         print(dog1.getNotification())
#         dog1.addCourse("MATH 3350")
#         print(dog1.getNotification())
#         courseSectionData = ArrayList[ArrayList]()
#         courseSectionData.add(ArrayList[Section]())
#         repeat =
#         courseSectionData.get(0).add(Section("CSE 1315-001", Time(10, 0), Time(10, 50),
#                                              DaysAvailable(False, True, False, True, False, True, False)))
#         repeat2 =
#         courseSectionData.get(0).add(Section("CSE 1315-002", Time(16, 0), Time(17, 20),
#                                              DaysAvailable(False, False, True, False, True, False, False)))
#         courseSectionData.add(ArrayList[Section]())
#         courseSectionData.get(1).add(Section("MATH 3330-001", Time(11, 0), Time(12, 00),
#                                              DaysAvailable(False, True, False, True, False, True, False)))
#         courseSectionData.get(1).add(Section("MATH 3330-002", Time(20, 0), Time(21, 20),
#                                              DaysAvailable(False, False, True, False, True, False, False)))
#         repeat3 =
#         courseSectionData.get(1).add(Section("MATH 3330-003", Time(22, 0), Time(23, 50),
#                                              DaysAvailable(False, False, True, False, False, False, False)))
#         courseSectionData.add(ArrayList[Section]())
#         courseSectionData.get(2).add(Section("MATH 3350-001", Time(13, 0), Time(14, 00),
#                                              DaysAvailable(False, True, False, True, False, True, False)))
#         courseSectionData.get(2).add(Section("MATH 3350-002", Time(13, 0), Time(14, 20),
#                                              DaysAvailable(False, False, True, False, True, False, False)))
#         courseSectionData.get(2).add(Section("MATH 3350-003", Time(12, 30), Time(15, 20),
#                                              DaysAvailable(False, False, True, False, False, False, False)))
#         # dog1.addCourse("yes");
#         # System.out.println(dog1.getNotification());
#         # int[] repetition = {1,1,1,1,1,1,1};
#         # //dog1.addBlockOut(new Block("sleep","home",new Time(0,0),new Time(6,0),repetition));
#         # //System.out.println(dog1.getNotification());
#         dog1.addBlockOut(
#             Block("work", "work", Time(12, 30), Time(12, 50), DaysAvailable(True, True, True, True, True, True, True)))
#         print(dog1.getNotification())
#         dog1.addBlockOut(
#             Block("work", "work", Time(6, 30), Time(12, 0), DaysAvailable(True, True, True, True, True, True, True)))
#         print(dog1.getNotification())
#         dog1.addBlockOut(
#             Block("other", "work", Time(21, 30), Time(23, 0), DaysAvailable(True, True, True, True, True, True, True)))
#         print(dog1.getNotification())
#         dog1.addBlockOut(
#             Block("other", "home", Time(19, 30), Time(20, 0), DaysAvailable(True, True, True, True, True, True, True)))
#         print(dog1.getNotification())
#         dog1.setSections(courseSectionData)
#         print("\nCurrent BlockOuts")
#         dog1.printBlockOuts()
#         print("\nCurrent Courses")
#         dog1.printCourses()
#         print("\nFetched Sections Information")
#         dog1.printSections(courseSectionData)
#         dog1.generateSchedules()
#         print(dog1.getNotification())
#
#     main = staticmethod(main)
