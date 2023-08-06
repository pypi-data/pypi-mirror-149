from teradataml import DataFrame, get_connection
from typing import List

import json
import sys


def save_evaluation_metrics(partition_df: DataFrame, metrics: List):
    """
    :param partition_df: teradata dataframe containing at least ["partition_id", "partition_metadata", "num_rows"]
    :param metrics: list of metrics to normalize and report
    :return: None
    """
    total_rows = int(partition_df.select(["num_rows"]).sum().to_pandas().iloc[0])

    metrics_sql = [f"SUM(CAST(partition_metadata AS JSON).JSONExtractValue('$.metrics.{metric}') * num_rows/{total_rows}) AS {metric}" for metric in metrics]
    joined_metrics_sql = ','.join(metrics_sql)
    metrics = DataFrame.from_query(f"SELECT {joined_metrics_sql} FROM {partition_df._table_name}").to_pandas()

    metrics = {metric: "{:.2f}".format(metrics.iloc[0][metric]) for metric in metrics}

    with open("artifacts/output/metrics.json", 'w+') as f:
        json.dump(metrics, f, indent=2)


def save_metadata(partition_df: DataFrame):
    """
    create statistic summaries based on the provided dataframe produced via training or evaluation

    partitions.json is {
        "<partition1 key>": <partition1_metadata>,
        "<partition2 key>": <partition2_metadata>,
        ...
    }

    data_stats.json is {
        "num_rows": <num_rows>,
        "num_partitions": <num_partitions>
    }

    :param partition_df: teradata dataframe containing at least ["partition_id", "partition_metadata", "num_rows"]
    :return: None
    """

    total_rows = int(partition_df.select(["num_rows"]).sum().to_pandas().iloc[0])

    metadata_df = partition_df.select(["partition_id", "partition_metadata", "num_rows"]).to_pandas()

    metadata_dict = {r["partition_id"]: json.loads(r["partition_metadata"])
                     for r in metadata_df.to_dict(orient='records')}

    with open("artifacts/output/partitions.json", 'w+') as f:
        json.dump(metadata_dict, f, indent=2)

    data_metadata = {
        "num_rows": total_rows,
        "num_partitions": int(metadata_df.shape[0])
    }

    with open("artifacts/output/data_stats.json", 'w+') as f:
        json.dump(data_metadata, f, indent=2)


def cleanup_cli(model_version: str, models_table: str = "aoa_sto_models"):
    """
    cli uses model version of "cli" always. We need to cleanup models table between runs.
    A better solution would be for the cli to write to a different table completely and just "recreate" on each run

    :param model_version: the model version being executed
    :param models_table: the models table for cleanup (default is aoa_sto_models)
    :return: None
    """
    if model_version == "cli":
        get_connection().execute("DELETE FROM {table} WHERE model_version='cli'".format(table = models_table))


def check_sto_version():
    """
    Check Python version In-Vantage against the version where this function is running,
    if it's incompatible raise an exception

    :return: None
    """
    version_query = """
    SEL DISTINCT ver
    FROM SCRIPT(
        SCRIPT_COMMAND('python3 -c "import sys; print(\\".\\".join(map(str, sys.version_info[0:2])))"')
        RETURNS('ver VARCHAR(10)') 
    );
    """
    local_version = '.'.join(map(str, sys.version_info[0:2]))
    result = get_connection().execute(version_query)
    if result.rowcount != 1:
        raise Exception('Different STO configuration on different nodes, please contact your system administrator')
    remote_version = next(iter(result))[0]
    if local_version != remote_version:
        raise Exception('Python versions not matching, local: {local}, In-Vantage: {remote}'.format(local = local_version, remote = remote_version))


def collect_sto_versions(raise_diff_config_exception=True):
    """
    Collects Python and packages information from In-Vantage installation

    :param raise_diff_config_exception: whether raise an exception if different Python versions are detected on different AMPs of Vantage system
    :return: Dict with python_version and packages versions
    """
    python_version_query = """
    SEL DISTINCT ver
    FROM SCRIPT(
        SCRIPT_COMMAND('python3 -c "import sys; print(sys.version.replace(\\"\\n\\",\\" \\"))"')
        RETURNS('ver VARCHAR(100)') 
    );
    """
    result = get_connection().execute(python_version_query)
    if result.rowcount != 1 and raise_diff_config_exception:
        raise Exception('Different STO configuration on different nodes, please contact your system administrator')
    python_version = next(iter(result))[0]

    packages_version_query = """
    SEL DISTINCT pkg
    FROM SCRIPT(
        SCRIPT_COMMAND('python3 -c "import pkg_resources; [print(pkg) for pkg in pkg_resources.working_set]"')
        RETURNS('pkg VARCHAR(100)') 
    );
    """
    result = get_connection().execute(packages_version_query)
    packages = {}
    for row in result:
        pair = row[0].split(" ")
        packages[pair[0]] = pair[1]

    return {'python_version' : python_version, 'packages' : packages}


def get_joined_models_df(data_table: str,
                         model_artefacts_table: str,
                         model_version: str,
                         partition_id: str = "partition_id"):
    """
    Joins the dataset which is to be used for scoring/evaluation with the model artefacts and appends the model_artefact
    to the first row with the column name 'model_artefact'.

    Args:
        data_table: the table/view of the dataset to join
        model_artefacts_table: the model artefacts table where the model artefacts are stored
        model_version: the model version to use from the model artefacts
        partition_id: the dataset partition_id

    Returns:
        DataFrame
    """
    query = f"""
    SELECT d.*, CASE WHEN n_row=1 THEN m.model_artefact ELSE null END AS model_artefact 
        FROM (SELECT x.*, ROW_NUMBER() OVER (PARTITION BY x.{partition_id} ORDER BY x.{partition_id}) AS n_row FROM {data_table} x) AS d
        LEFT JOIN {model_artefacts_table} m
        ON d.{partition_id} = m.partition_id
        WHERE m.model_version = '{model_version}'
    """

    return DataFrame(query=query)
