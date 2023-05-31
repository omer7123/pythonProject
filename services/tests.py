from shemas.tests import CreateTest, Test, TestInfo, PlayTest
import sql.db.db_tests as db
import sql.db.db as db_user
from shemas.users import UserInfo


class TestService:

    def add_test(self, test: CreateTest) -> CreateTest:
        if db_user.token_verification(test.user.token, test.id_authors):
            return db.create_test(test)

    def get_tests(self) -> list[TestInfo]:
        return db.get_tests()

    def get_test(self, id: str) -> Test:
        return db.get_test(id)

    def play_test(self, answers: PlayTest):
        if db_user.token_verification(answers.user.token, answers.user.id):
            if db.play_test(answers):
                db_user.update_passed(answers.user.id, answers.id)
            return db.play_test(answers)

    def refactor_access(self, id: str, user: UserInfo):
        if db_user.token_verification(user.token, user.id):
            return db.refactor_access(id, user)

    def get_created_tests(self, id: str, token: str) -> list[TestInfo]:
        if db_user.token_verification(token, id):
            return db.get_created_tests(id)

    def get_correctly_passed_tests(self, id, token):
        if db_user.token_verification(token, id):
            ids_list = db_user.get_correctly_ids_tests(id)
            return db.get_correctly_passed_tests(ids_list)

test_service: TestService = TestService()