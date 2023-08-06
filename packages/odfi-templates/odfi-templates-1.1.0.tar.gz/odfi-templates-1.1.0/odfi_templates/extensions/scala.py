import sys
import os
import glob
from os.path import basename
from os.path import dirname
import posixpath
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _
from sphinx.domains import _

from sphinx.util import logging
import logging


from xml.etree import ElementTree

from sphinx.builders import Builder
from sphinx.domains  import Domain 

class TraitDirective(Directive):
	""" Directive to set trait"""


class ScalaDomain(Domain):
	"""Scala Domain"""
	name = "scala"
	label = "Scala Domain"
	directives = {}
	directives['trait'] = TraitDirective




def setup(app):

	"""html=(visit_OdfiSVG_node, depart_OdfiSVG_node)"""
	app.add_config_value("maven_projects",[],'env')
	app.add_domain(ScalaDomain)
	#app.add_directive_to_domain('scala','trait',TraitDirective)