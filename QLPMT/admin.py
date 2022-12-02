from QLPMT import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea

admin = Admin(app=app, name='QUẢN TRỊ PHÒNG MẠCH TƯ', template_mode='bootstrap4')


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class QuyDinhSoTienKham(ModelView):
    column_labels = {
        'name': 'Số tiền khám',
            }



class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')



admin.add_view(StatsView(name='Thông kê'))
admin.add_view(QuyDinhSoTienKham(QuyDinhSoTienKham, db.session, name='Số tiền khám'))