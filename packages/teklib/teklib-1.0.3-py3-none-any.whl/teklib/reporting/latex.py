from datetime import date
import subprocess as sp
import os
import sys


class latexdocument:
    """ A MARINTEK latex document (base class).
        Don't call directly. Use sub classes:
        sub class report
        sub class beamer
    """
    def __init__(self,name="Statoil.tex", title="Presentation",
                 subtitle="", author="Timothy E. Kendon", 
                 institute="FD GPU UDWP\\"
                            "\\Statoil, Trondheim",
                 date = date.today().isoformat(), subject=""):
        self.name      = name      # This is the filename
        self.title     = title     # This is the main report title
        self.subtitle  = subtitle  # This is the sub title
        self.institute = institute # This is the issuing institute
        self.author    = author    # This is the author
        self.date      = date      # This is the date
        self.subject   = subject   # This is the subject

    def open(self):
        """ Opens a new document and sets preamble.
            self.type is set by the subclass 
        """ 
        # Open document
        self.file = open(self.name, "w")
        # Write generic preamble 
        self.file.write(
            "\\documentclass[]{%s}\n"
            "\\usepackage[absolute,overlay]{textpos}\n"
            "\\usepackage{epsfig}\n"
            "\\usepackage{graphics}\n"
            "\\usepackage[english]{babel}\n"
            "\\usepackage{subfigure}\n"
            "\\usepackage{rotating}\n"
            "\\usepackage[]{hyperref}\n"
            #"\\usepackage{a4wide}\n"
            "\\usepackage{xcolor}\n"
            "\\usepackage{array}\n"
            "\\usepackage{multirow}\n"
            "\\usepackage{tabularx}\n"
            "\\usepackage{lscape}\n"
            "\\usepackage{pdfpages}\n"
            "\\usepackage[latin1]{inputenc}\n"
            "\\usepackage{paralist}\n"
            "\\newenvironment{myinparaenum}\n"
            "{\\begin{inparaenum}[\\hspace{2em}(a)]\\hspace{-2em}\\ignorespaces}\n"
            "{\\end{inparaenum}}\n"
            "\\usepackage{times}\n"
            "\\usepackage[T1]{fontenc}\n"
            "\\setcounter{secnumdepth}{3}\n"
            "\\setcounter{tocdepth}{3}\n" 
            "\\let\\oldtabular=\\tabular\n"
            "\\def\\tabular{\\footnotesize\\oldtabular}\n"
            % self.type)

    def close(self):
        self.file.write("\\end{document}")
        self.file.close()


class report(latexdocument):
    """ A MARINTEK report document """
    def __init__(self,name="MARINTEK", *args , **kwargs):
        name = name + "-Report-%s.tex" % date.today().isoformat()
        latexdocument.__init__(self, name, *args , **kwargs)

    def open(self):
        self.type = "report"
        latexdocument.open(self)       
        

