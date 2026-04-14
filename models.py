import os
from uuid import uuid4

from sqlalchemy import func
from sqlmodel import Field, Session, SQLModel, create_engine, select

sqlite_filename = "jokes.db"
sqlite_url = f"sqlite:///{sqlite_filename}"
engine = create_engine(sqlite_url, echo=True)


class Joke(SQLModel, table=True):
    __tablename__ = "jokes"

    id: str = Field(default=str(uuid4()), primary_key=True)
    question: str = Field(index=True, nullable=False, unique=True)
    answer: str | None = None
    explanation: str | None = None
    image: str | None = None


def get_random_joke() -> Joke:
    with Session(engine) as session:
        joke = session.exec(select(Joke).order_by(func.random())).first()

    return joke


def get_joke_by_id(joke_id: str) -> Joke:
    with Session(engine) as session:
        statement = select(Joke).where(Joke.id == joke_id)
        results = session.exec(statement)
        joke = results.first()
        return joke


def save_joke(question: str, answer: str) -> str:
    # Create the tables if the db file does not exist
    if not os.path.isfile(sqlite_filename):
        SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Check if the joke already exists
        statement = select(Joke).where(Joke.question == question)
        results = session.exec(statement)
        joke = results.first()
        if joke:
            return joke.id
        else:  # Save the joke to the database
            joke_id = str(uuid4())
            new_joke = Joke(id=joke_id, question=question, answer=answer)
            session.add(new_joke)
            session.commit()

    return joke_id


def update_joke_image(joke_id: str, image: str = None):
    with Session(engine) as session:
        statement = select(Joke).where(Joke.id == joke_id)
        results = session.exec(statement)
        joke = results.first()
        joke.image = image
        session.add(joke)
        session.commit()


def update_joke_explanation(joke_id: str, explanation: str = None):
    with Session(engine) as session:
        statement = select(Joke).where(Joke.id == joke_id)
        results = session.exec(statement)
        joke = results.first()
        joke.explanation = explanation
        session.add(joke)
        session.commit()
