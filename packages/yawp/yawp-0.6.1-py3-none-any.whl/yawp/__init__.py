#!/usr/bin/python3

'''Yet Another Word Processor, an automatic word processor for text files, with PDF output

                       I sound my barbaric yawp over the roofs of the world
                       
                                                               Walt Whitman

The  name  "yawp"  here  means  Yet  Another Word Processor, and yawp is an
automatic  word  processor  for  plain  text files, with PDF output. If you
really  need  all  the features of a full-fledged WYSIWYG word processor as
LibreOffice  Writer,  yawp is not for you. But if you just want to create a
simple quick-and-dirty no-frills document, with yawp you can:

    • edit a text file by your favorite editor
    • run yawp in order to:
        • backup read format and rewrite the text file
        • export the text file in a PDF file
        • open the PDF file for check or print
    • possibly go back to the editor and update the text file, or finish

                                              ┌───────┐
                                              │backup │
                                              │       │
                                              │ file  │
                                              └─────┬─┘
                                                △   │
                                                │   │restore
                                                │   │ (undo)
                                          backup│   │
                                                │   │
                                                │   ▽
    ┌───────────┐                           ┌───┴───────┐
    │           │         ┌───────┐  read   │           │         ┌───────┐
    │           │  edit   │ text  ├────────▷│           │ export  │ PDF   │
    │  editor   ├────────▷│       │         │   yawp    ├────────▷│       │
    │           │         │ file  │◁────────┤           │         │ file  │
    │           │         └───────┘ rewrite │           │         └───┬───┘
    └───────────┘                           └───────────┘             │
          △                                                           │
          │                          check                            │
          └───────────────────────────────────────────────────────────┘

Main features are:

    • yawp  processes  in place a single text file, hereinafter referred to
      simply as the "file"
    • yawp  before  processing  makes  a  timestamped  backup  of the file,
      allowing undo operation
    • yawp  processing  is  driven by the text in the file and by arguments
      only, not by commands or tags embedded in text
    • yawp justifies text at left and right in:
        • unindented paragraphs
        • dot-marked indented paragraphs (as this one)
    • yawp  accepts  unjustified  pictures  (as  schemas,  tables  and code
      examples) freely intermixed with text
    • yawp  adopts  an  ad  hoc  policy  for  Python  files, formatting the
      docstrings but not the Python code
    • yawp  performs  multi-level  chapter  renumbering 
    • yawp  inserts  an  automatic  contents chapter in the file 
    • yawp  recognizes  relevant  subjects  (quoted  by '"') and inserts an
      automatic index chapter in the file
    • yawp cuts the file in pages, by automatic insertion of two-lines page
      headers
    • yawp  also  has some limited graphic feature, you can sketch pictures
      with  segments (by '`') and arrowheads (by '^'), yawp redraws them by
      proper   graphic  characters  (as  in  the  picture  above)
    • yawp  exports  the  resulting  lines in PDF format, with control over
      character  size  and page layout, and opens for you the generated PDF
      file, allowing preview and printing
    • yawp  corrects  errors  made  by  CUPS-PDF  about  font size and page
      margins, you can use default corrections or redefine them by yawp.cfg
    • yawp is "stable", namely if after a yawp execution you run yawp again
      on  the  same  file with the same arguments, the file content doesn't
      change (except date and time in page headers)

Everything has been kept as simple as possible.

In order to install yawp, type:

    │ $ sudo apt-get -y update
    │ $ sudo apt-get -y install printer-driver-cups-pdf

If you don't have pip, type:

    │ $ sudo apt-get -y install python3-pip

If you type at terminal:

    │ $ pip3 install --upgrade yawp

this command will:

    • install current version of yawp if not present
    • upgrade yawp to the current version if already installed

If you see a message like this:

    │ WARNING: The script yawp is installed in ... which is not on PATH.

don't worry, a reboot should fix the problem.

For any detail, see the yawp-generated "yawp manual" by typing:

    │ $ yawp -H
'''

__version__ = '0.6.1'

__all__ = []

#----- imports -----

from fnmatch import fnmatchcase
from glob import glob
from os import chdir, lstat, popen
from os.path import join as joinpath, split as splitpath, abspath, expanduser, splitext, exists, isfile, isdir
from subprocess import run, PIPE, CalledProcessError
from sys import exit, stdout, stderr
from time import localtime
import readline

#----- path & file functions -----

def longpath(path='.'):
    return abspath(expanduser(path))

def shortpath(path='.'):
    path, home = longpath(path), longpath('~')
    return '~' + path[len(home):] if path.startswith(home) else path

