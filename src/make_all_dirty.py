import logging
import math
import shutil
import time
from pathlib import Path

import hydra
from lxml import etree

import pandas as pd
import sqlalchemy
from sqlalchemy import Float, Column, Integer, Text, Identity, MetaData, Table, BigInteger
from sqlalchemy.sql import text
from preprocessing.file_preprocessing import preprocess_headers, read_original_file, save_csv
from configs.metanome_file_input import run_metanome, run_metanome_with_cli
from configs import create_bart_config
import numpy as np
import os
import subprocess
import random
import pickle

log = logging.getLogger(__name__)


def get_files_by_file_size(dirname, reverse=False):
    """ Return list of file paths in directory sorted by file size """

    # Get list of files
    filepaths = []
    for basename in os.listdir(dirname):
        filename = os.path.join(dirname, basename)
        if os.path.isfile(filename):
            filepaths.append(filename)

    # Re-populate list with filename, size tuples
    for i in range(len(filepaths)):
        filepaths[i] = (filepaths[i], os.path.getsize(filepaths[i]))

    # Sort list by file size
    # If reverse=True sort from largest to smallest
    # If reverse=False sort from smallest to largest
    filepaths.sort(key=lambda filename: filename[1], reverse=reverse)

    filenames = []
    # Re-populate list with just filenames
    for i in range(len(filepaths)):
        filenames.append(os.path.basename(filepaths[i][0]))

    return filenames


def find_det_dep(fd):
    determinant = fd['result']['determinant']['columnIdentifiers']
    dependant = fd['result']['dependant']['columnIdentifier']
    print()
    return determinant, dependant


def find_det_dep_cli(fd):
    determinant = fd['determinant']['columnIdentifiers']
    dependant = fd['dependant']['columnIdentifier']
    return determinant, dependant


def get_fd_list(fd_results):
    fd_list = []
    for fd in fd_results:
        determinant, dependant = find_det_dep_cli(fd)
        if len(determinant) == 1 and determinant != dependant \
                and determinant != None and dependant != None \
                and (dependant, determinant) not in fd_list:
            fd_list.append((determinant[0]['columnIdentifier'], dependant))
    return fd_list


def get_percentages(fd_list, error_percentage, outlier_error_cols, typo_cols):
    vio_gen_percentage, outlier_errors_percentage, typo_percentage = 0, 0, 0
    if len(fd_list) > 0:
        vio_gen_percentage = math.floor(error_percentage)
        if len(outlier_error_cols) > 0:
            vio_gen_percentage = math.floor(error_percentage / 2)
            outlier_errors_percentage = math.floor(error_percentage / 2)
            if len(typo_cols) > 0:
                # FD, OE, SE
                typo_percentage = math.floor(error_percentage / 2)
            else:
                # FD, OE
                outlier_errors_percentage = math.floor(error_percentage / 2)
        else:
            if len(typo_cols) > 0:
                # FD, SE
                vio_gen_percentage = math.floor(error_percentage / 2)
                typo_percentage = math.floor(error_percentage / 2)
            else:
                # FD
                pass

    else:
        if len(outlier_error_cols) > 0:
            outlier_errors_percentage = math.floor(error_percentage)
            if len(typo_cols) > 0:
                # OE, SE
                typo_percentage = math.floor(error_percentage)
            else:
                # OE
                outlier_errors_percentage = math.floor(error_percentage)
        else:
            # SE
            typo_percentage = error_percentage
    return vio_gen_percentage, outlier_errors_percentage, typo_percentage


def set_fd_ratio(fd_list, vio_gen_percentage, num_table_records, row_size):
    num_fd_violations = num_table_records * (vio_gen_percentage / 100)
    if num_fd_violations / 2 < 1:
        return dict()

    fd_ratio_dict = dict()
    assinged_fds = 0
    i = 0

    while assinged_fds < num_fd_violations:
        if fd_list[i] in fd_ratio_dict:
            fd_ratio_dict[fd_list[i]] += (2 / row_size) * 100
        else:
            fd_ratio_dict[fd_list[i]] = (2 / row_size) * 100
        assinged_fds += 1
        i += 1
        if i >= len(fd_list):
            i = 0
    return fd_ratio_dict


def get_database():
    parser = etree.XMLParser(strip_cdata=False)
    root_tree = etree.parse('src/bart_sample_config.xml', parser=parser)
    username = root_tree.xpath("//target/access-configuration/login")[0].text
    password = root_tree.xpath("//target/access-configuration/password")[0].text
    address = root_tree.xpath("//target/access-configuration/uri")[0].text
    address = address.split("//")[1]

    return sqlalchemy.create_engine(f"postgresql+psycopg2://{username}:{password}@{address}", echo=True)


