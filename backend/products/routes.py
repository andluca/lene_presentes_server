from fastapi import APIRouter, HTTPException, Path
from models import ProductIn
from .crud import create_product_db, list_products_db, get_product_db, delete_product_db, delete_all_products_db, update_product_db

products_router = APIRouter(prefix="/products", tags=["products"])

@products_router.post("/")
def create_product(product: ProductIn):
    try:
        return create_product_db(product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@products_router.get("/", response_model=list[ProductIn])
def list_products():
    try:
        return list_products_db()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@products_router.get("/{product_id}", response_model=ProductIn)
def get_product(product_id: str = Path(...)):
    try:
        return get_product_db(product_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@products_router.delete("/{product_id}")
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
def update_product(product_id: str, product: ProductIn):
    try:
        return update_product_db(product_id, product)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