def splitpath4(pathfile):
    '''return (long, short, file, ext), where:

    • long is the long path to file, without ending slash
    • short is the short path to file, without ending slash
    • file is the file name, without extension
    • ext is the file extension, without initial dot

    >>> splitpath4('~/yyy/aaa.bbb.ccc')
    ('/home/xxxx/yyy', '~/yyy', 'aaa.bbb', 'ccc')
    >>> splitpath4('/home/xxxx/yyy/aaa.bbb.ccc')
    ('/home/xxxx/yyy', '~/yyy', 'aaa.bbb', 'ccc')
'''
    long, filext = splitpath(longpath(pathfile))
    short = shortpath(long)
    fil, ext = splitext(filext)
    return long, short, fil, ext[1:]

def listfiles(pattern):
    "return a list of absolute paths to pattern-matching files ('**' in path is allowed)"
    return [file for file in glob(longpath(pattern), recursive=True) if isfile(file)]

def getfile(pattern):
    "return unique pattern-matching file, or '' if not found or ambiguous"
    files = listfiles(pattern)
    return files[0] if len(files) == 1 else ''

def lastfile(pattern):
    "return the newest path_file among matching path_files, or '' if not found"
    files = listfiles(pattern)
    return max((lstat(file).st_mtime, file) for file in files)[1] if files else ''

def localfile(pathfile):
    'return absolute path of a package relative pathfile'
    return joinpath(splitpath(__file__)[0], pathfile)

def listdirs(pattern):
    "return a list of absolute paths to pattern-matching dirs ('**' in path is allowed)"
    return [path for path in glob(longpath(pattern), recursive=True) if isdir(path)]

def getdir(pattern):
    "return unique pattern-matching dir, or '' if not found or ambiguous"
    dirs = listdirs(pattern)
    return dirs[0] if len(dirs) == 1 else ''

def chdir2(pattern='~'):
    '''like os.chdir(), but it accepts '~' '.' '..' '?' '*' '**' etc'''
    paths = listdirs(pattern)
    if not paths:
        print(f'cd: path {pattern!r} not found', file=stderr)
    elif len(paths) > 1:
        print(f'cd: path {pattern!r} is ambiguous', file=stderr)
    else:
        chdir(paths[0])

def newbackfile(file, YmdHMS=None):
    'create a timestamped filename for backup of file'
    path, ext = splitext(longpath(file))
    return f'{path}-%04d.%02d.%02d-%02d.%02d.%02d{ext}' % (YmdHMS or localtime())[:6]

def oldbackfile(file):
    "return filename of the newest timestamped backup of file, or '' if not found"
    path, ext = splitext(longpath(file))
    return lastfile(f'{path}-????.??.??-??.??.??{ext}')

#----- string functions -----

def hold(string, charpattern, default=''):
    'hold charpattern-matching chars in string and replace not matching chars with default'
    return ''.join(char if fnmatchcase(char, charpattern) else default for char in string)

def take(string, charset, default=''):
    'take chars in string found in charset and replace not found chars with default'
    return ''.join(char if char in charset else default for char in string)

def drop(string, charset, default=''):
    'drop chars in string found in charset and replace not found chars with default'
    return ''.join(default if char in charset else char for char in string)

def chars(charpattern):
    'return a sorted string of all charpattern-matching characters'
    kernel = charpattern[1:-1]
    a, z = ord(min(kernel)), ord(max(kernel)) + 1
    return ''.join(chr(j) for j in range(a, z) if fnmatchcase(chr(j), charpattern))

def upperin(string):
    'there is an uppercase letter in string?'
    return string != string.lower()

def lowerin(string):
    'there is a lowercase letter in string?'
    return string != string.upper()

def letterin(string):
    'there is a letter in string?'
    return string != string.lower() or string != string.upper()

def digitin(string):
    'there is a digit in string?'
    return any('0' <= char <= '9' for char in string)

def specialin(string):
    'there is a special (not alphanumeric) character in string?'
    return any(char == char.lower() == char.upper() and not '0' <= char <= '9' for char in string)

def split(string, separator=None):
    'return [] if not string else string.split(separator)'
    return [] if not string else string.split(separator)

def replace(string, *oldsnews):
    'replace(string, a, b, c, d, ...) == string.replace(a, b).replace(c, d)...'
    for j in range(0, len(oldsnews), 2):
        string = string.replace(oldsnews[j], oldsnews[j+1])
    return string

