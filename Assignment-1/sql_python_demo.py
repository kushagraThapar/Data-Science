import os
import sqlite3
import time

####################################################
# TODO assign [your netid].result to netid variable
####################################################

current_milli_time = lambda: int(round(time.time() * 1000))

directory = "./result/"
netid = "kthapa2"   # suppose your netid is "liu4", the output file should be
extension = ".result"    # liu4.result with extension .result

###########################################
# TODO put database file in the right path
###########################################
social_db = "./data/social.db"
matrix_db = "./data/matrix.db"
university_db = "./data/university.db"

#################################
# TODO write all your query here
#################################
query_1 = "SELECT name FROM Student WHERE grade = 9 ORDER BY name;"
query_2 = "SELECT grade, count(ID) FROM Student GROUP BY grade ORDER BY grade;"


# query_3 =
# query_4 =
# ...
# query_11 =

################################################################################

def get_query_list():
    """
    Form a query list for all the queries above
    """
    query_list = []
    ## TODO change query number here
    for index in range(1, 3):
        eval("query_list.append(query_" + str(index) + ")")
    # end for
    return query_list
    pass


def output_result(index, result, file_path):
    """
    Output the result of query to facilitate autograding.
    Caution!! Do not change this method
    """
    with open(file_path, 'a') as fout:
        fout.write("<" + str(index) + ">\n")
    with open(file_path, 'a') as fout:
        for item in result:
            fout.write(str(item))
            fout.write('\n')
            # end for
    # end with
    with open(file_path, 'a') as fout:
        fout.write("</" + str(index) + ">\n")
    pass


def run(file_path):
    ## get all the query list
    query_list = get_query_list()
    if len(query_list) > 0:
        if os.path.isfile(file_path):
            print("Existing File Found...\n")
            print("Moving it as backup file...\n")
            print("Creating new file with same name...\n")
            new_name = directory + netid + "-" + str(current_milli_time()) + extension
            os.rename(file_path, new_name)

    ## problem 1
    conn = sqlite3.connect(social_db)
    cur = conn.cursor()
    for index in range(0, 2):  # TODO query 1-8 for problem 1
        cur.execute(query_list[index])
        result = cur.fetchall()
        tag = "q" + str(index + 1)
        output_result(tag, result, file_path)
        # end for
        ## TODO problem 2
        ## TODO problem 3
        # end run()


if __name__ == '__main__':
    file_path = directory + netid + extension
    run(file_path)
