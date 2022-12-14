from flask import session
from flask_sqlalchemy.session import Session

from sqlalchemy import func, extract, union

from QLPMT.models import User, BenhNhan, DanhSachKham, UserRole, PhieuKhamBenh, QuyDinhSoTienKham, ChiTietPhieuKhamBenh, \
    Thuoc, QuyDinhSoBenhNhaKhamTrongNgay, HoaDon, DonVi, LoaiThuoc
from QLPMT import db
import hashlib


def get_so_luong_benh_nhan_kham_trong_ngay():
    return db.session.query(QuyDinhSoBenhNhaKhamTrongNgay) \
        .order_by(QuyDinhSoBenhNhaKhamTrongNgay.id.desc()).first() \
        .SoBenhNhanKhamTrongNgay


def online_register(HoTen, GioiTinh, NamSinh, DiaChi, DanhSachKham_id):
    b = BenhNhan(HoTen=HoTen, GioiTinh=GioiTinh, NamSinh=NamSinh, DiaChi=DiaChi, DanhSachKham_id=DanhSachKham_id)
    db.session.add(b)
    db.session.commit()


def count_patient_by_id(DanhSachKham_id):
    return db.session.query(func.count(BenhNhan.id)).filter(DanhSachKham_id == DanhSachKham_id).count()


def load_BenhNhan(DanhSachKham_id):
    return BenhNhan.query.filter(BenhNhan.DanhSachKham_id == DanhSachKham_id).all()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_phieukhambenh(id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.BenhNhan_id == id).all()


def get_name(id):
    return BenhNhan.query.get(id).HoTen


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


def get_ngaykham_danhsachkham():
    return db.session.query(DanhSachKham) \
        .order_by(DanhSachKham.id.desc()).first().NgayKham


def delete_patient(id):
    b = BenhNhan.query.get(id)
    db.session.delete(b)
    db.session.commit()


# Phieu kham benh
def add_medical_report(ngaykham, mabenhnhan, trieuchung, dudoanbenh):
    pk = PhieuKhamBenh(NgayKham=ngaykham, TrieuChung=trieuchung, DuDoanBenh=dudoanbenh, BacSi_id=1,
                       BenhNhan_id=mabenhnhan, HoaDon_id=1)
    db.session.add(pk)
    db.session.commit()


def add_detial_medical_report(tenloaithuoc, tenthuoc, soluong, cachdung):
    thuoc_id = get_med_id(tenthuoc, tenloaithuoc)
    phieukham_id = (get_medical_report_last_id())
    ctpkb = ChiTietPhieuKhamBenh(SoLuong=soluong, CachDung=cachdung, PhieuKhamBenh_id=phieukham_id,
                                 Thuoc_id=thuoc_id)
    db.session.add(ctpkb)
    db.session.commit()


def load_med_name(med_type=None):
    if med_type:
        return Thuoc.query. \
            filter(Thuoc.LoaiThuoc_id == LoaiThuoc.id).filter(LoaiThuoc.TenLoaiThuoc == med_type).all()
    return Thuoc.query.all()


def load_med_type():
    return LoaiThuoc.query.all()


def load_med_info():
    return db.session.query(Thuoc, LoaiThuoc, DonVi). \
        join(LoaiThuoc, Thuoc.LoaiThuoc_id == LoaiThuoc.id). \
        join(DonVi, Thuoc.DonVi_id == DonVi.id). \
        order_by(Thuoc.id.asc()).all()


def get_med_type_id(med_type):
    return db.session.query(LoaiThuoc.id).filter(LoaiThuoc.TenLoaiThuoc.__eq__(med_type)).all()


def get_med_id(med_name=None, med_type=None):
    return db.session.query(Thuoc.id).filter(LoaiThuoc.TenLoaiThuoc.__eq__(med_type),
                                             Thuoc.TenThuoc.__eq__(med_name),
                                             Thuoc.LoaiThuoc_id.__eq__(LoaiThuoc.id)).scalar()


def get_medical_date_of_patient(patient_id):
    return db.session.query(ChiTietPhieuKhamBenh, PhieuKhamBenh, BenhNhan). \
        join(PhieuKhamBenh, ChiTietPhieuKhamBenh.PhieuKhamBenh_id.__eq__(PhieuKhamBenh.id)). \
        join(BenhNhan, PhieuKhamBenh.BenhNhan_id.__eq__(BenhNhan.id)). \
        filter(BenhNhan.id.__eq__(patient_id)).all()


