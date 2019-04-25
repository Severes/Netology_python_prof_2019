import psycopg2 as pg
from pprint import pprint


def create_db():
    with pg.connect('dbname=netology_db user=netology_user password=user') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            create table course (
                id serial primary key,
                name varchar(100) not null
            ) 
             """)
            cur.execute("""
             create table student (
                id serial primary key,
                name varchar(100) not null,
                gpa numeric(10,2),
                birth timestamp with timezone
            ) 
             """)
            cur.execute("""
            create table student_course (
                id serial primary key,
                student_id integer references student(id),
                course_id integer references course(id)
            ) 
            """)


def insert_course(name):
    with pg.connect('dbname=netology_db user=netology_user password=user') as conn:
        with conn.cursor() as cur:
            cur.execute("""
                insert into course (name) values (%s)
            """, (name, ))


def add_student(name, birth):
    with pg.connect('dbname=netology_db user=netology_user password=user') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            insert into student (name, birth) values (%s, %s)
            """, (name, birth))


def get_student(student_id):
    with pg.connect('dbname=netology_db user=netology_user password=user') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            select * from student where id = (%s)
            """, (student_id, ))


def add_students(course_id, students):
    with pg.connect('dbname=netology_db user=netology_user password=user') as conn:
        with conn.cursor() as cur:
            for student in students:
                # print(student)
                # print(student['name'])
                # print(student['birth'])
                # print(type(student))
                # print(students)
                cur.execute("""
                insert into student (name, birth) values (%s, %s)
                """, (student['name'], student['birth']))
                cur.execute("""
                insert into student_course (student_id, course_id) values ((select max(id) from student), %s)
                """, (course_id, ))


def get_students(course_id):
    with pg.connect('dbname=netology_db user=netology_user password=user') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            select student.id, student.name, course.name 
            from student_course 
            join student on student.id = student_course.student_id 
            join course on course.id = student_course.course_id 
            where course_id = (%s)
            """, (course_id, ))
            result = pprint(cur.fetchall())
    return result


if __name__ == '__main__':

    # create_db()  # создает таблицы

    # insert_course(name)  # просто создает курс

    # add_student('Маша', '1999-08-24')  # просто создает студента

    # get_student(6)  # просто возвращает студента по id

    # add_students(1, [{'name':'Михаил', 'birth':'1987-01-25'},{'name':'Ирина', 'birth':'1997-01-25'}])  # создает студентов и записывает их на курс

    # get_students(1)  # возвращает студентов определенного курса

    pass


