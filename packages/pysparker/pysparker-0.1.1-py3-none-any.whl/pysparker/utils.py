"""Utils functions for Hadoop.
"""
from __future__ import annotations
from typing import Optional, Union
import sys
from io import StringIO
import datetime
import smtplib
from email.mime.text import MIMEText
from loguru import logger
from pyspark.sql import SparkSession, DataFrame, Window
import pyspark.sql.functions as sf
import datacompy


def sample(
    frame: DataFrame,
    ratio: Union[float, int],
    total: Union[int, None] = None,
    persist: bool = False
) -> DataFrame:
    """Sample rows from a PySpark DataFrame.
    :param frame: The PySpark DataFrame from which to sample rows.
    :param ratio: The acceptance ratio or the number of rows to sample.
    :param total: The total number of rows in the DataFrame.
    :param persist: Whether to persist the table when it is needed multiple times.
        False by default.
    :return: A PySpark DataFrame containing sampled rows.
    """
    if isinstance(ratio, int):
        if total is None:
            if persist:
                frame.persist()
            total = frame.count()
        if total == 0:
            return frame
        ratio /= total
    if ratio >= 1:
        return frame
    return frame.sample(ratio)


def calc_global_rank(frame: DataFrame, order_by: Union[str, list[str]]) -> DataFrame:
    """Calculate global ranks.
    This function uses a smart algorithm to avoding shuffling all rows
    to a single node which causes OOM.
    :param frame: A PySpark DataFrame.
    :param order_by: The columns to sort the DataFrame by.
    :return: A DataFrame with new columns
        ("part_id", "local_rank", "cum_rank", "sum_factor" and "rank") added.
    """
    if isinstance(order_by, str):
        order_by = [order_by]
    # calculate local rank
    wspec1 = Window.partitionBy("part_id").orderBy(*order_by)
    frame_local_rank = frame.orderBy(order_by).withColumn(
        "part_id", sf.spark_partition_id()
    ).withColumn("local_rank",
                 sf.rank().over(wspec1)).persist()
    # calculate accumulative rank
    wspec2 = Window.orderBy("part_id").rowsBetween(
        Window.unboundedPreceding, Window.currentRow
    )
    stat = frame_local_rank.groupBy("part_id").agg(
        sf.max("local_rank").alias("max_rank")
    ).withColumn("cum_rank",
                 sf.sum("max_rank").over(wspec2))
    # self join and shift 1 row to get sum factor
    stat2 = stat.alias("l").join(
        stat.alias("r"),
        sf.col("l.part_id") == sf.col("r.part_id") + 1, "left_outer"
    ).select(
        sf.col("l.part_id"),
        sf.coalesce(sf.col("r.cum_rank"), sf.lit(0)).alias("sum_factor")
    )
    return frame_local_rank.join(
        #broadcast(stat2),
        stat2,
        ["part_id"],
    ).withColumn("rank",
                 sf.col("local_rank") + sf.col("sum_factor"))


def repart_hdfs(
    spark,
    src_path: str,
    dst_path: str = "",
    num_parts: Optional[int] = None,
    mb_per_part: float = 64,
    min_num_parts: int = 1,
    coalesce: bool = False
) -> None:
    """Repartition a HDFS path of the Parquet format.
    :param spark: A SparkSession object.
    :param path: The HDFS path to repartition.
    :param num_parts: The new number of partitions.
    :param coalesce: If True, use coalesce instead of repartition.
    """
    spc = spark.sparkContext
    hdfs = spc._jvm.org.apache.hadoop.fs.FileSystem.get(spc._jsc.hadoopConfiguration())  # pylint: disable=W0212
    src_path = src_path.rstrip("/")
    src_path_hdfs = spc._jvm.org.apache.hadoop.fs.Path(src_path)  # pylint: disable=W0212
    # num of partitions
    if num_parts is None:
        bytes_path = hdfs.getContentSummary(src_path_hdfs).getLength()
        num_parts = round(bytes_path / 1_048_576 / mb_per_part)
    num_parts = max(num_parts, min_num_parts)
    # temp path for repartitioned table
    if dst_path == src_path:
        dst_path = ""
    if dst_path:
        path_tmp = dst_path
    else:
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        path_tmp = src_path + f"_repart_tmp_{ts}"
    # repartition
    if coalesce:
        spark.read.parquet(src_path).coalesce(num_parts) \
            .write.mode("overwrite").parquet(path_tmp)
    else:
        spark.read.parquet(src_path).repartition(num_parts) \
            .write.mode("overwrite").parquet(path_tmp)
    # path_tmp --> src_path
    if dst_path:
        return
    if hdfs.delete(src_path_hdfs, True):
        if not hdfs.rename(
            spc._jvm.org.apache.hadoop.fs.Path(path_tmp),  # pylint: disable=W0212
            src_path_hdfs,  # pylint: disable=W0212
        ):
            sys.exit(f"Failed to rename the HDFS path {path_tmp} to {src_path}!")
    else:
        sys.exit(f"Failed to remove the (old) HDFS path: {src_path}!")


def send_email(
    server: str,
    sender: str,
    recipient: Union[str, list[str]],
    subject: str,
    body: str,
) -> bool:
    """Send email using a authentication free SMTP server.

    :param server: A SMTP server which does not require authentication.
    :param sender: The email address of the sender.
    :param recipient: A (list of) email addresses to send the email to.
    :param subject: The subject of the email.
    :param body: The body of the email.
    :return: True if the email is sent successfully, and False otherwise.
    """
    mail = MIMEText(body, "plain", "utf-8")
    mail["Subject"] = subject
    if isinstance(recipient, list):
        recipient = ";".join(recipient)
    mail["To"] = recipient
    mail["From"] = sender
    smtp = smtplib.SMTP()
    try:
        smtp.connect(server)
        smtp.send_message(mail)
        smtp.close()
        logger.info("The following message is sent: {}", mail.as_string())
        return True
    except:
        logger.info(
            "The following message is constructed but failed to sent: {}",
            mail.as_string()
        )
        return False


def compare_dataframes(
    spark: SparkSession, df1: DataFrame, df2: DataFrame,
    join_columns: Union[str, list[str]], email: Optional[dict[str, str]]
):
    """Compare two Spark DataFrames for differences.

    :param spark: A SparkSession object.
    :param df1: A Spark DataFrame to compare.
    :param df2: Another Spark DataFrame to comapre.
    :param join_columns: A (list of) column(s) for joining the 2 DataFrames.
    :param email: An optional dictionary object containing information for sending emails.
        The dictionary should contain all parameters of the send_email function.
    """
    if isinstance(join_columns, str):
        join_columns = [join_columns]
    comparison = datacompy.SparkCompare(
        spark,
        df1,
        df2,
        join_columns=join_columns,
        cache_intermediates=True,
        match_rates=True
    )
    with StringIO() as sio:
        comparison.report(file=sio)
        report = sio.getvalue()
    logger.info("\n" + report)
    send_email(
        server=email["server"],
        sender=email["sender"],
        recipient=email["recipient"],
        subject="DataFrame Comparison Report",
        body=report,
    )
