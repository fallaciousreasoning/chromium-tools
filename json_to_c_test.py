#!/usr/bin/python3.6

import argparse
import sys
import json

from os import path

parser = argparse.ArgumentParser(description="Escape JSON for use in C tests")
parser.add_argument("json_or_path", nargs='?')
parser.add_argument("--no-pretty", action="store_true")
parser.add_argument("--indent", type=int, default=2)

args = parser.parse_args(sys.argv[1:])

def escape(j, pretty, indent):
  if pretty:
    j = json.dumps(json.loads(j), indent=indent)
  
  j = j.replace('"', '\\"')
  j = '\n'.join(['"' + line + '"' for line in j.split('\n')])

  return j

def run(): 
  j = args.json_or_path

  if path.exists(j):
    with open(j) as f:
      j = f.read()

  if not j:
    j = sys.stdin.read()
    
  print(escape(j, not args.no_pretty, args.indent))

run()