def change(string, olds, news, char='%'):
    'replace char + x with y for x, y in zip(olds, news)'
    trans = {old: new for old, new in zip(olds, news)}
    trans[char] = char # replace char + char with char
    value = ''
    skip = False
    for j, charj in enumerate(string):
        if charj == char:
            try:
                value += trans[string[j+1]]
            except (KeyError, IndexError):
                raise ValueError(string[j:j+2])
            else:
                skip = True
        elif skip:
            skip = False
        else:
            value += charj
    return value

def shrink(string, joinby=' ', splitby=None):
    'eliminate from string all leading, multiple and trailing blanks'
    return joinby.join(string.split(splitby))

def expand(string, width):
    "insert blanks into string until len(string) == width, on error return ''"
    string = shrink(string)
    if len(string) == width:
        return string
    if ' ' not in string[1:] or len(string) > width:
        raise ValueError(f'Impossible to right-justify: {string!r}')
    chars = list(string)
    jchar = 0
    while True:
        if chars[jchar] != ' ' and chars[jchar + 1] == ' ':
            chars.insert(jchar + 1, ' ')
            if len(chars) == width:
                return ''.join(chars)
        jchar = jchar + 1 if jchar < len(chars) - 2 else 0
        
def findchar(string, pattern):
    'return index of first pattern-matching char found in string, or -1 if not found'
    for j, char in enumerate(string):
        if fnmatchcase(char, pattern):
            return j
    else:
        return -1

def rfindchar(string, pattern):
    'return index of last pattern-matching char found in string, -1 if not found'
    for j, char in retroenum(string):
        if fnmatchcase(char, pattern):
            return j
    else:
        return -1

def chrs(jj):
    "return ''.join(chr(j) for j in jj)"
    return ''.join(chr(j) for j in jj)

def ords(string):
    'return [ord(char) for char in string]'
    return [ord(char) for char in string]

def plural(num, sing, plur=''):
    '''return f'1 {sing}' if num == 1 else f'{num} {plur}' if plur else f'{num} {sing}s'

    >>> plural(1, 'cat')
    '1 cat'
    >>> plural(3, 'cat')
    '3 cats'
    >>> plural(1, 'mouse')
    '1 mouse'
    >>> plural(3, 'mouse')
    '3 mouses'
    >>> plural(3, 'mouse', 'mice')
    '3 mice'
'''
    return f'1 {sing}' if num == 1 else f'{num} {plur}' if plur else f'{num} {sing}s'

def edit(item, width=0, ndig=None):
    'convert item to str, justifying numbers at right and anything else at left'
    if isinstance(item, int):
        return str(item).rjust(width)
    elif isinstance(item, float):
        string = str(item if ndig is None else round(item, ndig))
        return (string[:-2] if string.endswith('.0') else string).rjust(width)
    else:
        return str(item).ljust(width)

def table(head, body, ndig=None):
    '''
>>> for line in table(('n', 'n2', 'n3'),
	[(n, n * n, n ** 3) for n in range(11)]):
	print(f'    {line}')

    ┌──┬───┬────┐
    │N │ N2│ N3 │
    ├──┼───┼────┤
    │ 0│  0│   0│
    │ 1│  1│   1│
    │ 2│  4│   8│
    │ 3│  9│  27│
    │ 4│ 16│  64│
    │ 5│ 25│ 125│
    │ 6│ 36│ 216│
    │ 7│ 49│ 343│
    │ 8│ 64│ 512│
    │ 9│ 81│ 729│
    │10│100│1000│
    └──┴───┴────┘
'''
    head = [name.upper() for name in head]
    wids = [len(name) for name in head]
    lenhead = len(head)
    for jrow, row in enumerate(body):
        row = tuple(row[:lenhead]) + (lenhead - len(row)) * ('',)
        for jcol, item in enumerate(row):
            wids[jcol] = max(wids[jcol], len(edit(item, 0, ndig)))
        body[jrow] = row
    yield('┌' + '┬'.join(wid * '─' for wid in wids) + '┐')
    yield('│' + '│'.join(name.center(wid) for name, wid in zip(head, wids)) + '│')
    yield('├' + '┼'.join(wid * '─' for wid in wids) + '┤')
    for row in body:
        yield('│' + '│'.join(edit(item, wid, ndig) for item, wid in zip(row, wids)) + '│')
    yield('└' + '┴'.join(wid * '─' for wid in wids) + '┘')
    
#----- sequence functions -----

def retroenum(sequence):
    'like enumerate(sequence), but backwards from last to first item'
    for j in range(len(sequence) - 1, -1, -1):
        yield j, sequence[j]

def find(sequence, item):
    'return index of first item found in sequence, or -1 if not found'
    for j, itemj in enumerate(sequence):
        if itemj == item:
            return j
    else:
        return -1

