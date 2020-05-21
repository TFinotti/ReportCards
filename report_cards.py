import csv


def report_card_compiler(csv_courses, csv_students, csv_tests, csv_marks):
    # Reading each csv file and organizing the data in dictionaries
    with open(csv_students, 'r') as f_students:
        students = csv.reader(f_students)
        dict_students = {}
        headers = True
        for entry in students:
            if headers:
                headers = False
                continue
            else:
                dict_students[int(entry[0])] = entry[1]

    with open(csv_courses, 'r') as f_courses:
        courses = csv.reader(f_courses, skipinitialspace=True)
        dict_courses = {}
        headers = True
        for entry in courses:
            if headers:
                headers = False
                continue
            else:
                dict_courses[int(entry[0])] = [entry[1], entry[2], {}]

    with open(csv_tests, 'r') as f_tests:
        tests = csv.reader(f_tests)
        dict_tests = {}
        headers = True
        for entry in tests:
            if headers:
                headers = False
                continue
            else:
                dict_courses[int(entry[1])][2][int(entry[0])] = int(entry[2])
                dict_tests[int(entry[0])] = [int(entry[1]), int(entry[2])]

    with open(csv_marks, 'r') as f_marks:
        marks = csv.reader(f_marks)
        dict_marks = {}
        headers = True
        for entry in marks:
            if headers:
                headers = False
                continue
            else:
                if int(entry[1]) in dict_marks.keys():
                    dict_marks[int(entry[1])].extend([int(entry[0]), int(entry[2])])
                else:
                    dict_marks[int(entry[1])] = [int(entry[0]), int(entry[2])]

    # Calculating each student's weighted marks for each test of each course
    # Marks are saved into a dictionary where student ID are keys, and marks are values
    dict_student_marks = {}
    for student_id in dict_marks.keys():
        i = 0
        while i < len(dict_marks[student_id]):
            test_id = dict_marks[student_id][i]
            course_id = dict_tests[test_id][0]
            course_grade = dict_marks[student_id][i + 1] * dict_tests[test_id][1] / 100
            if student_id in dict_student_marks:
                dict_student_marks[student_id].extend([course_id, test_id, course_grade])
                i += 2
            else:
                dict_student_marks[student_id] = [course_id, test_id, course_grade]
                i += 2

    # Calculating each student's final marks for each course
    # Final marks are saved into a dictionary where student ID ares keys, and final marks are values
    dict_student_final_marks = {}
    for student_id in dict_student_marks.keys():
        i = 0
        grade = dict_student_marks[student_id][2]
        while i < len(dict_student_marks[student_id]):
            if i + 5 < len(dict_student_marks[student_id]) and dict_student_marks[student_id][i] == \
                    dict_student_marks[student_id][
                        i + 3]:
                grade += dict_student_marks[student_id][i + 5]
                i += 3
            else:
                if student_id in dict_student_final_marks:
                    dict_student_final_marks[student_id].extend([dict_student_marks[student_id][i], round(grade, 2)])
                    i += 3
                    if i < len(dict_student_marks[student_id]):
                        grade = dict_student_marks[student_id][i + 2]
                else:
                    dict_student_final_marks[student_id] = [dict_student_marks[student_id][i], round(grade, 2)]
                    i += 3
                    if i < len(dict_student_marks[student_id]):
                        grade = dict_student_marks[student_id][i + 2]

    # Calculating student's averages
    dict_student_averages = {}
    for student_id in dict_student_final_marks.keys():
        grade_sum = 0
        i = 1
        j = 0
        while i < len(dict_student_final_marks[student_id]):
            grade_sum += dict_student_final_marks[student_id][i]
            i += 2
            j += 1
        average = round(grade_sum / j, 2)
        dict_student_averages[student_id] = average

    # Writing all the report cards to a text file named "report_cards.txt"
    txt_output = open('report_cards.txt', 'w')
    for student_id in dict_student_final_marks.keys():
        line = 'Student Id: {0}, name: {1}\n'.format(student_id, dict_students[student_id])
        txt_output.write(line)
        line = 'Total Average:      {0}%\n\n'.format(dict_student_averages[student_id])
        txt_output.write(line)
        i = 0
        while i < len(dict_student_final_marks[student_id]):
            course_name = dict_courses[dict_student_final_marks[student_id][i]][0]
            teacher_name = dict_courses[dict_student_final_marks[student_id][i]][1]
            line = '        Course: {0}, Teacher: {1}\n'.format(course_name, teacher_name)
            txt_output.write(line)
            final_grade = dict_student_final_marks[student_id][i + 1]
            line = '        Final Grade:      {0}%\n\n'.format('{:.2f}'.format(final_grade))
            txt_output.write(line)
            i += 2
    txt_output.close()


report_card_compiler('courses.csv', 'students.csv', 'tests.csv', 'marks.csv')
