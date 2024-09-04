# Data Lake Error-Generator

table retrieval module: https://github.com/LUH-DBS/Data-Lake-Error-Generator/tree/main/data-retrieval
functional dependency discovery and error generation modules: https://github.com/LUH-DBS/Data-Lake-Error-Generator/blob/main/src/make_all_dirty.py


This repository contains a system that automatically configures Bart to introduce errors into a data lake of csv files.

The system introduces errors based upon functional dependencies, random typos and numerical outliers. In each column it
can generate either errors base upon functional dependencies and random typos or functional dependencies and 
numerical outliers or only one of the possible error types. Which error type is used for a column is decided by 
inferring the data type. 

The functional dependencies that are used to generate errors are determined with the data
profiling algorithm [HyFD](https://dl.acm.org/doi/10.1145/2882903.2915203).

## Requirements
The system runs under Python 3.10 and Java 20. A PostgreSQL 11 (or older) database server is required.

The environment can be set up like this:
- ```shell
  conda env create -f environment.yml
  conda activate Data-Lake-Error-Generator

Bart uses the build tool ant. It should be installed with the conda environment. If not, then it needs be installed manually.

The database server should contain a database specifically for this system.
PostgreSQL can be installed as a system by downloading it from their website and following their instructions or
it can be installed with conda by executing:

- ```shell
  conda install -c anaconda postgresql=11
- Setup a user and configure PostgreSQL as you want
- Then create the database and start the server:
   ```shell
   initdb -D bartdb
   pg_ctl -D bartdb -l logfile start

## Usage
1. Configure the database in file ``src/bart_sample_config.xml``.
   - Make sure to only change the values for the paths given here.
   - ``task.target.uri``: insert the uri to the database that has been created for this system
   (``jdbc:postgresql://$adress:$port/$databasename``) 
   - ``task.target.login``: A username for the database server
   - ``task.target.password``: The password associated with the given username

2. Configure the ``src/hydra_configs/base.yaml`` configuration file:
   - ``input.input_data_lake_path``: Path for a folder which contains several csv that should be dirtied
   - ``input.output_data_lake_path``: Path for a folder (does not need to exist beforehand), where a clean version, 
   a dirtied version, and the changes done are stored after the process has dirtied a file
   - ``input.bart_engine_path``: Path for the ``Bart_Engine`` folder of [Bart](https://github.com/dbunibas/BART) (by default set to submodule folder)
   - ``error-generation.with_fds``: A toggle to determine if errors based upon functional dependencies should be generated
   - ``error-generation.with_outliers``: A toggle to determine if errors based upon numerical outliers should be generated
   - ``error-generation.with_random_typos``: A toggle to determine if random typos should be generated
   - ``error-generation.lower_bound_error_percentage``: Sets the lower bound for the error-rate of one file (inclusive)
   - ``error-generation.upper_bound_error_percentage``: Sets the upper bound for the error-rate of one file (inclusive)

3. Run the file ``python src/make_all_dirty.py``
   - The working directory should be ``*/Data-Lake-error-Generator``

## Notes
The csv files in the input data lake are not allowed to contain PostgreSQL keywords as headers.

It is better to have a higher error percentage bound than the desired one, as sometimes Bart decides to not generate
errors for a given error type and column to ensure detectability. This means that the error percentage of the lake will
never go over the upper bound, but can slightly go under the lower bound.

The config file is configured for the example lake and needs to be adapted for any other lake that require error 
insertion
