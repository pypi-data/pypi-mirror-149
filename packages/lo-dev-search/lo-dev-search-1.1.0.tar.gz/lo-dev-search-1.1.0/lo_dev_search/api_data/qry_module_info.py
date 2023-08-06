# coding: utf-8
from typing import Dict, List, Optional, Union
from .base_sql import BaseSql
from .sql_ctx import SqlCtx
from ..data_class.module_info import ModuleInfo


class QryModuleInfo(BaseSql):
    def __init__(self, connect_str: str) -> None:
        super().__init__(connect_str=connect_str)

    def get_mod_info(self, id: str) -> Union[ModuleInfo, None]:
        """
        Gets a single ModuleInfo fo ra given id.

        Args:
            id (str): Id of the ModuleInfo

        Returns:
            Union[ModuleInfo, None]: ModuleInfo if id exist in database; Otherwise, None
        """        
        qry_str = """SELECT module_info.id_module_info, module_info.url_base, module_info.file
            FROM module_info
            WHERE module_info.id_module_info like :id
            LIMIT 1;"""
        args = {"id": id}
        result = None
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str, args)
            for row in db.cursor:
                result = ModuleInfo(
                    id_module_info=row['id_module_info'],
                    url_base=row['url_base'],
                    file=row['file']
                )
        return result

    def get_mod_infos(self, search_str: str, limit: int = 0) -> List[ModuleInfo]:
        """
        Gets a list of ModuleInfo for matching search criteraia.

        Args:
            search_str (str): Search String including wild cards.
            limit (int, optional): Limits number of return if Limt > 0. Defaults to 0.

        Returns:
            List[ModuleInfo]: Results of search
        """        
        qry_str = """SELECT module_info.id_module_info, module_info.url_base, module_info.file
            FROM module_info
            WHERE module_info.id_module_info like :search"""
        if limit > 0:
            qry_str += f"\nLimit {limit}"
        qry_str += ';'
        args = {"search": search_str}
        results: List[ModuleInfo] = []
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str, args)
            for row in db.cursor:
                results.append(ModuleInfo(
                    id_module_info=row['id_module_info'],
                    url_base=row['url_base'],
                    file=row['file']
                ))

        return results
