# How to Create and Apply Alembic Migrations

This guide explains how to generate and apply database migrations using Alembic after the initial setup is complete.

---

## 📦 Prerequisites

Before creating migrations, make sure you have the following libraries installed:

```bash
pip install alembic sqlalchemy psycopg2-binary
```
---

Add a .env variable called `DATABASE_URL` in the root of the file migrations. Assigning the value `db_url` located in the secrets.

---

## ✏️ Step 1: Modify your SQLAlchemy models

Update or create your models (e.g. add a new table or modify a column):

```python
# migrations/models.py

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

## 🛠️ Step 2: Autogenerate a migration script

Run the following command to generate a new migration file based on your model changes:

```bash
alembic -c migrations/alembic.ini revision --autogenerate -m "create posts table"
```

This will create a `.py` file under `migrations/alembic/versions/`.

---

## 👁️ Step 3: Review the migration file

Open the generated file and confirm the changes:

```python
def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('posts')
```

> 💡 Alembic doesn't include default values in migrations by default. You can manually add them if needed.

---

## 🚀 Step 4: Apply the migration

Run the upgrade command to apply the migration to the database:

```bash
alembic -c migrations/alembic.ini upgrade head
```

---

## 🔁 Optional: Rollback (downgrade) the migration

To undo the last migration:

```bash
alembic -c migrations/alembic.ini downgrade -1
```

---

## ✅ Summary

| Action               | Command                                               |
|----------------------|--------------------------------------------------------|
| Generate migration   | `alembic revision --autogenerate -m "message"`        |
| Apply migration      | `alembic upgrade head`                                |
| Rollback migration   | `alembic downgrade -1`                                |

> 💡 You only need to modify your SQLAlchemy models. Alembic reads the `Base.metadata` and compares it with the current database schema to generate migrations automatically.
