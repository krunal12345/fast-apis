from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session

from utils.user_utils import engine, get_current_user
from utils.unit_of_work import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from schemas.user_models import UserBase


def get_uow() -> Generator[AbstractUnitOfWork, None, None]:
    """
    FastAPI dependency that owns the full request transaction.

    Execution order:
      1. Open a fresh Session (before yield)
      2. Route handler runs (during yield)
      3. commit() if no exception, rollback() if any exception
      4. Close session (finally block, always)

    Why explicit try/except/finally instead of 'with SqlAlchemyUnitOfWork()'?
    FastAPI calls generator.close() (not generator.throw()) when the route
    raises an HTTPException — the 'with' block __exit__ would not see the
    exception type.  The explicit pattern below handles both cases correctly.
    """
    uow = SqlAlchemyUnitOfWork()
    uow.session = Session(engine)
    try:
        yield uow
        uow.commit()
    except Exception:
        uow.rollback()
        raise
    finally:
        uow.session.close()


# Reusable type aliases — import these in main.py instead of repeating Annotated[...]
UoWDep = Annotated[AbstractUnitOfWork, Depends(get_uow)]
CurrentUser = Annotated[UserBase, Depends(get_current_user)]
