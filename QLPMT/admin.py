from calendar import monthrange
from flask import request
from sqlalchemy import exc

from QLPMT import db, app, dao
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from QLPMT.models import QuyDinhSoTienKham, QuyDinhSoBenhNhaKhamTrongNgay, LoaiThuoc, DonVi


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class StatsView(BaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month')
        thuoc = dao.get_thuoc(month)
        total = 0

        revenue = dao.get_revenue(month)

        for r in revenue:
            total += r[2]



        num_of_patient = dao.count_patient(month)
        return self.render('admin/stats.html',
                           thuoc=thuoc,
                           revenue=revenue,
                           num_of_patient=num_of_patient,
                           total=total)


class QuyDinhSoTienKhamView(ModelView):
    can_view_details = True
    can_export = True


class QuyDinhSoBenhNhaKhamTrongNgayView(ModelView):
    can_view_details = True
    can_export = True


class LoaiThuocView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['TenLoaiThuoc']
    column_filters = ['TenLoaiThuoc']


class DonViView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['TenDonVi']
    column_filters = ['TenDonVi']


admin = Admin(app=app, name='QUẢN TRỊ PHÒNG MẠCH TƯ', template_mode='bootstrap4')

admin.add_view(QuyDinhSoTienKhamView(QuyDinhSoTienKham, db.session, name='Số tiền khám'))
admin.add_view(QuyDinhSoBenhNhaKhamTrongNgayView(
    QuyDinhSoBenhNhaKhamTrongNgay, db.session, name='Số bệnh nhân khám trong ngày'))
admin.add_view(LoaiThuocView(LoaiThuoc, db.session, name='Loại thuốc'))
admin.add_view(DonViView(DonVi, db.session, name='Đơn vị'))
admin.add_view(StatsView(name='Thống kê'))
