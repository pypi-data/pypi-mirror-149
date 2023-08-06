begin_tikz = """
\\documentclass[tikz,border=2mm]{standalone}

\\tikzset{white border/.style={preaction={draw,white,line width=4pt}}}

\\newcommand{\\nt}[1]{$\langle#1\\rangle$} % node text

\\begin{document}
\\begin{tikzpicture}[x=1.4cm,y=1.8cm]% <-- change this numbers if you need (separations)
% nodes
"""

end_tikz = """
\\end{tikzpicture}
\\end{document}
"""