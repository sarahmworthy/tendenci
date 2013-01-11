from django import template
from tracking.models import Visitor

register = template.Library()

"""
A revision of the template tag used by django-tracking to return a list of users instead
"""

class VisitorsOnSite(template.Node):
    """
    Adds the list of users viewing the page in the context
    """
    def __init__(self, varname, same_page=False):
        self.varname = varname
        self.same_page = same_page

    def render(self, context):
        try:
            request = context['request']
            visitors = Visitor.objects.active().filter(url=request.path).exclude(user=request.user)
        except KeyError:
            raise template.TemplateSyntaxError("Please add 'django.core.context_processors.request' to your TEMPLATE_CONTEXT_PROCESSORS if you want to see how many users are on the same page.")

        context[self.varname] = visitors
        return ''


def live_collaborators(parser, token):
    """
    Returns the list of users currently viewing the page
    """
    try:
        tag, a, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('live_collaborators usage: {% live_collaborators as visitors %}')

    return VisitorsOnSite(varname)
register.tag(live_collaborators)
