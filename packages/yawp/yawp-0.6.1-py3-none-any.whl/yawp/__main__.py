#!/usr/bin/python3

#----- imports -----

from .__init__ import __version__ as version, __doc__ as description
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from fnmatch import filter
from warnings import simplefilter
from sys import argv, stdout, stderr
from time import localtime, sleep
from os.path import join as joinpath, split as splitpath, isfile
from .__init__ import longpath, shortpath, splitpath4, listfiles, getfile, lastfile, localfile
from .__init__ import listdirs, getdir, chdir2, newbackfile, oldbackfile
from .__init__ import hold, take, drop, chars, upperin, lowerin, letterin, digitin, specialin, split, replace, change
from .__init__ import shrink, expand, findchar, rfindchar, chrs, ords, edit, plural, linterpol
from .__init__ import inform, warning, error, show
from .__init__ import in2in, in2pt, pt2in, in2cm, cm2in, in2mm, mm2in, in2str, str2in, str2inxin, ratio
from .__init__ import retroenum, find, rfind, shell, CalledProcessError, get, term, tryfunc, dump, ListDict, SetDict

#----- global data -----

class Container: pass
arg = Container() # container for arguments and other scalar global data

#----- constants -----

EMPT, CODE, TEXT, PICT, CONT, INDX, CHP1, CHP2, HEA1, HEA2 = range(10) # values for kind
KINDS = 'EMPT CODE TEXT PICT CONT INDX CHP1 CHP2 HEA1 HEA2'.split() # labels for kind
JLIN, KIND, JPAG, LPIC, LINE = range(5) # positions in buf.input[j] and buf.output[j]
PREF, TITL, JOUT = range(3) # positions in buf.contents[j]
FORMFEED = '\f' # page header, first character of first line
MACRON = '¯' # page header, second line, dashed
QUOTES = "'" + '"' # single and double quotation marks
INDENT = 4 * ' ' # tab indentation
MAX_QUALITY = 5 # max print quality
PAPERSIZE = { # names for -S
    'HALF LETTER':  '5.5x8.5in',
    'LETTER':       '8.5x11.0in',
    'LEGAL':        '8.5x14.0in',
    'JUNIOR LEGAL': '5.0x8.0in',
    'LEDGER':       '11.0x17.0in',
    'TABLOID':      '11.0x17.0in',
    'A0':  '841x1189mm',
    'A1':  '594x841mm',
    'A2':  '420x594mm',
    'A3':  '297x420mm',
    'A4':  '210x297mm',
    'A5':  '148x210mm',
    'A6':  '105x148mm',
    'A7':  '74x105mm',
    'A8':  '52x74mm',
    'A9':  '37x52mm',
    'A10': '26x37mm',
    'B0':  '1000x1414mm',
    'B1':  '707x1000mm',
    'B1+': '720x1020mm',
    'B2':  '500x707mm',
    'B2+': '520x720mm',
    'B3':  '353x500mm',
    'B4':  '250x353mm',
    'B5':  '176x250mm',
    'B6':  '125x176mm',
    'B7':  '88x125mm',
    'B8':  '62x88mm',
    'B9':  '44x62mm',
    'B10': '31x44mm'}
#
xyxy = {k: [] for k in 'plm llm prm lrm ptm ltm pbm lbm pcw lcw pch lch'.split()}
XYXY = '''
#----- yawp configuration file -----

plm 10mm 16mm # portrait left margin
plm 20mm 24mm 
plm 30mm 35mm 
plm 40mm 43mm 
plm 50mm 52mm
plm 60mm 62mm 
plm 70mm 72.5mm 
plm 80mm 83mm 
plm 90mm 92mm 
plm 100mm 101mm 

llm 10mm 20.5mm # landscape left margin
llm 20mm 29.5mm 
llm 30mm 39mm 
llm 40mm 48mm 
llm 50mm 57mm 
llm 60mm 66.5mm 
llm 70mm 75.5mm 
llm 80mm 84.5mm 
llm 90mm 94mm 
llm 100mm 104mm 

prm 10mm 15mm # portrait right margin
prm 20mm 25.5mm 
prm 30mm 34.5mm 
prm 40mm 44.5mm 
prm 50mm 54.5mm 
prm 60mm 64.5mm 
prm 70mm 72mm 
prm 80mm 81mm 
prm 90mm 91.5mm 
prm 100mm 100mm 

lrm 10mm 22mm # landscape left margin
lrm 20mm 30mm 
lrm 30mm 40mm 
lrm 40mm 49.5mm 
lrm 50mm 58mm 
lrm 60mm 68mm 
lrm 70mm 77.5mm 
lrm 80mm 86mm 
lrm 90mm 96mm 
lrm 100mm 104mm 

ptm 10mm 11.5mm # portrait top margin
ptm 20mm 21mm 
ptm 30mm 30.5mm 
ptm 40mm 39.5mm 
ptm 50mm 49mm 
ptm 60mm 59mm 
ptm 70mm 68mm 
ptm 80mm 77.5mm 
ptm 90mm 87mm 
ptm 100mm 96mm 

ltm 10mm 11mm # landscape top margin
ltm 20mm 20.5mm 
ltm 30mm 30mm 
ltm 40mm 39mm 
ltm 50mm 48.5mm 
ltm 60mm 57.5mm 
ltm 70mm 67mm 
ltm 80mm 76mm 
ltm 90mm 85mm 
ltm 100mm 95mm 

pbm 10mm 24mm # portrait bottom margin
pbm 20mm 34mm 
pbm 30mm 43mm 
pbm 40mm 52.5mm 
pbm 50mm 62mm 
pbm 60mm 71mm 
pbm 70mm 81mm 
pbm 80mm 90mm 
pbm 90mm 100mm 
pbm 100mm 109.5mm 

lbm 10mm 24mm # landscape bottom margin
lbm 20mm 32mm 
lbm 30mm 42mm 
lbm 40mm 52mm 
lbm 50mm 60mm 
lbm 60mm 70mm 
lbm 70mm 80mm 
lbm 80mm 88mm 
lbm 90mm 99mm 
lbm 100mm 107mm 

pcw 100mm 94.674mm # portrait character width

lcw 100mm 92.200mm # landscape character width

pch 100mm 94.358mm # portrait character height

lch 100mm 92.647mm # landscape character height
'''

