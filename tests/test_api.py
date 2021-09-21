from PIL import Image
from fastapi.testclient import TestClient

from app.utils import hash_image, load_index, save_index
from app.api import app

def test_single_upload():
  client = TestClient(app)
  with open("./tests/data/is_my_cat_normal.jpg", "rb") as f:
    response = client.post('/api/add/image', files={'file':  f} )
    assert response.status_code == 201
    assert response.json() == {"added": ["is_my_cat_normal.jpg"]}

def test_multiple_uploads():
  client = TestClient(app)
  multiple_files =[('files', open('./tests/data/is_my_cat_normal.jpg', 'rb')), 
    ('files', open('./tests/data/is_my_cat_normal_copy.jpg', 'rb'))]
  response = client.post('/api/add/images', files=multiple_files)
  assert response.status_code == 201
  assert response.json() == {"added": ["is_my_cat_normal.jpg", "is_my_cat_normal_copy.jpg"]}

def test_check_duplicate():
  hash_size = 16

  # reset index
  index = load_index(hash_size=hash_size)
  index.reset()

  # load image into index
  img = Image.open("./tests/data/is_my_cat_normal.jpg")
  img_hash = hash_image(img, hash_size)
  index.add(img_hash)
  save_index(index, hash_size=hash_size)

  client = TestClient(app)

  with open("./tests/data/is_my_cat_normal_copy.jpg", "rb") as f:
    test_file ={'file':  f} 
    response = client.post('/api/check', files=test_file, data={'dist': 5})
    assert response.status_code == 200
    assert response.json() == {"duplicate": True}

def test_check_non_duplicate():
  hash_size = 16

  # reset index
  index = load_index(hash_size=hash_size)
  index.reset()

  # load image into index
  img = Image.open("./tests/data/doge.png")
  img_hash = hash_image(img, hash_size)
  index.add(img_hash)
  save_index(index, hash_size=hash_size)

  client = TestClient(app)
  
  with open("./tests/data/is_my_cat_normal_copy.jpg", "rb") as f:
    test_file ={'file':  f} 
    response = client.post('/api/check', files=test_file, data={'dist': 5})
    assert response.status_code == 200
    assert response.json() == {"duplicate": False}