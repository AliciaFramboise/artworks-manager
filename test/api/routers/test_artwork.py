
from starlette import status

from database.database import get_db
from database.model.Artwork import Artwork
from main import app
from services.authService import get_current_user
from test.utils import override_get_db, override_get_current_user, client, test_artwork, TestingSessionLocal

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_all(test_artwork):
    response = client.get("/artwork")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title': 'La Baleine à lunettes',
                                'description': 'Une baleine à lunettes',
                                'id': 1,
                                'filename': 'baleine.png'}]


def test_get_artwork(test_artwork):
    response = client.get("/artwork/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'title': 'La Baleine à lunettes',
                               'description': 'Une baleine à lunettes',
                               'id': 1,
                               'filename': 'baleine.png'}


def test_get_artwork_given_wrong_id(test_artwork):
    response = client.get("/artwork/10")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Artwork not found.'}


# def test_create_todo(test_artwork):
#     request_data = {
#         'title': 'Finn the cutest dog',
#         'description': 'Currently Luc dog but mine soon',
#     }
#
#     test_dir = os.path.dirname(os.path.abspath(__file__))
#     with open(os.path.join(test_dir, "resources", "bmo.jpg"), "rb") as image_file:
#         response = client.post('/artwork/', data=request_data,
#                                files={"file": ("resources/bmo.jpg", image_file, "image""/jpeg")})
#
#     assert response.status_code == 201
#
#     db = TestingSessionLocal()
#     saved_artwork = db.query(Artwork).filter(Artwork.id == 2).first()
#     assert saved_artwork.title == request_data.get('title')
#     assert saved_artwork.description == request_data.get('description')
#     assert saved_artwork.filename == "bmo.jpg"


def test_update_artwork(test_artwork):
    request_data = {
        'title': 'Changed title',
        'description': 'Une baleine à lunettes',
    }

    response = client.put('/artwork/1', data=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Artwork).filter(Artwork.id == 1).first()
    assert model.title == 'Changed title'
    assert model.description == 'Une baleine à lunettes'


def test_update_artwork_not_found(test_artwork):
    request_data = {
        'title': 'Changed title',
        'description': 'Une baleine à lunettes',
    }

    response = client.put('/artwork/10', data=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Failed to update artwork: Artwork to update cannot be null'}


def test_delete_artwork(test_artwork):
    response = client.delete('/artwork/1')
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Artwork).filter(Artwork.id == 1).first()
    assert model is None


def test_delete_artwork_not_found():
    response = client.delete('/artwork/999')

    assert response.status_code == 404
    assert response.json() == {'detail': 'Artwork not found: Artwork to delete can not be null'}
