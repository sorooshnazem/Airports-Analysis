import pendulum

from airflow.sdk import dag, task

from scripts.build_database import main


@dag(
    dag_id="build_airports_database",
    schedule=None,
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="UTC"
    ),
    catchup=False,
    tags=["airports", "database"]
)
def build_database_dag():

    @task
    def build_database():

        main()

    build_database()


build_database_dag()
