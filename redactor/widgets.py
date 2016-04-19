from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.conf import settings

OPTIONS = getattr(settings, 'REDACTOR_OPTIONS', {'focus': True})

def extend(dict1, dict2):
    return dict(dict1, **dict2)

class JQueryEditor(widgets.Textarea):

    class Media:
        js = ('js/jquery-1.6.1.min.js','editor/editor.js',)
        css = {
            'all': ('editor/css/editor.css', ),
        }

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.options = dict(OPTIONS, **kwargs.pop('redactor_options', {}))

        kwargs['attrs'] = extend({
            'cols': 100,
            'rows': 30,
        }, kwargs.get('attrs', {}))

        super(JQueryEditor, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        input_ = super(JQueryEditor, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')

        options = json.dumps(extend({
            'image_upload': reverse('redactor_upload_image', kwargs={'upload_to': self.upload_to}),
            'file_upload': reverse('redactor_upload_file', kwargs={'upload_to': self.upload_to}),
#            'path': '/'.join((settings.MEDIA_URL,'redactor')),
        }, self.options))

        return mark_safe(input_ + (
            '<script type="text/javascript">' +
            'jQuery(document).ready(function(){' +
            '$("#%s").redactor(%s);' % (id_, options) +
            '});</script>'
        ))
