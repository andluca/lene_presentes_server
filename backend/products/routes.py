from fastapi import APIRouter, HTTPException, Path, UploadFile, File, Form, Query
from backend.models import ProductOut, ProductInDB, MessageResponse
from .crud import create_product_db, list_products_db, get_product_db, delete_product_db, delete_all_products_db, update_product_db
import cloudinary.uploader

products_router = APIRouter(prefix="/products", tags=["products"])

@products_router.post("/", response_model=ProductOut)
def create_product(category: str = Form(...), name: str = Form(...), price: float = Form(...), description: str = Form(None),image: UploadFile = File(...)):
    try:
        upload_result = cloudinary.uploader.upload(image.file)
        image_url = upload_result['secure_url']

        novo_produto = ProductInDB(
            category=category,
            name=name,
            price=price,
            description=description,
            image_url=image_url
        )

        prod = create_product_db(novo_produto)

        return ProductOut(
            id=prod[0],
            name=prod[1],
            price=prod[2],
            category=prod[3],
            description=prod[4],
            image_url=prod[5]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@products_router.get("/", response_model=list[ProductOut])
def list_products(category: str = Query(None)):
    try:
        filters = {}
        if category:
            filters["category"] = category
        products = list_products_db(filters)
        return [ProductOut(
            id=prod[0],
            name=prod[1],
            price=prod[2],
            category=prod[3],
            image_url=prod[4],
            description=prod[5]
        ) for prod in products]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@products_router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str = Path(...)):
    try:
        return get_product_db(product_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@products_router.delete("/{product_id}", response_model=MessageResponse)
def delete_product(product_id: str = Path(...)):
    try:
        return delete_product_db(product_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@products_router.delete("/")
def delete_all_products():
    try:
        return delete_all_products_db()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@products_router.patch("/{product_id}")
def update_product(product_id: str, product: ProductOut):
    try:
        return update_product_db(product_id, product)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
