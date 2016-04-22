#!/usr/bin/python

import sys
from lxml import etree

tree = etree.parse(sys.argv[1])

root = tree.getroot();

def TraverseXML(root,prefix):
    prefix=prefix + "/" + root.tag
    print prefix
    if root.attrib:
        for k in root.attrib:
            print prefix + "/@" + k ;
            print prefix + "[@" + k + "='" + root.attrib[k] + "']" ;
    for child in root:
        TraverseXML(child,prefix)

TraverseXML(root,"")
