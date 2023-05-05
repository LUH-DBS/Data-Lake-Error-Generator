# Data-Lake-Error-Generator
Generating errors in data lakes.

# Requirements
This system needs a PostgreSQL 11 database or older in order to work.

The csv files are not allowed to contain PostgreSQL keywords as headers

# Usage
First set the database config in the file ```src/bart_sample_config.xml```.
Next, set inside the python file ```src/make_all_dirty.py``` the parameters ```input_dir```, ```output_dir``` and 
```bart_engine_path```:
- ```input_dir```: Path for a folder which contains several csv that should be dirtied
- ```output_dir```: Path for a folder (does not need to exist beforehand), where a clean version, 
a dirtied version, and the changes done are stored after the process has dirtied a file
- ```bart_engine_path```: Path for the ```Bart_Engine``` folder of your compiled version of 
[Bart](https://github.com/dbunibas/BART)

Then run the file ```src/make_all_dirty.py```