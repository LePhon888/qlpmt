from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum, Date
from sqlalchemy.orm import relationship
from QLPMT import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    DOCTOR = 1
    NURSE = 2
    CASHIER = 3
    ADMIN = 4


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel):
    __tablename__ = 'User'

    name = Column(String(50), nullable=False)
    # username = Column(String(50), nullable=False)
    # password = Column(String(50), nullable=False)
    # active = Column(Boolean, default=True)
    # user_role = Column(Enum(UserRole))
    BacSi = relationship('BacSi', backref='user', lazy=True)
    YTa = relationship('YTa', backref='user', lazy=True)
    ThuNgan = relationship('ThuNgan', backref='user', lazy=True)

    # def __str__(self):
    #     return self.name


class BacSi(BaseModel):
    __tablename__ = 'BacSi'

    User_id = Column(Integer, ForeignKey(User.id), nullable=False)

    PhieuKhamBenh = relationship('PhieuKhamBenh',
                                 backref='bacsi', lazy=True)


class YTa(BaseModel):
    __tablename__ = 'YTa'

    User_id = Column(Integer, ForeignKey(User.id), nullable=False)

    DanhSachKham = relationship('DanhSachKham',
                                backref='yta', lazy=True)


class ThuNgan(BaseModel):
    __tablename__ = 'ThuNgan'

    User_id = Column(Integer, ForeignKey(User.id), nullable=False)
    HoaDon = relationship('HoaDon',
                          backref='thungan', lazy=True)


class NguoiQuanTri(BaseModel):
    __tablename__ = 'NguoiQuanTri'

    HoTen = Column(String(50), nullable=False)

    QuanLyLoaiThuoc = relationship('QuanLyLoaiThuoc', backref='nguoiquantri', lazy=True)
    QuanLyLoaiDonVi = relationship('QuanLyLoaiDonVi', backref='nguoiquantri', lazy=True)
    ThongKeBaoCao = relationship('ThongKeBaoCao', backref='nguoiquantri', lazy=True)
    QuyDinh = relationship('QuyDinh', backref='nguoiquantri', lazy=True)


class QuyDinh(BaseModel):
    __tablename__ = 'QuyDinh'

    NguoiQuanTri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)
    SoTienKham = relationship('SoTienKham', backref='QuyDinh', lazy=True)
    SoBenhNhaKhamTrongNgay = relationship('SoBenhNhaKhamTrongNgay', backref='QuyDinh', lazy=True)


class SoTienKham(BaseModel):
    __tablename__ = 'SoTienKham'

    SoTienKham = Column(Integer, nullable=False)
    QuyDinh_id = Column(Integer, ForeignKey(QuyDinh.id), nullable=False)
    HoaDon = relationship('HoaDon',
                          backref='SoTienKham', lazy=True)


class HoaDon(BaseModel):
    __tablename__ = 'HoaDon'
    TienDonThuoc = Column(Integer, nullable=True)
    ThuNgan_id = Column(Integer, ForeignKey(ThuNgan.id), nullable=False)
    SoTienKham_id = Column(Integer, ForeignKey(SoTienKham.id), nullable=False)

    PhieuKhamBenh = relationship('PhieuKhamBenh',
                                 backref='hoadon', lazy=True)


class DanhSachKham(BaseModel):
    __tablename__ = 'DanhSachKham'

    NgayKham = Column(Date, nullable=False)

    YTa_id = Column(Integer, ForeignKey(YTa.id), nullable=False)

    BenhNhan = relationship('BenhNhan',
                            backref='danhsachkham', lazy=True)


class BenhNhan(BaseModel):
    __tablename__ = 'BenhNhan'

    HoTen = Column(String(50), nullable=False)
    GioiTinh = Column(String(10), nullable=False)
    NamSinh = Column(Integer, nullable=False)
    DiaChi = Column(String(100), nullable=False)

    PhieuKhamBenh = relationship('PhieuKhamBenh',
                                 backref='benhnhan', lazy=True)
    DanhSachKham_id = Column(Integer, ForeignKey(DanhSachKham.id), nullable=False)


class PhieuKhamBenh(BaseModel):
    __tablename__ = 'PhieuKhamBenh'

    NgayKham = Column(Date, nullable=False)
    TrieuChung = Column(String(100), nullable=False)
    DuDoanBenh = Column(String(100), nullable=False)

    ChiTietPhieuKhamBenh = relationship('ChiTietPhieuKhamBenh',
                                        backref='phieukhambenh', lazy=True)
    BacSi_id = Column(Integer, ForeignKey(BacSi.id), nullable=False)
    BenhNhan_id = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    HoaDon_id = Column(Integer, ForeignKey(HoaDon.id), nullable=False)


class QuanLyLoaiThuoc(BaseModel):
    __tablename__ = 'QuanLyLoaiThuoc'

    LoaiThuoc = relationship('LoaiThuoc', backref='loaithuoc', lazy=True)
    NguoiQuanTri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)


class QuanLyLoaiDonVi(BaseModel):
    __tablename__ = 'QuanLyLoaiDonVi'

    LoaiDonViThuoc = relationship('DonVi', backref='donvi', lazy=True)
    NguoiQuanTri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)


