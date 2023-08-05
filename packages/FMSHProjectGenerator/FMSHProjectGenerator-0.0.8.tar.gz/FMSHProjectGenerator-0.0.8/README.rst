FMSH Project Generator
#########################

FMSH Project Generator is a project generation tool for FuDan Microelectronics general-purposed MCU families, including FM33LC0XXX series,
FM33LG0XX series, and much more on their ways. 

FMSH Project Generator allows you to define a project using .YAML files. It can generate IDE project based on the .yaml record, and one should
never spend a lot of time again migrating their projects among these IDEs. it also featured a 'import project' function, which allows user to 
generate their YAML project files more conveniently from presenting IDE projects.

This project is inspired by open-sourced project `project_generator`_.

.. _project_generator: https://github.com/project-generator/project_generator

Installing
-----------

Install and update using `pip`_::

    $ pip install -U FMSHProjectGenerator

.. _pip: https://pip.pypa.io/en/stable/quickstart/

How to use
-------------

User should first create an instance of ProjectGenerator before using any functions::

 from FMSHProjectGenerator import ProjectGenerator

 proj_gen = ProjectGenerator()

Generate IDE Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Following code example demonstrated how to use FMSHProjectGenerator and a project description file(\*.yaml) to generate IDE project 
(Keil5 project for this example, wich will generated in *./my_project_path/MDK-ARM*)::

 from FMSHProjectGenerator.generators import Keil5Generator, Keil5VersionType
 from FMSHProjectGenerator import ProjectGenerator

 # create an instance
 proj_gen = ProjectGenerator()

 # generate KEIL5 project using input YAML
 proj_gen.generate(dest_prj_path='./my_project_path',
                    generator=Keil5Generator(),
                    generator_version=Keil5VersionType.V5,
               	    input_desc='./my_project_path/project.yaml')

User can also generate IDE project using existing dict, which makes the FMSHProjectGenerator easier to work with other project. Just
modify the **input_desc param** to the dict which describes your project::

 proj_desc = { 
    # Your project description here 
 }

 proj_gen.generate(dest_prj_path='./my_project_path',
                    generator=Keil5Generator(),
                    generator_version=Keil5VersionType.V5,
               	    input_desc=proj_desc)

Import IDE Project
^^^^^^^^^^^^^^^^^^^^^

Following code example demonstrated how to use FMSHProjectGenerator to import IDE project (Keil5 project for this example,
which will generated the project YAML file as *./my_project_path/project.yaml*)::

 from FMSHProjectGenerator.converters import Keil5P27Converter
 from FMSHProjectGenerator import ProjectGenerator

 # create an instance
 proj_gen = ProjectGenerator()

 # convert KEIL5 project(will automatically search required project files)
 proj_gen.convert(src_prj_path='./my_project_path',
                    converter=Keil5P27Converter(),
               	    output_file='./my_project_path/project.yaml')

Noet that the **convert** function also return the generated project description in order to cooperate with other programs.

Import and Generate IDE Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After import or generate an IDE project, ProjectGenerator will always retain the latest project information. So it's easy
to import from one IDE Project and generate other IDEs' Project::

 from FMSHProjectGenerator.converters import Keil5Converter
 from FMSHProjectGenerator.generators import IARGenerator, IARVersionType
 from FMSHProjectGenerator import ProjectGenerator

 # create an instance
 proj_gen = ProjectGenerator()

 # convert KEIL5 project
 proj_gen.convert(src_prj_path='./my_project_path',
                    converter=Keil5P27Converter())

 # generate IAR 8.32 project using retained info
 proj_gen.generate(dest_prj_path='./my_project_path',
                    generator=IARGenerator(),
                    generator_version=IARVersionType.V8_32)

User should notice that the 'generate' and 'convert' function can both omit the 'input/output_file' option, which tells
the Project Generator to generate/import IDE Project using/updating retained project information only.

Status of the project
------------------------

The project is now in alpha phase.