#----- classes -----

class Paragraph:

    def __init__(par):
        par.string = ''
        par.indent = 0
        
    def append(par, string, indent=0):
        if par.string:
            par.string += ' ' + shrink(string)
        else:
            par.string = shrink(string)
            par.indent = indent

    def flush(par, jlin):
        if not par.string:
            return
        prefix = (par.indent - 2) * ' ' + '• ' if par.indent else ''
        while len(par.string) > arg.chars_per_line - par.indent:
            jchar = rfind(par.string[:arg.chars_per_line-par.indent+1], ' ')
            if jchar <= 0:
                error('Impossible to left-justify', jlin, string)
            string, par.string = par.string[:jchar], par.string[jchar+1:]
            if not arg.left_only:
                try:
                    string = expand(string, arg.chars_per_line - par.indent)
                except ValueError as error_message:
                    error('Impossible to right-justify', jlin, string)
            buf.append(jlin, TEXT, 0, 0, prefix + string)
            prefix = par.indent * ' '
        if  par.string:
            buf.append(jlin, TEXT, 0, 0, prefix + par.string)
            par.string = ''

par = Paragraph()

class Buffer:

    def __init__(buf):
        buf.input = [] # [[jlin, 0, 0, 0, line]] # input buffer
        buf.output = [] # [[jlin, kind, jpag, lpic, line]] # output buffer
        # jlin: line index in buf.input, for error message
        # kind: kind of line: CODE, TEXT, PICT, CONT, INDX, CHP1, CHP2, HEA1, HEA2
        # jpag: page number
        # lpic: lines in picture (in first line of pictures only, else 0)
        # line
        buf.contents = [] # [[pref, titl, jout]]
        # pref: chapter numbering, first word in chapter line as '1.', '1.1.'...
        # titl: rest of chapter line
        # jout: position of chapter line in buf.output
        buf.contents_start, buf.contents_stop = -1, -1 # start and stop of contents in output
        buf.qsub_jouts = SetDict() # {subject: {jout}}
        # subject: subject between double quotes
        # jout: position of subject in buf.output
        buf.uqsub_jouts = SetDict() # {subject: {jout}}
        # subject: subject not between double quotes
        # jout: position of subject in buf.output
        buf.index_start, buf.index_stop = -1, -1 # start and stop of index in output
        buf.subjects = set()

    def __len__(buf):
        return len(buf.output)

    def append(buf, jlin, kind, jpag, lpic, line):
        buf.output.append([jlin, kind, jpag, lpic, line])

    def char(buf, jout, jchar):
        'return buf.output[jout][LINE][jchar], used by redraw_segments() and redraw_arroheads()'
        if jout < 0 or jchar < 0:
            return ' '
        else:
            try:
                line = buf.output[jout][LINE]
                return line[jchar] if buf.output[jout][KIND] == PICT else ' '
            except IndexError:
                return ' '

    def dump(buf):
        'for debug only'
        print(f'\n' + '.' * 72)
        print(f'... contents_start = {buf.contents_start}, contents_stop = {buf.contents_stop} ...')
        print(f'... index_start = {buf.index_start}, index_stop = {buf.index_stop} ...')
        for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
            print(jout, ':', (jlin, KINDS[kind], jpag, lpic, line))
        print('\n... contents ...')
        for jout, rec in enumerate(buf.contents):
            print(jout, ':', rec)
        print('\n... index ...')
        for jout, rec in enumerate(buf.index):
            print(jout, ':', rec)
        print('.' * 72)

buf = Buffer()

#----- functions -----

def get_level_title(line):
    words = line.upper().split()
    if not words:
        return 0, ''
    status = 0; level = 0
    for char in words[0]:
        if status == 0:
            if '0' <= char <= '9': status = 1
            else: return (0, ' '.join(words))
        else: # status == 1
            if '0' <= char <= '9': pass
            elif char == '.': level += 1; status = 0
            else: return (0, ' '.join(words))
    return (level, ' '.join(words[1:])) if status == 0 and level > 0 else (0, ' '.join(words))
            
def get_margin_margin2(letter, margin):    
    x = tryfunc(str2in, (margin,), -1.0)
    if x < 0.0:
        error(f'Wrong -{letter} {margin}')
    if x < str2in('2cm') and arg.verbose:
        warning(f'-{letter} {margin} < 2cm, you may get unexpected results')
    margin = x
    if arg.calibration:
        margin2 = margin
    else:
        margin2 = max(0.0, linterpol(xyxy['pl'[arg.landscape] + letter.lower() + 'm'], margin))
        if arg.verbose: inform(f'Correct: -{letter} {in2str(margin2)}')
    return margin, margin2

#----- actions -----

