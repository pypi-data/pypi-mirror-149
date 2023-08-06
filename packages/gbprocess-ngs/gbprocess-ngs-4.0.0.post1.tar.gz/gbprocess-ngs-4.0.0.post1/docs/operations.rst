.. _GBSOperations:

==========
Operations
==========


.. tabs::
   
   .. tab:: Information
   
		| This page describes all available operations in **GBprocesS**. 
		| GBprocesS requires to specify parameters such as restriction enzyme cutsite remnants, sequencing primers, and other library-specific features. 
		| Please see the explanatory illustration in the next tab to help identify these features in your own libraries.
		| Detailed description of a common library preparation workflow and how these relate to the subsequent steps of read preprocessing ("what goes on, must come off") can be found on the page :ref:`How it Works <GBSHIW>`.
		| Examples of configuration .ini files for common scenarios can be found on the :ref:`Example <GBSexamples>`-page.

   .. tab:: Explanatory illustration
		
		.. image:: images/Operations_info.png
		
----

.. _GBSOperationsAverageQualityFilter:

AverageQualityFilter
--------------------
.. autoclass:: gbprocess.operations.AverageQualityFilter
	:exclude-members: supports_multiprocessing, perform

----

.. _GBSOperationsDemultiplex:

CutadaptDemultiplex
-------------------
.. autoclass:: gbprocess.operations.CutadaptDemultiplex
	:exclude-members: supports_multiprocessing, perform

----

.. _GBSOperationsTrimming:

CutadaptTrimmer
-------------------------
.. autoclass:: gbprocess.operations.CutadaptTrimmer
	:exclude-members: supports_multiprocessing, perform

----

.. _GBSOperationsLengthFilter:

LengthFilter
------------
.. autoclass:: gbprocess.operations.LengthFilter
	:exclude-members: supports_multiprocessing, perform

----

.. _GBSOperationsMaxNFilter:

MaxNFilter
----------
.. autoclass:: gbprocess.operations.MaxNFilter
	:exclude-members: supports_multiprocessing, perform

----

.. _GBSOperationsPear:

Pear
----
.. autoclass:: gbprocess.operations.Pear
	:exclude-members: supports_multiprocessing, perform

----

.. _GBSOperationsRemovePatternFilter:

RemovePatternFilter
-------------------
.. autoclass:: gbprocess.operations.RemovePatternFilter
	:exclude-members: supports_multiprocessing, perform
	
----

.. _GBSOperationsSlidingWindowQualityFilter:

SlidingWindowQualityFilter
--------------------------
.. autoclass:: gbprocess.operations.SlidingWindowQualityFilter
	:exclude-members: supports_multiprocessing, perform
	
