# Data-Lake-Error-Generator
This repository contains a system that automatically configures Bart to introduce errors into a data lake of csv files.

# Requirements
The system runs under Python 3.10 and Java 20. A PostgreSQL 11 database server is required. All required packages can be
found in the file ````environment.yml````. Using Anaconda the file can be directly turned into a conda environment.

# Usage
1.  set the database config in the file ```src/bart_sample_config.xml```.
    - Make sure you have created bartdb and target schema. 
2. Configure the ```base.yaml``` configuration file:
   - ```input_dir```: Path for a folder which contains several csv that should be dirtied
   - ```output_dir```: Path for a folder (does not need to exist beforehand), where a clean version, 
   a dirtied version, and the changes done are stored after the process has dirtied a file
   - ```bart_engine_path```: Path for the ```Bart_Engine``` folder of [Bart](https://github.com/dbunibas/BART)

3. Run the file ```src/make_all_dirty.py```

# Notes

The csv files in the input data lake are not allowed to contain PostgreSQL keywords as headers.