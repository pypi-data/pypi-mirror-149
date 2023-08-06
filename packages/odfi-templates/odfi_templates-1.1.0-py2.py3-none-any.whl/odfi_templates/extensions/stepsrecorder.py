
import sys
import os
import glob
from os.path import basename
from os.path import dirname

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _


from sphinx.util import logging
import logging
import re

from zipfile import ZipFile

from xml.etree import ElementTree



class StepsRecorder(nodes.Inline, nodes.Element):
	"""StepsRecorder Node"""



def visit_StepsRecorder_node(self, node):

	## Extract XML
	mainHTML = node.resultParts["main.htm"]
	#print("Search HTML: "+mainHTML)
	reportXML = re.search("<Report>.*</Report>",mainHTML)
	if reportXML is None:
		print("Report not found inside: ",mainHTML.encode(sys.stdout.encoding, errors='replace'))

	#print("Found Report: "+reportXML.group(0))

	report = ElementTree.fromstring(reportXML.group(0))

	## Create For each step a Div
	self.body.append('<div class="steps">')

	## File Name

	## Action
	eachAction = report.findall("./UserActionData/RecordSession/EachAction")

	## TOC?
	if node.stepsToc is True:
		counter = 0
		self.body.append('<ol class="steps-toc">')
		for action in eachAction: 
			number =  action.get("ActionNumber")
			counter += 1
			if action.get("ActionNumber") in node.resultParts:
				self.body.append('<li><a href="#%s-step%d">%s</a></li>' % (node.stepsName,counter,node.resultParts[action.get("ActionNumber")]))
		self.body.append('</ol>')

	#self.body.append('<div class="steps-header">Steps below:</div>')
	counter = 0 
	for action in eachAction: 
		counter += 1
		number =  action.get("ActionNumber")
		print("Action: "+number)
		self.body.append('<div class="step" id="%s-step%d">' %(node.stepsName,counter))


		if action.get("ActionNumber") in node.resultParts:
			self.body.append('<div class="caption"> %s </div>' %  node.resultParts[action.get("ActionNumber")])

			## Add Picture
			self.body.append('<div class="picture">')
			self.body.append('<img src="data:image/jpeg;base64,%s"/>' % node.resultParts[action.findtext("ScreenshotFileName")])
			self.body.append('</div>')

		# EOF Step
		self.body.append('</div>')
		
	
	self.body.append('</div>')

	pass
	

def depart_StepsRecorder_node(self, node):
	pass

class OdfiStepsRecorderDirective(Directive):

  
	has_content = True
	required_arguments = 1 
	optional_arguments = 64
           

	def run(self):

		print('Running ODFI Steps Recorder Directive')
		print( self.arguments)
		print( self.options)
		print( self.content)
		
		env = self.state.document.settings.env
		source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)

		## Get File, relative to current source
		fileName = self.arguments[0]
		sourceDirectory = dirname(source)
		stepsFile  = os.path.normpath(sourceDirectory+"/"+fileName)

		## Normalize name because of upper case issues on windows
		stepsFile = "%s[%s]" % (stepsFile[:-1], stepsFile[-1])
		stepsFile = glob.glob(stepsFile)[0]

		if os.path.exists(stepsFile):
			print("Steps File is at: ",stepsFile)
		else:
			return [nodes.error(None, nodes.paragraph(text = "Unable to Load Steps File at %s:%d: file %s does not exist" % (basename(source), self.lineno,stepsFile))) ]


		## Read file and split parts
		#################
		stepsNode = StepsRecorder()
		stepsNode.stepsName = fileName

		stepsBlock = nodes.container();

		##  Steps File can be a Zip File
		if stepsFile.endswith(".zip"):
			with ZipFile(stepsFile) as stepsZipFile:
				with stepsZipFile.open(stepsZipFile.namelist()[0]) as stepsFileEntry:
					stepsContent = stepsFileEntry.read().decode("cp1252").replace('\r','')
					#print("Steps content from zip: ",stepsContent.encode(sys.stdout.encoding, errors='replace'))

		else:
			with open(stepsFile) as f: stepsContent = f.read()
		## get boundary
		match = re.search('boundary="([\w_=\+\.\-]+)"',stepsContent)
		boundary= "--"+match.group(1)
		print("Steps Boundary: "+boundary)

		## Split
		parts = stepsContent.split(boundary)
		print("Parts: %s" % len(parts))

		## Store Each Part with name
		resultParts = {}
		for partContentIndex in range(1, len(parts)):

			## Get Part content line by line, to extract parameters
			## iF an empty line is encountered, it is the beginning of the content
			partContent = parts[partContentIndex].strip()
			partFileContent = ""
			fileName = ""
			contentStart = False
			lines = partContent.split("\n")
			for lineIndex in range(0, len(lines)):
				
				line = lines[lineIndex]
				
				if contentStart is True: 
					partFileContent+=line
				elif line.startswith("Content-Location:"):
					fileName =  line.strip("Content-Location:").strip()
					print("Part File Name: "+fileName)
				elif line == "":
					print("Found Content Start")
					contentStart = True 

			# Save part file content
			resultParts[fileName] = partFileContent

			## Make admonition

		## Save result Parts to node 
		stepsNode.resultParts = resultParts

		## Read Directive Content and save Step Description
		for contentLine in self.content: 
			match = re.search("([\d]+)\s+(.*)",contentLine)
			number = match.group(1)
			desc = match.group(2)
			print("Part desc: ",desc)
			resultParts[number] = desc

		## Add some more options
		if "toc" in self.arguments:
			stepsNode.stepsToc = True
		else:
			stepsNode.stepsToc = False

		if "slideshow" in self.arguments:
			stepsNode.slideshow = True
		else:
			stepsNode.slideshow = False



		return [stepsNode]

def setup(app):

	"""html=(visit_OdfiSVG_node, depart_OdfiSVG_node)"""
	app.add_node(StepsRecorder, html=(visit_StepsRecorder_node, depart_StepsRecorder_node))
	app.add_directive('odfi.stepsrecorder',OdfiStepsRecorderDirective)
	return {'version': '1.0.0'}