def rfind(sequence, item):
    'return index of last item found in sequence, or -1 if not found'
    for j, itemj in retroenum(sequence):
        if itemj == item:
            return j
    else:
        return -1

def get(sequence, index, default=None):
    'return sequence[index] if 0 <= index < len(sequence) else default'
    return sequence[index] if 0 <= index < len(sequence) else default

def unique(sequence):
    'return copy of sequence with no duplicate items'
    olds = set()
    result = []
    for item in sequence:
        if item not in olds:
            olds.add(item)
            result.append(item)
    return result

#----- shell functions -----

def shell(command, mode='p', file=stdout):
    '''
minimal shell, stderr is not piped
if 'C' in mode: print command
if 'p' in mode: pipe stdout and return stdout as a list of lines
if 'P' in mode: pipe stdout, print stdout on file and return stdout as a list of lines
if 'p' not in mode and 'P' not in mode: stdout is not piped, return []
'''
    if 'C' in mode:
        print(f'{shortpath()} --> {command}', file=file)
    command, out = command.strip(), []
    if command == 'cd':
        chdir2()
    elif command.startswith('cd '):
        chdir2(command[3:].strip())
    else:
        result = run(command, shell=True, text=True, stdout=PIPE if 'p' in mode.lower() else None)
        out = [line.rstrip() for line in (result.stdout or '').split('\n') if line.rstrip()]
        if 'P' in mode:
            for line in out:
                print(line, file=file)
    return out

def term(mode='P', file=stdout):
    '''
minimal terminal, type 'exit' to exit, '#'-comments not allowed"
'''
    print(70 * '<')
    while True:
        command = input(f'{shortpath()} --> ')
        if command.split('#')[0].strip() == 'exit':
            break
        shell(command, mode=mode, file=file)
    print(70 * '>')

#----- metric functions -----

in2in = lambda In: float(In) # inch converters
in2pt = lambda In: In * 72.0
pt2in = lambda pt: pt / 72.0
in2cm = lambda In: In * 2.54
cm2in = lambda cm: cm / 2.54
in2mm = lambda In: In * 25.4
mm2in = lambda mm: mm / 25.4

def in2str(inch, units='pt in mm cm', ndig=3):
    'convert float inch into a multi-unit human-readable string'
    return ' = '.join(str(round({'pt': in2pt, 'in': in2in, 'mm': in2mm, 'cm': in2cm}[unit](inch), ndig)) + unit for unit in units.split())
    
def str2in(string):
    '''convert '{float}{suffix}' into an inch float value
on error raise ValueError or KeyError
suffix can be: 'pt' = point, 'in' = inch, 'mm' = millimeter or 'cm' = centimeter
only zero value (as '0', '0.0'...) can lack the suffix
'''
    if tryfunc(float, (string,), 1.0) == 0.0:
        return 0.0
    else:
        return {'pt': pt2in, 'in': in2in, 'mm': mm2in, 'cm': cm2in}[string[-2:]](float(string[:-2]))
      
def str2inxin(string):
    '''convert '{float}x{float}{suffix}' into two inch float values
on error raise ValueError or KeyError
suffix can be: 'pt' = point, 'in' = inch, 'mm' = millimeter or 'cm' = centimeter
'''
    left, right = string.split('x')
    return str2in(left + right[-2:]), str2in(right)

def ratio(string):
    '''convert '{float}/{float}' or '{float}' into a float value
on error raise ValueError or ZeroDivisionError
'''
    if '/' in string:
        over, under = string.split('/')
        return float(over) / float(under)
    else:
        return float(string)
    
#----- numeric functions -----

def frange(start, stop, step, first=True, last=False):
    """float range
>>> list(frange(0, 1, 1/3, last=True))
[0.0, 0.3333333333333333, 0.6666666666666666, 1.0]
>>> list(frange(1, 0, -1/3, last=True))
[1.0, 0.6666666666666667, 0.33333333333333337, 0.0]"""
    start, stop, step = float(start), float(stop), float(step)
    if first:
        yield start
    for j in range(1, round((stop - start) / step)):
        yield start + j * step
    if last:
        yield stop

