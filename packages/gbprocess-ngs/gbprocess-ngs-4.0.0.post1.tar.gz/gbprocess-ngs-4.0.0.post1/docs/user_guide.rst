###################
Scope & Quick Start
###################

Scope 
-----

**GBprocesS** performs read preprocessing for Genotyping-By-Sequencing (GBS) libraries.
Preprocessing is executed as an ordered, linear workflow, built upon a set of predefined operations that perform:  

1. Demultiplexing (`Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_).
2. Trimming: Trimming barcodes, spacers, and restriction enzyme cutsite remnants at the 5’ end of the reads (while compensating for variable length barcodes and spacers by trimming at the 3' end of forward reads) and trimming of restriction enzyme cutsite remnants, barcodes, and adapter sequences at the 3’ end of the reads.
   (`Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_).
3. Merging of forward and reverse reads.
4. Removal of reads with low quality base-calling (Python).
5. Removal of reads with internal restriction sites (Python).

A list of the names of all available operations is available through::

    gbprocess --operations
    
Users can adjust the functionality of **GBprocesS** by listing the required operations, execution order, and run parameters in a configuration .ini file.
For a detailed explanation on what each specific operation does and how to configure it, see the :ref:`Operations <GBSOperations>` section.

----

Quick Start 
---------------------

The configuration syntax used by GBprocesS follows the `INI-file <https://en.wikipedia.org/wiki/INI_file>`_ format.
This format defines sections, parameters and comments. Note that sections and parameter definitions are case sensitive.

Sections start with a section header between square brackets (e.g. ``[header1]``). 
GBprocesS will parse sections in order, starting at the top of the configuration .ini file. 
GBprocesS recognizes two types of sections: the ``[General]`` section, 
and sections that define an operation to be executed. Below each section header, parameters can 
be defined by using the syntax ``parameter_name = parameter_value``:
the name of the parameter and the parameter value itself, separated by an equal sign ``=``. 

General
~~~~~~~

The first section that **must** be specified is the ``[General]`` section. The general section
allows to configure pipeline behavior, independent of the operations that will be performed
by the pipeline:

.. tabs::
   
   .. tab:: General example
   
		.. code-block:: ini

			[General]
			# Use 1 CPU core
			cores = 1
			# Location of the input files
			input_directory = /data/run/
			# Paired-end sequencing
			sequencing_type = pe
			# Template to parse the input files.
			## For example, 17146FL-13-01-01_S9_L002_R1_001.fastq.bz2: run = 17146FL-13-01-01_S9_L002; orientation = 1; extension = .fastq.bz2
			input_file_name_template = {run:24}_R{orientation:1}_001{extension:10}
			# Location to store temporary created files
			temp_dir = /tmp/

   .. tab:: Detailed explanation
    
		- ``cores`` *(int)* - Defines the maximum number of CPU cores used by GBprocesS.
		- ``input_directory`` *(str)* - Path to an existing directory that contains the .fastq files to be processed.
		- ``sequencing_type`` *(str)* - use either ``se`` for single-end reads or ``pe`` for paired-end reads .
		- ``input_file_name_template`` *(str)* - Template used to interprete the names of the input .fastq files in the ``input_directory``. 
		  The input_file_name_template follows a simplified syntax of format strings as 
		  described in `PEP 3101 <https://www.python.org/dev/peps/pep-3101/#id17/>`__. The template 
		  consists of text data that describes parts of the input file name that are considered constant
		  and and replacement fields (indicated by curly braces) that describe parts of the filenames that are 
		  stored as a property of the sample. These variable properties can be used later to determine the format 
		  of the output file names (see ``output_file_name_template`` in :ref:`Operations <GBSOperations>` section). The field name,
		  the element inside the curly braces of the replacement field, refers to the property name. Possible properties are:
		  ``{orientation}``, ``{run}``, ``{sample_name}`` and ``{extension}``. In the input_file_name_template,
		  the field name can be followed by a colon (``:``) and a number to indicate the width of the field in the input file name. 
		  This means that this part of the file name must be of equal length in all input .fastq files in the ``input_directory``.
		  Please note that if two adjacent fields do not have a specified width, it will not be possible to parse them,
		  as it is impossible to assign a part of the input file name to one field or the other. Thus, only one field may 
		  have unspecified width in the input_file_name_template, and for this field the maximum possible width is used.
		  In the example template ``{sample_name:3}_constant_text_{run:5}{extension:10}``, all file names in the input directory
		  start with a variable three character long sample name, followed by a constant part ``_constant_text_`` 
		  before the run name and the file extension, consisting of three and ten characters respectively. 
		- ``temp_dir`` *(str, optional)* - path to a directory to store the temporary files into. As a rule of thumb, this temporary directory 
		  must be able to hold approximately twice the amount of data present in ``input_directory``,
		  defaults to ``/tmp/``.


Operations
~~~~~~~~~~

.. tabs::
   
   .. tab:: Operations
   
		| Any section following the ``[General]`` section will be interpreted as being an operation added to the workflow.
		| There are **9** different available optional operations, each containing several parameters, the scheme below depicts these in a logical order. 
		| A detailed explanation of every possible operation can be found on :ref:`Operations <GBSOperations>`.
		
		.. image:: images/Workflow_operations.png
		   :width: 500
		
   .. tab:: Examples
   
		| Examples of config.ini files of four common types of data can be found on the :ref:`Examples <GBSexamples>` page.
		| These include:
	
			:ref:`Single-digest GBS and single-end sequencing <GBSexamplessinglesingle>`
			
			:ref:`Single-digest GBS and paired-end sequencing <GBSexamplessinglepaired>` (with or without merging)
			
			:ref:`Double-digest GBS and single-end sequencing <GBSexamplesdoublesingle>`
			
			:ref:`Double-digest GBS and paired-end sequencing <GBSexamplesdoublepaired>` (with or without merging)
			
			:ref:`Double-digest GBS and paired-end sequencing with spacers <GBSexamplesdoublepaired>` (with or without merging)
			
			:ref:`Processing sample sets that are already trimmed <GBSexamplesmerging>` (merging & quality filtering)


Starting the pipeline
~~~~~~~~~~~~~~~~~~~~~

Once your custom configuration .ini file is finished, run the program with the following command::
	
	gbprocess -c /path/to/config.ini

This makes it possible to re-use a template configuration .ini file by changing a few parameters and the paths to the data that needs to be preprocessed.

----

Output
------

By default, all run directories are created as defined by the user in the configuration .ini file (one per operation), and output FASTQ files are placed in the respective directories as full sized files or zipped files respective with the input.
Log files of the various third-party components (`Cutadapt <https://cutadapt.readthedocs.io/en/stable/>`_, `PEAR <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3933873/>`_) are placed in the respective directories, listing command line parameters and summary statistics per operation. Please note that as GBprocesS may be run in parallel on multiple cores, FASTQ files may be split and processed in parallel, so that the respective sample information may also appear in multiple log files (.out).

----

Debugging
---------
By default, only run information is reported when executing GBprocesS, and no stack trace is provided on error.
Use the ``--debug`` flag to report debugging information::

    gbprocess --debug -c /path/to/config.ini