# FASTAparser
Simple Python parser for FASTA data files.

## Usage
Check your Python 3 path and possibly alter the first line in `parseFASTA.py`.

Then run `./parseFASTA.py firstInput.fa secondInput.fa ... lastInput.fa`.

## Options
You can (aggregate from multiple files and) save the sequences to an output file with the optional argument `--output`, e.g.:

    ./parseFASTA.py firstInput.fa secondInput.fa --output out.fa
    
You can limit the length of each sequence line by also specifying the `--wrap` argument (default is 80), e.g.:

    ./parseFASTA.py firstInput.fa secondInput.fa --output out.fa --wrap 90
