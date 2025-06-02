from fastapi import HTTPException,Path
from db import get_connection
from models import ProductIn

def create_product_db(product: ProductIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO products (name, price, category, description)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (product.name, product.price, product.category, product.description))
        new_product = cur.fetchone()
        conn.commit()
        return new_product
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

def list_products_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products;")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return products

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

def update_product_db(product_id: str, product: ProductIn):
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
