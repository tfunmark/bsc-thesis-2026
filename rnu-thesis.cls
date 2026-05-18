\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{rnu-thesis}[2025/08/27 RNU Bachelor Thesis Class]

% \LoadClass[12pt,a4paper,oneside]{book}
\LoadClass[12pt,a4paper,oneside,openany]{book}

% ===== Packages =====
\RequirePackage{geometry}
\geometry{
  a4paper,
  left=35mm,right=20mm,top=25mm,bottom=25mm,
  headsep=12mm,footskip=15mm
}

\RequirePackage{fontspec}
\setmainfont{Times New Roman}
\RequirePackage{setspace}
\setstretch{1.5}

\RequirePackage{titlesec}
% Heading 1: 16pt bold; Heading 2: 14pt bold, left-aligned
\titleformat{\chapter}[hang]{\bfseries\fontsize{16pt}{16pt}\selectfont}{\thechapter.}{0.8em}{}
\titlespacing*{\chapter}{0pt}{*3}{*1.2}

\titleformat{\section}[hang]{\bfseries\fontsize{14pt}{14pt}\selectfont}{\thesection.}{0.6em}{}
\titlespacing*{\section}{0pt}{*2}{*0.8}

\titleformat{\subsection}[hang]{\bfseries\normalsize}{\thesubsection.}{0.6em}{}
\titlespacing*{\subsection}{0pt}{*1.6}{*0.6}

% Match starred chapter heads (LoF/LoT/LoA/LoL, Abstract, etc.)
\titleformat{name=\chapter,numberless}[hang]
  {\bfseries\fontsize{16pt}{16pt}\selectfont}{}{0pt}{}
\titlespacing*{name=\chapter,numberless}{0pt}{*3}{*1.2}

\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\RequirePackage{tocloft}
\setlength{\cftbeforechapskip}{6pt}

% ---- Unify meta-list/ToC title styling with chapter (16 pt bold) ----
\renewcommand{\cfttoctitlefont}{\bfseries\fontsize{16pt}{16pt}\selectfont}
\renewcommand{\cftloftitlefont}{\bfseries\fontsize{16pt}{16pt}\selectfont}
\renewcommand{\cftlottitlefont}{\bfseries\fontsize{16pt}{16pt}\selectfont}

% Optional: match the after-title spacing to your chapter spacing
\renewcommand{\cftaftertoctitle}{\par\vspace{1.2\baselineskip}}
\renewcommand{\cftafterloftitle}{\par\vspace{1.2\baselineskip}}
\renewcommand{\cftafterlottitle}{\par\vspace{1.2\baselineskip}}

\RequirePackage{graphicx}
\graphicspath{{chapters/chapter1/assets/}{frontmatter/assets/}}


\RequirePackage{listings}

\RequirePackage{caption}
\RequirePackage{ragged2e} % for \RaggedLeft (better ragged-left = flush-right)


\RequirePackage{etoolbox} % harmless if already loaded
\AtBeginEnvironment{lstlisting}{\captionsetup{type=lstlisting}}

% ---- Core math and linking ----
\RequirePackage{amsmath,amssymb,mathtools}
\numberwithin{equation}{chapter}

\RequirePackage{xcolor}          % needed by many listings examples
\RequirePackage[hidelinks]{hyperref}
\RequirePackage[nameinlink,noabbrev]{cleveref}

% ---- Figures/tables helpers used in Appendix A ----
\RequirePackage{subcaption}      % for subfigures
\RequirePackage{longtable}       % multi-page tables
\RequirePackage{pdflscape}       % landscape pages

% ---- TikZ and (optional) pgfplots if available ----
\RequirePackage{tikz}
\IfFileExists{pgfplots.sty}{%
  \RequirePackage{pgfplots}
  \pgfplotsset{compat=1.18}
}{}

% ---- Optional: nicer enum lists used in demos ----
\RequirePackage{enumitem}

\RequirePackage{csquotes}

% ===== Manual placeholders for thesis scope =====
% Users should manually set these values by counting their content
\newcommand{\totalpages}{XX}        % Total pages - set manually
\newcommand{\totaltables}{X}        % Total tables - set manually  
\newcommand{\totalfigures}{X}       % Total figures - set manually
\newcommand{\totalalgorithms}{X}    % Total algorithms - set manually
\newcommand{\totallistings}{X}      % Total listings - set manually
\newcommand{\totalannexes}{X}       % Total annexes - set manually
\newcommand{\totalreferences}{X}    % Total references - set manually

