import sys
from enchant import Dict
import editdistance
from nltk import word_tokenize

output_file_name = "cleaned.txt"


class SpellingReplacer(object):
    def __init__(self, dict_name='en_US', max_dist=2):
        self.spell_dict = Dict(dict_name)
        self.max_dist = max_dist

    def replace(self, word):
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)

        if suggestions and len(suggestions[0]) == len(word):
            return suggestions[0]
        elif suggestions:
            return self.spell_dict.suggest(suggestions[0])[0]

        for i in range(0, len(suggestions)):
            if len(word) == len(suggestions[i]) and \
                            editdistance.eval(word, suggestions[i]) <= self.max_dist:
                return suggestions[i]
        else:
            return word


# This functions corrects a word
def correct_word(word):
    replacer = SpellingReplacer()
    return replacer.replace(word)


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
        write_professor_data(registrar)
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
            professor = get_professor_data(single_line, registrar)
            registrar.professors.add(professor)

    return registrar


def get_professor_data(single_line, registrar):
    single_line_data = single_line.split("-", 1)
    full_name = single_line_data[0]
    full_name = full_name.strip(" \t\n\r")
    professor = get_professor_name(full_name)
    course_list = single_line_data[1]
    individual_courses = course_list.split("|")
    temp_prof = get_element_from_set(professor, registrar)
    if temp_prof is not None:
        professor = temp_prof

    for single_course in individual_courses:
        single_course = single_course.strip(" \t")
        single_course = tokenize_and_correct_word(single_course)
        professor.courses.add(single_course)

    return professor


def tokenize_and_correct_word(single_course):
    strings = word_tokenize(single_course.lower())
    correct_sentence = ""
    for s in strings:
        if s == '&':
            s = "and"
        elif s == 'intro.' or s == 'Intro.':
            s =  "introduction"
        elif s == "3D" or s == "3d":
            s = "3D"
        elif s == "2D" or s == "2d":
            s = "2D"
        elif s.lower() == "temporalitiez":
            s = "Temporalities"
        elif s.isalnum():
            s = correct_word(s)
        correct_sentence += s + " "

    correct_sentence = correct_sentence[:1].title() + correct_sentence[1:-1]
    return correct_sentence


def get_professor_name(full_name):
    professor = Professor()
    if "," in full_name:
        name_array = full_name.split(",")
        professor.last_name = name_array[0].strip().title()
        professor.first_name = name_array[1].strip().title()
    elif " " in full_name:
        name_array = full_name.split(" ")
        professor.first_name = name_array[0].strip().title()
        professor.last_name = name_array[-1].strip().title()
    elif "." in full_name:
        name_array = full_name.split(".")
        professor.first_name = name_array[0].strip().title()
        professor.last_name = name_array[-1].strip().title()
    else:
        professor.first_name = ""
        professor.last_name = full_name.strip().title()

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


def get_element_from_set(professor, registrar):
    for element in registrar.professors:
        if element.last_name == professor.last_name:
            return element

    return None


def write_professor_data(registrar):
    registrar.professors = sorted(registrar.professors)
    processed_data = ""
    for professor in registrar.professors:
        new_line = ""
        professor.courses = sorted(professor.courses)
        new_line += professor.last_name + " - "
        for course in professor.courses:
            new_line += course + "|"
        new_line = new_line[:-1]
        new_line += "\n"
        processed_data += new_line

    processed_data = processed_data[:-1]
    try:
        write_file(output_file_name, processed_data)
        print("Successfully created file [ " + output_file_name + " ]")
        print("Program will exit now... ")
    except FileExistsError:
        print("File with name cleaned.txt already exists.\nPlease delete cleaned.txt and run this program again")
        print("Program will exit now... ")
        sys.exit(1)


if __name__ == '__main__':
    main()
