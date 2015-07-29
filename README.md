# Exam Management System

A utility to manage series. Be sure to install _latexmk_ before using this tool

# Installation

    pip install exaManagementSystem
    
## Developers

### Final installation

from a terminal launch

    sudo python setup.py install --record files.txt

this will compile and install the project to the Python libraries (eg. /usr/local/lib/python2.7/dist-packages/Series_Management_System-1.1-py2.7.egg). Furthermore it will install a script in /usr/local/bin/:
* seriesManagementSystem
The configuration and logging.conf are copied into /etc/SeriesManagementSystem/ but it is possible to overwrite them either by placing a file with the same name (but prefixed with a dot eg. .logging.conf) in the user home directory or a file with the same name in the current working directory.

### Development installation

from a terminal launch

    sudo python setup.py develop --record files.txt
    
does the same as before but, uses links instead of copying files.

## Clean Working directory

To clean the working directory
    
    sudo python setup.py clean --all
    sudo rm -rf build/ dist/ exaManagementSystem.egg-info/ files.txt


# Uninstall

## Method 1
    pip uninstall exaManagementSystem

## Method 2
    cat files.txt |sudo xargs rm -rf

## Method 3

First find the installed package with pip and the uninstall it

    ~/SMS [master|✚ 1…1] 
    12:13 $ pip freeze |grep Series*
    4:Series-Management-System==1.1
    ~/SMS [master|✚ 1…1] 
    12:13 $ sudo pip uninstall Series-Management-System
    Uninstalling Series-Management-System:
      /Library/Python/2.7/site-packages/Series_Management_System-1.1-py2.7.egg
      /usr/local/bin/seriesManagementSystem
    Proceed (y/n)? y
        Successfully uninstalled Series-Management-System
     ~/SMS [master|✚ 1…1] 
    12:13 $
    
# Utilisation

Start by creating a new Exam-Folder

    exaManagementSystem --make-new-lecture -l GL
    
This creates a new folder _GL_ containing the necessary structure to start creating exam questions for the lecture _GL_.

Adapt the properties in the _exam.cfg_ to you needs.

The first step is to create a new exam question

    exaManagementSystem --make-new-exercise
    
This will create the necessary structure and files in the _exerciseDir_ folder of the _exam.cfg_ file. Fill in the exo1-french.tex, exo1-german.tex and exo1-solution.tex. Repeat this step for all exam quetions you would like to create. 

Define a new exam in the _examProperties_ (specified in the _exam.cfg_ file ) folder. Create a file named _examXXXXXX.cfg_, where XXXXX can be anything, with the following content
```
[Exam]
titles: Pattern, Théorie, SimJ
exo-numbers: 23,1,24
semester: Spring
percentage: 30,35,25
date: 9.6.2015 - 14h / PEII --- C120
```
and launch the compliation of the exam with the command
```
exaManagementSystem --build-exam -s XXXXXX
```
the XXXXX corresponding to the XXXXX in the _examXXXXX.cfg_ file name.
     

# Exercises

The exercises are made of two parts:
* a folder containing all exercises.
* a configuration file for each series of exercises and

By default the folder containing all exercises is Exercices. For the system to work this folder has to follow a strict hierarchy. It contains different folders, all named "ex" plus a number, eg. ex1, ex2, ... ex10 etc. Each of these folders contain only one exercise, its solution plus additional material (which will be zipped) to distribute with the series, respectively with the solution. The structure is as follows:
 
    ~:$ ls -lR Exercices/ex1
    total 0
    drwxr-xr-x  4 ruppena  staff   136B Oct  6  2014 code/
    drwxr-xr-x  3 ruppena  staff   204B May 28 08:07 latex/
    
    Exercices/ex1/code:
    total 0
    drwxr-xr-x  2 ruppena  staff    68B Oct  6  2014 donne/
    drwxr-xr-x  2 ruppena  staff    68B Oct  6  2014 solution/
    
    Exercices/ex1/code/donne:
    
    Exercices/ex1/code/solution:
    
    Exercices/ex1/latex:
    total 32
    -rw-r--r--  1 ruppena  staff   711B May 28 08:07 exo1-french.tex
    -rw-r--r--  1 ruppena  staff   774B May 28 08:07 exo1-german.tex
    -rw-r--r--  1 ruppena  staff   4.2K May 28 08:07 exo1-solution.tex
    drwxr-xr-x  4 ruppena  staff   136B Oct  6  2014 ressources/
    
    Exercices/ex1/latex/ressources:
    total 0
    drwxr-xr-x  2 ruppena  staff    68B Oct  6  2014 code/
    drwxr-xr-x  2 ruppena  staff   170B Oct  6  2014 figures/
    
    Exercices/ex1/latex/ressources/code:
    
    Exercices/ex1/latex/ressources/figures:
    total 792
    -rw-r--r--  1 ruppena  staff   233K Jun  7  2011 decorator_uml.png
    -rw-r--r--  1 ruppena  staff    76K Jun  7  2011 transparent_enclosure1.png
    -rw-r--r--  1 ruppena  staff    78K Jun  7  2011 transparent_enclosure2.png
    
Each exercise is made of two folders: code containing additional material to be distributed and latex containing the latex code to generate the serie.
    
Additional material to be distributed in zipped form with the series needs to be placed in a subfolder code/donnee whereas distributed material to be distributed with the solution needs to be placed in a subfolder code/solution.

The exercise latex code is in a file ex[number].tex where number must be the same as used in the folder containing the exercise. The same applies for the solution, which is written in a file called exo[number]sol.tex. 

Resources used for the latex code are stored in a subfolder resources. This folder contains a folder, figures to store images which are included with

    \includegraphics[height=7cm]{\compilationpath/Exercices/ex3/latex/resources/figures/inherit.png}
    

    

By default the properties for a serie are stored in the folder Exam_properties. A typical config file looks like:

    [Exam]
    titles: Pattern, Théorie, SimJ
    exo-numbers: 23,1,24
    semester: Spring
    percentage: 30,35,25
    date: 9.6.2015 - 14h / PEII --- C120

It contains only one section: Exam with five keys:
* The titles key defines the topics of the serie and is a comma separated list. In the final document this will produce an itemize in the serie header. 
* The exo-number defines which exercices are selected for this exam. The number references the last (numbered) part of one exercise folder.
* The semester will print the according semester on the first page of the exam.
* The percentage is used for creating the scale to print on the first page of the exam.
* The date contains the exam date and is also printed on the first page of the exam.