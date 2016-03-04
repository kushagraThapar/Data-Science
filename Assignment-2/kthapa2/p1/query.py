import sys

output_file_name = "cleaned.txt"


class Registrar:
    """This is a class which contains the set of professors objects"""
    def __init__(self):
        self.professors = set()

    professors = set()


class Professor:
    """This is a class for professor object"""
    first_name = ""
    last_name = ""
    courses = set()

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.courses = set()

    def __hash__(self):
        return hash(self.last_name.lower())

    def __ne__(self, other):
        return self.last_name.lower() != other.last_name.lower()

    def __le__(self, other):
        return self.last_name <= other.last_name

    def __gt__(self, other):
        return self.last_name > other.last_name

    def __eq__(self, other):
        return self.last_name.lower() == other.last_name.lower()

    def __ge__(self, other):
        return self.last_name >= other.last_name


def main():
    args = sys.argv[1:]
    # print(args)
    if not args or len(args) > 1:
        print('usage: clean.py [any-file].txt')
        sys.exit(1)

    try:
        unprocessed_data = read_file(args[0])
        registrar = process_raw_data(unprocessed_data)
        print("QUERY-1 -> Total number of distinct courses are [" + str(calculate_distinct_courses(registrar)) + "]")
        print("QUERY-2 -> Courses taught by professor Mitchell Theys are [" +
              str(calculate_courses_of_professor("Theys", registrar)) + "]")
        new_registrar = find_professor_with_max_jaccard_distance(registrar)
        prof_last_name = ""
        for prof in new_registrar.professors:
            prof_last_name += prof.last_name + ", "

        prof_last_name = prof_last_name[:-2]
        print("QUERY-3 -> Professors who have the most teaching aligned interest are[" + prof_last_name + "]")
    except FileNotFoundError:
        print("File [" + args[0] + "] not found.")
        print("Make sure file exists in this directory with this name.\nProgram will exit now... ")


def process_raw_data(unprocessed_data):
    # print(unprocessed_data)
    registrar = Registrar()
    split_data_list = unprocessed_data.split("\n")
    for single_line in split_data_list:
        single_line = single_line.strip(" \t\n\r")
        if single_line:
            professor = get_professor_data(single_line)
            registrar.professors.add(professor)

    return registrar


def get_professor_data(single_line):
    single_line_data = single_line.split("-", 1)
    last_name = single_line_data[0]
    last_name = last_name.strip(" \t\n\r")
    professor = Professor()
    professor.last_name = last_name
    course_list = single_line_data[1]
    individual_courses = course_list.split("|")
    for single_course in individual_courses:
        single_course = single_course.strip(" \t")
        professor.courses.add(single_course.title())

    return professor


def read_file(filename):
    f = open(filename, "rU")
    text = f.read()
    f.close()
    return text


def write_file(filename, text):
    f = open(filename, "w")
    f.write(text)
    f.close()
    return


def get_element_from_set(last_name, registrar):
    for element in registrar.professors:
        if element.last_name == last_name:
            return element

    return None


# This is the function which executes query-1
def calculate_distinct_courses(registrar):
    distinct_courses = set()
    for professor in registrar.professors:
        for courses in professor.courses:
            distinct_courses.add(courses)

    return len(distinct_courses)


# This is the function which executes the query-2
def calculate_courses_of_professor(professor_last_name, registrar):
    professor = get_element_from_set(professor_last_name, registrar)
    professor.courses = sorted(professor.courses)
    courses = ""
    for course in professor.courses:
        courses += course + ","

    courses = courses[:-1]
    return courses


# This is the function which executes query-3
def find_professor_with_max_jaccard_distance(registrar):
    max_jaccard_score = 0
    custom_map = {}
    professors = find_professors_with_courses(registrar, 5)
    length = len(professors)
    for i in range(0, length):
        for j in range(i, length):
            score = calculate_jaccard_for_professors(professors[i], professors[j])
            if 1 > score >= max_jaccard_score:
                max_jaccard_score = score
                if score not in custom_map:
                    custom_map[score] = []

                custom_map[score].append(professors[i])
                custom_map[score].append(professors[j])

    final_list = custom_map[max_jaccard_score]
    new_registrar = Registrar()
    for element in final_list:
        new_registrar.professors.add(element)

    return new_registrar


# This function calculates the Jaccard distance of two courses
def calculate_jaccard_distance(courses_1, courses_2):
    n = len(courses_1.intersection(courses_2))
    return n / float(len(courses_1) + len(courses_2) - n)


def calculate_jaccard_for_professors(prof_1, prof_2):
    course_1 = set()
    prof_1.courses = sorted(prof_1.courses)
    for course in prof_1.courses:
        course_1.add(course)

    course_2 = set()
    prof_2.courses = sorted(prof_2.courses)
    for course in prof_2.courses:
        course_2.add(course)

    jaccard_score = calculate_jaccard_distance(course_1, course_2)
    return jaccard_score


def find_professors_with_courses(registrar, len_courses=5):
    professors = []
    for professor in registrar.professors:
        if len(professor.courses) >= len_courses:
            professors.append(professor)

    return professors


if __name__ == '__main__':
    main()