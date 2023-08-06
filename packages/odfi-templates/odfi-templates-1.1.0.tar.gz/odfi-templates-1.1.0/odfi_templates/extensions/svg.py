
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


class svg(nodes.Inline, nodes.Element):
	"""SVG Node"""



def visit_svg_node(self, node):

	if hasattr(node,'groupId'):

		## Find Group content in source
		ns = {'svg': 'http://www.w3.org/2000/svg', 'inkscape' : 'http://www.inkscape.org/namespaces/inkscape'}
		svgDom = ElementTree.parse(node.source)
		svgRoot = svgDom.getroot()

		## Look for element by ID
		foundElement = svgRoot.find(".//*[@id='%s']" %(node.groupId),ns)
		print("Found id %s -> %s " %(node.groupId,foundElement))

		## Handle: Sindle element or Groups
		#########
		if foundElement is None : 
			return

		print("Found tag2:  %s " %(foundElement.tag))

		## Find defs in source
		foundDefs = svgRoot.find(".//svg:defs",ns)

		if foundElement.tag == "{http://www.w3.org/2000/svg}g" :

			foundGroup = foundElement
			#foundGroup = svgRoot.find(".//svg:g[@id='%s']" %(node.groupId),ns)
			foundGroup.set("transform","")

			

			## Find top most Y (lowest y) to set transformation to get the group back on top
			allwithy = foundGroup.findall(".//svg:rect[@y]",ns) + foundGroup.findall(".//svg:image[@y]",ns)
			allwithx = allwithy

			## First calculate translation in X and Y to substract from all X/Y coordinates
			## Sort X list by most Right first
			## Sort Y list by most down first
			## Take last element as most left and most down
			mostRightFirst = sorted(allwithx,key=lambda n: float(n.get("x")),reverse=True)
			mostDownFirst  = sorted(allwithy,key=lambda n: float(n.get("y")),reverse=True)
			
			minX = float(mostRightFirst[-1].get("x"))
			minY = float(mostDownFirst[-1].get("y"))

			## From here translate all X/Y coordnates because we place back the group to 0/0
			## This way sizes are correct
			allXAndWidth = filter(lambda elt: elt.get("x")!=None and elt.get("width")!=None,allwithx)
			allMostRightCoordinates = sorted(map(lambda elt: float(elt.get("x")) - minX + float(elt.get("width")), allXAndWidth),reverse=True)
			
			allYAndHeight = filter(lambda elt: elt.get("y")!=None and elt.get("height")!=None,allwithy)
			allMostDownCoordinates = sorted(map(lambda elt: float(elt.get("y")) - minY + float(elt.get("height")), allYAndHeight),reverse=True)

			

			maxX = allMostRightCoordinates[0]
			maxY = allMostDownCoordinates[0]

		else:



			minX = float(foundElement.get("x"))
			minY = float(foundElement.get("y"))

			maxX = float(foundElement.get("x")) - minX + float(foundElement.get("width"))
			maxY = float(foundElement.get("y")) - minY + float(foundElement.get("height"))


		
		## Modify Properties of SVG now
		################################



		## Create new SVG 
		newSvg = ElementTree.fromstring('<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg version="1.1"  xmlns="http://www.w3.org/2000/svg"></svg>')
		

		

		#ally = map(lambda n: float(n.get("y")),allwidthy)
		#allx = map(lambda n: float(n.get("x")),allwidthx)
		#allwidth = map(lambda n: float(n.get("width")),allwidthx)
		#allheight = map(lambda n: float(n.get("height")),allwidthx)
		#miny = min(map(lambda n: float(n.get("y")),allwidthy))
		#minx = min(map(lambda n: float(n.get("x")),allwidthx))

		print("Found Min y 2: ",minY)
		print("Found Min x 2: ",minX)
		print("Found Max y 2: ",maxY)
		print("Found Max x 2: ",maxX)

		## Translate Group
		#translateX = 0 if minX < 0 else minX
		#translateY = 0 if minY < 0 else minY
		translateX = minX
		translateY = minY
		foundElement.set("transform","translate(%s,%s)" % (-translateX,-translateY))
	

		## View Box is 0 0 maxX maxY
		## Min and max are already translated
		viewBox = "0 0 %s %s" % (maxX,maxY) 
		newSvg.set("viewBox",viewBox)


		##  add group to it
		newSvg.insert(0,foundElement)

		## Add Defs
		newSvg.insert(0,foundDefs)

		
		ElementTree.register_namespace("","http://www.w3.org/2000/svg")
		ElementTree.register_namespace("xlink","http://www.w3.org/1999/xlink")
		ElementTree.register_namespace("inkscape","http://www.inkscape.org/namespaces/inkscape")
		
		str = ElementTree.tostring(newSvg, encoding='utf8', method='xml').decode("utf-8") 
		#print("Found svg: ",str)

		## DIV Container and Style
		####################
		targetStyle= node.style if hasattr(node,'style') else ""

		if hasattr(node,'style_center'):
			targetStyle = targetStyle + ";margin-left:auto;margin-right:auto"

		if hasattr(node,'style_width'):
			targetStyle = targetStyle + (";width:%s" % node.style_width)

		## Set Container Div width provided style if defined
		self.body.append('<div class="odfi svg" style="%s">' % (targetStyle))
		self.body.append(str)
		self.body.append('</div>')

	else:
		with open(node.source) as f: s = f.read()

		targetStyle= node.style if hasattr(node,'style') else ""
		if hasattr(node,'style_center'):
			targetStyle = targetStyle + ";margin-left:auto;margin-right:auto"

		if hasattr(node,'style_width'):
			targetStyle = targetStyle + (";width:%s" % node.style_width)

		self.body.append('<div class="odfi svg" style="%s">' % (targetStyle))
		self.body.append(s)
		self.body.append('</div>')



