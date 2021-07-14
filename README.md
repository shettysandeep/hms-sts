# HMS-STS Audit Work
## Preprocessing of OR log files received from sites participating in the audit. 

Most participating sites submitted their OR log data (for the requested date
range) in Excel format. Few sites submitted scanned PDFs of handwritten documents (to
be processed separately). The excel files were cleaned and combined to produce a
final dataset with variables necessary for the audit {record
id, surgery date, admission date, discharge date, procedure}

`or_parsing_data.py` parses each sheet in an Excel workbook (ignores hidden
sheets) and generates a dataframe at the site-level, which is subsequently
combined to form a **pooled dataset** that includes all sites that submitted OR
data. Since the OR logs had more information than requested, this script
whittles the list of variables by loosely searching for key texts, such as
record, id, procedure, etc. in the columns.

`Rename_columns_file.csv` is a spreadsheet containing two columns. The first
contains variable names from the *pooled dataset* obtained via the above script.
The second column defines a new name for the variables with two objectives. A
singular new column names for variables containing similar information but
differ in names in the original submissions (such as, age vs patient age).
However, not all variables are assigned a new name. New name assigned only to
variables that are of interest for the auditing exercise. Thus, the absence of a
value in the new name column is used as a condition to remove variables that are
not needed. This spreadsheet was constructed manually by taking the columns from
the *pooled dataset*, then reviewing to select the necessary columns and
the assignment of new names.

`or_gen_data.py` operates on the *pooled dataset* obtained in
*or_parsing_data.py*. Uses information from *Rename_columns_file.csv*, to drop
irrelevant variables, combines variables under the new names, and generates a
final dataset.



