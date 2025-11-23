from sqlmodel import SQLModel, Session,create_engine, select, Field

DB_URL = 'mysql+pymysql://root:root@localhost:3306/bookstore_db'
engine = create_engine(DB_URL)

class Book(SQLModel, table = True):
  __tablename__ = 'books'
  id :int | None = Field(primary_key=True)
  title :str = Field(max_length=200,nullable=False)
  author :str = Field(max_length=100,nullable=False)
  pages :int
  price :float

# SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

def add_book(title, author, pages, price):
  with Session(engine) as session:
    book = Book(title=title, author=author, pages=pages, price=price)
    session.add(book)
    session.commit()
    session.refresh(book)
    print(f'book added! id: {book.id}')
    return book
  
def show_all_books():
  with Session(engine) as session:
    books = session.exec(select(Book)).all()
    if not books:
      print('books is empty!')
      return
    for book in books:
      print(f'ID: {book.id}\ntitle: {book.title}\nauthor: {book.author}\npages: {book.pages}\nprice: {book.price}')
      print('-' *10)

def get_book_by_id(book_id):
  book = None
  with Session(engine) as session:
    try:
      book = session.get_one(Book,book_id)
      print(f'ID: {book.id}\ntitle: {book.title}\nauthor: {book.author}\npages: {book.pages}\nprice: {book.price}')
      return
    except:
      print('book not found !')

def update_book_price(book_id, new_price):
  pass
show_all_books()
get_book_by_id(4)