def get_arguments():
    parser = ArgumentParser(prog='yawp', formatter_class=RawDescriptionHelpFormatter, description=description)
    add = parser.add_argument
    # general arguments
    add('-H','--manual', action='store_true', help='open yawp-generated PDF manual and exit')
    add('-V','--version', action='version', version=f'yawp {version}')
    add('-v','--verbose', action='store_true', help='display information messages on stderr')
    add('-s','--echo-shell', action='store_true', help='display invoked Unix commands on stderr')
    add('-N','--no-format', action='store_true', help="backup but don't format (default: backup and format)")
    add('-U','--undo', action='store_true', help="restore the file from last backup (default: backup and format)")
    add('-g','--graphics', action='store_true', help="redraw '`'-segments and '^'-arrowheads")
    add('-p','--print-file', action='store_true', help="at end print file on stdout")
    # formatting arguments
    add('-w','--chars-per-line', default='0', help="line width in characters per line (default: '0' = automatic)")
    add('-l','--left-only', action='store_true', help="justify text lines at left only (default: at left and right)")
    add('-c','--contents-title', default='contents', help="title of contents chapter (default: 'contents')")
    add('-i','--index-title', default='index', help="title of index chapter (default: 'index')")
    # paging arguments
    add('-f','--form-feed', action='store_true', help="insert page headers on full page")
    add('-F','--form-feed-chap', action='store_true', help="insert page headers on full page and before contents index and level-one chapters")
    add('-e','--even-left', default='%n/%N', help="headers of even pages, left (default: '%%n/%%N')")
    add('-E','--even-right', default='%f.%e %Y-%m-%d %H:%M:%S', help="headers of even pages, right (default: '%%f.%%e %%Y-%%m-%%d %%H:%%M:%%S')")
    add('-o','--odd-left', default='%c', help="headers of odd pages, left (default: '%%c')")
    add('-O','--odd-right', default='%n/%N', help="headers of odd pages, right (default: '%%n/%%N')")
    add('-a','--all-pages-E-e', action='store_true', help="put in all page headers -E at left and -e at right")
    # PDF exporting arguments
    add('-P','--file-pdf', default='%P/%f.pdf', help="at end export and open this PDF file ('0' = no export, default: '%%P/%%f.pdf')")
    add('-W','--char-width', default='0', help="character width (pt/in/mm/cm, default: '0' = automatic)")
    add('-A','--char-aspect', default='3/5', help="character aspect ratio = char width / char height ('1' = square grid, default: '3/5')")
    add('-S','--paper-size', default='A4', help="portrait paper size (width x height, pt/in/mm/cm, default: 'A4' = '210x297mm'")
    add('-Z','--landscape', action='store_true', help="turn page by 90 degrees (default: portrait)")
    add('-L','--left-margin', default='2cm', help="left margin (pt/in/mm/cm, default: '2cm')")
    add('-R','--right-margin', default='-L', help="right margin (pt/in/mm/cm, default: '-L')")
    add('-T','--top-margin', default='2cm', help="top margin (pt/in/mm/cm, default: '2cm')")
    add('-B','--bottom-margin', default='-T', help="bottom margin (pt/in/mm/cm, default: '-T')")
    add('-C','--calibration', action='store_true', help="don't correct character size and page margins")
    # positional argument
    add('file', nargs='?', help='text file to be processed')
    # arguments --> arg.*
    parser.parse_args(argv[1:], arg)

def get_configuration():
    if arg.calibration:
        if arg.verbose: inform('Correct: -C is turned on, no correction is performed')
    else:
        yawp_cfg = longpath('~/.yawp/yawp.cfg')
        if isfile(yawp_cfg):
            config = open(yawp_cfg)
            if arg.verbose: inform("Correct: corrections read from '~/.yawp/yawp.cfg'")
        else:
            config = XYXY.split('\n')
            if arg.verbose: inform("Correct: '~/.yawp/yawp.cfg' not found, default corrections")
        for jline, line in enumerate(config):
            for stmt in [s.strip() for s in line.split('#')[0].split(';')]:
                if stmt:
                    try:
                        k, y, x = stmt.split()
                        x, y = str2in(x), str2in(y)
                        assert x >= 0.0 <= y
                        xyxy[k].append((x, y))
                    except (ValueError, KeyError, AssertionError):
                        error(f'Wrong line in {shortpath(yawp_cfg)!r}', jline, line.rstrip())
    
