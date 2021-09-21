from typing import List, Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.param_functions import Form

from app.models import AddResponse
from app.utils import check_duplicate, hash_image, read_imagefile, load_index, save_index

app = FastAPI(
  title="Duplicate image detection system",
  version="1.0",
  description="An API for detecting duplicate images from a user-defined database"
)

"""
Upload a single image to the duplicate image database
"""
@app.post("/api/add/image", status_code=201, response_model=AddResponse)
async def add_image(file: UploadFile = File(...), hash_size:Optional[int] = Form(16), 
    index_name:Optional[str] = Form('faiss_index')):

    # load index
    index = load_index(index_name, hash_size)

    # hash image
    img = read_imagefile(await file.read())
    img_hash = hash_image(img, hash_size)

    # update index and save
    index.add(img_hash)
    save_index(index, hash_size=hash_size)

    return {"added": [file.filename] }

"""
Upload multiple images to the duplicate image database
"""
@app.post("/api/add/images", status_code=201, response_model=AddResponse)
async def add_images(files: List[UploadFile] = File(...), 
    hash_size:Optional[int] = Form(16), index_name:Optional[str] = Form('faiss_index')):

    # load index
    index = load_index(index_name, hash_size)

    # hash images
    imgs = [read_imagefile(await file.read()) for file in files]
    img_hashes = [hash_image(img, hash_size) for img in imgs]

    # update index and save
    for img_hash in img_hashes:
        index.add(img_hash)
    
    save_index(index, hash_size=hash_size)

    return {"added": [file.filename for file in files]}

"""
Check an image against the duplicate image database
"""
@app.post("/api/check")
async def check_image(dist:int = Form(...), file: UploadFile = File(...), 
    hash_size:Optional[int] = Form(16), index_name:Optional[str] = Form('faiss_index')):

    # load index
    index = load_index(index_name, hash_size)

    # hash image
    img = read_imagefile(await file.read())
    img_hash = hash_image(img, hash_size)

    return {"duplicate": check_duplicate(index, img_hash, dist)}