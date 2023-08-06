# coding: utf-8
from .sql_ctx import SqlCtx


class BaseSql:
    def __init__(self, connect_str: str) -> None:
        self._conn_str = connect_str

    @property
    def conn_str(self) -> str:
        """Gets connect_str value"""
        return self._conn_str

    def get_row_count(self) -> int:
        if self.has_data is False:
            return 0
        query = 'SELECT count() FROM ' + self.get_table_name()
        with SqlCtx(self._conn_str) as db:
            db.cursor.execute(query)
            num_of_rows = db.cursor.fetchone()[0]
        return num_of_rows

    def remove_all(self) -> None:
        self._drop_table_if_exist()
        self._create_table_if_not_exist()

    def has_data(self) -> bool:
        query = f"SELECT * FROM {self.get_table_name()} limit 1"
        has_data = False
        with SqlCtx(self._conn_str) as db:
            db.cursor.execute(query)
            for _ in db.cursor:
                has_data = True
        return has_data
