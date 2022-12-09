from flask import session
from flask_sqlalchemy.session import Session

from sqlalchemy import func, extract, union

from QLPMT.models import User, BenhNhan, DanhSachKham, UserRole, PhieuKhamBenh, QuyDinhSoTienKham, ChiTietPhieuKhamBenh, \
    Thuoc, QuyDinhSoBenhNhaKhamTrongNgay, HoaDon
from QLPMT import db
import hashlib

def get_so_luong_benh_nhan_kham_trong_ngay():
    return db.session.query(QuyDinhSoBenhNhaKhamTrongNgay)\
        .order_by(QuyDinhSoBenhNhaKhamTrongNgay.id.desc()).first()\
        .SoBenhNhanKhamTrongNgay


def online_register(HoTen, GioiTinh, NamSinh, DiaChi, DanhSachKham_id):
    b = BenhNhan(HoTen=HoTen, GioiTinh=GioiTinh, NamSinh=NamSinh, DiaChi=DiaChi, DanhSachKham_id=DanhSachKham_id)
    db.session.add(b)
    db.session.commit()


def count_patient(DanhSachKham_id):
    return db.session.query(func.count(BenhNhan.id)).filter(DanhSachKham_id==DanhSachKham_id).count()


def load_BenhNhan(DanhSachKham_id):
    return BenhNhan.query.filter(BenhNhan.DanhSachKham_id==DanhSachKham_id).all()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_phieukhambenh(id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.BenhNhan_id == id).all()


def get_name(id):
    return BenhNhan.query.get(1).HoTen


def get_date(id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.BenhNhan_id == id).first().NgayKham


def count_bill(id):
    return db.session.query(PhieuKhamBenh.BenhNhan_id == id).count()


def tien_kham():
    return db.session.query(QuyDinhSoTienKham).order_by(QuyDinhSoTienKham.id.desc()).first().SoTienKham


def get_don_gia_so_luong(id):
    return db.session.query(ChiTietPhieuKhamBenh, PhieuKhamBenh, Thuoc) \
        .join(PhieuKhamBenh).join(Thuoc).filter(PhieuKhamBenh.BenhNhan_id == id)


def get_date_in_danhsachkham():
    return db.session.query(DanhSachKham) \
        .order_by(DanhSachKham.id.desc()).first().NgayKham


def get_id_danhsachkham():
    return db.session.query(DanhSachKham) \
        .order_by(DanhSachKham.id.desc()).first().id


def add_danhsachkham(ngaykham):
    ds = DanhSachKham(NgayKham=ngaykham, YTa_id=1)
    db.session.add(ds)
    db.session.commit()


def delete_patient(id):
    b = BenhNhan.query.get(id)
    db.session.delete(b)
    db.session.commit()


def register(name, username, password, avatar, type):
    if type == 'doctor':
        type = UserRole.DOCTOR
    elif type == 'nurse':
        type = UserRole.NURSE
    elif type == 'cashier':
        type = UserRole.CASHIER
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(),
             password=password, image=avatar, user_role=type)
    db.session.add(u)
    db.session.commit()





def count_patient(month):
    #ngay sobenhnhan doanhthu
    return db.session.query(DanhSachKham.NgayKham, func.count(BenhNhan.id))\
            .join(BenhNhan, BenhNhan.DanhSachKham_id.__eq__(DanhSachKham.id))\
            .filter(extract('month', DanhSachKham.NgayKham) == month)\
            .group_by(DanhSachKham.id)\
            .all()

def get_patient(month):
     return db.session.query(DanhSachKham.NgayKham, BenhNhan.id,
                            func.count(PhieuKhamBenh.id)*100000)\
            .filter(BenhNhan.DanhSachKham_id == DanhSachKham.id)\
            .filter(extract('month', DanhSachKham.NgayKham) == month) \
            .filter(PhieuKhamBenh.BenhNhan_id == BenhNhan.id) \
            .group_by(BenhNhan.id)\
            .all()


def count_phieu():
    return db.session.query(BenhNhan.id, func.count(PhieuKhamBenh.id)*100000)\
            .filter(PhieuKhamBenh.BenhNhan_id == BenhNhan.id)\
            .group_by(BenhNhan.id).all()
def count_revenue(month):
    return db.session.query(PhieuKhamBenh.BenhNhan_id, func.count(PhieuKhamBenh.id)*100000)\
        .filter(extract('month', PhieuKhamBenh.NgayKham) == month)\
        .group_by(PhieuKhamBenh.BenhNhan_id)\
        .filter(extract('month', PhieuKhamBenh.NgayKham) == month)\
        .all()

def get_id_phieukham(id):
    return db.session.query(ChiTietPhieuKhamBenh.id)\
            .filter(ChiTietPhieuKhamBenh.PhieuKhamBenh_id == PhieuKhamBenh.id)\
            .filter(PhieuKhamBenh.BenhNhan_id == id) \
            .all()


def get_dongia(id):
    return db.session.query(Thuoc.DonGia)\
            .filter(ChiTietPhieuKhamBenh.PhieuKhamBenh_id==id).all


if __name__ == '__main__':
    from QLPMT import app
    with app.app_context():
        # print(count_patient(12))
        #
        print(get_patient(12))
        # print(count_revenue(12))
        # print(count_phieu())
        # print(get_id_phieukham(1))
        # for i in get_id_phieukham(1):
        #     print(get_dongia(i.id))