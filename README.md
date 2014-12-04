NRKSuperDump
============

Python script to download MP4 videos from NRK based on web url
Require Python2, BeautifulSoup, Requests and libav-tools to be installed

Install them as follows:

```bash
$ sudo apt-get install libav-tools
$ sudo pip install BeautifulSoup4
$ sudo pip install Requests
```

HOW TO USE IT:
-------
Run the script as:

```bash
$ python dumper.py
```
You will then be requested to enter a full URL to a NRK Super TV series:

```bash
Enter URL to extract clips from (ex. http://tv.nrksuper.no/serie/bien-maja): 
```

Use for example:

+ http://tv.nrksuper.no/serie/bien-maja
+ http://tv.nrksuper.no/serie/alle-vi-barna-i-bakkebygrenda
+ http://tv.nrksuper.no/serie/blekksprut
+ http://tv.nrksuper.no/serie/georg-krymp
+ http://tv.nrksuper.no/serie/jul-i-skomakergata

![](http://gfx.nrk.no/8sRT_QPaVu33e0-D0PtokwI4jkvXS9yXoyKGrggZeuiw "Jul i skomakergata")

FEATURES TO COME
----------------

+ Parameter for running in batch mode, with textfile containing lines of urls as parameter
+ Parameter for choosing download format and quality
+ Understanding urls better, for example if the url given is a single program and not a serie
  + http://tv.nrksuper.no/program/FBUI50002800/historien-om-den-foerste-paasken
+ What if there are multiple seasons?
