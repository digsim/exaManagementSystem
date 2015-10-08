# Exam Management System

This is a tool to automatically generate exams based on individual problems. For this, individual problems are stored in the `Exercises` folder (configurable, see `exerciseDir` option), each in  separate sub-folders named `exXX` where `XX` are digits.

Exams are defined using `cfg` files, one for each exam. The `cfg` files contains information like which problems to include. Using LaTeX, the system compiles different problems into exam.

## Installation

### Requirements

Install LaTeX on you system. Make sure the commands `pdflatex`, `bibtex` and `latexmk` are available on the `$PATH` of your operating system. Furthermore the script sometimes uses either `gs` or `pdftk` (configurable, see `usepdftk` option) to combine several PDF documents.

### User Installation
from a terminal launch
```
ruppena@tungdil:~$ sudo pip install exaManagementSystem
```
this will compile and install the project to the Python libraries (eg. `/usr/local/lib/python2.7/dist-packages/Exa_Management_System-1.1-py2.7.egg`). Furthermore it will install a script in `/usr/local/bin/`:
* exaManagementSystem
The configuration and logging.conf are copied into `/etc/ExaManagementSystem/` but it is possible to overwrite them either by placing a file with the same name (but prefixed with a dot eg. `.logging.conf`) in the user home directory or a file with the same name in the current working directory.

### Developer Installation
from a terminal launch
```
ruppena@tungdil:~$ git clone https://github.com/digsim/exaManagementSystem.git
ruppena@tungdil:~$ cd exaManagementSystem
ruppena@tungdil:~$ sudo python setup.py install --record files.txt
```

#### Clean Working directory

To clean the working directory

    sudo python setup.py clean --all
    sudo rm -rf build/ dist/ Exa_Management_System.egg-info/ files.txt

### Bash Completion Installation

If your system supports bash-completion, it can be activated to have option completion for this script. The file `exaManagementSystem-completion.bash` is copied during the installation into the folder `/usr/local/etc/bash_completion.d/` make sure this folder is activated as bash-completion folder in your `.bashrc`, `.bash_login` or `.profile`

```
if ! shopt -oq posix; then
  if [ -f /usr/local/etc/bash-completion ]; then
    . /usr/local/etc/bash-completion
fi
```

### Uninstall
from a terminal launch
```
ruppena@tungdil:~$ sudo pip uninstall exaManagementSystem
ruppena@tungdil:~$ sudo rm -rf /Library/Python/2.7/site-packages/exaManagementSystem*
```
this will remove the package and any associated artifacts.

## Utilization

### Overview

* To get help type following command in the console:
```
ruppena@tungdil:~$ exaManagementSystem --help
```
* To create a new exercise empty structure type:
```
ruppena@tungdil:~$ exaManagementSystem --make-new-problem
```

* To build a new exam:
```
ruppena@tungdil:~$ exaManagementSystem --build-exam -e XX
```
where `XX` is the number identifying a `serieXX.cfg` file in the `Series_properties` folder.

* To create all the exams
```
ruppena@tungdil:~$ exaManagementSystem --build-all-exams
```
This compiles all defines series in the `Exam_properties` folder.

* To generate a quick pdf preview for a given problem
```
ruppena@tungdil:~$ exaManagementSystem --preview-problem -p XX
```
where `XX` identifies on of the `exXX` folders of the `Exercises` folder. The PDF is opened with the viewer specified in the `opencmd` option.

* To generate a quick pdf preview for a given problem solution
```
ruppena@tungdil:~$ exaManagementSystem --preview-solution -p XX
```
where `XX` identifies on of the `exXX` folders of the `Exercises` folder. The PDF is opened with the viewer specified in the `opencmd` option.

* To create a single PDF containing all exams and the associated solutions in the defined order.
```
ruppena@tungdil:~$ exaManagementSystem --make-workbook
```
* To create a single PDF containing the collection of all defined problems
```
ruppena@tungdil:~$ exaManagementSystem --make-catalogue
```

### Use-Case discussion

Start by creating a new Exam-Folder

    exaManagementSystem --make-new-lecture -l GL

This creates a new folder `GL` containing the necessary structure to start creating exam questions for the lecture `GL`.

Adapt the properties in the `exam.cfg` to your needs.

The first step is to create a new exam question

    exaManagementSystem --make-new-problem

This will create the necessary structure and files in the `exerciseDir` folder of the `exam.cfg` file. Fill in the exo-french.tex, exo-german.tex and exo-solution.tex. Repeat this step for all exam quetions you would like to create.

