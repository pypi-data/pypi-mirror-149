from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from redshift_client.data_type.core import (
    DataType,
    PrecisionType,
    StaticTypes,
)
from redshift_client.id_objs import (
    TableId,
)
from redshift_client.sql_client import (
    QueryValues,
    RowData,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.sql_client.query import (
    dynamic_query,
    new_query,
)
from redshift_client.table._assert import (
    to_column,
)
from redshift_client.table.core import (
    new as new_table,
    Table,
)
from typing import (
    Callable,
    Dict,
    Optional,
)


@dataclass(frozen=True)
class ManifestId:
    uri: str


def _encode_data_type(d_type: DataType) -> str:
    if isinstance(d_type.value, StaticTypes):
        return d_type.value.value
    if isinstance(d_type.value, PrecisionType):
        return f"{d_type.value.data_type.value}({d_type.value.precision})"
    return f"DECIMAL({d_type.value.precision},{d_type.value.scale})"


@dataclass(frozen=True)
class TableClient:
    _db_client: SqlClient

    def unload(
        self, table: TableId, prefix: str, role: str
    ) -> Cmd[ManifestId]:
        """
        prefix: a s3 uri prefix
        role: an aws role id-arn
        """
        stm = """
            UNLOAD ('SELECT * FROM {schema}.{table}')
            TO %(prefix)s iam_role %(role)s MANIFEST ESCAPE
        """
        args: Dict[str, PrimitiveVal] = {"prefix": prefix, "role": role}
        return self._db_client.execute(
            dynamic_query(
                stm,
                FrozenDict({"schema": table.schema.name, "table": table.name}),
            ),
            QueryValues(FrozenDict(args)),
        ).map(lambda _: ManifestId(f"{prefix}manifest"))

    def load(
        self,
        table: TableId,
        manifest: ManifestId,
        role: str,
        nan_handler: bool = True,
    ) -> Cmd[None]:
        """
        If `nan_handler` is disabled, ensure that the table does not contain NaN values on float columns
        """
        nan_fix = "NULL AS 'nan'" if nan_handler else ""
        stm = f"""
            COPY {{schema}}.{{table}} FROM %(manifest_file)s
            iam_role %(role)s MANIFEST ESCAPE {nan_fix}
        """
        args: Dict[str, PrimitiveVal] = {
            "manifest_file": manifest.uri,
            "role": role,
        }
        return self._db_client.execute(
            dynamic_query(
                stm,
                FrozenDict({"schema": table.schema.name, "table": table.name}),
            ),
            QueryValues(FrozenDict(args)),
        )

    def get(self, table: TableId) -> Cmd[Table]:
        stm = """
            SELECT ordinal_position,
                column_name,
                data_type,
                CASE WHEN character_maximum_length IS not null
                        THEN character_maximum_length
                        ELSE numeric_precision end AS max_length,
                numeric_scale,
                is_nullable,
                column_default AS default_value
            FROM information_schema.columns
            WHERE table_name = %(table_name)s
                AND table_schema = %(table_schema)s
            ORDER BY ordinal_position
        """
        args: Dict[str, PrimitiveVal] = {
            "table_schema": table.schema.name,
            "table_name": table.name,
        }
        exe = self._db_client.execute(
            new_query(stm),
            QueryValues(FrozenDict(args)),
        )
        results = self._db_client.fetch_all()

        def _extract(raw: FrozenList[RowData]) -> Table:
            columns_pairs = tuple(to_column(column.data) for column in raw)
            columns = FrozenDict(dict(columns_pairs))
            order = tuple(i for i, _ in columns_pairs)
            return new_table(order, columns, frozenset()).unwrap()

        return (exe + results).map(_extract)

    def new(
        self, table_id: TableId, table: Table, if_not_exist: bool = False
    ) -> Cmd[None]:
        enum_primary_keys = tuple(enumerate(table.primary_keys))
        enum_columns = tuple(
            enumerate(tuple((i, table.columns[i]) for i in table.order))
        )
        p_fields = ",".join([f"{{pkey_{i}}}" for i, _ in enum_primary_keys])
        pkeys_template = (
            f",PRIMARY KEY({p_fields})" if table.primary_keys else ""
        )
        not_exists = "" if not if_not_exist else "IF NOT EXISTS"
        encode_nullable: Callable[[bool], str] = (
            lambda b: "NULL" if b else "NOT NULL"
        )
        fields_template: str = ",".join(
            [
                f"""
                    {{name_{n}}} {_encode_data_type(c.data_type)}
                    DEFAULT %(default_{n})s {encode_nullable(c.nullable)}
                """
                for n, (_, c) in enum_columns
            ]
        )
        stm = f"CREATE TABLE {not_exists} {{schema}}.{{table}} ({fields_template}{pkeys_template})"
        identifiers: Dict[str, Optional[str]] = {
            "schema": table_id.schema.name,
            "table": table_id.name,
        }
        for index, cid in enum_primary_keys:
            identifiers[f"pkey_{index}"] = cid.name
        for index, (cid, _) in enum_columns:
            identifiers[f"name_{index}"] = cid.name
        values = FrozenDict(
            {f"default_{index}": c.default for index, (_, c) in enum_columns}
        )
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), QueryValues(values)
        )
