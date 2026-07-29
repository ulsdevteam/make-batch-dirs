# Description:

This script is used to read a list of PIDs from a spreadsheet and a
passed in batch name, create the batch folder and corresponding PID
sub-folders in preparation for DRL to perform their scanning processes.

**Notes:**

- For local spreadsheet files (--xls-file), the script reads the first
  'Sheet' tab in the workbook (usually 'Sheet1'). This limitation does
  not apply when using Google Sheets, where the tab is set explicitly
  via --google-sheet-name.
- The 'id' column may be located anywhere in the sheet (lookup is by
  column name, not position).
- The column name used to identify the object id defaults to 'id' but
  can be overridden via --id-column or the id_column key in the config
  file.

## Spreadsheet requirements:

Spreadsheet Columns:

  |Required Columns    ||           
  |------------------- |---------------------------------------------------|
  |'id' (configurable) |This is the PID of the object. The column may be located anywhere in the sheet. The column name defaults to 'id' but can be changed via --id-column or the config file's id_column setting.|

  |Optional Columns    ||           
  |------------------- |---------------------------------------------------|
  |Any                 |Any additional columns as needed.|

## Script Parameters:

  |Parameter           |Description|
  |:--- |:--- |
  |\--config-file      |Path to the script config file containing the scanning directory (scanning_path), and if required the id_column.|
  |\--xls-file         |Path to the spreadsheet to be processed.|
  |\--batch-name       |The Name of the batch that will be created.|
  |\--log-file         |Path to the log file.|
  |\--use-google       |Set this to true if using Google Sheets.|
  |\--google-sheet-id  |The Google Sheet Identifier.|
  |\--google-sheet-name|The Google Sheet Tab Name. This defaults to 'Sheet1' if not included.|
  |\--google-creds-file|The file containing the Google credentials file.|
  |\--id-column        |Column name to use as the object id. Overrides the config file's id_column setting if both are provided. Defaults to 'id'.|

## Config File requirements:

The config file contains a single option "scanning_path" that points the script to where you would like to build the directory structure for the batch-name you are passing in to the script.  This is the top level folder usually where you would store all your batches.  In our example, we would set "scanning_path" to "/scanning" as in the following.

An optional "id_column" key can also be set in the config file to
specify the default column name used as the object id, if you don't
want to rely on the built-in default of 'id' or pass --id-column each
run.

```
scanning_path: /scanning
id_column: id
```

An example config file can be found in the make-batch-dirs.conf-sample file.


## Usage:

Script Usage Examples:
  |Type|Example|
  |:--- |:--- |
  |Spreadsheet|make-batch-dirs --config-file config.conf --xls-file input_spreadsheet.xls --log-file log.txt --batch-name MyNewBatch|
  |Google Sheet|make-batch-dirs --config-file config.conf --log-file log.txt --batch-name MyNewBatch --use-google {true\\|false} --google-sheet-id {sheet id} --google-sheet-name {E.g. 'Sheet1'} --google-creds-file {path to credentials file.} --id-column identifier|


## Function:

For each row in the spreadsheet, obtain the contents of the id column
(named 'id' by default, or the name given via --id-column / id_column)
and construct a new directory structure in the format of
{scanning_path}/{batch-name}/{id}.

E.g. Result: /scanning/MyNewBatch/317350000001,
/scanning/MyNewBatch/317350000002, /scanning/MyNewBatch/317350000003
