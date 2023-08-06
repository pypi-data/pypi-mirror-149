Examples
======================

Here are two examples of how Q-Force can be used: In default settings and with some customization.
For the purposes of these examples, whenever you need an additional file, QM outputs or otherwise,
they are provided in the directory *necessary_files*.

First, please get the example files by:

:code:`git clone https://github.com/selimsami/qforce_examples.git`

|

Default settings
-------------------

Creating the initial QM input
++++++++++++++++++++++++++++++++

Find in *examples/gaussian/default_settings* a coordinate file (propane.xyz) for the propane
molecule.

Let's first create the QM input file:

:code:`qforce propane.xyz`

This will create a *propane_qforce* directory, and in it, you will find 'propane_hessian.inp'.
Now run this QM calculation and put the necessary output files (.out, .fchk) in the same directory.
(remember: the output files are available in *necessary_files*)

Treating the flexible dihedrals
++++++++++++++++++++++++++++++++

Now we can run Q-Force again from the same directory to create fragments and the corresponding
QM dihedral scan input files by:

:code:`qforce propane`

This will create all the necessary input files in the subdirectory *propane_qforce/fragments*.
Then, run these calculations and put the output file(s) (.out) in the same subdirectory.

Creating the force field
++++++++++++++++++++++++++++++++

Now that all necessary QM data is available, let's create our force field:

:code:`qforce propane`

You can now find the Q-Force force field files in the *propane_qforce* directory.

|

Custom settings
------------------
Find in *examples/gaussian/custom_settings* a coordinate file (benzene.pdb) for the benzene
molecule. In this example, we look at some of the custom settings available with Q-Force and how
they can be executed.
The custom settings are provided with an external file with:

:code:`qforce benzene.pdb -o settings`

Now let's create the **settings** file.

Custom Lennard-Jones interactions
+++++++++++++++++++++++++++++++++

By default, Q-Force determines the atom types for Lennard-Jones interactions automatically.
Alternatively, the user can also provide atom types manually, for a force field of their choice.
Here, we choose to use the GAFF force field by adding the following line to the **settings** file:

.. code-block:: text

    [ff]
    lennard_jones = gaff

With this command, the user also has to provide the atom types manually
in the 'benzene_qforce' directory in a file called "ext_lj". In this file, every line should
contain the atom type of one atom in the same order as the coordinate file.


Conversion to job script
++++++++++++++++++++++++

Often the QM calculations are needed to be submitted as jobs in supercomputers.
For large molecules Q-Force can have a large number of QM dihedral scans that needs to be
performed and therefore it may be convenient to have input files converted to job scripts.
This can be done by adding the **[qm::job_script]** block to the **settings** file:

.. code-block:: text

    [qm::job_script]
    #!/bin/bash
    #SBATCH --time=1-00:00:00
    #SBATCH -o <jobname>.out

    g16<<EOF
    <input>
    EOF

Here we make a SLURM job script. Two placeholders that can be used are **<outfile>** and
**<input>**. **<jobname>** gets replaced by the name of the calculation, for example in the case
of the 'benzene_hessian.inp', it will be 'benzene_hessian.out'.
**<input>** is where the content of the QM input file will be placed.



Creating the initial QM input
++++++++++++++++++++++++++++++++

Now that we know what these settings do, let's supply them to Q-Force:

:code:`qforce benzene.pdb -o settings`


Again, this will create a *benzene_qforce* directory, and in it, you will find
'benzene_hessian.inp', this time as a job script instead of an input file. Now run this QM
calculation and put the output file (.out) and the formatted checkpoint file (.fchk) in
the same directory.



Creating the force field
++++++++++++++++++++++++++++++++

As benzene does not have any flexible dihedrals, the second step is skipped in this case.
Make sure you have also added this time the **ext_lj** file in *benzene_qforce* and then we can
already create the force field with:

:code:`qforce benzene -o settings`

You can now find the necessary force field files in the *benzene_qforce* directory.
As you will notice, in this case GAFF atom types are used.

|

Choosing the QM software
------------------------

The default QM software is Gaussian. If the user wants to use another QM software
(current alternative: Q-Chem), this can be indicated in the same **settings** file:

.. code-block:: text

    [qm]
    software = qchem


An example for running Q-Force with Q-Chem can be found in the *examples/qchem/default_settings*
directory. This works in the same way as the first example, except the additional argument for
choosing the QM software, as shown above.
