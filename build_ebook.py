import json
import os
import re
import shutil
import subprocess

bookmarks_fmt = """BookmarkBegin
BookmarkTitle: {}
BookmarkLevel: 1
BookmarkPageNumber: 1
"""

def err(s):
    print('============')
    print(s)
    print('============')
    exit(1)

def main():
    if (os.path.exists('.temp')):
        shutil.rmtree('.temp')
    os.mkdir('.temp')

    with open('contents.json', encoding = 'UTF-8') as f:
        contents = json.load(f)
    with open('papers/common/preamble.tex', encoding = 'UTF-8') as f:
        preamble = f.read()
    toc = ''
    bookmarks = ''

    # Build articles
    totalPages = 0

    for article in contents['articles']:
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
        proc = subprocess.run([
            'latexmk', '-interaction=nonstopmode', '-pdf', '-xelatex', fn + '.tex'
        ], cwd=cwd, stdout=subprocess.DEVNULL, timeout=60)

        # Restore page number
        with open('papers/common/preamble.tex', mode='w', encoding = 'UTF-8') as f:
            f.write(preamble)
            
        if (proc.returncode != 0):
            err('{}.tex failed to build.'.format(fn))
        
        # Run pdftk to get bookmarks and page
        proc = subprocess.run(['pdftk', fn + '.pdf', 'dump_data'],
                cwd=cwd, capture_output=True, encoding='utf-8', timeout=60)
        
        print(proc.stderr)
        if (proc.returncode != 0):
            err('pdftk {}.pdf failed to run.'.format(fn))

        def repl1(m):
            return 'BookmarkLevel: ' + str(int(m.group(1)) + 1)
        cur_bookmark = '\n'.join(re.findall('Bookmark.*', proc.stdout)) + '\n'
        cur_bookmark = bookmarks_fmt.format(article['title']) + re.sub('BookmarkLevel: (\d+)', repl1, cur_bookmark)

        def repl2(m):
            return 'BookmarkPageNumber: ' + str(int(m.group(1)) + totalPages)
        bookmarks += re.sub('BookmarkPageNumber: (\d+)', repl2, cur_bookmark)
        totalPages += int(re.search(r'NumberOfPages: (\d+)', proc.stdout).group(1))

    # Make TOC
    with open('parts/front/front.tex', 'r', encoding = 'UTF-8') as f:
        front = f.read()
    with open('parts/front/front.tex', 'w', encoding = 'UTF-8') as f:
        f.write(re.sub(r'%\s*!\s*TOC', toc, front))
    
    proc = subprocess.run([
        'latexmk', '-interaction=nonstopmode', '-pdf', '-xelatex', 'front.tex'
    ], cwd='parts/front', stdout=subprocess.DEVNULL, timeout=60)

    with open('parts/front/front.tex', mode='w', encoding = 'UTF-8') as f:
        f.write(front)
                
    if (proc.returncode != 0):
        err('front.tex failed to build.')
    
    # Get page number of front.pdf and update bookmark
    frontPages = 1 # Cover
    proc = subprocess.run(['pdftk', 'parts/front/front.pdf', 'dump_data'],
            capture_output=True, encoding='utf-8', timeout=60)
    if (proc.returncode != 0):
        err('pdftk front.pdf failed to run.')
    frontPages += int(re.search(r'NumberOfPages: (\d+)', proc.stdout).group(1))
    def repl3(m):
        return 'BookmarkPageNumber: ' + str(int(m.group(1)) + frontPages)
    bookmarks = re.sub('BookmarkPageNumber: (\d+)', repl3, bookmarks)

    # Merge all PDF files
    cmd = ['pdftk', 'cover/src/front.pdf', 'parts/front/front.pdf']
    for article in contents['articles']:
        fn = article['fileName']
        cmd.append('papers/{0}/{0}.pdf'.format(fn))
    cmd.extend(['cover/src/back.pdf', 'cat', 'output', '.temp/hesi_ebook.pdf'])
    proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, encoding='utf-8', timeout=60)

    # Update bookmark and output
    if os.path.exists('hesi_ebook.pdf'):
        os.remove('hesi_ebook.pdf')
    with open('.temp/bookmarks.txt', 'w', encoding='utf-8') as f:
        f.write(bookmarks)
    with open('bookmarks.txt', 'w', encoding='utf-8') as f:
        f.write(bookmarks)
    proc = subprocess.run(['pdftk', '.temp/hesi_ebook.pdf', 'update_info', '.temp/bookmarks.txt', 'output', 'hesi_ebook.pdf'],
        stdout=subprocess.DEVNULL, encoding='utf-8', timeout=60)
    
    shutil.rmtree('.temp')

    print('============')
    print('Output written to {} ({} + {} pages)'.format(
        'hesi_ebook.pdf', frontPages, totalPages
    ))
    print('============')
            
if __name__ == "__main__":
    main()
