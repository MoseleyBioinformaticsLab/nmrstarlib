The nmrstarlib Tutorial
=======================

The :mod:`nmrstarlib` package provides classes and other facilities for parsing,
accessing, and manipulating data stored in NMR-STAR and JSONized NMR-STAR formats.
Also, :mod:`nmrstarlib` package provides simple command-line interface.

Using nmrstarlib as a library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Importing nmrstarlib module
---------------------------

If :mod:`nmrstarlib` package is installed on the system the :mod:`nmrstarlib.nmrstarlib`
module can be imported:

>>> from nmrstarlib import nmrstarlib

Constructing StarFile generator
-------------------------------

The :mod:`~nmrstarlib.nmrstarlib` module provides :func:`~nmrstarlib.nmrstarlib.read_files`
generator function that yields :class:`~nmrstarlib.nmrstarlib.StarFile` instances. Constructing
:class:`~nmrstarlib.nmrstarlib.StarFile` generator is easy - specify path to local NMR-STAR file,
directory of NMR-STAR files, archive of NMR-STAR files or BMRB id:

>>> from nmrstarlib import nmrstarlib
>>>
>>> single_starfile = nmrstarlib.read_files(["bmr18569.str"])  # single NMR-STAR file
>>>
>>> starfiles = nmrstarlib.read_files(["bmr18569.str", "bmr336.str"]) # several NMR-STAR files
>>>
>>> dir_starfiles = nmrstarlib.read_files(["starfiles_dir"])   # directory of NMR-STAR files
>>>
>>> arch_starfiles = nmrstarlib.read_files(["starfiles.zip"])  # archive of NMR-STAR files
>>>
>>> url_starfile = nmrstarlib.read_files(["18569"])            # BMRB id of NMR-STAR file
>>>

Processing StarFile generator
-----------------------------

The :class:`~nmrstarlib.nmrstarlib.StarFile` generator can be processed in several ways:

   * Feed it to a for-loop and process one file at a time:

   >>> for starfile in dir_starfiles:
   ...     print(starfile.bmrbid)                  # print BMRB id of StarFile
   ...     print(starfile.source)                  # print source of StarFile
   ...     for saveframe_name in starfile.keys():  # print saveframe names
   ...         print(saveframe_name)
   >>>

   .. note:: Once generator is consumed it becomes empty and needs to be created again.

   * Since the :class:`~nmrstarlib.nmrstarlib.StarFile` generator behaves like an iterator,
     we can call the :py:func:`next` built-in function:

   >>> starfile1 = next(dir_starfiles)
   >>> starfile2 = next(dir_starfiles)
   >>> ...

   .. note:: Once the generator is consumed, :py:class:`StopIteration` will be raised.

   * Convert the :class:`~nmrstarlib.nmrstarlib.StarFile` generator into a :py:class:`list` of
     :class:`~nmrstarlib.nmrstarlib.StarFile` objects:

   >>> starfiles_list = list(dir_starfiles)
   >>>

   .. warning:: Do not convert the :class:`~nmrstarlib.nmrstarlib.StarFile` generator into a
                :py:class:`list` if the generator can yield a large number of files, e.g.
                several thousand, otherwise it can consume all available memory.

Accessing and manipulating data from a single StarFile
------------------------------------------------------

