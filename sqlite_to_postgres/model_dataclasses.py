import uuid
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    id: uuid.UUID = field(default_factory=uuid.uuid4)

    # def save(self):
    #     self.modified = datetime.now()


@dataclass
class Person:
    full_name: str
    created_at: datetime
    updated_at: datetime

    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre_Film_work:
    created_at: datetime

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person_Film_work:
    role: str
    created_at: datetime

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Film_work:
    title: str
    description: str
    creation_date: datetime
    file_path: str
    type: str
    created_at: datetime
    updated_at: datetime

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    rating: float = field(default=0.0)
