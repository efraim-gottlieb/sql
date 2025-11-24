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
      print('books list is empty!')
    else:
      for book in books:
        print(f'ID: {book.id}\ntitle: {book.title}\nauthor: {book.author}\npages: {book.pages}\nprice: {book.price}')
        print('-' *10)

def get_book_by_id(book_id):
  book = None
  with Session(engine) as session:
    try:
      book = session.get(Book,book_id)
      print(f'ID: {book.id}\ntitle: {book.title}\nauthor: {book.author}\npages: {book.pages}\nprice: {book.price}')
      return
    except:
      print('book not found !')

def update_book_price(book_id, new_price):
  with Session(engine) as session:
    try:
      book = session.exec(select(Book).where(Book.id == book_id)).first()
      book.price = new_price
      session.commit()
      print('price updated !')
    except:
      print('book not found !')

def delete_book(book_id):
  with Session(engine) as session:
    try:
      book = session.exec(select(Book).where(Book.id == book_id)).first()
      session.delete(book)
      session.commit()
      print('book deleted !')
    except:
      print('book not found !')

def count_books():
  with Session(engine) as session:
    books = session.exec(select(Book)).all()
    print(f'number of books: {len(books)}')

def add_books(books: list[object]):
  if books:
    for book in books:
      add_book(book.title, book.author, book.pages, book.price)
      print(f'added {len(books)} books !')
  else:
    print('no books to add !')

def book_exists(title):
  with Session(engine) as session:
      return bool(session.exec(select(Book).where(Book.title == title)).first())




# update_book_price(4, 50)
# show_all_books()
# # delete_book(4)
# add_book('Tora', 'Gad', 450, 35)
# count_books()
# a  = Book(title= 'mishna', author='tanaim', pages='450', price='10')
# b  = Book(title= 'mishna2', author='tanaim', pages='670', price='50')
# add_books([])
print(book_exists('mishna'))