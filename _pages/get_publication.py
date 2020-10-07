import subprocess
import sys
import os

MyName = "Hollands"

try:
    link = sys.argv[1]
except IndexError:
    print("Provide ADS URL")
    sys.exit() 

if not link.startswith("https://ui.adsabs.harvard.edu/abs/"):
    link = "https://ui.adsabs.harvard.edu/abs/" + link

if not link.endswith("/abstract"):
    link = link + "/abstract"

subprocess.call(["wget", link], stderr=subprocess.DEVNULL)

if not os.path.exists("abstract"):
    print("Could not download file")
    exit()

authors = []
with open("abstract", 'r') as F:
    for line in F:
        if '<meta name="citation_title"' in line:
            title = line.replace('<meta name="citation_title" content="', '')
            title = title.replace('">', '')
            title = title.strip()
        if '<meta property="article:author"' in line:
            author = line.replace('<meta property="article:author" content="', '')
            author = author.replace('">', '')
            author = author.strip()
            surname, initials = author.split(',')
            initials = initials.replace(' -', '-')
            author = ' '.join([initials.strip(), surname])
            if MyName in author:
                author = f"<strong>{author}</strong>"
            authors.append(author)
        if '<meta name="prism.publicationName"' in line:
            journal = line.replace('<meta name="prism.publicationName" content="', '')
            journal = journal.replace('" />', '')
            journal = journal.strip()
        if '<meta name="prism.publicationName"' in line:
            journal = line.replace('<meta name="prism.publicationName" content="', '')
            journal = journal.replace('" />', '')
            journal = journal.strip()
            if journal == 'Natur':
                journal = 'Nature'
            elif journal == 'NatAs':
                journal = 'Nature Astronomy'
            elif journal == 'Sci':
                journal = 'Science'
            journal = f'<em>{journal}</em>'
        if '<meta name="prism.volume"' in line:
            volume = line.replace('<meta name="prism.volume" content="', '')
            volume = volume.replace('" />', '')
            volume = volume.strip()
        if '<meta name="prism.startingPage"' in line:
            page = line.replace('<meta name="prism.startingPage" content="', '')
            page = page.replace('" />', '')
            page = page.strip()
        if '<meta name="citation_publication_date"' in line:
            date = line.replace('<meta name="citation_date" content="', '')
            date = date.replace('">', '')
            date = date.strip()
            _, year = date.split("/")
os.remove("abstract")

authors = ", ".join(authors)
            
print("## [{}]({})".format(title, link))
print("{}, {} {}, {} ({})".format(authors, journal, volume, page, year))
