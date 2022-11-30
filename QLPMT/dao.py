from QLPMT.models import User, BenhNhan, DanhSachKham, UserRole, UserLogin, PhieuKhamBenh
from QLPMT import db
import hashlib


def online_register(HoTen, GioiTinh, NamSinh, DiaChi, DanhSachKham_id):
    b = BenhNhan(HoTen=HoTen, GioiTinh=GioiTinh, NamSinh=NamSinh, DiaChi=DiaChi, DanhSachKham_id=DanhSachKham_id)
    db.session.add(b)
    db.session.commit()


def count_patient():
    return db.session.query(BenhNhan).count()


def load_BenhNhan():
    return BenhNhan.query.all()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return UserLogin.query.filter(UserLogin.username.__eq__(username.strip()),
                                  UserLogin.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return UserLogin.query.get(user_id)


def get_phieukhambenn(id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.BenhNhan_id == id).all()


def register(name, username, password, avatar, type):
    if type == 'doctor':
        type = UserRole.DOCTOR
    elif type == 'nurse':
        type = UserRole.NURSE
    elif type == 'cashier':
        type = UserRole.CASHIER
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = UserLogin(name=name, username=username.strip(),
                  password=password, image=avatar, user_role=type)
    db.session.add(u)
    db.session.commit()
