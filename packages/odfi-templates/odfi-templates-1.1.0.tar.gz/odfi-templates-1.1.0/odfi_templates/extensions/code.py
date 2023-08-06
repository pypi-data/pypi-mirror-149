import sys
import os
from os.path import basename
from os.path import dirname

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _


from sphinx.util import logging
import logging


from xml.etree import ElementTree

class Code(nodes.Inline, nodes.Element):
	"""SVG Node"""



def visit_code_node(self, node):
	if hasattr(node,"language"):
		lang=('class="%s"' % node.language)
	else:
		lang=""
	self.body.append('<pre>')
	self.body.append('<code %s>' % lang)
	self.body.append("\n".join(node.content))

def depart_code_node(self, node):
	self.body.append('</code>')
	self.body.append('</pre>')



class OdfiCodeDirective(Directive):
	has_content = True
	optional_arguments = 1
	def run(self):

		codeNode = Code()

		## Get language arg
		print(self.arguments)
		if len(self.arguments) == 1:
			codeNode.language = self.arguments[0]

		## Set content
		codeNode.content = self.content
		print(self.content)

		return [codeNode]

def setup(app):

	"""html=(visit_OdfiSVG_node, depart_OdfiSVG_node)"""
	app.add_node(Code, html=(visit_code_node, depart_code_node))
	app.add_directive('odfi.code',OdfiCodeDirective)
	return {'version': '1.0.0'}