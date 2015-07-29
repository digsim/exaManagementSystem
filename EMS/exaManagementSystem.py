#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################################################
# This script is a simple management system for series made of exercises and solution.                         #
# It is possible to make zipped series for moodle, a zip containing all series. Furthermore one can            #
# generate previews for one exercise/solution. Two handy functions are the make-workbook and the               #
# make-catalogue. The former one creaets a pdf containig all series, each one followed by its solution         #
# just like they were distributed. The latter one create a sort of index of all available exercises in         #
# the system. Each exercise is followed by its solution.                                                       #
#                                                                                                              #
# The structure for a new exercise should be created by using the make-new-exercise function.                  #
# For further help, please refer to the help function of the software.                                         #
# -------------------------------------------------------------------------------------------------------------#
# Author: Andreas Ruppen                                                                                       #                                                                                                                                                             #
# Licensed under the Apache License, Version 2.0 (the "License");                                              #
#   you may not use this file except in compliance with the License.                                           #
#   You may obtain a copy of the License at                                                                    #
#                                                                                                              #
#       http://www.apache.org/licenses/LICENSE-2.0                                                             #
#                                                                                                              #
#   Unless required by applicable law or agreed to in writing, software                                        #
#   distributed under the License is distributed on an "AS IS" BASIS,                                          #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                   #
#   See the License for the specific language governing permissions and                                        #
#   limitations under the License.                                                                             #
################################################################################################################

import sys
import logging
import logging.config
if float(sys.version[:3])<3.0:
    import ConfigParser
else: 
    import configparser as ConfigParser
import shutil
import getopt
import os
import subprocess
import time
from utils import Utils, ZipUtils, LaTeX
from utils.LaTeX import *
from os.path import dirname, join, expanduser
from pkg_resources import Requirement, resource_filename
from distutils.dir_util import copy_tree

