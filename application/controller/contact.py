# -*- encoding: utf-8 -*-
# -*- mamba-file-type: mamba-controller -*-
# Copyright (c) 2013 - Oscar Campos <oscar.campos@member.fsf.org>

"""
.. controller:: Contact
    :platform: Linux
    :synopsis: Contact Controller

.. controllerauthor:: Oscar Campos <oscar.campos@member.fsf.org>
"""

from twisted.internet import defer
from zope.interface import implements

from mamba.application import route
from mamba.utils.config import Application
from mamba.web.response import Ok, BadRequest
from mamba.core import interfaces, templating
from mamba.application.controller import Controller

from application.lib import smtp
from application import controller


class Contact(Controller):
    """
    Contact Controller
    """

    implements(interfaces.IController)
    name = 'Contact'
    loaded = False
    __route__ = 'contact'

    def __init__(self):
        """
        Put your initialization code here
        """
        super(Contact, self).__init__()

        self.template = templating.Template(controller=self)

    @route('/')
    def root(self, request, **kwargs):
        controller.toggle_menu(controller.CONTACT)
        template_args = controller.template_args

        return Ok(self.template.render(**template_args).encode('utf-8'))

    @route('/form_request/<name>/<email>/<content>', method='POST')
    @defer.inlineCallbacks
    def form_request(self, request, name, email, content, **kwargs):

        message = (
            'New message from {name} <{email}> using contact '
            'form on main site\n\n{content}'.format(
                name=name,
                email=email,
                content=content
            )
        )

        result = yield smtp.sendmail(
            message=message,
            subject='[PyMamba] Contact Form Request {}'.format(name),
            sender='contact@pymamba.com',
            recipients=Application().contact_recipients,
            host='localhost'
        )

        retval = Ok({'success': True}) if result is True else BadRequest()
        defer.returnValue(retval)
