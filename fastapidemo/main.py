from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

@app.get("/")

def greet():
    return "Hello User"

products = [
    product(id = 1, name =  "phone", description = "Samsung", price = 100000.00, quantity = 1),    
    product(id = 2, name =  "Laptop", description = "Apple", price = 1000090.00, quantity = 4),
    product(id = 3, name =  "Tablet", description = "Apple", price = 10000.00, quantity = 5),
    product(id = 4, name =  "Car", description = "RR", price = 10000000.00, quantity = 6),
    ]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    
    count = db.query(database_models.product).count

    if count == 0:
        for product in products:
            db.add(database_models.product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    # db = session()
    # db = query()
    db_products = db.query(database_models.product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
     return db_product
    return "Product not found"


@app.post("/products")
def add_product(product: product, db:Session = Depends(get_db)):
    db.add(database_models.product(**product.model_dump()))
    db.commit()
    return products


@app.put("/products/{id}")
def update_product(id:int, product:product, db:Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "No product found"

@app.delete("/products/{id}")
def delete_product(id:int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    else:
        return "Product not found"