\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{exam-german}
\LoadClassWithOptions{article}
\usepackage[german]{babel}
\usepackage{sms}

\newcommand{\studentheader}{
{\Large

\begin{tabular}{p{0.6\textwidth}p{0.4\textwidth}}
Name & Note\hrulefill \\
& \\
Vorname & Unterschrift des Professors \\
& \\
Studenten Nr. & \hrulefill \\
& \\
Fakultät &  \\
& \\
\end{tabular}%\vspace{1cm}
}

}

\newcommand{\indications}{
\begin{itemize}
\item Keine Hilfe ist erlaubt. Keine elektronischen Hilfsmittel (Natel, Notebook, etc) sind erlaubt.
\item Die Prüfung dauert insgesamt 90 Minuten. Der "Wert" bei der Korrektur jedes Problems entspricht den vorgschlagenen Zeiten.
\item Alle Blätter (Fragebogen und Antworten) müssen abgegeben werden.
\end{itemize}
}

\newcommand{\donepoints}{
\begin{flushright}
Korrektur (nur für die Professoren)


\begin{tabular}{lll}
No & \% & Koef. \\
\custompercentages
\hline
&& \\
Mu & ......... & \totalpercentage \\
\end{tabular}
\end{flushright}
}

\newcommand{\exampreamble}{
{\bf
{\Large
\begin{tabularx}{\textwidth}{|lXr|}
\hline
Universität Freiburg &\vspace{1cm}& \prof \\ 
&& \\
\course && \theyear\\ \hline
\end{tabularx}\vspace{1cm} 
}
Bermerkungen:
}
\indications
\vspace{0.5cm}
\rule{\linewidth}{1pt}
\vspace{0.5cm}
\donepoints
\newpage
}



\newcommand{\content}[1]{
\textbf{\thecontent}
#1
}



\newcommand{\apath}[1]{\url{#1}}
\newcommand{\squote}[1]{``#1''}
\newcommand{\exercice}[1]{\section{#1}}
%\newcommand{\subquestion}[1]{\subsection{#1}}
\makeatletter
\newcommand{\subquestion}{\@ifstar\ssubquestion\osubquestion}
\newcommand{\ssubquestion}[1]{\subsection*{#1}}
\newcommand{\osubquestion}[1]{\subsection{#1}}
\makeatother
\newcommand{\solution}[1]{\section{#1}}
\newcommand{\question}[1]{\subsection{#1}}
\newcommand{\lastVisited}[3]{(accessed #2 #1, #3)}
\newcommand{\biburl}[4]{{\apath{#1} \lastVisited{#2}{#3}{#4}}}
\newcommand{\compilationpath}{./}
\newcommand{\includepath}{\compilationpath}


% Headers and footers
\makeatother
\pagestyle{fancy}

\rhead{
\begin{tabular}{r}
\multirow{4}{1.6cm}{\includegraphics[height=1.1cm]{\compilationpath/logos/\groupelogo}} \\
\\
\\
\\
\end{tabular}
\vspace{0.05mm} }

\chead{
\begin{tabular}{c}
\\
\footnotesize{ \textsl{\textsf{\course\hspace{1mm}\hspace{1mm}\exercisetext}}}  \\
\footnotesize{ \textsl{\textsf{\prof}}}                                                                       \\
\\
\end{tabular}
\vspace{0.05mm} }

\lhead{
\begin{tabular}{l}
\multirow{4}{2.45cm}{\includegraphics[height=1.2cm]{\compilationpath/logos/\unilogo}}  \\
\\
\\
\\
\end{tabular}
\vspace{0.05mm} }

\cfoot{--\hspace{2mm} \thepage\ von \pageref{LastPage} \hspace{2mm}--}
