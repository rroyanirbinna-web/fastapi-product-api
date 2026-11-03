from fastapi import FastAPI, Depends ,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session
app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)


@app.get("/")
def greet():
    return "Welcome !"




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products


@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id).first()
    if db_product:
        return db_product
    raise HTTPException(status_code=404,detail="Product not found")


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated successfully"
    else:
         raise HTTPException(status_code=404,detail="Product not found")


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else:
        raise HTTPException(status_code=404,detail="Product not found")

# dictionary check variation
