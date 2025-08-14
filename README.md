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

  -----------------------------------------------------------------------
  **Required          
  Columns**           
  ------------------- ---------------------------------------------------
  'id'                This is the PID of the object. Must currently be
                      the first column of the sheet.

  **Optional          
  Columns**           

  Any                 Any additional columns as needed.
  -----------------------------------------------------------------------

Script Parameters:

  -----------------------------------------------------------------------
  Parameter           Description
  ------------------- ---------------------------------------------------
  \--config_file      Path to the script config file containing paths to
                      the workbench directory (workbench_path), the
                      scanning directory (scanning_path), and the path to
                      the python executable.

  \--xls-file         Path to the spreadsheet to be processed.

  \--batch-name       The Name of the batch that will be created.
  -----------------------------------------------------------------------

## Usage:

Script Usage Example:

make-batch-dirs ---config_file config.conf ---xls-file
input_spreadsheet.xls ---batch-name MyNewBatch

## Function:

For each row in the spreadsheet, obtain the first column contents which
should be the 'id' column and construct a new directory structure in the
format of {scanning_path}/{batch-name}/{id}.

E.g. Result: /scanning/MyNewBatch/317350000001,
/scanning/MyNewBatch/317350000002, /scanning/MyNewBatch/317350000003
