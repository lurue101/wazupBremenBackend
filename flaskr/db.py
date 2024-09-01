import json
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import create_engine

from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    date: Mapped[datetime]
    author_s: Mapped[Optional[str]]
    url: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, title={self.title!r}, date={self.date!r})"


engine = create_engine(
    "sqlite:////home/rueckelu/wazupHBBackend/flaskr/events.db", echo=True
)
# Nur zum erstellen

# Base.metadata.create_all(engine)
with open("/home/rueckelu/wazupHB/kukoon.json", "r") as f:
    events = json.loads(f.read())

with Session(engine) as session:
    events_to_add = []
    for event in events:
        day, month, year = event["date"].split(".")
        events_to_add.append(
            Event(
                title=event["title"],
                date=datetime(year=int(year), month=int(month), day=int(day)),
            )
        )
        session.add_all(events_to_add)
        session.commit()
