import sys
import os
import glob
from os.path import basename
from os.path import dirname
import posixpath
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _


from sphinx.util import logging
import logging


from xml.etree import ElementTree

from sphinx.builders import Builder



class Pdf(nodes.Inline, nodes.Element):
	"""PDF Node"""



def visit_pdf_node(self, node):
	
	#print("Visit pdf: ",self.builder,"\n")
	
	finalPath = posixpath.join(self.builder.dlpath,node.fileName)
	self.builder.env.dlfiles[node.file] = [node.file,node.fileName]

	containerClasses = ""
	if node.sticky is True:
		containerClasses = containerClasses +" ui sticky"

	#self.builder.images[node.file]= "lecture"
	classes = "pdfjs"
	

	self.body.append('<div id="pdfjs-container" class="%s">' % (containerClasses))
	self.body.append('<canvas class="%s" data-file="%s"></canvas>' %(classes,finalPath))
	self.body.append('<div class="pdfjs-controls">')
	self.body.append('<i class="ui left arrow icon" onclick="pdfjs.previousPage(this);"></i>')
	self.body.append('<i class="ui right arrow icon" onclick="pdfjs.nextPage(this);"></i>')
	self.body.append('</div>')

def depart_pdf_node(self, node):
	self.body.append('</div>')


#self.body.append('</canvas>')

class OdfiPdfPageDirective(Directive):

	optional_arguments = 1

	def run(self):

		print("PDF Page: ",self.arguments[0])



class OdfiPdfDirective(Directive):
	has_content = True
	optional_arguments = 10
	def run(self):

		pdfNode = Pdf()

		## Get File, relative to current source
		###############

		fileName = self.arguments[0]
		env = self.state.document.settings.env
		source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)
		sourceDirectory = dirname(source)
		pdfFile  = os.path.normpath(sourceDirectory+"/"+fileName)

		## Normalize name because of upper case issues on windows
		pdfFile = "%s[%s]" % (pdfFile[:-1], pdfFile[-1])
		pdfFile = glob.glob(pdfFile)[0]

		if os.path.exists(pdfFile):
			print("PDF File is at: ",pdfFile)
		else:
			return [nodes.error(None, nodes.paragraph(text = "Unable to Load PDF File at %s:%d: file %s does not exist" % (basename(source), self.lineno,pdfFile))) ]


		pdfNode.fileName  = fileName
		pdfNode.file = pdfFile

		## Set content
		pdfNode.content = self.content

		## Sticky
		if ":sticky:" in self.arguments:
			pdfNode.sticky = True
		else:
			pdfNode.sticky = False



		return [pdfNode]




def setup(app):

	"""html=(visit_OdfiSVG_node, depart_OdfiSVG_node)"""
	app.add_node(Pdf, html=(visit_pdf_node, depart_pdf_node))
	app.add_directive('odfi.pdf',OdfiPdfDirective)
	app.add_role('odfi.pdfPage',OdfiPdfPageDirective)


	return {'version': '1.0.0'}