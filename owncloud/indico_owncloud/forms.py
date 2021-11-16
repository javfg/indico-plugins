from wtforms import Field
from wtforms.validators import DataRequired, ValidationError

from indico.modules.attachments.forms import AttachmentFormBase
from indico.util.i18n import _
from indico.web.forms.widgets import JinjaWidget

from indico_owncloud.util import get_auth_settings


class IndicoOwncloudField(Field):

    widget = JinjaWidget('owncloud_file_picker_widget.html', plugin='owncloud', single_line=True, single_kwargs=True)

    def __init__(self, label=None, validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.auth_settings = get_auth_settings()

    def process_formdata(self, valuelist):
        if valuelist and len(valuelist):
            self.data = {
                'files': [f.rstrip() for f in valuelist[0].split('\n')],
                'token': valuelist[1]
            }


class AttachmentOwncloudFormMixin:
    owncloud_file_picker = IndicoOwncloudField(_('Files'), [DataRequired()])

    def validate_owncloud_file_picker(self, field):
        if self.owncloud_file_picker.data and self.owncloud_file_picker.data['files'] == ['']:
            raise ValidationError("Select files to add and click 'Select resources'")


class AddAttachmentOwncloudForm(AttachmentOwncloudFormMixin, AttachmentFormBase):
    pass


class EditAttachmentOwncloudForm(AttachmentOwncloudFormMixin, AttachmentFormBase):
    pass
