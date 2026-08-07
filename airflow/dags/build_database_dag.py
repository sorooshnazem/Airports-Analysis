import pendulum
from datetime import timedelta
from airflow.sdk import dag, task

from scripts.pipeline_tasks import (
    build_airports_table,
    build_countries_table,
    build_frequencies_table,
    build_regions_table,
    build_runways_table,
    build_airport_weather_table,
    validate_database
)


@dag(
    dag_id="build_airports_database",
    schedule="0 6 * * *",
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="UTC"
    ),
    catchup=False,
    tags=["airports", "database", "etl"]
)
def build_airports_database_dag():

    @task(
        retries=2,
        retry_delay=timedelta(minutes=2)
    )
    def create_airports_table():
        build_airports_table()

    @task(
        retries=2,
        retry_delay=timedelta(minutes=2)
    )
    def create_runways_table():
        build_runways_table()

    @task(
        retries=2,
        retry_delay=timedelta(minutes=2)
    )
    def create_frequencies_table():
        build_frequencies_table()

    @task(
        retries=2,
        retry_delay=timedelta(minutes=2)
    )
    def create_countries_table():
        build_countries_table()

    @task(
        retries=2,
        retry_delay=timedelta(minutes=2)
    )
    def create_regions_table():
        build_regions_table()

    @task(
        retries=2,
        retry_delay=timedelta(minutes=2)
    )
    def run_database_validations():
        validate_database()

    @task(
        retries=2,
        retry_delay=timedelta(minutes=2)
    )
    def create_airport_weather_table():

        build_airport_weather_table(
            "LIRF"
        )

    airports_task = create_airports_table()
    runways_task = create_runways_table()
    frequencies_task = create_frequencies_table()
    countries_task = create_countries_table()
    regions_task = create_regions_table()
    validation_task = run_database_validations()
    weather_task = create_airport_weather_table()

    (
        airports_task
        >> runways_task
        >> frequencies_task
        >> countries_task
        >> regions_task
        >> weather_task
        >> validation_task
    )


build_airports_database_dag()