Since :class:`~nmrstarlib.nmrstarlib.StarFile` is a Python :py:class:`collections.OrderedDict`,
data can be accessed and manipulated as with any regular Python :py:class:`dict` object
using bracket accessors.

   * Accessing data in :class:`~nmrstarlib.nmrstarlib.StarFile`:

   >>> list(starfile.keys())  # list StarFile-level keys, i.e. saveframe names
   ['data', 'save_entry_information', 'save_entry_citation', 'save_assembly',
    'save_EVH1', 'save_natural_source', 'save_experimental_source',
    'save_sample_1', 'save_sample_2', 'save_sample_3', 'save_sample_4',
    'save_sample_conditions_1', 'save_sample_conditions_2',
    'save_sample_conditions_3', 'save_sample_conditions_4', 'save_AZARA',
    'save_xwinnmr', 'save_ANSIG', 'save_CNS', 'save_spectrometer_1',
    'save_spectrometer_2', 'save_NMR_spectrometer_list', 'save_experiment_list',
    'save_chemical_shift_reference_1', 'save_assigned_chem_shift_list_1',
    'save_combined_NOESY_peak_list']
   >>>
   >>> starfile["data"]
   '18569'
   >>>
   >>> starfile["save_entry_information"]
   OrderedDict([
    ('Entry.Sf_category', 'entry_information'),
    ('Entry.Sf_framecode', 'entry_information'),
    ('Entry.ID', '18569'),
    ('Entry.Title', ';\n13C, 15N and 1H backbone and sidechain assignments\n of the
                      ENA-VASP homology 1 (EVH1) domain of the human
                      vasodilator-stimulated phosphoprotein (VASP)\n;'),
    ('Entry.Type', '.'),
    ('Entry.Version_type', 'original'),
    ('Entry.Submission_date', '2012-07-05'),
    ('Entry.Accession_date', '2012-07-05'), ...
   ])
   >>>
   >>> list(starfile["save_entry_information"].keys())  # list saveframe-level keys
   ['Entry.Sf_category', 'Entry.Sf_framecode', 'Entry.ID', 'Entry.Title',
    'Entry.Type', 'Entry.Version_type', 'Entry.Submission_date',
    'Entry.Accession_date', 'Entry.Last_release_date', 'Entry.Original_release_date',
    'Entry.Origination', 'Entry.NMR_STAR_version', 'Entry.Original_NMR_STAR_version',
    'Entry.Experimental_method', 'Entry.Experimental_method_subtype', 'Entry.Details',
    'Entry.BMRB_internal_directory_name', 'loop_0', 'loop_1', 'loop_2', 'loop_3', 'loop_4']
   >>>
   >>> starfile["save_entry_information"]["Entry.Submission_date"]
   '2012-07-05'
   >>>
   >>> starfile["save_entry_information"]["loop_0"]
   (['Entry_author.Ordinal', 'Entry_author.Given_name', 'Entry_author.Family_name',
     'Entry_author.First_initial', 'Entry_author.Middle_initials',
     'Entry_author.Family_title', 'Entry_author.Entry_ID'],
     [OrderedDict([('Entry_author.Ordinal', '1'),
                   ('Entry_author.Given_name', 'Linda'),
                   ('Entry_author.Family_name', 'Ball'),
                   ('Entry_author.First_initial', '.'),
                   ('Entry_author.Middle_initials', 'J.'),
                   ('Entry_author.Family_title', '.'),
                   ('Entry_author.Entry_ID', '18569')]),
      OrderedDict([('Entry_author.Ordinal', '2'),
                   ('Entry_author.Given_name', 'Schmieder'),
                   ('Entry_author.Family_name', 'Peter'),
                   ('Entry_author.First_initial', '.'),
                   ('Entry_author.Middle_initials', '.'),
                   ('Entry_author.Family_title', '.'),
                   ('Entry_author.Entry_ID', '18569')])
   ])
   >>>
   >>> starfile["save_entry_information"]["loop_0"][0]  # list loop-level keys
   ['Entry_author.Ordinal', 'Entry_author.Given_name', 'Entry_author.Family_name',
   'Entry_author.First_initial', 'Entry_author.Middle_initials',
   'Entry_author.Family_title', 'Entry_author.Entry_ID']
   >>>
   >>> # loop values is a list of dictionaries:
   >>> starfile["save_entry_information"]["loop_0"][1]
   [OrderedDict([('Entry_author.Ordinal', '1'),
                 ('Entry_author.Given_name', 'Linda'),
                 ('Entry_author.Family_name', 'Ball'),
                 ('Entry_author.First_initial', '.'),
                 ('Entry_author.Middle_initials', 'J.'),
                 ('Entry_author.Family_title', '.'),
                 ('Entry_author.Entry_ID', '18569')]),
    OrderedDict([('Entry_author.Ordinal', '2'),
                 ('Entry_author.Given_name', 'Schmieder'),
                 ('Entry_author.Family_name', 'Peter'),
                 ('Entry_author.First_initial', '.'),
                 ('Entry_author.Middle_initials', '.'),
                 ('Entry_author.Family_title', '.'),
                 ('Entry_author.Entry_ID', '18569')])]
   >>>
   >>> # every loop entry is accessed by index:
   >>> starfile["save_entry_information"]["loop_0"].[1][0]["Entry_author.Family_name"]
   'Ball'
   >>> starfile["save_entry_information"]["loop_0"].[1][1]["Entry_author.Family_name"]
   'Peter'

   * Manipulating data in a :class:`~nmrstarlib.nmrstarlib.StarFile` is easy - access data
     using bracket accessors and set a new value:

   >>> starfile["data"]
   '18569'
   >>>
   >>> starfile["data"] = "18569_modified"
   '18569_modified'
   >>>
   >>> # change submission date
   >>> starfile["save_entry_information"]["Entry.Submission_date"]
   '2012-07-05'
   >>>
   >>> starfile["save_entry_information"]["Entry.Submission_date"] = "2015-07-05"
   '2015-07-05'
   >>>

   * Printing a :class:`~nmrstarlib.nmrstarlib.StarFile` and its components (`saveframe` and `loop` data):

   >>> starfile.print_starfile(format="nmrstar")
   data_18569
   save_entry_information
       _Entry.Sf_category	 entry_information
       _Entry.Sf_framecode	 entry_information
       _Entry.ID	 18569
   ...
   >>>
   >>> starfile.print_starfile(format="json")
   {
    "data": "18569",
    "save_entry_information": {
        "Entry.Sf_category": "entry_information",
        "Entry.Sf_framecode": "entry_information",
        "Entry.ID": "18569",
    ...
   }
   >>>
   >>> starfile.print_saveframe("save_entry_information", format="nmrstar")
   _Entry.Sf_category	 entry_information
   _Entry.Sf_framecode	 entry_information
   _Entry.ID	 18569
   _Entry.Title
   ;
   13C, 15N and 1H backbone and sidechain assignments of the
   ENA-VASP homology 1 (EVH1) domain of the human
   vasodilator-stimulated phosphoprotein (VASP)
   ;
   _Entry.Type	 .
   _Entry.Version_type	 original
   _Entry.Submission_date	 2012-07-05
   _Entry.Accession_date	 2012-07-05
   _Entry.Last_release_date	 2012-07-18
   _Entry.Original_release_date	 2012-07-18
   _Entry.Origination	 author
   _Entry.NMR_STAR_version	 3.1.1.61
   _Entry.Original_NMR_STAR_version	 3.1
   _Entry.Experimental_method	 NMR
   _Entry.Experimental_method_subtype	 solution
   _Entry.Details	 'ANSIG v3.3 exported crosspeaks file'
   _Entry.BMRB_internal_directory_name	 .
   ...
   >>>
   >>> starfile.print_saveframe("save_entry_information", format="json")
   {
       "Entry.Sf_category": "entry_information",
       "Entry.Sf_framecode": "entry_information",
       "Entry.ID": "18569",
       "Entry.Title": ";\n13C, 15N and 1H backbone and sidechain assignments of the
                        ENA-VASP homology 1 (EVH1) domain of the human
                        vasodilator-stimulated phosphoprotein (VASP)\n;",
       "Entry.Type": ".",
       "Entry.Version_type": "original",
       "Entry.Submission_date": "2012-07-05",
       "Entry.Accession_date": "2012-07-05",
       "Entry.Last_release_date": "2012-07-18",
       "Entry.Original_release_date": "2012-07-18",
       "Entry.Origination": "author",
       "Entry.NMR_STAR_version": "3.1.1.61",
       "Entry.Original_NMR_STAR_version": "3.1",
       "Entry.Experimental_method": "NMR",
       "Entry.Experimental_method_subtype": "solution",
       "Entry.Details": "'ANSIG v3.3 exported crosspeaks file'",
       "Entry.BMRB_internal_directory_name": ".",
       ...
   }
   >>>
   >>> starfile.print_loop("save_entry_information", "loop_1", format="nmrstar")
   _Data_set.Type
   _Data_set.Count
   _Data_set.Entry_ID
   assigned_chemical_shifts 1 18569
   spectral_peak_list 1 18569
   >>>
   >>> starfile.print_loop("save_entry_information", "loop_1", format="json")
   [
       [
           "Data_set.Type",
           "Data_set.Count",
           "Data_set.Entry_ID"
       ],
       [
           {
               "Data_set.Type": "assigned_chemical_shifts",
               "Data_set.Count": "1",
               "Data_set.Entry_ID": "18569"
           },
           {
               "Data_set.Type": "spectral_peak_list",
               "Data_set.Count": "1",
               "Data_set.Entry_ID": "18569"
           }
       ]
   ]
   >>>

   * Accessing chemical shift data:

   Chemical shift data can be accessed using bracket accessors as described above using a
   `saveframe` name and `loop` name:

   >>> starfile["save_assigned_chem_shift_list_1"]["loop_1"][0]
   ['Atom_chem_shift.ID', 'Atom_chem_shift.Assembly_atom_ID',
    'Atom_chem_shift.Entity_assembly_ID', 'Atom_chem_shift.Entity_ID',
    'Atom_chem_shift.Comp_index_ID', 'Atom_chem_shift.Seq_ID',
    'Atom_chem_shift.Comp_ID', 'Atom_chem_shift.Atom_ID',
    'Atom_chem_shift.Atom_type', 'Atom_chem_shift.Atom_isotope_number',
    'Atom_chem_shift.Val', 'Atom_chem_shift.Val_err',
    'Atom_chem_shift.Assign_fig_of_merit', 'Atom_chem_shift.Ambiguity_code',
    'Atom_chem_shift.Occupancy', 'Atom_chem_shift.Resonance_ID',
    'Atom_chem_shift.Auth_entity_assembly_ID', 'Atom_chem_shift.Auth_asym_ID',
    'Atom_chem_shift.Auth_seq_ID', 'Atom_chem_shift.Auth_comp_ID',
    'Atom_chem_shift.Auth_atom_ID', 'Atom_chem_shift.Details',
    'Atom_chem_shift.Entry_ID', 'Atom_chem_shift.Assigned_chem_shift_list_ID']
   >>>
   >>> starfile["save_assigned_chem_shift_list_1"]["loop_1"][1][0]["Atom_chem_shift.Seq_ID"]
   '1'
   >>> starfile["save_assigned_chem_shift_list_1"]["loop_1"][1][0]["Atom_chem_shift.Comp_ID"]
   'MET'
   >>> starfile["save_assigned_chem_shift_list_1"]["loop_1"][1][0]["Atom_chem_shift.Atom_ID"]
   'H'
   >>> starfile["save_assigned_chem_shift_list_1"]["loop_1"][1][0]["Atom_chem_shift.Val"]
   '8.55'
   >>> starfile["save_assigned_chem_shift_list_1"]["loop_1"][1][1]["Atom_chem_shift.Atom_ID"]
   'HA'
   >>> starfile["save_assigned_chem_shift_list_1"]["loop_1"][1][1]["Atom_chem_shift.Val"]
   '4.548'
   >>> starfile["save_assigned_chem_shift_list_1"]["loop_1"][1][2]["Atom_chem_shift.Atom_ID"]
   'HB2'
   >>> starfile["save_assigned_chem_shift_list_1"]["loop_1"][1][2]["Atom_chem_shift.Val"]
   '1.994'
   >>>

   Also the :class:`~nmrstarlib.nmrstarlib.StarFile` class provides a
   :meth:`~nmrstarlib.nmrstarlib.StarFile.chem_shifts_by_residue` method that organizes
   chemical shits into :py:class:`collections.OrderedDict` data structure (`keys` - tuple of
   sequence id and amino acid residue type; `values` - chemical shift data):

   >>> starfile.chem_shifts_by_residue()
   [OrderedDict([(('1', 'MET'), OrderedDict([('H', '8.55'),
                                             ('HA', '4.548'),
                                             ('HB2', '1.994'),
                                             ('HB3', '2.118'),
                                             ('CA', '55.489'),
                                             ('CB', '32.848'),
                                             ('N', '122.221')])),
                 (('2', 'SER'), OrderedDict([('H', '8.225'),
                                             ('HA', '4.420'),
                                             ('HB2', '3.805'),
                                             ('HB3', '3.857'),
                                             ('CA', '58.593'),
                                             ('CB', '64.057'),
                                             ('N', '117.197')])),
                 (('3', 'GLU'), OrderedDict([('H', '8.002'),
                                             ('HA', '4.848'),
                                             ('HB2', '1.852'),
                                             ('HB3', '1.963'),
                                             ('HG2', '1.981'),
                                             ('HG3', '2.191'),
                                             ('CA', '55.651'),
                                             ('CB', '32.952'),
                                             ('CG', '37.425'),
                                             ('N', '119.833')])), ...
   ...
   ]
   >>>
   >>> starfile.chem_shifts_by_residue(aminoacids=["SER"], atoms=["CA", "CB"])
   [OrderedDict([(('2', 'SER'), OrderedDict([('CA', '58.593'),
                                             ('CB', '64.057')])),
                 (('8', 'SER'), OrderedDict([('CA', '57.456'),
                                             ('CB', '64.863')])),
                 (('9', 'SER'), OrderedDict([('CA', '57.852'),
                                             ('CB', '67.332')])),
                 (('34', 'SER'), OrderedDict([('CA', '59.113'),
                                              ('CB', '66.248')])),
                 (('46', 'SER'), OrderedDict([('CA', '55.939'),
                                              ('CB', '66.829')])),
                 (('95', 'SER'), OrderedDict([('CA', '57.013'),
                                              ('CB', '66.501')])),
                 (('108', 'SER'), OrderedDict([('CA', '61.617'),
                                               ('CB', '62.493')]))])
   ]
   >>>

Writing data from a StarFile object into a file
-----------------------------------------------
Data from :class:`~nmrstarlib.nmrstarlib.StarFile` can be written into file in original NMR-STAR format
or in equivalent JSON format using :meth:`~nmrstarlib.nmrstarlib.StarFile.write()`:

   * Writing into a NMR-STAR formatted file:

   >>> with open("bmr18569_modified.str", "w") as outfile:
   ...     starfile.write(outfile, fileformat="nmrstar")
   >>>

   * Writing into a JSONized NMR-STAR formatted file:

   >>> with open("bmr18569_modified.json", "w") as outfile:
   ...     starfile.write(outfile, fileformat="json")
   >>>

Converting NMR-STAR files
-------------------------

NMR-STAR files can be converted between the NMR-STAR file format and a JSONized NMR-STAR
file format using the :mod:`nmrstarlib.converter` module.

   * Converting from the NMR-STAR file format into its equivalent JSON file format:

   >>> from nmrstarlib.converter import Converter
   >>>
   >>> # Using valid BMRB id to access file from URL: from_path="18569"
   >>> converter = Converter(from_path="18569", to_path="bmr18569.json",
   ...                       from_format="nmrstar", to_format="json")
   >>> converter.convert()
   >>>

   * Converting from JSON file format into its equivalent NMR-STAR file format:

   >>> from nmrstarlib.converter import Converter
   >>>
   >>> converter = Converter(from_path="bmr18569.json", to_path="bmr18569.str",
   ...                       from_format="json", to_format="nmrstar")
   >>> converter.convert()
   >>>

.. note:: See :mod:`nmrstarlib.converter` for full list of available conversions.

Visualizing chemical shifts values
----------------------------------

Chemical shifts values can be visualized using the :mod:`nmrstarlib.csviewer`
Chemical Shifts Viewer module.

>>> from nmrstarlib.csviewer import CSViewer
>>>
>>> csviewer = CSViewer(from_path="18569", filename="18569_chem_shifts_all", csview_format="png")
>>> csviewer.csview(view=True)
>>>
>>> csviewer = CSViewer(from_path="18569", aminoacids=["SER", "THR"], atoms=["CA", "CB"],
...                     filename="18569_chem_shifts_SER_THR_CA_CB", csview_format="png")
>>> csviewer.csview(view=True)  # open in a default image viewer or pdf viewer
>>> csviewer.csview(view=False) # save output file in current working directory
>>>

:mod:`nmrstarlib.csviewer` output example:

.. image:: _static/images/18569_chem_shifts_all.png
   :width: 110%
   :align: center


Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~
Command Line Interface functionality:
   * Convert from NMR-STAR file format into its equivalent JSON file format and vice versa.
   * Visualize assigned chemical shift values.

.. code::

   nmrstarlib command-line interface

   Usage:
       nmrstarlib -h | --help
       nmrstarlib --version
       nmrstarlib convert (<from_path> <to_path>) [--from_format=<format>]
                                                  [--to_format=<format>]
                                                  [--bmrb_url=<url>]
                                                  [--nmrstarversion=<version>]
                                                  [--verbose]

       nmrstarlib csview <starfile_path> [--aminoacids=<aa>]
                                         [--atoms=<at>]
                                         [--csview_outfile=<path>]
                                         [--csview_format=<format>]
                                         [--nmrstarversion=<version>]
                                         [--verbose]

   Options:
       -h, --help                   Show this screen.
       --version                    Show version.
       --verbose                    Print what files are processing.
       --from_format=<format>       Input file format, available formats:
                                    nmrstar, json [default: nmrstar]
       --to_format=<format>         Output file format, available formats:
                                    nmrstar, json [default: json]
       --nmrstarversion=<version>   Version of NMR-STAR format to use, available:
                                    3, 2 [default: 3]
       --bmrb_url=<url>             URL to BMRB REST interface
                                    [default: http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/]
       --aminoacids=<aa>            Comma-separated amino acid three-letter codes
       --atoms=<at>                 Comma-separated BMRB atom codes
       --csview_outfile=<path>      Where to save chemical shifts table
       --csview_format=<format>     Format to which save chamical shift table
                                    [default: svg]

Converting NMR-STAR files in bulk
---------------------------------

One-to-one file conversions
***************************

   * Convert from a local file in NMR-STAR format to a local file in JSON format:

   .. code:: bash

      $ python3 -m nmrstarlib convert bmr18569.str bmr18569.json \
                --from_format=nmrstar --to_format=json

   * Convert from a local file in JSON format to a local file in NMR-STAR format:

   .. code:: bash

      $ python3 -m nmrstarlib convert bmr18569.json bmr18569.str \
                --from_format=json --to_format=nmrstar

   * Convert from a compressed local file in NMR-STAR format to a compressed local file in JSON format:

   .. code:: bash

      $ python3 -m nmrstarlib convert bmr18569.str.gz bmr18569.json.gz \
                --from_format=nmrstar --to_format=json

   * Convert from a compressed local file in JSON format to a compressed local file in NMR-STAR format:

   .. code:: bash

      $ python3 -m nmrstarlib convert bmr18569.json.gz bmr18569.str.gz \
                --from_format=json --to_format=nmrstar

   * Convert from a uncompressed URL file in NMR-STAR format to a compressed local file in JSON format:

   .. code:: bash

      $ python3 -m nmrstarlib convert 18569 bmr18569.json.bz2 \
                --from_format=nmrstar --to_format=json

   .. note:: See :mod:`nmrstarlib.converter` for full list of available conversions.

Many-to-many files conversions
******************************

   * Convert from a directory of files in NMR-STAR format to a directory of files in JSON format:

   .. code:: bash

      $ python3 -m nmrstarlib convert starfiles_dir_nmrstar starfiles_dir_json \
                --from_format=nmrstar --to_format=json

   * Convert from a directory of files in JSON format to a directory of files in NMR-STAR format:

   .. code:: bash

      $ python3 -m nmrstarlib convert starfiles_dir_json starfiles_dir_nmrstar \
                --from_format=json --to_format=nmrstar

   * Convert from a directory of files in NMR-STAR format to a zip archive of files in JSON format:

   .. code:: bash

      $ python3 -m nmrstarlib convert starfiles_dir_nmrstar starfiles_json.zip \
                --from_format=nmrstar --to_format=json

   * Convert from a compressed tar archive of files in JSON format to a directory of files in NMR-STAR format:

   .. code:: bash

      $ python3 -m nmrstarlib convert starfiles_json.tar.gz starfiles_dir_nmrstar \
                --from_format=json --to_format=nmrstar

   * Convert from a zip archive of files in NMR-STAR format to a compressed tar archive of files in JSON format:

   .. code:: bash

      $ python3 -m nmrstarlib convert starfiles_nmrstar.zip starfile_json.tar.bz2 \
                --from_format=nmrstar --to_format=json

   .. note:: See :mod:`nmrstarlib.converter` for full list of available conversions.


Visualizing chemical shift values
---------------------------------

   * Visualize chemical shift values for the entire sequence:

   .. code:: bash

      $ python3 -m nmrstarlib csview 18569 \
                --csview_outfile=18569_chem_shifts_all --csview_format=png

   .. image:: _static/images/18569_chem_shifts_all.png
      :width: 110%
      :align: center

   * Visualize `CA`, `CB`, `CG`, and `CG2` chemical shift values for `GLU` and `THR` amino acid residues:

   .. code:: bash

      $ python3 -m nmrstarlib csview 18569 \
                --aminoacids=GLU,THR --atoms=CA,CB,CG,CG2 \
                --csview_outfile=18569_chem_shifts_GLU_THR_CA_CB_CG_CG2 \
                --csview_format=png

   .. image:: _static/images/18569_chem_shifts_GLU_THR_CA_CB_CG_CG2.png
      :width: 60%
      :align: center