class beamer(latexdocument):
    """ A MARINTEK beamer document """
    def __init__(self,name="MARINTEK", *args , **kwargs):
        name = name + "-Slides-%s.tex" % date.today().isoformat()
        latexdocument.__init__(self, name=name, *args , **kwargs)
        path = os.path.dirname(os.path.abspath( __file__ ))# + "\marintek02.pdf"
        path = "\\\\".join(path.split('\\'))
        sp.Popen('copy "%s\\\\frontpage_statoil_ppt.png" .' % path, shell=True)
        sp.Popen('copy "%s\\\\backpage_statoil_ppt.png" .'  % path, shell=True)
        sp.Popen('copy "%s\\\\statoil.png" .'               % path, shell=True)
        sp.Popen('copy "%s\\\\statoil_ppt.png" .'           % path, shell=True)

    def open(self):
        self.type = "beamer"
        latexdocument.open(self)
        self.file.write(
            "\\mode<presentation>{\n"
            "\\usetheme{Boadilla}\n"
            "\\setbeamercovered{transparent}}\n"
            "\\title[]{%s}\n"
            "\\subtitle{%s}\n"
            "\\author{%s}\n"
            "\\institute[]{%s}\n"
            "\\date[%s]{%s}\n"
            "\\subject{%s}\n"
            "\\AtBeginSubsection[]{\n"
            "\\begin{frame}<beamer>{Outline}\n"
            "\\tableofcontents[currentsection,currentsubsection,subsubsectionstyle=show/shaded]\n"
            "\\end{frame}}\n"
            "\setbeamertemplate{footline}[page number]{}\n"
            "\\setbeamertemplate{navigation symbols}{}\n"
            "\\usebackgroundtemplate{\n"
            "\\includegraphics[width=\\paperwidth,height=\\paperheight]{statoil_ppt.png}}\n"
            "\\newcommand\TitleText[1]{ \n"
            "\\begin{textblock*}{0.7\\paperwidth}(1em,0.8\\textheight)\n"
            "\\raggedright #1\\hspace{.5em}\n"
            "\\end{textblock*}}\n"
            "\\begin{document}\n"            
            "{\n"
            "\\usebackgroundtemplate{\\includegraphics[width=\\paperwidth]{frontpage_statoil_ppt.png}}\n"
            "\\begin{frame}\n"
            "\\TitleText{%s}"
            "\\end{frame}\n"
            "}\n"
            "\\begin{frame}{Outline}\n"
            "\\tableofcontents\n"
            "\\end{frame}\n" %
            (self.title,self.subtitle,self.author,
             self.institute,self.date,self.date,self.subject, self.title))


    def addSection(self,name):
        self.file.write("\\section{%s}\n" % name)
        
    def addSubsection(self,name):
        self.file.write("\\subsection{%s}\n" % name)

    def addSubsubsection(self,name):
        self.file.write("\\subsubsection{%s}\n" % name)
            
    def addFrame(self,title,subtitle,imagelist=None,bullets=None):
        self.file.write(
            "\\begin{frame}{%s}{%s}\n" % (title, subtitle))
        if imagelist is not None:
            for im in imagelist: self.file.write(
                "\\includegraphics[width=1.0\\textwidth]{%s}" % im)
        self.file.write("\\end{frame}\n")
            

    def addBackPage(self):
        self.file.write(
            "{\n"
            "\\usebackgroundtemplate{\\includegraphics[width=\\paperwidth]{backpage_statoil_ppt.png}}\n"
            "\\begin{frame}\n"
            "\\end{frame}\n"
            "}\n")



def main():
    """ Test Program for routines in latex.py """
    wamdoc = beamer(name = "DiffractionAnalysis",
                    title= "Diffraction Analysis for the Njord A TLP")
    wamdoc.open()
    wamdoc.addSection("1st Order Diffraction Analysis")
    Modes = ["Surge","Sway","Heave","Roll","Pitch","Yaw"]

    # Add Wave Excitation Coefficients
    wamdoc.addSubsection("Wave Excitation Force Coefficients")
    for mode in Modes:
        wamdoc.addFrame("Wave Excitation Force Coefficients", 
                        "Platform %s Direction" % mode,
                        imagelist=["figures/Fexc_D_%s.png" % mode])

    # Add R.A.Os
    wamdoc.addSubsection("Response Amplitude Operators")
    for mode in Modes:
        wamdoc.addFrame("Wave Excitation Coefficients", 
                        "Platform %s Direction" % mode,
                        imagelist=["figures/Response_%s.png" % mode])


    # Add Mean Wave Drift Coefficients
    wamdoc.addSubsection("Mean Wave Drift Force Coefficients")
    for mode in Modes:
        wamdoc.addFrame("Mean Wave Drift Force Coefficients", 
                        "Platform %s Direction" % mode,
                        imagelist=["figures/Drift_P_%s.png" % mode])


    # Add Added Mass or Damping Coefficients
    wamdoc.addSubsection("Added Mass and Damping Coefficients")
    Modes = ["11", "15", "22", "24", "33", "42", "44","51","55","66"]
    for mode in Modes:
        wamdoc.addFrame("Added Mass Coefficients", 
                        "A%s" % mode, 
                        imagelist=["figures/A%s.png" % mode])
    for mode in Modes:
        wamdoc.addFrame("Damping Coefficients", 
                        "B%s" % mode, 
                        imagelist=["figures/B%s.png" % mode])

    wamdoc.close()





import sys
if __name__ == '__main__':
    sys.exit(main())
