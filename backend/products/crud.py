from fastapi import HTTPException,Path
from backend.db import get_connection
from backend.models import ProductInDB

def create_product_db(product: ProductInDB):
    conn = get_connection()
    cur = conn.cursor()
    print(product)
    try:
        cur.execute("""
            INSERT INTO products (name, price, category, description, image_url)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *;
        """, (product.name, product.price, product.category, product.description, product.image_url))
        new_product = cur.fetchone()
        conn.commit()
        return new_product
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def list_products_db(filters: dict = None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        query = "SELECT * FROM products"
        params = []
        if filters and filters.get("category"):
            query += " WHERE category = %s"
            params.append(filters["category"])
        cur.execute(query, tuple(params))
        products = cur.fetchall()
        return products
    finally:
        cur.close()
        conn.close()

def get_product_db(product_id: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
        product = cur.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def delete_product_db(product_id: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM products WHERE id = %s;", (product_id,))
        deleted_count = cur.rowcount
        conn.commit()
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": f"Product {product_id} deleted successfully."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def delete_all_products_db():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM products;")
        conn.commit()
        return {"message": "All products deleted successfully."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def update_product_db(product_id: str, product: ProductInDB):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE products
            SET name = %s, price = %s, category = %s, description = %s
            WHERE id = %s
            RETURNING *;
        """, (product.name, product.price, product.category, product.description, product_id))
        updated_product = cur.fetchone()
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        conn.commit()
        return updated_product
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()