def prepare_database(dataframe: pd.DataFrame, file_path: str):
    type_mapping = {'float64': Float, 'int64': BigInteger, 'object': Text}
    columns = [Column('oid', Integer, Identity(start=1))]
    for column, dtype in zip(dataframe.columns.tolist(), dataframe.dtypes.tolist()):
        columns.append(Column(column, type_mapping[str(dtype)]))

    metadata = MetaData()
    table = Table('clean', metadata, *columns, schema="target")

    database_con = get_database()
    with database_con.connect() as con:
        con.execute(text('CREATE SCHEMA IF NOT EXISTS target'))
        con.commit()
    table.drop(database_con, checkfirst=True)
    table.create(database_con)
    dataframe.to_sql("clean", database_con, schema='target', index=False, if_exists="append")


def make_it_dirty(cfg, error_percentage, file_path, output_dir):
    df = pd.read_csv(file_path)
    df_without_null = df.dropna(axis=1)

    log.info("Preparing FDs")
    if cfg["error-generation"]["with_fds"]:

        fd_results = run_metanome_with_cli(file_path)
        fd_list = get_fd_list(fd_results)

        log.info("Prepared FDs")
    else:
        log.info("Skipping FDs")
        fd_list = []

    outlier_error_cols = df_without_null.select_dtypes(include=[np.number]).columns.to_list()
    typo_cols = df.select_dtypes(include=['object']).columns.to_list()

    if not cfg["error-generation"]["with_outliers"]:
        outlier_error_cols = []

    if not cfg["error-generation"]["with_random_typos"]:
        typo_cols = []

    vio_gen_percentage, outlier_errors_percentage, typo_percentage = get_percentages(fd_list, error_percentage,
                                                                                     outlier_error_cols, typo_cols)

    log.info(
        f"Full Percentage: {error_percentage} -> fds: {vio_gen_percentage}, "
        f"outlier: {outlier_errors_percentage}, random typos: {typo_percentage}"
    )

    fd_ratio_dict = set_fd_ratio(fd_list, vio_gen_percentage, df.size, df.shape[0])
    config_file_path = create_bart_config.create_config_file(file_path, list(df.columns.values), outlier_error_cols,
                                                             outlier_errors_percentage, typo_cols, typo_percentage,
                                                             fd_ratio_dict, output_dir)
    log.debug(f"Using bart conf at {config_file_path}")
    # Prepare database here
    prepare_database(df, file_path)
    log.info("Start Bart")
    val = subprocess.check_call(["./run.sh", config_file_path],
                                shell=False, timeout=3600, cwd=Path(cfg["input"]["bart_engine_path"]).resolve())


def get_all_files(directory: Path):
    if not directory.is_dir():
        raise ValueError("Input is no Directory")

    files = []
    for child in directory.iterdir():
        if child.is_file():
            files.append(child)
        elif child.is_dir():
            files.extend(get_all_files(child))

    return files


@hydra.main(version_base=None, config_path="hydra_configs", config_name="base")
def main(cfg):
    files = get_all_files(Path(cfg["input"]["input_data_lake_path"]))
    log.debug(files)
    reserved_words = open("src/preprocessing/reserved_words.txt", "r").read().split(",")
    files_errors = dict()
    count = 0
    time_0 = time.time()
    for file in files:
        try:
            path_postfix = os.path.relpath(file, Path(cfg["input"]["input_data_lake_path"]))
            file_name = Path(Path(cfg["input"]["output_data_lake_path"]), path_postfix).name
            processed_file_path = Path(Path(cfg["input"]["output_data_lake_path"]), path_postfix).resolve()
            if not os.path.exists(processed_file_path):
                os.makedirs(processed_file_path)
            if not os.path.exists(os.path.join(processed_file_path, "dirty_clean.csv")):
                log.info(file_name + " is being processed.")
                df = read_original_file(file)
                df = preprocess_headers(df, reserved_words)
                # Calculate the mode of each column
                modes = df.mode().iloc[0]
                # Fill missing values with the corresponding column mode
                df = df.fillna(modes)
                df_name = save_csv(df, processed_file_path, file)
                error_precentage = random.randint(cfg["error-generation"]["lower_bound_error_percentage"],
                                                  cfg["error-generation"]["upper_bound_error_percentage"])
                # error_precentage = 25
                files_errors[file_name] = error_precentage
                make_it_dirty(cfg, error_precentage, os.path.join(processed_file_path, df_name), processed_file_path)
                count += 1
                log.info(file_name + " is done.")
                if count % 10 == 0:
                    log.info(f'''{count} files processed.''')
                    with open('files_error_percentages.pickle', 'wb') as handle:
                        pickle.dump(files_errors, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            log.error(e)

    time_1 = time.time()
    log.info("********time*******:{} seconds".format(time_1 - time_0))


if __name__ == '__main__':
    main()
