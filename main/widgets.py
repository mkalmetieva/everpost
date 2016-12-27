import json

from django import forms
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils.safestring import mark_safe


class NicEditWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        self.js_options = kwargs.pop('js_options', {})
        super(NicEditWidget, self).__init__(*args, **kwargs)

    class Media:
        js = (
            staticfiles_storage.url('js/nicedit.js'),
        )

    def render(self, name, value, attrs=None):
        self.js_options['buttonList'] = ['bold',
                                         'italic',
                                         'underline',
                                         'strikethrough',
                                         'left',
                                         'center',
                                         'right',
                                         'justify',
                                         'upload',
                                         'link',
                                         'ol',
                                         'ul',
                                         'removeformat'
                                         ]
        self.js_options['uploadURI'] = reverse('nicedit_upload')
        self.js_options = json.dumps(self.js_options)

        rendered = super(NicEditWidget, self).render(name, value, attrs=attrs)
        return rendered + mark_safe('''
<script>
     new nicEditor(%s).panelInstance('id_%s');
</script>''' % (self.js_options, name))
