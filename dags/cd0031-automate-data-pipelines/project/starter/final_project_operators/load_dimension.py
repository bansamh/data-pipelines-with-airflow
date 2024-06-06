from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    sql_insert = """
        insert into {} {}
    """

    @apply_defaults
    def __init__(self,
                redshift_conn_id = "",
                table = "",
                sql_statement = "",
                append_only = "",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_statement = sql_statement
        self.append_only = append_only

    def execute(self, context):
        self.log.info('Get Credentials')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # delete data from table
        if not self.append_only:
            self.log.info(f"Clear data from Redshift table {self.table}")
            redshift.run("DELETE FROM {}".format(self.table))

        self.log.info(f"Load data into fact table in Redshift {self.table}")
        formatted_sql = LoadDimensionOperator.sql_insert.format(self.table, self.sql_statement)

        redshift.run(formatted_sql)