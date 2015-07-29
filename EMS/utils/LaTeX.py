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

import logging


class LaTeX:
    
    def __init__(self, lecturer, lecture, exercisetext, solutiontext, unilogo, grouplogo, pdftitle, pdfauthor, pdfkeyword, nociteList, language):
        """initialization stuff"""
        self.__lecturer = lecturer
        self.__lecturename = lecture
        self.__exercisetext = exercisetext
        self.__solutiontext = solutiontext
        self.__unilogo = unilogo
        self.__grouplogo = grouplogo
        self.__pdftitle = pdftitle
        self.__pdfauthor = pdfauthor
        self.__pdfkeyword = pdfkeyword
        self.__nociteList = nociteList
        self.__language = language
        self.__log = logging.getLogger('exaManagementSystem')


    def createHeader(self, file, titles, date, percentages, isSolution):
        if isSolution:
            file.write(r'\documentclass['+self.__language+',a4paper,12pt]{solution}'+"\n")
        else:
            file.write(r'\documentclass['+self.__language+',a4paper,12pt]{exam-'+self.__language+'}'+"\n")

        file.write(r'\newcommand{\prof}{'+self.__lecturer+'}'+"\n")
        file.write(r'\newcommand{\course}{'+self.__lecturename+'}'+"\n")
        
        file.write(r'\newcommand{\theyear}{'+date+'}'+"\n")
        file.write(r'\newcommand{\exercisetext}{'+self.__exercisetext+'}'+"\n")
        
        file.write(r'\newcommand{\solutiontext}{'+self.__solutiontext+'}'+"\n")
    
        file.write(r'\newcommand{\unilogo}{'+self.__unilogo+'}'+"\n")
        file.write(r'\newcommand{\groupelogo}{'+self.__grouplogo+'}'+"\n")
    
        file.write(r'\hypersetup{pdftitle={'+self.__pdftitle+'},pdfauthor={'+self.__pdfauthor+'},pdfkeywords={'+self.__pdfkeyword+"}}\n")
        file.write(r"\begin{document}"+"\n")
        file.write(r"\input{\compilationpath/captionnames}"+"\n")
        file.write(r"% Header of the exercise:"+"\n")
        if not isSolution :
            per = ""
            counter = 1
            totalper = 0
            for percentage in percentages.split(','):
                per += r"&&\\"+"\n"
                per += ""+str(counter)+" & ......... & "+str(percentage)+r"\\"+"\n"
                counter += 1
                totalper += int(percentage)
            file.write(r"\newcommand{\custompercentages}{"+per+"}"+"\n")
            file.write(r"\newcommand{\totalpercentage}{"+str(totalper)+"}"+"\n")
            
            file.write(r"\studentheader"+"\n")
            file.write(r"\exampreamble"+"\n")
    
    
    def createFooter(self, file):
        for bib in self.__nociteList:
            file.write(r'\nocite{'+bib+'}\n')
        file.write(r'\end{document}'+'\n')
        
