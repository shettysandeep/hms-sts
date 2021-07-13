# HMS-STS Audit Work
## Preprocessing of OR log files received from the  sites participating in this audit. 

Most participating sites submitted their OR log data (for the requested date
range) in Excel format. Few sites submitted PDFs of hand-written documents (to
be processed separately). The excel files were cleaned and combined to produce a
final dataset with only variables necessary for the audit {record
id, surgery date, admission date, discharge date, procedure}

`or_parsing_data.py` parses each sheet in an Excel workbook
(ignores hidden sheets) and generates a dataframe at the site-level, which is
subsequently combined to form a **pooled dataset** that includes all sites that
submitted OR data. Since the OR logs had more information than requested, this
script whittles the list of variables by loosely searching for key texts, such as
record, id, procedure, etc. in the columns.

`Rename_columns_file.csv` is a spreadsheet containing two key columns. The first
contains variable names from the *pooled dataset* obtained in the script above.
The second column serves two purposes. By containing new column names for
variables containing similar information but differ in names in the original
submission (age vs patient age), it sets the stage for combining these variables
in the dataset, and helps retain only relevant colums by means of having no
value for columns that are irrelevant for the final dataset. That is, any
variable name without an entry for a new name will get dropped from the dataset.
This spreadsheet was constructed by taking the columns from the *pooled
dataset*, then reviewing manually to select the necessary columns and assigning
new names.

`or_gen_data.py` operates on the *pooled dataset* obtained in
*or_parsing_data.py*. Uses information from *Rename_columns_file.csv*, to drop
irrelevant variables, combines variables under the new names, and generates a
final dataset.