% Global defaults
\captionsetup{
  font=normalsize,
  labelfont=bf,
  labelsep=period,
  skip=6pt
}

% ---- Make listings captions robust with caption package ----
\makeatletter
\providecommand*\lstlistingname{Listing}          % singular
\providecommand*\lstlistlistingname{List of Listings} % list title
\providecommand*\fname@lstlisting{\lstlistingname}    % full-name hook used by caption
\makeatother

% Source line for figures (use before \caption inside a figure)
\newcommand{\figsource}[1]{%
  \captionsetup{type=figure}%
  \caption*{\emph{Source: #1}}%
}


% Commands to set the manual values (users should call these in main.tex)
\newcommand{\setthesisscope}[7]{%
  \renewcommand{\totalpages}{#1}%
  \renewcommand{\totaltables}{#2}%
  \renewcommand{\totalfigures}{#3}%
  \renewcommand{\totalalgorithms}{#4}%
  \renewcommand{\totallistings}{#5}%
  \renewcommand{\totalannexes}{#6}%
  \renewcommand{\totalreferences}{#7}%
}

% English scope line
\newcommand{\thesisscopeEN}{%
  The Bachelor Paper is written in \textbf{\totalpages} pages and contains
  \textbf{\totaltables} tables,
  \textbf{\totalfigures} figures,
  \textbf{\totalalgorithms} algorithms,
  \textbf{\totallistings} listings,
  \textbf{\totalannexes} annexes, and a list of references with
  \textbf{\totalreferences} sources.
}

% Latvian scope line
\newcommand{\thesisscopeLV}{%
  Bakalaura darbs izstrādāts \textbf{\totalpages} lapaspusēs un ietver
  \textbf{\totaltables} tabulas,
  \textbf{\totalfigures} attēlus,
  \textbf{\totalalgorithms} algoritmus,
  \textbf{\totallistings} programmu kodu izdrukas (listings),
  \textbf{\totalannexes} pielikumus, kā arī literatūras sarakstu ar
  \textbf{\totalreferences} avotiem.
}


% --- Teach 'caption' about listings (works for float & non-float)
\makeatletter
\providecommand*\lstlistingname{Listing}
\providecommand*\lstlistlistingname{List of Listings}
\@ifundefined{fname@lstlisting}{%
  \expandafter\newcommand\csname fname@lstlisting\endcsname{\lstlistingname}%
}{}
\makeatother

% Optional but harmless: set default caption style for listings
\captionsetup[lstlisting]{position=top, justification=raggedright,
                          singlelinecheck=false, name=\lstlistingname}




% Set up captions at begin document
\AtBeginDocument{%
  % Figures: caption below, centered
  \captionsetup[figure]{position=bottom, justification=centering, singlelinecheck=false}

  % Tables: caption above, ragged-right (no forced centering)
  \captionsetup[table]{position=top, justification=raggedright, singlelinecheck=false}

  % Algorithms: caption above, ragged-right, name "Algorithm"
  \captionsetup[algorithm]{position=top, justification=raggedright,
                           singlelinecheck=false, name=Algorithm}

  % Listings (listings.sty): caption above, ragged-right, name "Listing"
  \captionsetup[lstlisting]{position=top, justification=raggedright,
                            singlelinecheck=false, name=Listing}
}

% Number algorithms/listings within chapters (Algorithm 2.1, Listing 3.2)
% (safe even if a type is missing)
\RequirePackage{chngcntr}
\makeatletter
\@ifundefined{c@algorithm}{}{ \counterwithin{algorithm}{chapter} }
% \@ifundefined{c@listing}{}{  \counterwithin{listing}{chapter}  }
\@ifundefined{c@lstlisting}{}{ \counterwithin{lstlisting}{chapter} }
\makeatother



\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{indentfirst}
\setlength{\parindent}{1.25cm} % 1 TAB ≈ 1.25 cm

% ===== Meta fields (bilingual) =====
% Names usually identical in both languages, but keep separate hooks if needed
\newcommand{\studentnameLV}{} \newcommand{\studentnameEN}{}
\newcommand{\supervisornameLV}{} \newcommand{\supervisornameEN}{}

\newcommand{\thesistitleLV}{}     \newcommand{\thesistitleEN}{}
\newcommand{\studyprogrammeLV}{}  \newcommand{\studyprogrammeEN}{}
\newcommand{\departmentLV}{}      \newcommand{\departmentEN}{}

\newcommand{\thesisyear}{\number\year}
\newcommand{\thesiscityLV}{RĪGA}  \newcommand{\thesiscityEN}{Riga}

% Set LV metadata
\newcommand{\setthesisinfoLV}[6]{%
  \renewcommand{\thesistitleLV}{#1}%
  \renewcommand{\studentnameLV}{#2}%
  \renewcommand{\supervisornameLV}{#3}%
  \renewcommand{\studyprogrammeLV}{#4}%
  \renewcommand{\departmentLV}{#5}%
  \renewcommand{\thesisyear}{#6}%
}

% Set EN metadata
\newcommand{\setthesisinfoEN}[6]{%
  \renewcommand{\thesistitleEN}{#1}%
  \renewcommand{\studentnameEN}{#2}%
  \renewcommand{\supervisornameEN}{#3}%
  \renewcommand{\studyprogrammeEN}{#4}%
  \renewcommand{\departmentEN}{#5}%
  \renewcommand{\thesisyear}{#6}%
}


% ===== Title page =====

% ===== Logo & Title-Block helpers =====
% Path & size can be changed here instead of inside the macro
\newcommand{\rnulogopath}{a_frontmatter/assets/RNU_large_logo.png}
\newcommand{\rnulogowidth}{52mm} % tweak as needed for wide logo

% 16pt bold helper
\newcommand{\sixteenptbf}{\bfseries\fontsize{16pt}{16pt}\selectfont}
% 12pt normal helper
\newcommand{\twelvept}{\fontsize{12pt}{12pt}\selectfont}


\newcommand{\makethesistitle}{
  \thispagestyle{empty}

  % --- Top-left wide logo ---
  \noindent
  \includegraphics[width=\rnulogowidth]{\rnulogopath}

  \vspace{6mm}

  \noindent
  \begin{tabular*}{\textwidth}{@{}l@{\extracolsep{\fill}}r@{}}
    {\bfseries\fontsize{12pt}{12pt}\selectfont Studiju programma} &
    {\bfseries\fontsize{12pt}{12pt}\selectfont 42484 Informācijas sistēmas (bak)} \\
        % 42345 Uzņēmējdarbības vadība (bak.)\\
        % 42345 Uzņēmējdarbības vadība tūrismā\\
        % 47345 Uzņēmējdarbības vadība (maģ.)\\
        % 42484 Informācijas sistēmas (bak)\\
        % 47483 Datorsistēmas (maģ)
  \end{tabular*}


  \vspace{8mm}

  \begin{center}
    {\bfseries\fontsize{16pt}{16pt}\selectfont Dabaszinātņu un datortehnoloģiju katedra}
      % Vadības, Tiesību, Ekonomikas, Dabaszinātņu un datortehnoloģiju, Starptautiskā biznesa komunikāciju, Kultūras un mākslas\\
  \end{center}

  \vspace{10mm}

  \begin{center}
    {\Large Rīgas Ziemeļvalstu Universitāte}\\[2mm]
    {\large (RZU)}\\[8mm]

    {\bfseries\fontsize{16pt}{16pt}\selectfont \thesistitle}\\[10mm]
    {\bfseries\large BAKALAURA DARBS}\\[18mm]

    \begin{tabular}{@{}p{6cm}p{8cm}@{}}
      Students:& \studentname\\[2mm]
      Darba vadītājs:& \supervisorname\\
    \end{tabular}

    \vfill
    {\thesiscity\ \thesisyear}
  \end{center}

  \clearpage
}

% ===== Front-matter formatting =====
\providecommand{\frontmatterpage}{}

% ===== Utilities =====
% Unnumbered chapter that appears in ToC
\newcommand{\unchapter}[1]{%
  \chapter*{#1}\addcontentsline{toc}{chapter}{#1}%
}

% Lists of Figures/Tables optional toggle (rename to avoid TeX primitive \showlists)
\newif\ifshowlotlof
\showlotloffalse
\newcommand{\enablelists}{\showlotloftrue}

% Bibliography (simple manual list)
\newcommand{\printliterature}{%
  \chapter*{Literature}\addcontentsline{toc}{chapter}{Literature}
  \input{chapters/references.tex}
}

\endinput