def depart_svg_node(self, node):
	pass

class OdfiSVGDirective(Directive):

  
	has_content = True
	required_arguments = 2 
	optional_arguments = 64
           

	def run(self):

		print('Running ODFI SVG Directive')
		print( self.arguments)
		print( self.options)
		
		env = self.state.document.settings.env
		source = self.state_machine.input_lines.source(self.lineno - self.state_machine.input_offset - 1)

		
		#logger = logging.getLogger(__name__)
		#logger.info('Running ODFI SVG Directive')

		## Get File
		fileName = self.arguments[0]
		
		#if not "file" in self.arguments: 
		#	return [nodes.error(None, nodes.paragraph(text = "Unable to Load SVG at %s:%d: file argument not defined" % (basename(source), self.lineno))) ]
		
		## Get File name relative to local source
		#fileName = self.arguments[(self.arguments.index('file') +1)]
		sourceDirectory = dirname(source)
		sourceSVG  = os.path.normpath(sourceDirectory+"/"+fileName)

		if os.path.exists(sourceSVG):
			print("SVG File is at: ",sourceSVG)
		else:
			return [nodes.error(None, nodes.paragraph(text = "Unable to Load SVG at %s:%d: file %s does not exist" % (basename(source), self.lineno,sourceSVG))) ]

		
		## Create SVG Node
		targetid = "svg-%d" % env.new_serialno('svg')
		svgNode = svg()
		svgNode.source = sourceSVG
	
		## Set Target Group Id if necessary
		if "gid" in self.arguments: 
			print('Found Elementid')
			svgNode.groupId = self.arguments[(self.arguments.index('gid') +1)]

		

		## Style Arguments
		######################
		## Set Style if necessary
		if "style" in self.arguments: 
			svgNode.style = self.arguments[(self.arguments.index('style') +1)].replace('"',"").replace("'","")

		if "align" in self.arguments and self.arguments[(self.arguments.index('align') +1)] == "center":
			svgNode.style_center = True

		if ":width:" in self.arguments:
			svgNode.style_width = self.arguments[(self.arguments.index(':width:') +1)]


		## Animation Arguments
		######################

		return [svgNode]


def setup(app):

	"""html=(visit_OdfiSVG_node, depart_OdfiSVG_node)"""
	app.add_node(svg, html=(visit_svg_node, depart_svg_node))
	app.add_directive('odfi.svg',OdfiSVGDirective)
	return {'version': '1.0.0'}



