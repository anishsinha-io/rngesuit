# Copyright (C) 2024 Anish Sinha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from dataclasses import dataclass
from typing import LiteralString, cast

import psycopg
from psycopg.sql import SQL
from sqlalchemy import Engine, Table, inspect
from sqlalchemy.orm import DeclarativeBase

from rngesuit.digraph import Digraph


class Base(DeclarativeBase):
    pass


@dataclass
class SchemaTopology:
    """
    Dataclass representing the topology of a PostgreSQL schema.
    """

    table_graph: Digraph[str]
    orm_classes: dict[str, type[Base]]


def migrate(url: str, sql: str) -> None:
    """
    Migrates the PostgreSQL database using the given SQL script.
    """
    with psycopg.connect(conninfo=url) as conn:
        query = SQL(cast(LiteralString, sql))
        conn.execute(query)


def generate_classes(
    engine: Engine, table_names: list[str], schema: str
) -> dict[str, type[Base]]:
    """
    Dynamically generates SQLAlchemy ORM classes for the given table names.

    :param engine: SQLAlchemy engine connected to the PostgreSQL database.
    :param table_names: List of table names for which to generate ORM classes.
    :return: A dictionary mapping table names to their dynamically created classes.
    """
    Base.registry.dispose()
    Base.metadata.clear()
    classes: dict[str, type] = {}
    for table_name in table_names:
        class_name = "".join(
            word.capitalize() for word in table_name.split("_")
        )  # PascalCase
        new_class = type(
            class_name + "Entity",
            (Base,),
            {
                "__table__": Table(
                    table_name,
                    Base.metadata,
                    autoload_with=engine,
                    schema=schema,
                )
            },
        )
        classes[table_name] = new_class
    return classes


def introspect(engine: Engine, schema: str = "public") -> SchemaTopology:
    """
    Introspects the given PostgreSQL database and returns its schema topology.
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    orm_classes = generate_classes(engine, tables, schema)
    table_graph = Digraph()
    for table_name, klass in orm_classes.items():
        table = klass.__table__
        for fk in table.foreign_keys:
            referenced_table = fk.column.table.name
            table_graph.add_edge(table_name, referenced_table)
    return SchemaTopology(table_graph=table_graph, orm_classes=orm_classes)
