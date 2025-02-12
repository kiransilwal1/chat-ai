from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from chatai.models import ChatData, ChatPath
from features.chat.path_context.path_context_datasource_interface import (
    IPathContextDatasource,
)
from sqlalchemy import exc


class PathContextSqlite(IPathContextDatasource):
    def __init__(self, datasource: sessionmaker[Session]):
        self._datasource = datasource

    async def summarize(self, response_string: str, model_path: str) -> str:
        return ""

    async def get_summaries(self, path_id: str) -> str:
        session: Session = (
            self._datasource()
        )  # assuming _datasource() provides a session
        # use column expression to resolve the type mismatch
        paths = (
            session.query(ChatData).filter(ChatData.chat_path_id == int(path_id)).all()
        )

        data = ""
        for path in paths:
            data = f"{data}: {path.summary}"

        return data

    async def limit_context(self, text: str) -> str:
        return ""

    async def create_context_path(self, path: str) -> str:
        session: Session = (
            self._datasource()
        )  # assuming _datasource() provides a session
        try:
            new_path = ChatPath(path=path)
            session.add(new_path)
            session.commit()
            session.refresh(new_path)  # Ensures new_path.id is populated after commit
            return str(new_path.id)
        except exc.IntegrityError:
            print(f"Path {path} already exists in the database.")
            return f"Path {path} already exists in the database."
        finally:
            session.close()

    async def has_path(self, path: str) -> str | None:
        session: Session = (
            self._datasource()
        )  # assuming _datasource() provides a session
        try:
            path_obj = (
                session.query(ChatPath).filter(ChatPath.path == path).first()
            )  # Use `.first()` instead of `.all()`
            return (
                str(path_obj.id) if path_obj else None
            )  # Return ID if found, otherwise None
        except exc.SQLAlchemyError as e:  # Catch general SQLAlchemy errors
            print(f"Database error: {e}")
            return None
        finally:
            session.close()

    # async def has_path(self, path: str) -> str | None:
    #     session: Session = (
    #         self._datasource()
    #     )  # assuming _datasource() provides a session
    #     try:
    #         session.add(ChatPath(path=path))
    #         paths = session.query(ChatPath).filter(ChatPath.path == path).all()
    #         session.commit()
    #         return str(paths[0].id)
    #     except exc.IntegrityError:
    #         print(f"Path {path} could not be found in the database")
    #     finally:
    #         session.close()

    async def add_context(self, path_id: int, full_chat: str, summary: str) -> str:
        session: Session = (
            self._datasource()
        )  # assuming _datasource() provides a session
        try:
            session.add(
                ChatData(
                    chat_path_id=path_id,
                    full_chat=full_chat,
                    summary=summary,
                )
            )
            session.commit()
            return summary
        except exc.IntegrityError:
            print("Something went wrong!")
            raise ValueError("Context could not be added")
        finally:
            session.close()
