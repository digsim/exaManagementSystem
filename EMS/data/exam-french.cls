\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{exam-french}
\LoadClassWithOptions{article}
\usepackage[french]{babel}
\usepackage{sms}

\newcommand{\studentheader}{
{\Large

\begin{tabular}{p{0.6\textwidth}p{0.4\textwidth}}
Nom & Note\hrulefill \\
& \\
Prénom & Signature du Professeur \\
& \\
No. Etudiant & \hrulefill \\
& \\
Faculté &  \\
& \\
\end{tabular}%\vspace{1cm}
}

}

\newcommand{\indications}{
\begin{itemize}
\item Aucune aide n'est autorisée. Aucun moyen électronique (Natel, ordinateur portable, etc.) n'est autorisé.
\item L'examen a une durée totale de 90 min. Les temps suggérés pour chaque problème correspondent à leur "valeur" lors de la correction.
\item Toutes les feuilles (données, réponses) doivent être rendues.
\end{itemize}
}

\newcommand{\donepoints}{
\begin{flushright}
Correction (seul. pour les professeurs)


\begin{tabular}{lll}
No & \% & Coef. \\
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
Université de Fribourg &\vspace{1cm}& \prof \\ 
&& \\
\course && \theyear\\ \hline
\end{tabularx}\vspace{1cm} 
}
Remarque:
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

\cfoot{--\hspace{2mm} \thepage\ sur \pageref{LastPage} \hspace{2mm}--}
