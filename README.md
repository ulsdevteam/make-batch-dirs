# Description:

This script is used to read a list of PIDs from a spreadsheet and a
passed in batch name, create the batch folder and corresponding PID
sub-folders in preparation for DRL to perform their scanning processes.

**Notes:**

- The script needs to be converted to use Google Sheets instead of a
  spreadsheet.

- The script needs to be adjusted to look instead of the first column to
  look for the column named 'id' to allow the column to be located
  anywhere in the google sheet.

- The script assumes that it should work with the first 'Sheet' tab in
  the file -- usually 'Sheet1'.

## Spreadsheet requirements:

Spreadsheet Columns:

  |Required Columns    ||           
  |------------------- |---------------------------------------------------|
  |'id'                |This is the PID of the object. Must currently be the first column of the sheet.|

  |Optional Columns    ||           
  |------------------- |---------------------------------------------------|
  |Any                 |Any additional columns as needed.|

## Script Parameters:

  |Parameter           |Description|
  |:--- |:--- |
  |\--config-file      |Path to the script config file containing paths to the workbench directory (workbench_path), the scanning directory (scanning_path), and the path to the python executable.|
  |\--xls-file         |Path to the spreadsheet to be processed.|
  |\--batch-name       |The Name of the batch that will be created.|
  |\--log-file         |Path to the log file.|
  |\--use-google       |Set this to true if using Google Sheets.|
  |\--google-sheet-id  |The Google Sheet Identifier.|
  |\--google-sheet-name|The Google Sheet Tab Name.|
  |\--google-creds-file|The file containing the Google credentials file.|

## Config File requirements:

The config file contains a single option "scanning_path" that points the script to where you would like to build the directory structure for the batch-name you are passing in to the script.  This is the top level folder usually where you would store all your batches.  In our example, we would set "scanning_path" to "/scanning" as in the following.

```
scaning_path: /scanning
```

An example config file can be found in the make-batch-dirs.conf-sample file.


## Usage:

Script Usage Examples:
  |Type|Example|
  |:--- |:--- |
  |Spreadsheet|make-batch-dirs --config_file config.conf --xls-file input_spreadsheet.xls --log-file log.txt --batch-name MyNewBatch|
  |Google Sheet|make-batch-dirs --config_file config.conf --log-file log.txt --batch-name MyNewBatch --use_google {true\\|false} --google-sheet-id {sheet id} --google-sheet-name {E.g. 'Sheet1'} --google-creds-file {path to credentials file.}|


## Function:

For each row in the spreadsheet, obtain the 'id' column contents and construct a new directory structure in the format of {scanning_path}/{batch-name}/{id}.

E.g. Result: /scanning/MyNewBatch/317350000001,
/scanning/MyNewBatch/317350000002, /scanning/MyNewBatch/317350000003
