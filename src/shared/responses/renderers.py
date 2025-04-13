from rest_framework.renderers import JSONRenderer
from django.utils.timezone import now

class SuccessJsonResponse(JSONRenderer):
    """Custom Success Renderer"""
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context['response'].exception:
            data = {
                'success': True,
                'response': data,
                'timestamp': now()
            }
        return super(SuccessJsonResponse, self).render(data, accepted_media_type, renderer_context)