def check_arguments():
    arg.start_time = localtime()[:]
    # -s
    arg.shell_mode = 'CP' if arg.echo_shell else 'p'
    # -H
    if arg.manual:
        yawp_pdf = localfile('docs/yawp.pdf')
        shell(f'xdg-open {yawp_pdf}', mode=arg.shell_mode, file=stderr)
        exit()
    # file
    if not arg.file:
        error("Mandatory positional argument file, not found")
    arg.file = longpath(arg.file)
    arg.PpfeYmdHMS = splitpath4(arg.file) + tuple(('%04d %02d %02d %02d %02d %02d' % arg.start_time[:6]).split())
    # -U -N
    if arg.undo and arg.no_format:
        error("You can't set both -U and -N")
    # -w >= 0
    w = tryfunc(int, (arg.chars_per_line,), -1)
    if w < 0:
        error(f'Wrong -w {arg.chars_per_line}')
    arg.chars_per_line = w
    # -c -i
    if not arg.contents_title:
        error("Wrong -c ''")
    if not arg.index_title:
        error("Wrong -i ''")
    arg.contents_title = shrink(arg.contents_title).upper()
    arg.index_title = shrink(arg.index_title).upper()
    if arg.contents_title == arg.index_title:
        error(f"Wrong -c = -i {arg.contents_title}")
    # -f -F
    if arg.file.endswith('.py'):
        if arg.form_feed:
            inform("Python file, -f turned off")
            arg.form_feed = False
        if arg.form_feed_chap:
            inform("Python file, -F turned off")
            arg.form_feed_chap = False
    arg.form_feed = arg.form_feed or arg.form_feed_chap
    # -e -E -o -O
    for char, argx in zip('eEoO', [arg.even_left, arg.even_right, arg.odd_left, arg.odd_right]):
        try:
            change(argx, 'PpfeYmdHMSnNc', 'PpfeYmdHMSnNc', '%')
        except ValueError as illegal:
            error(f'Wrong -{char} {argx!r}, illegal {str(illegal)!r}')
    # -P
    if tryfunc(float, (arg.file_pdf,), -1) == 0.0:
        arg.file_pdf = ''
    if arg.file_pdf:
        try:
            arg.file_pdf = change(arg.file_pdf, 'PpfeYmdHMS', arg.PpfeYmdHMS, '%')
        except ValueError as illegal:
            error(f'Wrong -P {shortpath(arg.file_pdf)!r}, illegal {str(illegal)!r}')
        arg.file_pdf = longpath(arg.file_pdf)
        if not arg.file_pdf.endswith('.pdf'):
            error(f"Wrong -P {shortpath(arg.file_pdf)!r}, doesn't end with '.pdf'")
    # -W >= 0
    W = tryfunc(str2in, (arg.char_width,), -1.0)
    if W < 0.0:
        error(f'Wrong -W {arg.char_width}')
    arg.char_width = W
    # -A > 0
    A = tryfunc(ratio, (arg.char_aspect,), -1.0)
    if A <= 0.0:
        error(f'Wrong -A {arg.char_aspect}')
    arg.char_aspect = A
    # -S 0 < Sw <= Sh
    Sw, Sh = tryfunc(str2inxin, (PAPERSIZE.get(arg.paper_size.upper(), arg.paper_size),), (-1.0, -1.0))
    if not 0 < Sw <= Sh:
        error(f'Wrong -S {arg.paper_size}')
    arg.paper_width, arg.paper_height = Sw, Sh
    # -Z
    if arg.landscape:
        arg.paper_width, arg.paper_height = arg.paper_height, arg.paper_width
    # -L -R
    if arg.right_margin == '-L':
        arg.right_margin = arg.left_margin
    arg.left_margin, arg.left_margin2 = get_margin_margin2('L', arg.left_margin)
    arg.right_margin, arg.right_margin2 = get_margin_margin2('R', arg.right_margin)
    arg.free_width = arg.paper_width - arg.left_margin - arg.right_margin
    if arg.free_width <= 0:
        error('-L and/or -R too big, no horizontal space on paper')
    # -T -B
    if arg.bottom_margin == '-T':
        arg.bottom_margin = arg.top_margin
    arg.top_margin, arg.top_margin2 = get_margin_margin2('T', arg.top_margin)
    arg.bottom_margin, arg.bottom_margin2 = get_margin_margin2('B', arg.bottom_margin)
    arg.free_height = arg.paper_height - arg.top_margin - arg.bottom_margin
    if arg.free_height <= 0:
        error('-T and/or -B too big, no vertical space on paper')

def restore_file():
    backfile = oldbackfile(arg.file)
    if not backfile:
        error(f'Backup file for file {shortpath(arg.file)!r} not found')
    shell(f'rm -f {arg.file!r}', mode=arg.shell_mode, file=stderr)
    shell(f'mv {backfile!r} {arg.file!r}', mode=arg.shell_mode, file=stderr)
    if arg.verbose: inform(f'Restore: {shortpath(arg.file)!r} <-- {shortpath(backfile)!r}')

