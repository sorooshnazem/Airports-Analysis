import pendulum

from airflow.sdk import dag, task


@dag(
    dag_id="airports_hello",
    schedule=None,
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="UTC"
    ),
    catchup=False,
    tags=["airports", "learning"]
)
def airports_hello_dag():

    @task
    def say_hello():

        print(
            "Hello from the Airports Analysis Airflow pipeline!"
        )

    say_hello()


airports_hello_dag()
