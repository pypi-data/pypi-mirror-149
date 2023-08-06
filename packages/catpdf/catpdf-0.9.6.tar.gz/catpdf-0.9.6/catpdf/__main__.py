#!/usr/bin/python3

# imports

from .__init__ import __doc__ as description, __version__ as version
from os import popen
from os.path import abspath, expanduser, exists, isfile
from sys import argv, exit
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from libfunx import get_source, get_target, ask, split
from pdfrw import PdfReader, PdfWriter

# classes

class args:
    "container for arguments"
    pass

# functions

def choice2couples(choice):
    """translate a choice string into a list of (first, last) couples
pages are numbered from 1 to n
"n" is translated into 0, it will be substituted by number of pages
>>> choice2couples("23,25-25,23-34,55-22,23-n,n-34,n,n-n")
[(23, 23), (25, 25), (23, 34), (55, 22), (23, 0), (0, 34), (0, 0), (0, 0)]"""
    try:
        couples = []
        for s in split(choice.replace("n", "0"), ","):
            if "-" in s:
                a, z = [int(x) for x in s.split("-")]
            else:
                a = z = int(s)
            couples.append((a, z))
        return couples
    except:
        raise SyntaxError(f"syntax error in {choice!r}")
                
# main

def catpdf(argv):
    "conCATenate one or more source PDF files (or pieces of) into a target PDF file"

    # get arguments
    parser = Parser(prog="catpdf", formatter_class=Formatter, description=description)
    parser.add_argument("-V", "--version", action="version", version=version)
    parser.add_argument("-v", "--verbose", action="store_true", help="show what happens")
    parser.add_argument("-y", "--yes",  action="store_true", help="overwrite existing target file (default: ask)")
    parser.add_argument("-n", "--no",  action="store_true", help="don't overwrite existing target file (default: ask)")
    parser.add_argument("-o", "--open",  action="store_true", help="at end open the target file for check and print (default: ask)")
    parser.add_argument("-q", "--quit",  action="store_true", help="at end don't open the target file for check and print (default: ask)")
    parser.add_argument("source", nargs="+", help="one or more source files (each with choice or not), followed by...")
    parser.add_argument("target", help="...one target file")
    parser.parse_args(argv[1:], args)
    
    # check arguments
    if args.yes and args.no:
        exit("ERROR: you can't give both -y/--yes and -n/--no arguments")
    if args.open and args.quit:
        exit("ERROR: you can't give both -o/--open and -q/--quit arguments")
    sources, source_couples = [], []
    for source_choice in args.source:
        if ":" in source_choice:
            source, choice = source_choice.split(":", 1)
        else:
            source, choice = source_choice, "1-n"
        sources.append(get_source(source, ext=".pdf"))
        source_couples.append(choice2couples(choice))
    target = get_target(args.target, ext=".pdf", yes=args.yes, no=args.no)
    
    # open target, scan sources
    writer = PdfWriter()
    target_pages = 0
    for source, couples in zip(sources, source_couples):
    
        # check source content
        try:
            pages = PdfReader(source).pages
            assert pages
        except:
            exit(f"ERROR: source file {source!r} is corrupted or does not contain any pages")
        source_pages = len(pages)
        if args.verbose:
            print(f"source {source!r} contains {source_pages} pages\ncopied:", end=" ")
        
        # source --> target
        copied_pages = 0
        for first, last in couples:
            first = first or source_pages
            last = last or source_pages
            if min(first, last) <= source_pages:
                start, stop, step = (first, min(source_pages, last) + 1, 1) if first <= last else (
                                     min(source_pages, first), last - 1, -1) 
                for jpage in range(start, stop, step):
                    writer.addpage(pages[jpage - 1])
                    copied_pages += 1
                    target_pages += 1
                    if args.verbose:
                        print(jpage, end=" ")
        if args.verbose:
            print(f"\ncopied {copied_pages} pages from source {source!r} ...\n... into target {target!r}")

    # write target
    try:
        writer.write(target)
    except:
        exit(f"ERROR: error writing target file {target!r}")
    if args.verbose:
        print(f"target {target!r} contains {target_pages} pages")
    if args.open or not args.quit and ask(f"open the target file {target!r} for check and print or Quit? (o/q) --> ", "oq") == "o":
        popen(f"xdg-open {target!r}")
    
def main():
    try:
        catpdf(argv)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