def read_file_into(buf_records):
    if not isfile(arg.file):
        error(f'File {shortpath(arg.file)!r} not found')
    header_lines, body_lines, arg.num_pages, max_body_width, max_header_width = 0, 0, 1, 0, 0
    for jlin, line in enumerate(open(arg.file)):
        line = line.replace('\t', INDENT).rstrip()
        if line.startswith(FORMFEED):
            arg.num_pages += 1
            max_header_width = max(max_header_width, len(line) - 1)
            header_lines += 1
            if arg.undo or arg.no_format:
                buf_records.append([jlin + 1, PICT, 1, 0, line])
        elif line.startswith(MACRON):
            max_header_width = max(max_header_width, len(line))
            header_lines += 1
            if arg.undo or arg.no_format:
                buf_records.append([jlin + 1, PICT, 1, 0, line])
        else:
            buf_records.append([jlin + 1, PICT, 1, 0, line])
            max_body_width = max(max_body_width, len(line))
            body_lines += 1
    if arg.verbose: inform(f"Read: yawp <-- {shortpath(arg.file)!r}")
    if arg.verbose: inform(f"    {plural(header_lines, 'header line')}, max {plural(max_header_width, 'char')} per line, {plural(arg.num_pages, 'page')}")
    if arg.verbose: inform(f"    {plural(body_lines, 'body line')}, max {plural(max_body_width, 'char')} per line")
    max_total_width = max(max_header_width, max_body_width)
    if arg.verbose: inform(f"    {plural(header_lines + body_lines, 'total line')}, max {plural(max_total_width, 'char')} per line")
    if not max_body_width:
        error(f'File {shortpath(arg.file)!r}, no printable character found')
    if arg.chars_per_line and not arg.char_width: # -w > 0 and -W == 0
        arg.char_width = arg.free_width / arg.chars_per_line # -W <-- -w
        if arg.verbose: inform(f'Compute: -W {in2str(arg.char_width)}')
        if arg.char_width <= 0: error(f'Wrong -W {in2str(arg.char_width)} <= 0')
    elif not arg.chars_per_line and arg.char_width: # -w == 0 and -W > 0
        arg.chars_per_line = int(arg.free_width / arg.char_width) # -w <-- -W
        if arg.verbose: inform(f'Compute: -w {arg.chars_per_line}')
        if arg.chars_per_line <= 0: error(f'Wrong -w {in2str(arg.chars_per_line)} <= 0')
    elif not arg.chars_per_line and not arg.char_width: # -w == 0 and -W == 0
        arg.chars_per_line = max_body_width # -w <-- file
        if arg.verbose: inform(f'Compute: -w {arg.chars_per_line}')
        if arg.chars_per_line <= 0: error(f'Wrong -w {in2str(arg.chars_per_line)} <= 0')
        arg.char_width = arg.free_width / arg.chars_per_line # -W <-- -w
        if arg.verbose: inform(f'Compute: -W {in2str(arg.char_width)}')
        if arg.char_width <= 0: error(f'Wrong -W {in2str(arg.char_width)} <= 0')
    if arg.calibration:
        arg.char_width2 = arg.char_width
    else:
        arg.char_width2 = max(0.0, linterpol(xyxy['pl'[arg.landscape] + 'cw'], arg.char_width))
        if arg.verbose: inform(f'Correct: -W {in2str(arg.char_width2)}')
    arg.chars_per_inch = 1.0 / arg.char_width
    arg.chars_per_margin2 = 1.0 / arg.char_width2
    arg.char_height = arg.char_width / arg.char_aspect
    if arg.verbose: inform(f'Compute: char height {in2str(arg.char_height)}')
    if arg.calibration:
        arg.char_height2 = arg.char_height
    else:
        arg.char_height2 = linterpol(xyxy['pl'[arg.landscape] + 'ch'], arg.char_height)
        if arg.verbose: inform(f'Correct: char height {in2str(arg.char_height2)}')
    arg.lines_per_inch = 1.0 / arg.char_height
    arg.lines_per_margin2 = 1.0 / arg.char_height2
    arg.lines_per_page = int(arg.lines_per_inch * arg.free_height) - 3
    arg.max_title = arg.chars_per_line // 2
    arg.max_subject = arg.chars_per_line // 2
 
def justify_input_into_output():
    is_python_file = arg.file.endswith('.py')
    format = not is_python_file 
    for jlin, x, x, x, line in buf.input: # input --> par --> buf.output
        is_switch_line = is_python_file and "\'\'\'" in line
        if is_switch_line:
            format = not format
        if is_switch_line or not format: # Python code
            par.flush(jlin)
            buf.append(jlin, CODE, 0, 0, line)
        elif not line: # empty-line
            par.flush(jlin)
            buf.append(jlin, EMPT, 0, 0, '')
        else:
            jdot = findchar(line, '[! ]')
            if jdot >= 0 and line[jdot:jdot+2] in ['• ','. ']: # dot-line
                par.flush(jlin)
                par.append(line[jdot+2:], indent=jdot+2)
            elif line[0] == ' ': # indented-line
                if par.string:
                    par.append(line)
                else:
                    if len(line) > arg.chars_per_line:
                        error(f'Length of picture line is {len(line)} > -w {arg.chars_per_line}', jlin, line)
                    buf.append(jlin, PICT, 0, 0, line)
            else: # unindented-line
                par.append(line)
    par.flush(jlin)
    if is_python_file and format:
        error('Python file, odd number of switch lines')

def delete_redundant_empty_lines():
    '''reduce multiple EMPT lines between TEXT line and TEXT line
    (or between TEXT line and EOF) to one EMPT line only'''
    jout, first, last, kind0 = 0, -1, -1, PICT
    while jout < len(buf.output):
        kind = buf.output[jout][KIND]
        if kind0 == TEXT == kind and 0 < first < last:
            del buf.output[first:last]
            jout -= last - first
        if kind == EMPT:
            if first < 0: first = jout
            last = jout
        else: # kind in [TEXT, PICT, CODE]
            kind0 = kind
            first, last, = -1, -1
        jout += 1
    if kind0 == TEXT and 0 < first < last:
        del buf.output[first:last]

def redraw_segments():
    charstr = '`─│┐│┘│┤──┌┬└┴├┼'
    #          0123456789ABCDEF
    charset = frozenset(charstr)
    for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
        if kind == PICT:
            chars = list(line)
            for jchar, char in enumerate(chars):
                if char in charset:
                    chars[jchar] = charstr[1 * (buf.char(jout, jchar - 1) in charset) +
                                           2 * (buf.char(jout + 1, jchar) in charset) +
                                           4 * (buf.char(jout - 1, jchar) in charset) +
                                           8 * (buf.char(jout, jchar + 1) in charset)]
            buf.output[jout][LINE] = ''.join(chars)
    
def redraw_arrowheads():
    charstr = '^▷△^▽^^^◁^^^^^^^'
    #          0123456789ABCDEF
    charset = frozenset(charstr)
    for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
        if kind == PICT:
            chars = list(line)
            for jchar, char in enumerate(chars):
                if char in charset:
                    chars[jchar] = charstr[1 * (buf.char(jout, jchar - 1) == '─') +
                                           2 * (buf.char(jout + 1, jchar) == '│') +
                                           4 * (buf.char(jout - 1, jchar) == '│') +
                                           8 * (buf.char(jout, jchar + 1) == '─')]
            buf.output[jout][LINE] = ''.join(chars)
            
