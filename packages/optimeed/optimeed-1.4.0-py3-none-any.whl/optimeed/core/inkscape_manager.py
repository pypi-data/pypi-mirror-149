import subprocess
import re
from .tools import printIfShown, SHOW_WARNING
from subprocess import DEVNULL, STDOUT


def get_inkscape_version():
    converter_cmd_line = 'inkscape --version'
    result = subprocess.run(converter_cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = str(result.stdout)
    res = re.search(r'([\d].[\d])', result)  # Match the version number
    try:
        return float(res.group(0))
    except AttributeError:
        return None


inkscape_version = get_inkscape_version()


def inkscape_svg_to_pdf(filename_svg, filename_pdf):
    if inkscape_version is None:
        printIfShown("Inkscape not available for pdf export", SHOW_WARNING)
        return
    elif inkscape_version < 1.0:
        converter_cmd_line = 'inkscape -z {} -A {} --export-area-drawing'.format(filename_svg, filename_pdf)
    else:
        converter_cmd_line = 'inkscape --export-type=pdf {} -o {} --export-area-drawing'.format(filename_svg, filename_pdf)
    subprocess.Popen(converter_cmd_line, shell=True, stdout=DEVNULL, stderr=STDOUT)


def inkscape_svg_to_png(filename_svg, filename_png):
    if inkscape_version is None:
        printIfShown("Inkscape not available for png export", SHOW_WARNING)
        return
    elif inkscape_version < 1.0:
        converter_cmd_line = 'inkscape -z {} -D -e {} -d 400 --export-area-drawing'.format(filename_svg, filename_png)
    else:
        converter_cmd_line = 'inkscape --export-type=png {} -o {} -d 400 --export-area-drawing'.format(filename_svg, filename_png)
    subprocess.Popen(converter_cmd_line, shell=True, stdout=DEVNULL, stderr=STDOUT)
