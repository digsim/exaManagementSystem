\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{solution}
\LoadClassWithOptions{article}
\usepackage{sms}



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

\cfoot{--\hspace{2mm} \thepage\ of \pageref{LastPage} \hspace{2mm}--}