def load_all_medical_report(patient_id, med_date):
    return db.session.query(ChiTietPhieuKhamBenh, PhieuKhamBenh, BenhNhan, Thuoc, LoaiThuoc, DonVi). \
        join(PhieuKhamBenh, ChiTietPhieuKhamBenh.PhieuKhamBenh_id.__eq__(PhieuKhamBenh.id), isouter=True). \
        join(BenhNhan, PhieuKhamBenh.BenhNhan_id.__eq__(BenhNhan.id), isouter=True). \
        join(Thuoc, ChiTietPhieuKhamBenh.Thuoc_id.__eq__(Thuoc.id), isouter=True). \
        join(DonVi, Thuoc.DonVi_id.__eq__(DonVi.id), isouter=True). \
        join(LoaiThuoc, Thuoc.LoaiThuoc_id.__eq__(LoaiThuoc.id), isouter=True). \
        filter(BenhNhan.id.__eq__(patient_id) and PhieuKhamBenh.NgayKham.strftime("%d%m%Y") == med_date).all()


def some_test():
    return db.session.query()


def get_medical_report_last_id():
    return db.session.query(func.max(PhieuKhamBenh.id)).scalar()


def get_payment_last_id():
    return db.session.query(func.max(HoaDon.id)).scalar()


def update_med_amount(med_name, amount):
    db.session.query(Thuoc).filter(Thuoc.TenThuoc.__eq__(med_name)). \
        update({'SoLuongConLai': Thuoc.SoLuongConLai - amount})
    db.session.commit()


def get_med_unit(med_name):
    return db.session.query(DonVi.TenDonVi).join(Thuoc, Thuoc.DonVi_id.__eq__(DonVi.id)). \
        filter(Thuoc.TenThuoc.__eq__(med_name)).scalar()


def get_patient_name(id):
    return db.session.query(BenhNhan.HoTen).filter(BenhNhan.id.__eq__(id)).scalar()


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


def get_thuoc(month):
    return db.session.query(ChiTietPhieuKhamBenh.Thuoc_id,
                            Thuoc.TenThuoc,
                            DonVi.TenDonVi,
                            Thuoc.SoLuongConLai,
                            func.sum(ChiTietPhieuKhamBenh.SoLuong)) \
        .join(ChiTietPhieuKhamBenh, ChiTietPhieuKhamBenh.Thuoc_id.__eq__(Thuoc.id)) \
        .filter(ChiTietPhieuKhamBenh.PhieuKhamBenh_id == PhieuKhamBenh.id) \
        .filter(extract('month', PhieuKhamBenh.NgayKham) == month) \
        .filter(Thuoc.DonVi_id == DonVi.id) \
        .group_by(ChiTietPhieuKhamBenh.Thuoc_id) \
        .all()


def get_revenue(month):
    return db.session.query(DanhSachKham.NgayKham, Thuoc.TenThuoc,
                            func.count(BenhNhan.id),
                            func.count(PhieuKhamBenh.id) * tien_kham() +
                            func.sum(ChiTietPhieuKhamBenh.SoLuong * Thuoc.DonGia)) \
        .join(ChiTietPhieuKhamBenh, ChiTietPhieuKhamBenh.Thuoc_id.__eq__(Thuoc.id)) \
        .join(PhieuKhamBenh, ChiTietPhieuKhamBenh.PhieuKhamBenh_id.__eq__(PhieuKhamBenh.id)) \
        .join(BenhNhan, PhieuKhamBenh.BenhNhan_id.__eq__(BenhNhan.id)) \
        .join(DanhSachKham, BenhNhan.DanhSachKham_id.__eq__(DanhSachKham.id)) \
        .filter(extract('month', DanhSachKham.NgayKham) == month) \
        .group_by(DanhSachKham.NgayKham) \
        .all()


def count_patient(month):
    # ngay sobenhnhan doanhthu
    return db.session.query(DanhSachKham.NgayKham, func.count(BenhNhan.id)) \
        .join(BenhNhan, BenhNhan.DanhSachKham_id.__eq__(DanhSachKham.id)) \
        .filter(extract('month', DanhSachKham.NgayKham) == month) \
        .group_by(DanhSachKham.id) \
        .all()


if __name__ == '__main__':
    from QLPMT import app

    with app.app_context():
        print(get_revenue(12))
        # print(count_patient(12))
        # print(get_ngaykham_danhsachkham())