class ExaManagementSystem:
    def __init__(self):
        """Do some initialization stuff"""
        self.__CONFIG_DIR = '/etc/ExaManagementSystem/'
        logging.basicConfig(level=logging.ERROR)
        logging.config.fileConfig(
            [join(self.__CONFIG_DIR, 'logging.conf'), expanduser('~/.logging.conf'), 'logging.conf'])
        self.__log = logging.getLogger('exaManagementSystem')
        
        # General settings
        self.__examStructure = ["code", "code/donne", "code/solution", "latex", "latex/ressources", "latex/ressources/figures", "latex/ressources/code"]
        self.__outputDir = "./"
        self.__cwd = os.getcwd()
        self.__keepTempFiles = False
        
        
        smsConfig = ConfigParser.SafeConfigParser()
        self.__log.debug("Reading general configuration from lecture.cfg")
        smsConfig.read([join(resource_filename(__name__, 'data'), 'exam.cfg'), "exam.cfg"])
        #Read the config options
        self.__smscExamOutputDir = smsConfig.get("Config", "examOutputDir")
        self.__smscremoveUnzipped = smsConfig.getboolean("Config", "removeUnzipped")
        self.__smscupdateBibTex = smsConfig.getboolean("Config", "updateBibTex")
        self.__smscopencmd = smsConfig.get("Config", "opencmd")
        self.__smcsdebuglevel = smsConfig.getint("Config", "debugLevel")
        self.__examProperties = smsConfig.get('Config', 'examProperties')
        self.__exerciseDir = smsConfig.get('Config', 'exerciseDir')
        if smsConfig.has_option("Config", "addClearPage"):
            self.__smscaddClearPage = smsConfig.getboolean("Config", "addClearPage")
        else:
            self.__smscaddClearPage = False
        if smsConfig.has_option("Config", "usepdftk"):
            self.__usepdftk = smsConfig.getboolean("Config", "usepdftk")
        else:
            self.__usepdftk = False
            
        # Read the Lecture configuration
        self.__smscname = smsConfig.get("Lecture", "name")
        self.__smsclecturer = smsConfig.get("Lecture", "lecturer")
        self.__smscyear = smsConfig.get("Lecture", "year")
        
        self.__smscsolutiontext = smsConfig.get("Lecture", "solutiontext")
        self.__smscbibtex = smsConfig.get("Lecture", "bibtex")
        self.__noCiteList = []
        if smsConfig.has_option("Lecture", "nocite"):
            self.__noCiteList = smsConfig.get("Lecture", "nocite").split(",")
            
        # Read the logos
        self.__smscunilogo = smsConfig.get("Logo", "unilogo")
        self.__smscgroupelogo = smsConfig.get("Logo", "groupelogo")
        
        # Read the PDF configuration options
        self.__smscpdfkeyword = smsConfig.get("PDF", "pdfkeyword")
        self.__smscpdftitle = smsConfig.get("PDF", "pdftitle")
        self.__smscpdfauthor = smsConfig.get("PDF", "pdfauthor")
        
        # Language Parsing
        self.__languages = {}
        for lang in smsConfig.options('Language'):
            self.__languages[lang] = smsConfig.get('Language', lang)
        
        
        self.__exam = -1
        self.__exercise = -1
        self.__log.setLevel(self.__smcsdebuglevel)
        
    def doCreateNewExercise(self):
        """ Creates a new empty exercise with the next free exercise number"""
        self.__exercise = Utils.nextUnusedExercice(self.__exerciseDir)
        self.__log.debug("Creating Exercice Structure %s", self.__exercise)
        os.chdir(self.__cwd)
        os.mkdir(self.__exerciseDir+"/"+"ex"+str(self.__exercise))
        for directory in self.__examStructure:
            os.mkdir(self.__exerciseDir+"/"+"ex"+str(self.__exercise)+"/"+directory)
        for lang in self.__languages:
            latexfile = open(self.__exerciseDir+"/"+"ex"+str(self.__exercise)+"/latex/exo"+str(self.__exercise)+"-"+lang+".tex", 'w')
            latexfile.write("\exercice{}\n")
            latexfile.write("Put some text here\n")
            latexfile.write("%%% Local Variables:\n")
            latexfile.write("%%% mode: latex\n")
            latexfile.write("%%% TeX-PDF-mode : t\n")
            latexfile.write('%%% ispell-local-dictionary: "fr_CH"\n')
            latexfile.write("%%% End:\n")
            latexfile.close
        latexsolution = open(self.__exerciseDir+"/"+"ex"+str(self.__exercise)+"/latex/exo"+str(self.__exercise)+"-solution.tex", 'w')
        latexsolution.write("\exercice{}\n")
        latexsolution.write("Write down the solution\n")
        latexsolution.write("%%% Local Variables:\n")
        latexsolution.write("%%% mode: latex\n")
        latexsolution.write("%%% TeX-PDF-mode : t\n")
        latexsolution.write('%%% ispell-local-dictionary: "fr_CH"\n')
        latexsolution.write("%%% End:\n")
        latexsolution.close
        
    def doBuildExam(self):
        """Builds just one exam"""
        if self.__smscupdateBibTex:
            self.__doUpdateBibTex()
        seriesConfig = ConfigParser.SafeConfigParser()
        self.__log.debug(self.__examProperties+"/exam"+str(self.__exam)+".cfg")
        seriesConfig.read(self.__examProperties+"/exam"+str(self.__exam)+".cfg")
        titles = seriesConfig.get('Exam', 'titles')
        numbers = seriesConfig.get('Exam', 'exo-numbers')
        semester = seriesConfig.get('Exam', 'semester')
        date = seriesConfig.get('Exam', 'date')
        percentages = seriesConfig.get('Exam', 'percentage')
        
        
        # check if dir exists with os.path.isdir
        if os.path.isdir(os.path.join(self.__outputDir, self.__smscExamOutputDir+str(self.__exam))):
            shutil.rmtree(os.path.join(self.__outputDir, self.__smscExamOutputDir+str(self.__exam)))
        os.mkdir(os.path.join(self.__outputDir, self.__smscExamOutputDir+str(self.__exam)))
        os.mkdir(os.path.join(os.path.join(self.__outputDir, self.__smscExamOutputDir+str(self.__exam)),'donne'))
        os.mkdir(os.path.join(os.path.join(self.__outputDir, self.__smscExamOutputDir+str(self.__exam)),'solution'))

        outputDir=os.path.join(os.path.join(self.__outputDir, self.__smscExamOutputDir+str(self.__exam)),'donne')
        for lang in self.__languages:
            self.__doCreateExam(titles.split(','), numbers.split(','), outputDir, date, percentages, lang, False)

        outputDir =  os.path.join(os.path.join(self.__outputDir, self.__smscExamOutputDir+str(self.__exam)),'solution')
        self.__doCreateSolution(titles.split(','), numbers.split(','), outputDir, date, percentages)

        
    def __doCreateExam(self, titles, numbers, outputDir, date, percentages, language, doPreview):
        texfile = "/tmp/exam-"+language+str(self.__exam)+".tex"
        serie = open(texfile, 'w')
        latex = LaTeX(self.__smsclecturer, self.__smscname, self.__languages[language], 'solution', self.__smscunilogo, self.__smscgroupelogo, self.__smscpdftitle, self.__smscpdfauthor, self.__smscpdfkeyword, self.__noCiteList, language)
        latex.createHeader(serie, titles, date, percentages, doPreview)

        for number in numbers:
            serie.write(r"\newpage"+"\n")
            serie.write(r'\renewcommand{\includepath}{\compilationpath/'+self.__exerciseDir+'/ex'+number+'/latex/ressources}'+'\n')
            exo = open(self.__exerciseDir+"/"+"ex"+number+"/latex/exo"+number+"-"+language+".tex", 'r')
            for line in exo:
                serie.write(line)
            serie.write(r"\clearpage"+"\n")
        latex.createFooter(serie)
        serie.close()

        Utils.doLatex(texfile, outputDir)


    def __doCreateSolution(self, titles, numbers, outputDir, date, percentages):
        texfile = "/tmp/solution"+str(self.__exam)+".tex"
        solution = open(texfile, 'w')
        latex = LaTeX(self.__smsclecturer, self.__smscname, '', 'solution', self.__smscunilogo, self.__smscgroupelogo, self.__smscpdftitle, self.__smscpdfauthor, self.__smscpdfkeyword, self.__noCiteList, 'french')
        latex.createHeader(solution, titles, date, percentages, True)

        for number in numbers:
            solution.write(r"\newpage"+"\n")
            solution.write(r'\renewcommand{\includepath}{\compilationpath/'+self.__exerciseDir+'/ex'+number+'/latex/ressources}'+'\n')
            exo = open(self.__exerciseDir+"/"+"ex"+number+"/latex/exo"+number+"-solution.tex", 'r')
            for line in exo:
                solution.write(line)

        latex.createFooter(solution)
        solution.close()

        Utils.doLatex(texfile, outputDir)
        
        
    def doBuildAllExams(self):
        """Builds all configured Exams"""
        examConfigFiles = os.listdir(self.__examProperties)
        #seriesConfigFiles = Utils.natsort(examConfigFiles)
        examConfigFiles.sort()
        if os.path.isdir(self.__smscExamOutputDir):
            shutil.rmtree(self.__smscExamOutputDir)
        os.mkdir(self.__smscExamOutputDir)
        self.__outputDir = self.__smscExamOutputDir
        for config in examConfigFiles:
            if not config.startswith("."):
                self.__log.debug("Will treat from file: "+config)#+" serie:"+config.split(".")[0].partition("serie")[2])
                #self.__serie=int(config.split(".")[0].partition("serie")[2])
                #self.__log.info("Found Serie "+str(self.__serie)+". Will now build it.")
                self.__exam=config.split("exam")[1].partition(".")[0]
                self.__log.info("Found Exam "+self.__exam+". Will now build it.")
                self.doBuildExam()
                
    def doMakeWorkbook(self):
        """Creates on big pdf containig all passed exams"""
        self.__log.error("Workbook funktionality is not yet implemented")
        return -2
        
    def doMakeCatalogue(self):
        """Creates on big pdf containing all available exercises"""
        outputDir = "Catalogue"
        if os.path.isdir(outputDir):
            shutil.rmtree(outputDir)
        os.mkdir(outputDir)
        file = "/tmp/catalog.tex"
        catalog = open(file, 'w')
        latex = LaTeX(self.__smsclecturer, self.__smscname, '', 'solution', self.__smscunilogo, self.__smscgroupelogo, self.__smscpdftitle, self.__smscpdfauthor, self.__smscpdfkeyword, self.__noCiteList, 'french')
        latex.createHeader(catalog, '', '', '', True)
        catalog.write(r'\renewcommand{\exercice}[1]{\subsection*{Problem: #1}}'+"\n")
        catalog.write(r'\renewcommand{\solution}[1]{\subsection*{Solution: #1}}'+"\n")
        catalog.write(r'\renewcommand{\question}[1]{\subsubsection*{#1}}'+"\n")
        catalog.write(r''+"\n")
        catalog.write(r'\makeatletter'+"\n")
        catalog.write(r'\renewcommand{\section}{\@startsection{section}{3}{2pt}{12pt}{10pt}{\center \huge \sffamily \bfseries}}'+"\n")
        catalog.write(r'\renewcommand{\thesection}{(\roman{section})}'+"\n")
        catalog.write(r'\renewcommand{\thesubsection}{(\roman{subsection})}'+"\n")
        exos = os.listdir(self.__exerciseDir)
        exos = Utils.natsort(exos)
        for exo in exos:
            if exo.find("ex") != -1:
                number = exo[2:]
                catalog.write(r'\section*{Exercise '+number+'}'+"\n")
                catalog.write(r'\renewcommand{\includepath}{\compilationpath/'+self.__exerciseDir+'/ex'+number+'/latex/ressources}'+'\n')
                for lang in self.__languages:
                    catalog.write(r'\renewcommand{\exercice}[1]{\subsection*{Problem '+lang+': #1}}'+"\n")
                    exo = open(os.path.join(os.path.join(self.__exerciseDir, "ex"+number),"latex/exo"+number+"-"+lang+".tex"), 'r')
                    for line in exo:
                        catalog.write(line)
                    exo.close()
                catalog.write(r'\renewcommand{\includepath}{\compilationpath/'+self.__exerciseDir+'/ex'+number+'/latex/ressources}'+'\n')
                catalog.write(r'\renewcommand{\exercice}[1]{\subsection*{Solution: #1}}'+"\n")
                solution = open(os.path.join(os.path.join(self.__exerciseDir, "ex"+number),"latex/exo"+number+"-solution.tex"), 'r')
                for line in solution:
                    catalog.write(line)
                solution.close()
                if self.__smscaddClearPage:
                    catalog.write("\clearpage")
        

        latex.createFooter(catalog)
        catalog.close()
        Utils.doLatex(file, outputDir)
        
    def __doPreviewExam(self):
        """Generate a quick preview (pdf) of one exercise"""
        for lang in self.__languages:
            self. __doCreateExam([], [str(self.__exercise)],  "/tmp", time.strftime("%d.%m.%Y")+" --- 14h00 / PEII --- G120", "20,30,50,50", lang, True)
        
        if self.__usepdftk:
            subprocess.call(["pdftk "+"/tmp/exam-*-1.pdf cat output /tmp/exam.pdf"], shell=True, cwd="./", stdout=open("/dev/stdout", 'w'))
        else:
            subprocess.call(["gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=/tmp/exam.pdf "+"/tmp/exam-*.pdf"], shell=True, cwd="./", stdout=open("/dev/stdout", 'w'))
        if self.__smscopencmd.find(",") == -1:
            cmd = self.__smscopencmd
            arg = [cmd, "/tmp/exam.pdf"]
        else:
            cmd = self.__smscopencmd.split(",")[0]
            arg = self.__smscopencmd.split(",")[1:]
            arg.append("/tmp/exam.pdf")
            arg.insert(0, cmd)
        subprocess.Popen(cmd+" /tmp/exam.pdf", shell=True)
        
    def __doPreviewSolution(self):
        """Generates a quick preview (pdf) of the solution of one exercise"""
        self.__exam = 0
        
        self. __doCreateSolution([], [str(self.__exercise)], "/tmp", time.strftime("%d.%m.%Y")+" --- 14h00 / PEII --- G120", "20,30,50,50")
        if self.__smscopencmd.find(",") == -1:
            cmd = self.__smscopencmd
            arg = [cmd, "/tmp/solution0.pdf"]
        else:
            cmd = self.__smscopencmd.split(",")[0]
            arg = self.__smscopencmd.split(",")[1:]
            arg.append("/tmp/solution0.pdf")
            arg.insert(0, cmd)
        subprocess.Popen(cmd+" /tmp/solution0.pdf", shell=True)

    def __doCreateNewLecture(self, lecturename):
        """Create the directory structure for a new lecture"""
        if os.path.exists(lecturename):
            self.__log.critical("This lecture already exists. Please choose another name")
            return -1
        os.mkdir(lecturename)
        os.mkdir(join(lecturename, 'Exercises'))
        os.mkdir(join(lecturename, 'Exam_properties'))
        f = open(join(join(lecturename, 'Exam_properties'), 'exam'+time.strftime("%Y")+'-1.cfg'),'w')
        f.write('[Exam]\n')
        f.write('titles: Pattern, Théorie, SimJ\n')
        f.write('exo-numbers: 3,1,2\n')
        f.write('semester: Spring\n')
        f.write('percentage: 30,35,25\n')
        f.write('date: '+time.strftime("%d.%m.%Y")+' - 14h / PEII --- C120\n')
        self.__log.debug(resource_filename(__name__, 'data'))
        copy_tree(resource_filename(__name__, 'data'),
                        lecturename)
        
    @staticmethod
    def usage():
        print ('Usage:')
        print (os.path.basename(sys.argv[0])+' [option] <command>') #sys.argv[0]
        print ('\033[1;33mWhere option is one of:\033[0m')
        print ('    -e for specifying an exercise')
        print ('    -s for specifying a particular exam')
        print ('    -u for updating/or not last visited date in bibtex')
        print ('    -k for keeping/or not unzipped files')
        print ('    -t for keeping temporary files in /tmp')
        print ('    -l lecture name')
        print ('\033[1;33mWhere command is one of:\033[0m')
        print ('    make-new-exercise.........................Creates a new exercise structure')
        print ('    build-exam (-s option mandatory)..........Builds all for the specified exam and packs it for moodle')
        print ('    build-all-exams...........................Builds all available exams and packs them for moodle')
        print ('    make-workbook.............................Creates one big pdf wich contains all concatenated exams')
        print ('    make-catalogue............................Creates a pdf containing all exercices')
        print ('    preview-exercise (-e option mandatory)....Previews the specified exercise')
        print ('    preview-solution (-e option mandatory)....Previews the solution for the specified exercise')
        print ('    make-new-lecture..........................Creates the directory structure for a new Lecture')

    def getArguments(self, argv):
        # Parse the command line options
        if len(argv) == 0:
            self.usage()
            sys.exit(3)
        try:
            options, args = getopt.getopt(argv, "e:s:huktl:", ["make-new-exercise", "build-exam", "build-all-exams", "make-workbook", "make-catalogue", "preview-exercise", "preview-solution", "make-new-lecture", "--help"])
        except getopt.GetoptError:
            self.usage()
            sys.exit(2)
        Utils.cleanDSStore("./")
        Utils.doCheckInstall()
        Utils.cleanTempFiles(True)
        self.__log.debug("Parsing options")
        for option, arg in options:
            self.__log.debug("Passed options are  %s  and args are %s", option, arg)

            if option in ["-e"]:
                self.__log.info("Current exercise is: %s", arg)
                self.__exercise=int(arg)
            elif option in ["-s"]:
                self.__log.info("Current exam is: %s", arg)
                self.__exam=arg
            if option in ["-u"]:
                if self.__smscupdateBibTex:
                    self.__smscupdateBibTex=False
                else:
                    self.__log.info("Updating Bibtex Last visited date")
                    self.__smscupdateBibTex=True
            if option in ["-k"]:
                if self.__smscremoveUnzipped:
                    self.__smscremoveUnzipped = False
                else:
                    self.__log.info("Keeping unzipped files")
                    self.__smscremoveUnzipped = True
            if option in ["-t"]:
                self.__keepTempFiles = True
            if option in ["-l"]:
                lecturename = arg
        self.__log.debug("Parsing arguments")
        for option, arg in options:
            self.__log.debug("Passed options are  \"%s\"  and args are \"%s\"", option, arg)
            if option in ["--make-new-exercise"]:
                self.__log.info("Creating a new Exercice")
                self.doCreateNewExercise()
                break
            elif option in ["--build-exam"]:
                if self.__exam == -1:
                    self.__exam = int(raw_input ("Which exam do you want to build? "))
                self.__log.info("Building Exam %s", self.__exam)
                self.doBuildExam()
                self.__log.info("Zipping "+self.__smscExamOutputDir+str(self.__exam)+" into "+self.__smscExamOutputDir+str(self.__exam)+'.zip')
                ZipUtils.myZip(self.__smscExamOutputDir+str(self.__exam), self.__smscExamOutputDir+str(self.__exam)+'.zip', self.__smscExamOutputDir+str(self.__exam))
                if self.__smscremoveUnzipped:
                    shutil.rmtree(self.__smscExamOutputDir+str(self.__exam))
                break
            elif option in ["--build-all-exams"]:
                self.__log.info("Building All Available Exams")
                self.doBuildAllExams()
                self.__log.info("Zipping "+self.__smscExamOutputDir+" into "+self.__smscExamOutputDir+'.zip')
                ZipUtils.myZip(self.__smscExamOutputDir, self.__smscExamOutputDir+'.zip', self.__smscExamOutputDir)
                if self.__smscremoveUnzipped:
                    shutil.rmtree(self.__smscExamOutputDir)
                break
            elif option in ["--make-workbook"]:
                self.__log.info("Building Workbook")
                self.doMakeWorkbook()
                break
            elif option in ["--make-catalogue"]:
                self.__log.info("Creating Catalogue of available Exercices")
                self.doMakeCatalogue()
                break
            elif option in ["--preview-exercise"]:
                if self.__exercise == -1:
                    self.__exercise = int(raw_input ("Which exercise do you want to preview? "))
                self.__log.info("Previewing exercise %s", self.__exercise)
                self.__keepTempFiles = True
                self.__doPreviewExam()
                break
            elif option in ["--preview-solution"]:
                if self.__exercise == -1:
                    self.__exercise = int(raw_input ("Which solution do you want to preview? "))
                self.__log.info("Previewing solution %s", self.__exercise)
                self.__keepTempFiles = True
                self.__doPreviewSolution()
                break
            elif option in ["--make-new-lecture"]:
                self.__doCreateNewLecture(lecturename)
            elif option in ["--help", "-h"]:
                self.usage()
                break
        Utils.cleanTempFiles(self.__keepTempFiles)



if __name__ == "__main__":
    ems = ExaManagementSystem()
    ems.getArguments(sys.argv[1:])
