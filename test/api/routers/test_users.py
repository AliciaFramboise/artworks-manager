from starlette import status

from database.database import get_db
from main import app
from services.authService import get_current_user
from test.utils import override_get_db, override_get_current_user, client, test_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'baleine_a_lunettes'
    assert response.json()['email'] == 'baleine.lunettes@gmail.com'
    assert response.json()['first_name'] == 'Baleine'
    assert response.json()['last_name'] == 'Lunettes'
    assert response.json()['role'] == 'admin'


def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "testpassword",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={"password": "wrong_password",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change: Password is incorrect'}
