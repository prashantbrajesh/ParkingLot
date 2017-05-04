#!/usr/bin/python

import sys
import json
import traceback
import getopt
import numbers

from xml.dom.minidom import Document
from backend.lib.LogSetup import logging

def parse_element(doc, root, j):
	if isinstance(j, dict):
		for key in j.keys():
			value = j[key]
			if isinstance(value, list):
				parentElem = doc.createElement(key)
				for e in value:
					elem = doc.createElement('_')
					parse_element(doc, elem, e)
					parentElem.appendChild(elem)
				root.appendChild(parentElem)
			else:
				if key.isdigit():
					elem = doc.createElement('item')
					elem.setAttribute('value', key)
				else:
					elem = doc.createElement(key)
				parse_element(doc, elem, value)
				root.appendChild(elem)
	elif isinstance(j, str) or isinstance(j, unicode):
		text = doc.createTextNode(j)
		root.appendChild(text)
	elif isinstance(j, numbers.Number):
		text = doc.createTextNode(str(j))
		root.appendChild(text)
	else:
		raise Exception("bad type '%s' for '%s'" % (type(j), j,))

def parse_doc(root, j):
	doc = Document()
	if root is None:
		if len(j.keys()) > 1:
			raise Exception('Expected one root element, or use --root to set root')
		root = j.keys()[0]
		elem = doc.createElement(root)
		j = j[root]
	else:
		elem = doc.createElement(root)
	parse_element(doc, elem, j)
	doc.appendChild(elem)
	return doc

def parse_json_stdin(root):
	js = "".join(sys.stdin.readlines())
	j = json.loads(js)
	doc = parse_doc(root, j)
	logging.info(doc.toprettyxml(encoding="utf-8", indent="  "))

def usage():
	logging.info("Error occurred while trying to convert JSON to xml. Incorrect usage.")


def main():

	root = None

	if len(sys.argv[1:]):
		try:
			(opts, args) = getopt.getopt(sys.argv[1:], 'r:', ['root'])
			if (len(args)):
				raise getopt.GetoptError('bad parameter')
		except getopt.GetoptError:
			usage()
			sys.exit(0)

		for (opt, arg) in opts:
			if opt in ('-r', '--root'):
				root = arg

	parse_json_stdin(root)

if __name__ == '__main__':
	try:
		main()
	except:
		logging.exception("An error occurred while trying to convert JSON to XML")