def renumber_chapters():
    levels = []
    nout = len(buf.output)
    for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
        prev_line = buf.output[jout-1][LINE] if jout > 0 else ''
        next_line = buf.output[jout+1][LINE] if jout + 1 < nout else ''
        if kind == TEXT and line and not prev_line and not next_line:
            level, title = get_level_title(line)
            if level > 0: # numbered chapter line
                if level > len(levels) + 1:
                    error(f'Numbered chapter level > {len(levels)+1}', jlin, line)
                elif level == len(levels) + 1:
                    levels.append(1)
                else:
                    levels = levels[:level]
                    levels[-1] += 1
                buf.output[jout][KIND] = CHP1 if level == 1 else CHP2
                buf.output[jout][LINE] = '.'.join(str(level) for level in levels) + '. ' + title
            elif title == arg.contents_title: # contents line
                buf.output[jout][KIND] = CONT
                buf.output[jout][LINE] = title
            elif shrink(line).upper() == arg.index_title: # index line
                buf.output[jout][KIND] = INDX
                buf.output[jout][LINE] = title
            else:
                title = ''
            if len(title) > arg.max_title:
                error(f'Length of chapter title {title!r} = {len(title)} > {arg.max_title} = -w / 2', jlin, line)

def add_chapters_to_contents():
    for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
        if kind == CONT:
            if buf.contents_start > -1:
                error('More than one contents line in file', jlin, line)
            buf.contents_start = jout
            if buf.index_stop == -1 < buf.index_start:
                buf.index_stop = jout
        elif kind == INDX:
            if buf.index_start > -1:
                error('More than one index line in file', jlin, line)
            buf.index_start = jout
            if buf.contents_stop == -1 < buf.contents_start:
                buf.contents_stop = jout
            buf.contents.append(['', arg.index_title.title(), jout])
        elif kind in [CHP1, CHP2]:
            prefix, title = (line.split(None, 1) + [''])[:2]
            if buf.contents_stop == -1 < buf.contents_start:
                buf.contents_stop = jout
            if buf.index_stop == -1 < buf.index_start:
                buf.index_stop = jout
            buf.contents.append([prefix, title.title(), jout])
    if buf.contents_start > -1 == buf.contents_stop:
        buf.contents_stop = len(buf.output)
    elif buf.index_start > -1 == buf.index_stop:
        buf.index_stop = len(buf.output)

def add_quoted_subjects_to_index():
    if buf.index_start > -1:
        buf.qsub_jouts = SetDict() # {subject: jout}
        quote = False; subject = ''; in_contents_or_index = False
        for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
            if kind in [CONT, INDX]:
                in_contents_or_index = True
            elif kind in [CHP1, CHP2]:
                in_contents_or_index = False
            elif not in_contents_or_index:
                for jchar, char in enumerate(line + ' '):
                    if quote:
                        if (char == '"' and
                            get(line, jchar-1, ' ') not in QUOTES and
                            get(line, jchar+1, ' ') not in QUOTES):
                            subject = shrink(subject)
                            buf.qsub_jouts.add(subject, jout)
                            buf.subjects.add(subject)
                            quote = False
                        else:
                            subject += char
                            if len(subject) > arg.max_subject:
                                    error(f'Length of subject "{subject}..." = {len(subject)} > {arg.max_subject}')
                    elif (char == '"' and
                          get(line, jchar-1, ' ') not in QUOTES and
                          get(line, jchar+1, ' ') not in QUOTES):
                        subject = ''
                        quote = True
            else:
                if quote:
                    error('Unpaired \'"\' found while filling the index')
        if quote:
            error('Unpaired \'"\' found while filling the index')

def add_unquoted_subjects_to_index():
    if buf.index_start > -1:
        buf.uqsub_jouts = SetDict() # {subject: jout}
        charset = set(chars('[a-zA-Z0-9]') + ''.join(buf.qsub_jouts.keys()))
        word_jouts = [] # [(word, jout)]
        in_contents_or_index = False
        for jout, (jlin, kind, jpag, lpic, line) in enumerate(buf.output):
            if kind in [CONT, INDX]:
                in_contents_or_index = True
            elif kind in [CHP1, CHP2]:
                in_contents_or_index = False
            elif not in_contents_or_index:
                for word in take(line, charset, ' ').split():
                    word_jouts.append((word, jout))
        sub0_subws = ListDict() # {subject.word[0]: subject.word[1:]}
        for subject in buf.qsub_jouts.keys():
            subjectwords = subject.split()
            sub0_subws.append(subjectwords[0], subjectwords[1:])
        for jword_jouts, (sub0, jout) in enumerate(word_jouts):
            if sub0 in sub0_subws:
                for subw in sub0_subws[sub0]:
                    subject = sub0 + ' ' + ' '.join(subw) if subw else sub0
                    if subject == ' '.join(w for w, j in word_jouts[jword_jouts: jword_jouts + len(subw) + 1]):
                        buf.uqsub_jouts.add(subject, jout)
                        buf.subjects.add(subject)

def insert_contents():
    jlin = buf.output[buf.contents_start][JLIN]
    del buf.output[buf.contents_start + 1:buf.contents_stop] # delete old contents
    buf.output.insert(buf.contents_start + 1, [jlin, TEXT, 0, 0, '']) # insert new contents
    fmt_prefix = max((len(prefix) for prefix, titl, jpag in buf.contents), default=0)
    fmt_title = max((len(titl) for prefix, titl, jpag in buf.contents), default=0)
    for prefix, title, jpag in buf.contents[::-1]:
        buf.output.insert(buf.contents_start+1,
            [jlin, TEXT, 0, 0, f'{INDENT}• {edit(prefix, fmt_prefix)} {edit(title, fmt_title)}'])
    buf.output.insert(buf.contents_start+1, [jlin, TEXT, 0, 0, ''])