def linterpol(xyxy, x=None):
    '''linear interpolation (by least squares if len(xyxy) > 2)
xyxy = [(x, y), (x, y),...], len(xyxy) = n
if x is None: return (a, b, err) such that:
    . y = a * x + b is the interpolating line
    . err = sqrt(sum((a * x + b - y) ** 2) / n)
else: return a * x + b
'''
    n = len(xyxy)
    if n == 0: # straight line by [(0.0, 0.0), (1.0, 1.0)]
        return (1.0, 0.0, 0.0) if x is None else x
    elif n == 1: # straight line by [(0.0, 0.0), (x0, y0)]
        x0, y0 = xyxy[0]
        return (y0 / x0, 0.0, 0.0) if x is None else (y0 / x0) * x
    elif n == 2: # straight line by [(x0, y0), (x1, y1)]
        x0, y0 = xyxy[0]
        x1, y1 = xyxy[1]
        d = x1 - x0
        a = (y1 - y0) / d
        b = (y0 * x1 - y1 * x0) / d
        return (a, b, 0.0) if x is None else a * x + b
    else: # n > 2, least squares straight line by [(x0, y0), (x1, y1), (x2, y2), ...]
        sx = sum(x for x, y in xyxy)
        sx2 = sum(x * x for x, y in xyxy)
        sy = sum(y for x, y in xyxy)
        sxy = sum(x * y for x, y in xyxy)
        d = n * sx2 - sx * sx
        a = (n * sxy - sx * sy) / d
        b = (sx2 * sy - sx * sxy) / d
        err = (sum((a * x + b - y) ** 2 for x, y in xyxy) / n) ** 0.5
        return (a, b, err) if x is None else a * x + b

def moving_means(xx, n=7):
    """return [yy[j] = sum(xx[j+1-n:j+1]) / n]
>>> moving_means(list(range(10)))
[0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
>>> moving_means(list(range(10)), 3)
[0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
"""
    return [sum(xx[max(0, j + 1 - n): j + 1]) / min(n, j + 1) for j in range(len(xx))]

#----- messages -----

def inform(message):
    'print an information message and continue'
    print(message, file=stderr)

def warning(message, jline=-1, line=''):
    'print a warning message and continue'
    if jline > -1:
        print(f'LINE {jline+1}: {line}', file=stderr)
    print(f'WARNING: {message}', file=stderr)

def error(message, jline=-1, line=''):
    'print an error message and exit'
    if jline > -1:
        print(f'LINE {jline+1}: {line}', file=stderr)
    exit(f'ERROR: {message}')

#----- other functions -----

def tryfunc(func, args, default=None):
    'try: return func(*args); except: return default'
    try:
        return func(*args)
    except:
        return default

def idem(x):
    'return x'
    return x

def dump(object, undertoo=False):
    items = sorted((key, value) for key, value in object.__dict__.items() if undertoo or not key.startswith('_'))
    length = max((len(key) for key, value in items), default=0)
    for key, value in items:
        value = (in2str if isinstance(value, float) else str)(value)
        print(f'    {edit(key, length)} = {value}')

def show(names, *vars):
    '''
>>> a, b, c = 'xyz'; show('a, b, c', a, b, c)
a = 'x'
b = 'y'
c = 'z'
'''
    names = [name.strip() for name in names.split(',')]
    assert len(names) == len(vars), f'show(): {len(names)} names but {len(vars)} vars'
    for name, var in zip(names, vars):
        if isinstance(var, tuple):
            if not var:
                print(name, '= ()')
            else:
                print(name, '= (')
                for j, v in enumerate(var):
                    print(f'    {v!r},{")"*(j==len(var)-1)}')
        elif isinstance(var, list):
            if not var:
                print(name, '= []')
            else:
                print(name, '= [')
                for j, v in enumerate(var):
                    print(f'    {v!r},{"]"*(j==len(var)-1)}')
        elif isinstance(var, dict):
            if not var:
                print(name, '= {}')
            else:
                print(name, '= {')
                for j, (k, v) in enumerate(sorted(var.items())):
                    print(f'    {k!r}: {v!r},{"}"*(j==len(var)-1)}')
        elif isinstance(var, (set, frozenset)):
            if not var:
                print(name, '= set()')
            else:
                print(name, '= {')
                for j, v in enumerate(sorted(var)):
                    print(f'    {v!r},{"}"*(j==len(var)-1)}')
        else:
            print(f'{name} = {var!r}')

#----- classes -----

class ListDict(dict):
    'dictionary of lists'

    def append(listdict, key, value):
        if key not in listdict:
            listdict[key] = []
        listdict[key].append(value)

    def __getitem__(listdict, key):
        return listdict.get(key, [])

class SetDict(dict):
    'dictionary of sets'

    def add(setdict, key, value):
        if key not in setdict:
            setdict[key] = set()
        setdict[key].add(value)

    def __getitem__(setdict, key):
        return setdict.get(key, set())

#----- end -----
