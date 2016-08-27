import sqlite3

netid = "kthapa2.result"

social_db = "./data/social.db"
matrix_db = "./data/matrix.db"
university_db = "./data/university.db"

query_1 = "SELECT name FROM Student WHERE grade = 9 ORDER BY name;"

query_2 = "SELECT grade, count(ID) FROM Student GROUP BY grade ORDER BY grade;"

query_3 = "SELECT DISTINCT name, grade " \
          "FROM Student AS S JOIN Friend AS F " \
          "ON S.ID = F.ID1 " \
          "GROUP BY F.ID1 " \
          "HAVING count(F.ID1) > 2 " \
          "ORDER BY S.name, S.grade;"

query_4 = "SELECT DISTINCT S1.name, S1.grade " \
          "FROM Student AS S1 JOIN Likes AS L " \
          "ON S1.ID = L.ID2 " \
          "JOIN Student AS S2 " \
          "ON S2.ID = L.ID1 " \
          "WHERE S2.grade > S1.grade " \
          "ORDER BY S1.name, S1.grade;"

query_5 = "SELECT DISTINCT S1.name, S1.grade FROM " \
          "Student AS S1 WHERE S1.ID IN " \
          "(SELECT DISTINCT S.ID FROM " \
          "Student AS S JOIN Likes AS L " \
          "ON S.ID = L.ID1 " \
          "JOIN Friend AS F " \
          "ON L.ID2 = F.ID2 AND L.ID1 = F.ID1) " \
          "UNION " \
          "SELECT DISTINCT S.name, S.grade FROM " \
          "Student S WHERE S.ID NOT IN (SELECT L.ID1 FROM Likes AS L) " \
          "ORDER BY name;"

query_6 = "SELECT L.ID1, S1.NAME AS NAME1, " \
          "L.ID2, S2.NAME AS NAME2 " \
          "FROM Likes L " \
          "JOIN Student S1 ON L.ID1 = S1.ID " \
          "JOIN Student S2 ON L.ID2 = S2.ID " \
          "LEFT JOIN Friend F " \
          "ON L.ID1 = F.ID1 AND L.ID2 = F.ID2 " \
          "WHERE F.ID1 IS NULL AND F.ID2 IS NULL " \
          "ORDER BY L.ID1, L.ID2;"

"""
#   A different way to perform query - 6

query_6 = "select ID1, S1.NAME as NAME1, ID2, S2.NAME as NAME2 from Likes L " \
          "JOIN Student S1 ON L.ID1 = S1.ID " \
          "JOIN Student S2 ON L.ID2 = S2.ID " \
          "WHERE NOT EXISTS (SELECT * from Friend where l.ID1 = ID1 and L.ID2 = ID2) " \
          "ORDER BY ID1, ID2;"
"""

query_7 = "SELECT L.ID1, S1.NAME AS NAME1, L.ID2, S2.NAME AS NAME2, S3.ID AS ID3, S3.NAME AS NAME3 " \
          "FROM Likes L  " \
          "JOIN Student S1 ON L.ID1 = S1.ID " \
          "JOIN Student S2 ON L.ID2 = S2.ID " \
          "JOIN Student S3 " \
          "JOIN Friend F ON S3.ID = F.ID1 " \
          "WHERE EXISTS(SELECT * FROM Friend WHERE ID1 = F.ID1 AND ID2 = L.ID1 AND F.ID2 = L.ID2) " \
          "AND NOT EXISTS (SELECT * FROM Friend WHERE l.ID1 = ID1 AND L.ID2 = ID2) " \
          "ORDER BY L.ID1, L.ID2;"

query_8 = "SELECT DISTINCT F1.ID1 AS ID1, S1.NAME AS NAME1, " \
          "F1.ID2 AS ID2, S2.NAME AS NAME2, " \
          "F2.ID2 AS ID3, S3.NAME AS NAME3 " \
          "FROM Friend AS f1 JOIN Friend AS f2 JOIN Friend AS f3 " \
          "ON f1.ID2=f2.ID1 AND f2.ID2 = f3.ID1 AND f1.ID1=f3.ID2 " \
          "JOIN Student S1 ON F1.ID1 = S1.ID " \
          "JOIN Student S2 ON F1.ID2 = S2.ID " \
          "JOIN Student S3 ON F2.ID2 = S3.ID " \
          "ORDER BY F1.ID1, F1.ID2, F2.ID1;"

query_9 = "SELECT P.tenured, avg(F.class_score) AS AVERAGE_CLASS_SCORE " \
          "FROM DIM_PROFESSOR P JOIN FACT_COURSE_EVALUATION F " \
          "ON P.ID = F.professor_id " \
          "GROUP BY P.tenured " \
          "ORDER BY P.tenured;"

query_10 = "SELECT Term.YEAR, T.AREA, avg(F.CLASS_SCORE) AS AVERAGE_CLASS_SCORE " \
           "FROM Fact_Course_Evaluation F JOIN Dim_Type T " \
           "ON F.type_id = T.id " \
           "JOIN Dim_Term Term " \
           "ON F.term_id = Term.id " \
           "WHERE T.TYPE LIKE 'course' " \
           "GROUP BY T.area, Term.year " \
           "ORDER BY Term.year, T.area;"

query_11 = "SELECT A.ROW_NUM, B.COL_NUM, SUM(A.VALUE * B.VALUE) " \
           "FROM A JOIN B ON A.COL_NUM = B.ROW_NUM " \
           "GROUP BY A.ROW_NUM, B.COL_NUM " \
           "ORDER BY A.ROW_NUM, B.COL_NUM;"


################################################################################

def get_query_list():
    """
    Form a query list for all the queries above
    """
    query_list = []
    for index in range(1, 12):
        eval("query_list.append(query_" + str(index) + ")")
    # end for
    return query_list
    pass


def output_result(index, result):
    """
    Output the result of query to facilitate autograding.
    Caution!! Do not change this method
    """
    with open(netid, 'a') as fout:
        fout.write("<" + str(index) + ">\n")
    with open(netid, 'a') as fout:
        for item in result:
            fout.write(str(item))
            fout.write('\n')
            # end for
    # end with
    with open(netid, 'a') as fout:
        fout.write("</" + str(index) + ">\n")
    pass


def run():
    ## get all the query list
    query_list = get_query_list()

    ## problem 1
    conn = sqlite3.connect(social_db)
    cur = conn.cursor()
    for index in range(0, 8):
        cur.execute(query_list[index])
        result = cur.fetchall()
        tag = "q" + str(index + 1)
        output_result(tag, result)
    # end for
    ## end problem 1

    ## problem 2
    conn = sqlite3.connect(university_db)
    cur = conn.cursor()
    for index in range(8, 10):
        cur.execute(query_list[index])
        result = cur.fetchall()
        tag = "q" + str(index + 1)
        output_result(tag, result)
    # end for
    ## end problem 2

    ## problem 3
    conn = sqlite3.connect(matrix_db)
    cur = conn.cursor()
    for index in range(10, 11):
        cur.execute(query_list[index])
        result = cur.fetchall()
        tag = "q" + str(index + 1)
        output_result(tag, result)
        # end for
        #  end problem 3
        # end run()


if __name__ == '__main__':
    run()
