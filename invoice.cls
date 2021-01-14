\ProvidesClass{invoice}

\LoadClass[12pt]{article}

\usepackage[letterpaper,hmargin=0.79in,vmargin=0.79in]{geometry}
\usepackage[parfill]{parskip} % Do not indent paragraphs
\usepackage{fp} % Fixed-point arithmetic
\usepackage{calc} % Counters for totaling hours and cost
\usepackage{longtable}
\usepackage{multicol}
\usepackage{setspace}

\pagestyle{empty} % No page numbers
\linespread{1.5} % Line spacing

\setlength{\doublerulesep}{\arrayrulewidth} % Double rules look like one thick one

% Command for setting a default hourly rate
\newcommand{\feetype}[1]{
    \textbf{#1}
    \\
}

% Counters for totaling up hours and dollars
\newcounter{hours} \newcounter{subhours} \newcounter{cost} \newcounter{subcost}
\setcounter{hours}{0} \setcounter{subhours}{0} \setcounter{cost}{0} \setcounter{subcost}{0}

% Formats inputed number with 2 digits after the decimal place
\newcommand*{\formatNumber}[1]{\FPround{\cost}{#1}{2}\cost} %

% Returns the total of counter
\newcommand*{\total}[1]{\FPdiv{\t}{\arabic{#1}}{1000}\formatNumber{\t}}

% Create an invoice table
\newenvironment{invoiceTable}{
    % Create a new row from title, unit quantity, unit rate, and unit name
    \newcommand*{\unitrow}[4]{%
         \addtocounter{cost}{1000 * \real{##2} * \real{##3}}%
         \addtocounter{subcost}{1000 * \real{##2} * \real{##3}}%
         \tab ##1 & \formatNumber{##2} ##4 & \$\formatNumber{##3} & \$\FPmul{\cost}{##2}{##3}\formatNumber{\cost}%
         \\
    }
    % Create a new row from title and expense amount
    \newcommand*{\feerow}[2]{%
         \addtocounter{cost}{1000 * \real{##2}}%
         \addtocounter{subcost}{1000 * \real{##2}}%
         ##1 & & \$\formatNumber{##2} & \$\FPmul{\cost}{##2}{1}\formatNumber{\cost}%
         \\
    }

    \newcommand{\subtotalNoStar}{
        {\bf Subtotal} & {\bf \total{subhours} hours} &  & {\bf \$\total{subcost}}%
        \setcounter{subcost}{0}%
        \setcounter{subhours}{0}%
        \\*[1.5ex]
    }
    \newcommand{\subtotalStar}{
        {\bf Subtotal} & & & {\bf \$\total{subcost}}%
        \setcounter{subcost}{0}
        \\*[1.5ex]
    }
    \newcommand{\subtotal}{
         \hline
         \@ifstar
         \subtotalStar%
         \subtotalNoStar%
    }

    % Create a new row from date and hours worked (use stored fee type and hourly rate)
    \newcommand*{\hourrow}[3]{%
        \addtocounter{hours}{1000 * \real{##2}}%
        \addtocounter{subhours}{1000 * \real{##2}}%
        \unitrow{##1}{##2}{##3}{hours}%
    }
    \renewcommand{\tabcolsep}{0.8ex}
    \setlength\LTleft{0pt}
    \setlength\LTright{0pt}
    \begin{longtable}{@{\extracolsep{\fill}\hspace{\tabcolsep}} l r r r }
    \hline
    {\bf Description of Services} & \multicolumn{1}{c}{\bf Quantity} & \multicolumn{1}{c}{\bf Unit Price} & \multicolumn{1}{c}{\bf Amount} \\*
    \hline\hline
    \endhead
}{
    \hline\hline\hline
    & & {\bf Balance Due} & {\bf \$\total{cost}} \\
    \end{longtable}
}
\def \tab {\hspace*{3ex}} % Define \tab to create some horizontal white space
\setlength\columnsep{4cm}
\newenvironment{parties}[2]{
	\singlespacing
	\begin{multicols}{2}{}
		{#1} \columnbreak \\ {#2}
	\end{multicols}
}{}

\newcommand{\payer}[4]{
	{\bf Invoice to:} \\
	\tab #1 \\
	\tab #2 \\
	\tab #3 \\
	\tab #4
}

\newcommand{\payee}[4]{
	{\bf Pay to:} \\
	\tab #1 \\
	\tab #2 \\
	\tab #3 \\
	\tab #4
}