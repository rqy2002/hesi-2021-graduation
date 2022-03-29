import json
import os
import re
import shutil
import subprocess
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject

def main():
    with open('contents.json', encoding = 'UTF-8') as f:
        contents = json.load(f)
    with open('papers/common/preamble.tex', encoding = 'UTF-8') as f:
        preamble = f.read()
    toc = ''

    # Build articles
    totalPages = 0
    for part in contents['parts']:
        toc += '\\\\tocsection{{{}}}\n'.format(part['name'])

        for article in part['articles']:
            toc += '\\\\tocitem{{{}}}{{{}}}{{{}}}\n'.format(
                article['title'], article['author'], totalPages + 1
            )

            fn = article['fileName']
            print('Building {}.tex ...'.format(fn))

            # Set page number
            with open('papers/common/preamble.tex', mode='w', encoding = 'UTF-8') as f:
                f.write(preamble + 
                    '\n\\AtBeginDocument{{\\setcounter{{page}}{{{}}}}}\n'.format(totalPages + 1))

            # Run latexmk
            cwd = 'papers/{}/'.format(fn)
            proc = subprocess.Popen([
                'latexmk', '-interaction=nonstopmode', '-pdf', '-xelatex', fn + '.tex'
            ], cwd=cwd, stdout=subprocess.DEVNULL)
            proc.wait(timeout=60)

            # Restore page number
            with open('papers/common/preamble.tex', mode='w', encoding = 'UTF-8') as f:
                f.write(preamble)
                
            if (proc.returncode != 0):
                print('============')
                print('{}.tex failed to build.'.format(fn))
                print('============')
                exit(1)
            
            # Read pdf to get the number of pages
            with open('papers/{0}/{0}.pdf'.format(fn), 'rb') as f:
                reader = PdfFileReader(f)
                totalPages += reader.numPages

            if (totalPages % 2 == 1): totalPages += 1

    # Make TOC
    with open('parts/front/front.tex', 'r', encoding = 'UTF-8') as f:
        front = f.read()
    with open('parts/front/front.tex', 'w', encoding = 'UTF-8') as f:
        f.write(re.sub(r'%\s*!\s*TOC', toc, front))
    
    proc = subprocess.Popen([
        'latexmk', '-interaction=nonstopmode', '-pdf', '-xelatex', 'front.tex'
    ], cwd='parts/front', stdout=subprocess.DEVNULL)
    proc.wait(timeout=60)

    with open('parts/front/front.tex', mode='w', encoding = 'UTF-8') as f:
        f.write(front)
                
    if (proc.returncode != 0):
        print('============')
        print('front.tex failed to build.')
        print('============')
        exit(1)
    
    # Merge all PDF files
    writer = PdfFileWriter()
    frontPages = 0

    reader = PdfFileReader(open('parts/front/front.pdf', 'rb'))
    writer.appendPagesFromReader(reader)
    if (reader.numPages % 2 == 1):
        writer.addBlankPage()
    frontPages = reader.numPages + reader.numPages % 2
    
    for part in contents['parts']:
        for article in part['articles']:
            fn = article['fileName']

            reader = PdfFileReader(open('papers/{0}/{0}.pdf'.format(fn), 'rb'))
            writer.appendPagesFromReader(reader)
            if (reader.numPages % 2 == 1):
                writer.addBlankPage()
    
    if (os.path.exists('.temp')):
        shutil.rmtree('.temp')
    os.mkdir('.temp')
    with open('.temp/hesi.pdf', 'wb') as f:
        writer.write(f)

    # Merge page template
    with open('.temp/temp.tex', 'w', encoding = 'UTF-8') as f:
        f.write('\\documentclass{article}\\usepackage[paperwidth=210mm,paperheight=297mm,left=0mm,right=0mm,top=0mm,bottom=0mm]{geometry}\\usepackage{tikz}\\begin{document}\\noindent\\begin{tikzpicture}\\draw[white] (0mm,0mm) rectangle (210mm,-290mm);\\draw[thick](2.5mm,-30mm)--(12.5mm,-30mm)(2.5mm,-265mm)--(12.5mm,-265mm)(207.5mm,-30mm)--(197.5mm,-30mm)(207.5mm,-265mm)--(197.5mm,-265mm)(27.5mm,-5mm)--(27.5mm,-15mm)(27.5mm,-290mm)--(27.5mm,-280mm)(182.5mm,-5mm)--(182.5mm,-15mm)(182.5mm,-290mm)--(182.5mm,-280mm);\\end{tikzpicture}\\end{document}')
    proc = subprocess.Popen([
        'latexmk', '-interaction=nonstopmode', '-pdf', '-xelatex', 'temp.tex'
    ], cwd='.temp', stdout=subprocess.DEVNULL)
    proc.wait(timeout=60)

    print('============')
    print('Adding page margin...')
    print('============')

    writer = PdfFileWriter()
    reader1 = PdfFileReader(open('.temp/hesi.pdf', 'rb'))
    reader2 = PdfFileReader(open('.temp/temp.pdf', 'rb'))
    templatePage = reader2.getPage(0)
    mm = float(templatePage.mediaBox.getWidth() / 210)
    for i in range(reader1.numPages):
        page = PageObject.createBlankPage(width=210 * mm, height=297 * mm)
        page.mergePage(reader2.getPage(0))
        page.mergeTranslatedPage(reader1.getPage(i), 27.5 * mm, 30 * mm)
        writer.addPage(page)
    with open('hesi.pdf', 'wb') as f:
        writer.write(f)

    shutil.rmtree('.temp')

    print('============')
    print('Output written to {} ({} + {} pages)'.format(
        'hesi.pdf', frontPages, totalPages
    ))
    print('============')
            
if __name__ == "__main__":
    main()
