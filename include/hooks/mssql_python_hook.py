import mssql_python
from airflow.providers.common.sql.hooks.sql import DbApiHook


class MsSqlPythonHook(DbApiHook):
    conn_name_attr = "mssql_python_conn_id"
    default_conn_name = "mssql_python_default"
    conn_type = "mssql_python"
    hook_name = "MS SQL Python"

    def __init__(
        self,
        mssql_python_conn_id: str = default_conn_name,
        database: str | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.mssql_python_conn_id = mssql_python_conn_id
        self.database = database

    def get_conn(self):
        airflow_conn = self.get_connection(self.mssql_python_conn_id)

        extras = airflow_conn.extra_dejson or {}

        auth_method = extras.get("authentication", "SqlPassword")

        encrypt = extras.get("encrypt", "yes")
        if isinstance(encrypt, bool):
            encrypt = "yes" if encrypt else "no"

        trust_server_certificate = extras.get(
            "trustservercertificate",
            extras.get("trust_server_certificate", "no"),
        )
        if isinstance(trust_server_certificate, bool):
            trust_server_certificate = "yes" if trust_server_certificate else "no"

        conn_parts = [
            f"SERVER=tcp:{airflow_conn.host},{airflow_conn.port or 1433}",
            f"Encrypt={encrypt}",
            f"TrustServerCertificate={trust_server_certificate}",
        ]

        database = self.database or airflow_conn.schema or extras.get("database")
        if database:
            conn_parts.append(f"DATABASE={database}")

        if auth_method == "SqlPassword":
            username = (
                airflow_conn.login
                or extras.get("uid")
                or extras.get("user")
                or extras.get("username")
                or extras.get("login")
            )
            password = airflow_conn.password or extras.get("pwd") or extras.get("password")

            if not username or not password:
                raise ValueError(
                    "SqlPassword authentication requires username and password. "
                    "Set connection Login/Password or extras uid/user/username and pwd/password."
                )

            conn_parts.extend(
                [
                    f"UID={username}",
                    f"PWD={password}",
                ]
            )
        else:
            conn_parts.append(f"Authentication={auth_method}")

        conn_string = ";".join(conn_parts) + ";"

        return mssql_python.connect(conn_string)
