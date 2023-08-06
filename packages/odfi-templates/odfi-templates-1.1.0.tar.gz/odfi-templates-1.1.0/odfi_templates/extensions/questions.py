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



class Question(nodes.Admonition, nodes.TextElement):
	"""Node for questions.
	"""

class QuestionDirective(Directive):

    # this enables content in the directive
	has_content = True

	def run(self):

		env = self.state.document.settings.env

		targetid = "question-%d" % env.new_serialno('question')
		targetnode = nodes.target('', '', ids=[targetid])
 

		ad = Question('\n'.join(self.content))
		ad += nodes.title(_('Question'), _('Question'))
		#ad += nodes.class(_('Question'), _('Question'))
		self.state.nested_parse(self.content, self.content_offset, ad)
		ad.attributes["classes"] =  ["question"]
		#ad.options["class"] = "question"

		#ad = Question()
		#ad.name = self.name 
		#ad.content_offset = self.content_offset 
		#ad.options = self.options 
		#ad.content = self.content 
		#ad.block_text = self.block_text
		#ad.state = self.state
		#ad.state_machine = self.state_machine

		#ad = make_admonition(Question, self.name, [_('Question')], self.options,
		#					self.content, self.lineno, self.content_offset,
		#					self.block_text, self.state, self.state_machine)

		return [targetnode,ad]


def visit_question_node(self, node):
	self.visit_admonition(node)

def depart_question_node(self, node):
	self.depart_admonition(node)


def setup(app):

	app.add_node(Question, html=(visit_question_node, depart_question_node))
	app.add_directive('odfi.question',QuestionDirective)
	return {'version': '1.0.0'}