def insert_index():
    jlin = buf.output[buf.index_start][JLIN]
    del buf.output[buf.index_start + 1:buf.index_stop] # delete old index
    buf.output.insert(buf.index_start + 1, [jlin, TEXT, 0, 0, '']) # insert new index
    room = max((len(subject) for subject in buf.subjects), default=0) + 1
    for subject in sorted(buf.subjects, reverse=True):
        buf.output.insert(buf.index_start+1, [jlin, TEXT, 0, 0, f'{INDENT}• {edit(subject, room)}'])
    buf.output.insert(buf.index_start+1, [jlin, TEXT, 0, 0, ''])

def insert_contents_and_index():
    if -1 < buf.contents_start < buf.index_start: 
        insert_contents()
        index_shift = (len(buf.contents) + 2) - (buf.contents_stop - buf.contents_start - 1)
        buf.index_start += index_shift
        buf.index_stop += index_shift
        insert_index()
    elif -1 < buf.index_start < buf.contents_start:
        insert_index()
        contents_shift = (len(buf.index) + 2) - (buf.index_stop - buf.index_start - 1)
        buf.contents_start += contents_shift
        buf.contents_stop += contents_shift
        insert_contents()
    elif -1 < buf.contents_start:
        insert_contents()
    elif -1 < buf.index_start:
        insert_index()

def count_picture_lines():
    jpic = 0
    for jout, (jlin, kind, jpag, lpic, line) in retroenum(buf.output):
        if kind == PICT:
            jpic += 1
            if jout == 0 or buf.output[jout-1][KIND] != PICT:
                buf.output[jout][LPIC] = jpic
        else:
            jpic = 0

def count_pages():
    jpag, jpagline = 1, 0
    for jout, (jlin, kind, zero, lpic, line) in enumerate(buf.output):
        if (jpagline + lpic * (lpic < arg.lines_per_page) >= arg.lines_per_page or
            arg.form_feed_chap and kind in [CONT, INDX, CHP1] and not
            (jout >= 2 and not buf.output[jout-1][LINE] and buf.output[jout-1][JPAG] > buf.output[jout-2][JPAG])):
            jpag += 1
            jpagline = 0
        else:
            jpagline += 1
        buf.output[jout][JPAG] = jpag
    arg.tot_pages = jpag

def add_page_numbers_to_contents():
    if buf.contents_start > -1:
        fmt_jpag = len(str(buf.output[-1][JPAG])) + 1
        for jcontents, (prefix, titl, jout) in enumerate(buf.contents):
            buf.output[buf.contents_start + 2 + jcontents][LINE] += edit(buf.output[jout][JPAG], fmt_jpag)

def add_page_numbers_to_index():
    if buf.index_start > -1:
        qsub_jpags = SetDict() # {quoted_subject: {jpag}}
        for subject, jouts in buf.qsub_jouts.items():
            for jout in jouts:
                qsub_jpags.add(subject, buf.output[jout][JPAG])
        uqsub_jpags = SetDict() # {unquoted_subject: {jpag}}
        for subject, jouts in buf.uqsub_jouts.items():
            for jout in jouts:
                jpag = buf.output[jout][JPAG]
                if jpag not in qsub_jpags[subject]:
                    uqsub_jpags.add(subject, jpag)
        for jindex, subject in enumerate(sorted(buf.subjects)):
            jpag_strjs = sorted((jpag, f'"{jpag}"' if jpag in qsub_jpags[subject] else str(jpag))
                for jpag in (qsub_jpags[subject] | uqsub_jpags[subject])) # [(jpag, str(jpag))]
            line = buf.output[buf.index_start + 2 + jindex][LINE] + ', '.join(strj for jpag, strj in jpag_strjs)
            if len(line) > arg.chars_per_line:
                warning(f'Index line for subject {subject!r} longer than -w {arg.chars_per_line}, truncated')
                while True:
                    line = line[:line.rfind(',')]
                    if len(line) + 5 <= arg.chars_per_line:
                        break
                line += ', ...'
            buf.output[buf.index_start + 2 + jindex][LINE] = line
    
def insert_page_headers():
    jout = 0; jpag0 = 1; chapter = ''; npag = buf.output[-1][JPAG]
    header2 = arg.chars_per_line * MACRON
    while jout < len(buf.output):
        jlin, kind, jpag, lpic, line = buf.output[jout]
        if kind in [CONT, INDX, CHP1]:
            chapter = line.title()
        if jpag > jpag0:
            left, right = ((arg.even_right, arg.even_left) if arg.all_pages_E_e else
                           (arg.odd_left, arg.odd_right) if jpag % 2 else
                           (arg.even_left, arg.even_right))
            PpfeYmdHMSnNc = arg.PpfeYmdHMS + (str(jpag), str(npag), chapter)
            left = change(left, 'PpfeYmdHMSnNc', PpfeYmdHMSnNc, '%')
            right = change(right, 'PpfeYmdHMSnNc', PpfeYmdHMSnNc, '%')
            blanks = ' ' * (arg.chars_per_line - len(left) - len(right))
            if not blanks:
                header1 = f'{left} {right}' 
                error(f"Length of header {header1!r} is {len(header1)} > -w {arg.chars_per_line}")
            header1 = f'{FORMFEED}{left}{blanks}{right}'
            buf.output.insert(jout, [0, HEA2, jpag, 0, header2])
            buf.output.insert(jout, [0, HEA1, jpag, 0, header1])
            jout += 2
            jpag0 = jpag
        elif jout >= 3 and not buf.output[jout-1][LINE] and buf.output[jout-3][LINE].startswith(FORMFEED):
            left, right = ((arg.even_right, arg.even_left) if arg.all_pages_E_e else
                           (arg.odd_left, arg.odd_right) if jpag % 2 else
                           (arg.even_left, arg.even_right))
            PpfeYmdHMSnNc = arg.PpfeYmdHMS + (str(jpag), str(npag), chapter)
            left = change(left, 'PpfeYmdHMSnNc', PpfeYmdHMSnNc, '%')
            right = change(right, 'PpfeYmdHMSnNc', PpfeYmdHMSnNc, '%')
            blanks = ' ' * (arg.chars_per_line - len(left) - len(right))
            if not blanks:
                header1 = f'{left} {right}' 
                error(f"Length of header {header1!r} is {len(header1)} > -w {arg.chars_per_line}")
            buf.output[jout-3][LINE] = f'{FORMFEED}{left}{blanks}{right}'
        jout += 1

