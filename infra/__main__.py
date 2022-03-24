import secrets
import string
import time
import pulumi
import pulumi_gcp as gcp

with open('../sql_query.sql') as f:
    my_query = f.read()

gen = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(8))

bucket = gcp.storage.Bucket(
    "code-bucket",
    location="US"
)

archive = gcp.storage.BucketObject(
    "code-archive",
    bucket=bucket.name,
    source=pulumi.FileArchive("../app")
)

storage = gcp.storage.Bucket(
    "laura-dataset",
    location="US",
    force_destroy=True
)

bar = gcp.bigquery.Dataset(
    "bar",
    dataset_id="job_query_dataset",
    friendly_name="test",
    description="This is a test description",
    location="US"
)

foo = gcp.bigquery.Table(
    "foo",
    deletion_protection=False,
    dataset_id=bar.dataset_id,
    table_id="job_query_table"
)

job = gcp.bigquery.Job(
    "laura-test-job",
    job_id="laura-test-job-pytexas-%s" % gen,
    query=gcp.bigquery.JobQueryArgs(
        query=my_query,
        destination_table=gcp.bigquery.JobQueryDestinationTableArgs(
            project_id=foo.project,
            dataset_id=foo.dataset_id,
            table_id=foo.table_id
        ),
        allow_large_results=True,
        flatten_results=True,
        default_dataset=gcp.bigquery.JobQueryDefaultDatasetArgs(
            dataset_id="noaa_historic_severe_storms",
            project_id="bigquery-public-data"
        ),
        script_options=gcp.bigquery.JobQueryScriptOptionsArgs(
            key_result_statement="LAST"
        )
    ),
)
#
export = gcp.bigquery.Job(
    "laura-export-job",
    job_id="laura-export-job-pytexas-%s" % gen,
    extract=gcp.bigquery.JobExtractArgs(
        destination_uris=[storage.url.apply(lambda url: f"{url}/extract.csv")],
        source_table=gcp.bigquery.JobExtractSourceTableArgs(
            project_id=foo.project,
            dataset_id=foo.dataset_id,
            table_id=foo.table_id
        ),
        destination_format="CSV",
        compression="NONE"
    ),
    opts=pulumi.ResourceOptions(depends_on=[job])
)

function = gcp.cloudfunctions.Function(
    "laura-function",
    description="To analyze data for PyTexas",
    runtime="python39",
    region="us-central1",
    source_archive_bucket=bucket.name,
    source_archive_object=archive.name,
    trigger_http=True,
    entry_point="get_data",
    environment_variables={'DATA': storage.url.apply(lambda url: f"{url}/extract.csv")}
)
run_me = gcp.cloudfunctions.FunctionIamMember(
    "laura-runner",
    project=function.project,
    region=function.region,
    cloud_function=function.name,
    role="roles/cloudfunctions.invoker",
    member="allUsers"
)

pulumi.export("bucket-url", storage.url)
pulumi.export("function-url", function.https_trigger_url)
