'''manage.py - Database migration configuration'''
from stackoverflow.api.v2.models import (
    User, blackList,
    Question, Answer
)
question = Question()
answer = Answer()


class DBMigration(object):

    @staticmethod
    def create_all():
        """Creates the tables"""
        User.create_table()
        question.create_table()
        answer.create_table()
        blackList.create_table()

    @staticmethod
    def drop_tables():
        """drops all the tables"""
        answer = Answer()
        quiz = Question()
        my_list = [answer, quiz]
        for i in my_list:
            i.drop_all()
        blackList.drop_all()
        User.drop_all()


create = DBMigration()
if __name__ == '__main__':
    create.create_all()
