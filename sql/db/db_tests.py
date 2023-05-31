from fastapi import HTTPException
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, BOOLEAN, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from shemas.tests import CreateTest, Test, Answers, Question, TestInfo, PlayTest, PlayAnswer, ResultTest, PlayQuestion, \
    CreateQuestion, CreateAnswers
from shemas.users import UserInfo

Base = declarative_base()


class AnswersTable(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    right = Column(BOOLEAN)
    title = Column(String)
    question_id = Column(Integer, ForeignKey('question.id'))


class QuestionTable(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    right_answer = Column(Integer)
    test_id = Column(Integer, ForeignKey('test.id'))
    passed = Column(Integer)
    passed_correctly = Column(Integer)
    answers = relationship('AnswersTable', backref='question')


class TestTable(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    access = Column(BOOLEAN)
    id_authors = Column(String)
    username = Column(String)
    passed = Column(Integer)
    passed_correctly = Column(Integer)
    questions = relationship('QuestionTable', backref='test')


engine = create_engine("sqlite:///db/tests.db", echo=False)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_test(test: CreateTest):
    test2 = TestTable(
        title=test.title,
        username=test.username,
        access=True,
        passed=0,
        passed_correctly=0,
        id_authors=test.id_authors,
        questions=[QuestionTable(
            question=q.question,
            passed=0,
            passed_correctly=0,
            right_answer=q.right_answer,
            answers=[AnswersTable(
                right=a.right,
                title=a.title
            ) for a in q.answers]
        ) for q in test.questions]
    )

    session.add(test2)
    session.commit()
    return test


def table_to_test(test: TestTable):
    return ResultTest(
        id=test.id,
        result="",
        questions=[CreateQuestion(
            question=q.question,
            right_answer=q.right_answer,
            answers=[CreateAnswers(
                title=a.title,
                right=a.right
            ) for a in q.answers]
        ) for q in test.questions]
    )


def get_tests() -> list[TestInfo]:
    tests = session.query(TestTable).filter(TestTable.access == True).all()
    return tests


def get_test(id: str) -> Test:
    test = session.query(TestTable).get(id)
    if test:
        return test
    raise HTTPException(status_code=400, detail="Test not found")


def play_test(answers: PlayTest):
    test = session.query(TestTable).filter(TestTable.id == answers.id).first()
    test_result = table_to_test(test)

    if test:
        if not test.id_authors == answers.user.id:
            # +1 к passed теста
            test.passed += 1
            stmt = update(TestTable).where(TestTable.id == answers.id).values(passed=test.passed)
            session.execute(stmt)
            session.commit()

            count = 0
            for question in test.questions:
                question_from_db = session.query(QuestionTable).filter(QuestionTable.id == question.id).first()
                question_from_db_pydantic = Question.from_orm(question_from_db)

                # +1 к passed вопроса
                question.passed += 1
                stmt = update(QuestionTable).where(QuestionTable.id == question.id).values(passed=question.passed)
                session.execute(stmt)
                session.commit()

                # right_answer = question_from_db_pydantic.right_answer
                for answer in question.answers:
                    answer_from_db = session.query(AnswersTable).filter(AnswersTable.id == answer.id).first()
                    answer_from_db_p = PlayAnswer.from_orm(answer_from_db)
                    if answer_from_db_p.right == True and answer.right == True:
                        count += 1
                        # +1 к passed_correctly вопроса
                        question.passed_correctly += 1
                        stmt = update(QuestionTable).where(QuestionTable.id == question.id).values(
                            passed_correctly=question.passed_correctly)
                        session.execute(stmt)
                        session.commit()

            save = count / len(answers.questions) * 100
            if save == 100:
                # +1 к passed_correctly теста
                test.passed_correctly += 1
                stmt = update(TestTable).where(TestTable.id == answers.id).values(passed_correctly=test.passed_correctly)
                session.execute(stmt)
                session.commit()
            test_result.result = save.__str__() + "%"
            return test_result
        raise HTTPException(status_code=400, detail="Вы являетесь автором данного теста, поэтому пройти невозможно")
    raise HTTPException(status_code=400, detail="Тест с данным id не найден")


def refactor_access(id: str, user: UserInfo):
    test = session.query(TestTable).get(id)
    test = TestInfo.from_orm(test)
    if user.id == test.id_authors:
        access = not test.access
        stmt = update(TestTable).where(TestTable.id == id).values(access=access)
        session.execute(stmt)
        session.commit()

        test = session.query(TestTable).get(id)
        return test
    raise HTTPException(status_code=400, detail="Вы не являетесь автором этого теста")


def get_created_tests(id: str) -> list[TestInfo]:
    tests = session.query(TestTable).filter(TestTable.id_authors == id).all()
    return tests


def get_correctly_passed_tests(passed_tests: list[str]):
    tests = []
    for id_test in passed_tests:
        test = session.query(TestTable).filter(TestTable.id == id_test).first()
        tests.append(test)
    return tests