def backup_file():
    backfile = newbackfile(arg.file, arg.start_time)
    shell(f'mv {arg.file!r} {backfile!r}', mode=arg.shell_mode, file=stderr)
    if arg.verbose: inform(f'Backup: {shortpath(arg.file)!r} --> {shortpath(backfile)!r}')

def rewrite_file():
    header_lines, body_lines, arg.num_pages, max_body_width, max_header_width = 0, 0, 1, 0, 0
    with open(arg.file, 'w') as output:
        for jlin, kind, jpag, lpic, line in buf.output:
            print(line, file=output)
            if line.startswith(FORMFEED):
                arg.num_pages += 1
                max_header_width = max(max_header_width, len(line) - 1)
                header_lines += 1
            elif line.startswith(MACRON):
                max_header_width = max(max_header_width, len(line))
                header_lines += 1
            else:
                max_body_width = max(max_body_width, len(line))
                body_lines += 1
    if arg.verbose: inform(f"Rewrite: yawp --> {shortpath(arg.file)!r}")
    if arg.verbose: inform(f"    {plural(header_lines, 'header line')}, max {plural(max_header_width, 'char')} per line, {plural(arg.num_pages, 'page')}")
    if arg.verbose: inform(f"    {plural(body_lines, 'body line')}, max {plural(max_body_width, 'char')} per line")
    max_total_width = max(max_header_width, max_body_width)
    if arg.verbose: inform(f"    {plural(header_lines + body_lines, 'total line')}, max {plural(max_total_width, 'char')} per line")

def print_output_into_stdout():
    if arg.verbose: inform(f'Print: {shortpath(arg.file)!r} --> stdout')
    for rec in buf.output:
        print(rec[LINE])

def export_output_into_file_pdf():
    shell(f'lp -d PDF '
          f'-o print-quality={MAX_QUALITY} '
          f'-o media=Custom.{in2pt(arg.paper_width)}x{in2pt(arg.paper_height)} '
          f'-o cpi={arg.chars_per_margin2} '
          f'-o lpi={arg.lines_per_margin2} '
          f'-o page-top={in2pt(arg.top_margin2)} '
          f'-o page-left={in2pt(arg.left_margin2)} '
          f'-o page-right={0 if arg.num_pages > 1 else in2pt(arg.right_margin2)} '
          f'-o page-bottom={0 if arg.num_pages > 1 else in2pt(arg.bottom_margin2)} '
          f'{arg.file!r}', mode=arg.shell_mode, file=stderr)
    while True: # wait lp completion
        sleep(0.1)
        lines = shell(f'lpq -P PDF', mode=arg.shell_mode, file=stderr)
        if not any(line.startswith('active') for line in lines):
            break
    file_pdf = lastfile('~/PDF/*.pdf')
    if not file_pdf:
        error('Exported PDF file not found')
    shell(f'rm -f {arg.file_pdf!r}', mode=arg.shell_mode, file=stderr)
    shell(f'mv {file_pdf!r} {arg.file_pdf!r}', mode=arg.shell_mode, file=stderr)
    if arg.verbose: inform(f'Export: {shortpath(arg.file)!r} --> {shortpath(arg.file_pdf)!r}')

def open_file_pdf():
    shell(f'xdg-open {arg.file_pdf}', mode=arg.shell_mode, file=stderr)

#-----main -----

def main():
    try:
        simplefilter('ignore')
        get_arguments()
        get_configuration()
        check_arguments()
        if arg.undo: # -U ?
            restore_file()
            read_file_into(buf.output)
        elif arg.no_format: # -N ?
            read_file_into(buf.output)
            if arg.graphics: # -g ?
                redraw_segments()
                redraw_arrowheads()
            backup_file()
            rewrite_file()
        else: # not -U and not -N ?
            read_file_into(buf.input)
            justify_input_into_output()
            delete_redundant_empty_lines()
            if arg.graphics: # -g ?
                redraw_segments()
                redraw_arrowheads()
            renumber_chapters()
            add_chapters_to_contents()
            add_quoted_subjects_to_index()
            add_unquoted_subjects_to_index()
            insert_contents_and_index()
            if arg.form_feed: # -f or -F ?
                count_picture_lines()
                count_pages()
                add_page_numbers_to_contents()
                add_page_numbers_to_index()
                insert_page_headers()
            backup_file()
            rewrite_file()
        if arg.print_file: # -p ?
            print_output_into_stdout()
        if arg.file_pdf: # -P ?
            export_output_into_file_pdf()
            open_file_pdf()
    except KeyboardInterrupt:
        print()

if __name__ == '__main__':
    main()

#----- end -----
