# coding: utf-8
from typing import Dict, List, Optional, Union
from .base_sql import BaseSql
from .sql_ctx import SqlCtx
from .ooo_type import OooType
from ..data_class.component import Component


class QryComponent(BaseSql):
    def __init__(self, connect_str: str) -> None:
        super().__init__(connect_str=connect_str)

    def get_component(self, full_ns: str) -> Union[Component, None]:
        """
        Gets component instance for a given namespace

        Args:
            full_ns (str): full namespace used for match.

        Returns:
            Union[Component, None]: Component instance if ``full_ns`` is a match; Otherwise, ``None``
        """
        qry_str = """SELECT component.id_component, component.name, component.namespace as ns,
            component.type, component.version, component.lo_ver, component.file, component.url, component.c_name,
            component.map_name, module_detail.sort as sort
            FROM component
            LEFT JOIN module_detail ON module_detail.id_namespace = component.id_component
            Where component.id_component like :namespace
            Limit 1;"""
        args = {"namespace": full_ns}
        result = None
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str, args)
            for row in db.cursor:
                result = Component(
                    id_component=row['id_component'],
                    name=row['name'],
                    namespace=row['ns'],
                    type=row['type'],
                    version=row['version'],
                    lo_ver=row['lo_ver'],
                    file=row['file'],
                    url=row['url'],
                    c_name=row['c_name'],
                    map_name=row['map_name'],
                    sort=row['sort']
                )

        return result

    def get_component_by_map_name(self, map_name: str) -> Union[Component, None]:
        """
        Gets component instance for a given map_name

        Args:
            map_name (str): map_name used for match.

        Returns:
            Union[Component, None]: Component instance if ``map_name`` is a match; Otherwise, ``None``
        """
        qry_str = """SELECT component.id_component, component.name, component.namespace as ns,
            component.type, component.version, component.lo_ver, component.file, component.url, component.c_name,
            component.map_name, module_detail.sort as sort
            FROM component
            LEFT JOIN module_detail ON module_detail.id_namespace = component.id_component
            WHERE component.map_name like :mapped_name
            Limit 1;"""
        args = {"mapped_name": map_name}
        result: Component = None
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str, args)
            for row in db.cursor:
                result = Component(
                    id_component=row['id_component'],
                    name=row['name'],
                    namespace=row['ns'],
                    type=row['type'],
                    version=row['version'],
                    lo_ver=row['lo_ver'],
                    file=row['file'],
                    url=row['url'],
                    c_name=row['c_name'],
                    map_name=row['map_name'],
                    sort=row['sort']
                )

        return result

    def get_components(self, search_str: str, type: Optional[OooType] = None, limit: int = 0) -> List[Component]:
        """
        Gets component instances for a given namespace

        Args:
            search_str (str): search string that can be used with % and _
            limit (int, optional): Limits number of return if Limt > 0. Defaults to 0.

        Returns:
            List[Component]: Component instances.
        """
        if type is None:
            s_type = ""
        else:
            s_type = f"\nAND component.type like '{type}'"
        qry_str = """SELECT component.id_component, component.name, component.namespace as ns,
            component.type, component.version, component.lo_ver, component.file, component.url, component.c_name,
            component.map_name, module_detail.sort as sort
            FROM component
            LEFT JOIN module_detail ON module_detail.id_namespace = component.id_component
            Where component.id_component like :namespace
            """
        qry_str += s_type
        qry_str += "\nORDER By module_detail.sort"
        if limit > 0:
            qry_str += f"\nLimit {limit}"
        qry_str += ';'
        args = {"namespace": search_str}
        results: List[Component] = []
        with SqlCtx(self.conn_str) as db:
            db.cursor.execute(qry_str, args)
            for row in db.cursor:
                results.append(Component(
                    id_component=row['id_component'],
                    name=row['name'],
                    namespace=row['ns'],
                    type=row['type'],
                    version=row['version'],
                    lo_ver=row['lo_ver'],
                    file=row['file'],
                    url=row['url'],
                    c_name=row['c_name'],
                    map_name=row['map_name'],
                    sort=row['sort']
                ))

        return results

    def get_components_group_by_ns(self, search_str: Optional[str] = None) -> Dict[str, Component]:
        """
        Gets component instances for a given namespace

        Args:
            search_str (str, optional): search string that can be used with % and _

        Returns:
            Dict[str, Component]: Component instances grouped by namespace.
        """
        qry_str = """SELECT component.id_component, component.name, component.namespace as ns,
            component.type, component.version, component.lo_ver, component.file, component.url, component.c_name,
            component.map_name, module_detail.sort as sort
            FROM component
            LEFT JOIN module_detail ON module_detail.id_namespace = component.id_component"""
        if search_str:
            qry_str += " Where component.id_component like :namespace"
        qry_str += " ORDER By component.id_component;"
        args = {"namespace": search_str}
        results: Dict[str, Component] = {}
        with SqlCtx(self.conn_str) as db:
            if search_str:
                db.cursor.execute(qry_str, args)
            else:
                db.cursor.execute(qry_str)
            for row in db.cursor:
                component = Component(
                    id_component=row['id_component'],
                    name=row['name'],
                    namespace=row['ns'],
                    type=row['type'],
                    version=row['version'],
                    lo_ver=row['lo_ver'],
                    file=row['file'],
                    url=row['url'],
                    c_name=row['c_name'],
                    map_name=row['map_name'],
                    sort=row['sort']
                )
                if not component.namespace in results:
                    results[component.namespace] = []
                results[component.namespace].append(component)
        return results
