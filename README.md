# oauth-server


# quick start:
```bash
cp .env.template .env
```
```bash
alembic init alembic
```
add in alembic/env.py:
```python
from app.models import Base
target_metadata = Base.metadata
```

in alembic.ini set:
```ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```
```bash
alembic revision --autogenerate -m "initial migration"
```
```bash
alembic upgrade head
```