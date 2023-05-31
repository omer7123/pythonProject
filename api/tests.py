from fastapi import APIRouter, Query, Body
from services.tests import test_service
from shemas.tests import Test, CreateTest, TestInfo, PlayTest, ResultTest
from shemas.users import UserInfo

router = APIRouter()


@router.post(
    "/test/create",
    response_model=CreateTest,
)
def create_test(test: CreateTest) -> CreateTest:
    return test_service.add_test(test)


@router.get(
    "/tests",
    response_model=list[TestInfo]
)
def get_tests():
    return test_service.get_tests()


@router.get(
    "/test/{id}",
    response_model=Test
)
def get_test(id: str):
    return test_service.get_test(id)


@router.post(
    "/test/play",
    response_model=ResultTest
)
def test_play(answers: PlayTest):
    return test_service.play_test(answers)


@router.put(
    "/test/access/{id}",
    response_model=TestInfo
)
def refactor_access(id: str, user: UserInfo):
    return test_service.refactor_access(id, user)


@router.get(
    "/test/my/tests",
    response_model=list[TestInfo]
)
def get_created_tests(id: str = Query(...), token: str = Query(...)):
    return test_service.get_created_tests(id, token)


@router.get(
    "/tests/my/correctly/tests",
    response_model=list[TestInfo]
)
def get_correctly_passed_tests(id: str = Query(...), token: str = Query(...)):
    return test_service.get_correctly_passed_tests(id, token)
# @router.delete(
#     "/tests/delete/{id}",
#     response_model=str
# )
# def delete_test(id: str, user: UserInfo):
#     return test_service.delete_test(id, user)

