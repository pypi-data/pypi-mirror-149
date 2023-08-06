# Release notes
# 4.0.0
- GBprocesS is now licensed GPLv3.
- Support python 3.10 ([#25](https://gitlab.com/dschaumont/GBprocesS/-/issues/25))

# 3.1.1
- Bumped cutadapt version to 3.1.1 ([#24](https://gitlab.com/dschaumont/GBprocesS/-/issues/24))

# 3.1.0
- Trim barcode and cutsite remnant irrespective of the sequences when not using a spacer sequence ([#22](https://gitlab.com/dschaumont/GBprocesS/-/issues/22)).
- The version of the Cutadapt depedency is now pinned ([#23](https://gitlab.com/dschaumont/GBprocesS/-/issues/22)). 

# 3.0.2
- Added the current data and time to the statistics .csv file name ([#18](https://gitlab.com/dschaumont/GBprocesS/-/issues/18))
- Fixed an issue where the minimum read length would not be applied when trimming sequences ([#17](https://gitlab.com/dschaumont/GBprocesS/-/issues/17))

# 3.0.1
- Publish GBprosesS on pypi ([#15](https://gitlab.com/dschaumont/GBprocesS/-/issues/15))

# 3.0.0
- Fixed an issue where operations could not be configured correctly when using single-end data.
- Auxiliary files now also get merged after splitting for multiprocessing.
- Moved PatternTrimmer and PositionalTrimmer into a new operation CutadaptTrimmer that does both.
- Added the trimming of adapter spacers (LGC data).
- Fix running GBprocesS when cpu=1
- Allow the usage of .fasta files to specify per-sample restriction enzyme remnants

# 2.3.1
- Fix an issue where dots are used in file names outide the file name extension.

# 2.3.0
- Fix error message when two different run or sample names are used for the same sample.
- Fix an issue where an operation would only be executed if duplicates were configured.
Duplicate headers in the .ini file are no longer allowed. If an operation needs to be executed more than once in a pipeline,
the header in the ini file can be made unique by seperating the operation name with dot (.) from a unique string of choice.

# 2.2.0
- Removed unused FastpMerger and FastqJoinMerger.
- The definition of restriction site remnants is now consistent.
- Adapter sequences are actually the illumina sequencing primers, this was semantically changed.
- Primer sequences (formerly adapter sequences) can be defined using 'Nextera' and 'TruSeq' keywords, as well as the actual sequences.
- Multiprocessing for compressing and decompressing files.
- Compression is now performed in the background, while continuing with the next operation.
- Output basic statistics on the number of sequences after each operation.

# 2.1.1
- Remove deprecated Bio.Alphabet dependency

# 2.1.0
- Fix an issue where reverse reads were incorrectly trimmed by CutadaptPatternTrimmer.
# 2.0.6
- Fixed an issue where using the same output_file_name_template for two operations caused FileExistsError.

# 2.0.5 
 - Fixed an issue where specifying the temporary directory in the general section would not work.

# 2.0.4
- Asynchronous compression + decompress only once per pipeline
- Refactoring

# 2.0.3
- Fix incorrect bound checking for error_rate in CutadaptPatternTrimmer operation
- Added more parameter checking in CutadaptPatternTrimmer.

# 2.0.2
- Added documentation

# 2.0.1
- Fixed a bug with the detection of paired-end .fastq files.

# 1.0.0
- Fix a bug with output files in merging using PEAR.
- Add docstrings and improve code style.
- Rename program to 'gbprocess'.

## 0.2.0
- Fix splitting paired-end files when there are differences in read lengths between forward and reverse files
- Prevented operations to be performed while files are empty.
- Fix a bug where samples would not be processed further after being split.
- Removed unused variable in pattern trimming.
- Fix searching for patterns when non-palindromic sequences are used as a cut-site.
- Dont't allow for usage of format specifiers in output file name templates.
- Allow duplicate operations

## 0.1.3
- Fix multiprocessing bug.

## 0.1.2
- Add versioning to release archives.
- Add tests for older code.
- Improved regex parsing of file names.
- Better parsing of command line options.

## 0.1.1
- Fix running from command line.
- Re-add PEAR option next to fastq-join and fastp for merging.
- Add more tests.
- Files with only whitespace characters are now considered empty.
- Fix problem with joining files that end with new line characters.

## 0.1.0
- Replace PEAR with fastq-join

## 0.0.3
- Code syntax changes
- Added more tests to code

## 0.0.2
- Improved input checking for fasta files (containing barcodes).
- Fix bug in CutadaptPositionalTrimmer.
- Print version at start of program.
- Clean exit when not arguments are passed.

## 0.0.1
- Initial release.