Define a new exam in the `examProperties` (specified in the `exam.cfg` file ) folder. Create a file named `examXXXXXX.cfg`, where XXXXX can be anything, with the following content
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
the XXXXX corresponding to the XXXXX in the `examXXXXX.cfg` file name.



## Exam Definition

By default the properties for an exam are stored in the folder `Exam_properties` (configurable, see `examProperties` option). A typical config file looks like:
```
[Exam]
titles: Pattern, Théorie, SimJ
exo-numbers: 23,1,24
semester: Spring
percentage: 30,35,25
date: 9.6.2015 - 14h / PEII --- C120
```
It contains only one section: `Exam` with five keys:
* The titles key defines the topics of the serie and is a comma separated list. In the final document this will produce an itemize in the serie header.
* The exo-number defines which exercices are selected for this exam. The number references the last (numbered) part of one exercise folder.
* The semester will print the according semester on the first page of the exam.
* The percentage is used for creating the scale to print on the first page of the exam.
* The date contains the exam date and is also printed on the first page of the exam.

## Configuration

The general configuration is hold in a file called `exam.cfg`. It contains a bunch of key values which are grouped into 5 sections: `Config`, `Lecture`, `Logo`, `PDF ` and `Language`.

The `Config` sections defines various folders like the one containing the individual exercises, the output directory, whether `pdftk` or `gs` is used for PDF concatenation or whether the generated files are zipped or not.

The `Lecture` folder defines some strings specific for each lecture like its name and the name of the lecturer. It also contains strings for naming the series and the solutions.

The `Logo` part defines the logos which are shown on the left and right of the header.

The `PDF` part contains options used by LaTeX when creating the PDF file.

The `Language` sections contains for each language a key value pair where the key defines the language and the value defines the exam title in the PDF. Additionally, the key is also used as postfix for the corresponding problem description in this language.

Additionally, the generated `exam.cfg` file is fully documented.

## Exercise Folder Structure

By default the folder containing all exercises is `Exercices` (configurable, see `exoDirName` option). For the system to work, this folder needs to contain a strict hierarchy. It contains several folders, all named "ex" plus a number, eg. `ex1`, `ex2`, ... `ex10` etc. Each of these folders contain only one exercise, its solution plus additional material (which will be zipped) to be distributed together with the series and the solution respectively. The structure is as follows:
```
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
-rw-r--r--  1 ruppena  staff   711B May 28 08:07 exo-french.tex
-rw-r--r--  1 ruppena  staff   774B May 28 08:07 exo-german.tex
-rw-r--r--  1 ruppena  staff   4.2K May 28 08:07 exo-solution.tex
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
```
Each problem is made of two folders: `code` containing additional material to be distributed and `latex` containing the latex code to generate the problem.

Additional material to be distributed in zipped form with the problem needs to be placed in a subfolder `code/donnee` whereas distributed material to be distributed with the solution needs to be placed in a subfolder `code/solution`.

The problem latex code is in a file `exo-[language].tex` where `[language]` is one of the defined languages in the `Language` section of the `exam.cfg` file. The solution is written in a file called `exo-sol.tex`.

You can define as many exam languages as you want. Just be sure that for each used language suffix:
* there is a corresponding entry in the [Language] section of `exam.cfg` configuration
* there exist a `exam-[language].cls` defining the first page of the exam in the corresponding language.
Therefore it would be possible to have another file called `exo-english.tex` and a file `exam-english.cls` together with a definition `english: Exam` in the `exam.cfg`. Thus, the script would produce the exam in three languages: german, french and english. The global config file `exam.cfg` decides which languages are produced.  

The layout of the titlepage can be adapted by modifying the `exam-[language].cls` files. Following keys need to be defined:
* the layout of the points (per exercise / total) can be modified by changing the `\donepoints` variable.
* `\indications` contains general indications (No books, no smart-phone etc.).
* `\exampreamble` puts together the `\indications`, `date`, `university/course` header and `\donepoints`.
* `\studentheader` contains the header where students put their names etc.


Resources used for the latex code are stored in a subfolder `resources`. This folder contains two sub-folders; one for `figures` to store images which are included with

    \includegraphics[height=7cm]{\includepath/figures/inherit.png}

and one to store listings to be included in the LaTeX code.

Furthermore, it contains a subfolder `code` used to store source code which is later included into the LaTeX source with

    \lstinputlisting{\includepath/code_tex/ADT.java}