class DonVi(BaseModel):
    __tablename__ = 'DonVi'

    TenDonVi = Column(String(20), nullable=False)
    Thuoc = relationship('Thuoc', backref='donvi', lazy=True)
    QuanLyDonVi_id = Column(Integer, ForeignKey(QuanLyLoaiDonVi.id), nullable=False)


class LoaiThuoc(BaseModel):
    __tablename__ = 'LoaiThuoc'

    TenLoaiThuoc = Column(String(50), nullable=False)

    Thuoc = relationship('Thuoc', backref='loaithuoc', lazy=True)
    QuanLyLoaiThuoc_id = Column(Integer, ForeignKey(QuanLyLoaiThuoc.id), nullable=False)


class Thuoc(BaseModel):
    __tablename__ = 'Thuoc'

    DonGia = Column(Integer, nullable=False)
    SoLuongConLai = Column(Integer, nullable=False)

    DonVi_id = Column(Integer, ForeignKey(DonVi.id), nullable=False)
    LoaiThuoc_id = Column(Integer, ForeignKey(LoaiThuoc.id), nullable=False)
    SuDungThuoc = relationship('SuDungThuoc', backref='thuoc', lazy=True)

    ChiTietPhieuKhamBenh = relationship('ChiTietPhieuKhamBenh',
                                        backref='thuoc', lazy=True)


class ChiTietPhieuKhamBenh(BaseModel):
    __tablename__ = 'ChiTietPhieuKhamBenh'

    SoLuong = Column(Integer, nullable=False)
    CachDung = Column(String(50), nullable=False)

    PhieuKhamBenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False)
    Thuoc_id = Column(Integer, ForeignKey(Thuoc.id))


class ThongKeBaoCao(BaseModel):
    __tablename__ = 'ThongKeBaoCao'

    Thang = Column(Integer, nullable=False)

    NguoiQuanTri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)
    SuDungThuoc = relationship('SuDungThuoc', backref='thongkebaocao', lazy=True)
    TanSuatKham = relationship('TanSuatKham', backref='thongkebaocao', lazy=True)
    DoanhThu = relationship('DoanhThu', backref='thongkebaocao', lazy=True)


class SuDungThuoc(BaseModel):
    __tablename__ = 'SuDungThuoc'

    ThongKeBaoCao_id = Column(Integer, ForeignKey(ThongKeBaoCao.id), nullable=False)
    Thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False)


class TanSuatKham(BaseModel):
    __tablename__ = 'TanSuatKham'

    GiaTri = Column(Integer, nullable=False)
    ThongKeBaoCao_id = Column(Integer, ForeignKey(ThongKeBaoCao.id), nullable=False)


# class DoanhThu(BaseModel, db.Model):
#     __tablename__ = 'DoanhThu'
#
#     TongDoanhThu = Column(Integer, nullable=False)
#     ThongKeBaoCao_id = Column(Integer, ForeignKey(ThongKeBaoCao.id), nullable=False)
#
#     # ChiTietBaoCaoDoanhThu = relationship('CTDT',
#     #                                      backref='doanhthu', lazy=True)


class DoanhThu(BaseModel):
    __tablename__ = 'DoanhThu'

    TongDoanhThu = Column(Integer, nullable=False)
    ThongKeBaoCao_id = Column(Integer, ForeignKey(ThongKeBaoCao.id), nullable=False)

    ChiTietDoanhThu = relationship('ChiTietDoanhThu',
                                   backref='DoanhThu', lazy=True)


class ChiTietDoanhThu(BaseModel):
    __tablename__ = 'ChiTietDoanhThu'

    Ngay = Column(Date, nullable=False)
    SoBenhNhan = Column(Integer, nullable=False)
    DoanhThuTheoNgay = Column(Integer, nullable=False)
    TiLe = Column(Integer, nullable=False)

    DoanhThu_id = Column(Integer, ForeignKey(DoanhThu.id), nullable=False)


class SoBenhNhaKhamTrongNgay(BaseModel):
    __tablename__ = 'SoBenhNhaKhamTrongNgay'

    SoBenhNhaKhamTrongNgay = Column(Integer, nullable=False)
    QuyDinh_id = Column(Integer, ForeignKey(QuyDinh.id), nullable=False)


class UserLogin(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    image = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.DOCTOR)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # u1 = User(name='Nguyen Van An')
        # u2 = User(name='Nguyen Do Tai')
        # u3 = User(name='Nguyen Yen Phi')
        # u4 = User(name='Nguyen Thuy Linh')
        #
        # db.session.add_all([u1, u2, u3, u4])
        # db.session.commit()

        # yta1 = YTa(User_id=1)
        # yta2 = YTa(User_id=2)
        #
        # db.session.add_all([yta1, yta2])
        # db.session.commit()

        # ds1 = DanhSachKham(NgayKham='2020-01-02', YTa_id=1)
        # db.session.add_all([ds1])
        # db.session.commit()

        p1 = PhieuKhamBenh(NgayKham='2020-01-22', TrieuChung='ho', DuDoanBenh='ho',
                           BacSi_id=1, BenhNhan_id=1, HoaDon_id=1)
        p2 = PhieuKhamBenh(NgayKham='2020-01-27', TrieuChung='ho', DuDoanBenh='ho',
                           BacSi_id=1, BenhNhan_id=1, HoaDon_id=1)
        db.session.add_all([p2])
        db.session.commit()
        # import hashlib
        #
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u = UserLogin(username='admin', password=password, user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()
