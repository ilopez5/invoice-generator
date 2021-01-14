[![Generic badge](https://img.shields.io/badge/Stage-v2.0-blue.svg)](#)

# Invoice Generator

## For ZipBooks Users
This is a quick way to generate an invoice using ZipBooks API. It of course
requires usage of ZipBooks for logging hours, and depends `pdflatex` as well
as my Python progress bar [spout](https://github.com/ilopez5/spout). The
invoice template included is can be 
[found here](https://github.com/ilopez5/latex/tree/master/invoice) (with
appropriate credit given).

## Usage:
Put your ZipBooks credentials in a file of your choice and specify a directory
in which you intend on storing your invoices. This is necessary so that the
script can count how many invoices exist and determine the new invoice number.
Additionally, modify `invoice.tex` to have your payer and payee information.

### Credentials File Syntax
Like most `.env` files, syntax looks like so:
```
ZIP_EMAIL=<zipbooks-email>
ZIP_PASSWORD=<zipbooks-password>
```
The name of the variable is not important, as only the right side of the
'=' sign is parsed.

### Example
```bash
python3 invoice.py <filename>.env <archive-directory>
```

[![asciicast](https://asciinema.org/a/jaa3ajUSRsDFECMsBVP2V4qgI.svg)](https://asciinema.org/a/jaa3ajUSRsDFECMsBVP2V4qgI)
