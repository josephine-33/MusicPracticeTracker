import pytest
from ...models.users import create_user, authenticate_user

@pytest.mark.usefixtures("client")
class TestUserAuth:
    def test_create_user_success(self):
        result = create_user("josephine", "josephine@gmail.com", "password")
        assert result == True

    def test_create_duplicate_user_email(self):
        create_user("josephine", "josephine@gmail.com", "password")
        result = create_user("josephine", "josephine@gmail.com", "password")
        assert result == False

    def test_authenticate_user_success(self):
        create_user("josephine", "josephine@gmail.com", "password")
        user_id = authenticate_user("josephine@gmail.com", "password")
        assert user_id is not None
    
    def test_authenticate_user_wrong(self):
        create_user("josephine", "josephine@gmail.com", "password")
        user_id = authenticate_user("josephine@gmail.com", "wrong_password")
        assert user_id is None



# need to test
# - create a new user and check the database to see if they are there (use a clean database)
# - "login" / authenticate a user 