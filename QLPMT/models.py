from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum, DateTime
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


class User(BaseModel, UserMixin):
    __tablename__ = 'User'

    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    image = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRole))

    BacSi = relationship('BacSi', backref='user', lazy=True)
    YTa = relationship('YTa', backref='user', lazy=True)
    ThuNgan = relationship('ThuNgan', backref='user', lazy=True)
    NguoiQuanTri = relationship('NguoiQuanTri', backref='user', lazy=True)

    def __str__(self):
        return self.name


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

    User_id = Column(Integer, ForeignKey(User.id), nullable=False)
    QuyDinhSoTienKham = relationship('QuyDinhSoTienKham',
                                     backref='nguoiquantri', lazy=True)

    QuyDinhSoBenhNhaKhamTrongNgay = relationship('QuyDinhSoBenhNhaKhamTrongNgay',
                                                 backref='nguoiquantri', lazy=True)


class QuyDinhSoTienKham(BaseModel):
    __tablename__ = 'SoTienKham'

    SoTienKham = Column(Integer, nullable=False)
    NguoiQuanTri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)
    HoaDon = relationship('HoaDon',
                          backref='SoTienKham', lazy=True)


class HoaDon(BaseModel):
    __tablename__ = 'HoaDon'
    ThuNgan_id = Column(Integer, ForeignKey(ThuNgan.id), nullable=False)
    SoTienKham_id = Column(Integer, ForeignKey(QuyDinhSoTienKham.id), nullable=False)

    PhieuKhamBenh = relationship('PhieuKhamBenh',
                                 backref='hoadon', lazy=True)


class DanhSachKham(BaseModel):
    __tablename__ = 'DanhSachKham'

    NgayKham = Column(DateTime, default=datetime.now())

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

    NgayKham = Column(DateTime, default=datetime.now())
    TrieuChung = Column(String(100), nullable=False)
    DuDoanBenh = Column(String(100), nullable=False)

    ChiTietPhieuKhamBenh = relationship('ChiTietPhieuKhamBenh',
                                        backref='phieukhambenh', lazy=True)
    BacSi_id = Column(Integer, ForeignKey(BacSi.id), nullable=False)
    BenhNhan_id = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    HoaDon_id = Column(Integer, ForeignKey(HoaDon.id), nullable=False)


class DonVi(BaseModel):
    __tablename__ = 'DonVi'

    TenDonVi = Column(String(20), nullable=False)
    Thuoc = relationship('Thuoc', backref='donvi', lazy=True)


class LoaiThuoc(BaseModel):
    __tablename__ = 'LoaiThuoc'

    TenLoaiThuoc = Column(String(50), nullable=False)
    Thuoc = relationship('Thuoc', backref='loaithuoc', lazy=True)


class Thuoc(BaseModel):
    __tablename__ = 'Thuoc'

    TenThuoc = Column(String(50), nullable=False)
    SoLuongConLai = Column(Integer, nullable=False)
    DonGia = Column(Integer, nullable=False)
    DonVi_id = Column(Integer, ForeignKey(DonVi.id), nullable=False)
    LoaiThuoc_id = Column(Integer, ForeignKey(LoaiThuoc.id), nullable=False)

    ChiTietPhieuKhamBenh = relationship('ChiTietPhieuKhamBenh',
                                        backref='thuoc', lazy=True)


class ChiTietPhieuKhamBenh(BaseModel):
    __tablename__ = 'ChiTietPhieuKhamBenh'

    SoLuong = Column(Integer, nullable=False)
    CachDung = Column(String(50), nullable=False)
    PhieuKhamBenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False)
    Thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=True)


class QuyDinhSoBenhNhaKhamTrongNgay(BaseModel):
    __tablename__ = 'SoBenhNhaKhamTrongNgay'

    SoBenhNhaKhamTrongNgay = Column(Integer, nullable=False)
    NguoiQuanTri_id = Column(Integer, ForeignKey(NguoiQuanTri.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #
        # import hashlib
        #
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u1 = User(name='Nguyen Van An', username='nguyenvanan', password=password,
        #           image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #           user_role=UserRole.NURSE)
        # u2 = User(name='Nguyen Do Tai', username='nguyendotai', password=password,
        #           image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #           user_role=UserRole.DOCTOR)
        # u3 = User(name='Nguyen Yen Phi', username='nguyenyenphi', password=password,
        #           image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #           user_role=UserRole.CASHIER)
        # u4 = User(name='Nguyen Thuy Linh', username='nguyenthuylinh', password=password,
        #           image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #           user_role=UserRole.ADMIN)
        #
        # db.session.add_all([u1, u2, u3, u4])
        # db.session.commit()
        #
        # yta = YTa(User_id=1)
        # bacsi = BacSi(User_id=2)
        # thungan = ThuNgan(User_id=3)
        # nqt = NguoiQuanTri(User_id=4)
        # db.session.add_all([yta])
        # db.session.commit()
        # db.session.add_all([bacsi])
        # db.session.commit()
        # db.session.add_all([thungan])
        # db.session.commit()
        # db.session.add_all([nqt])
        # db.session.commit()
        #
        # ds = DanhSachKham(YTa_id=1)
        # db.session.add_all([ds])
        # db.session.commit()
        #
        # stk = QuyDinhSoTienKham(SoTienKham=100000, NguoiQuanTri_id=1)
        # db.session.add_all([stk])
        # db.session.commit()
        #
        # hd = HoaDon(ThuNgan_id=1, SoTienKham_id=1)
        # db.session.add_all([hd])
        # db.session.commit()
        #
        # b1 = BenhNhan(HoTen='Nguyen Thi Anh', GioiTinh='Nam',
        #               NamSinh='2002', DiaChi='Go Vap', DanhSachKham_id=1)
        #
        # db.session.add_all([b1])
        # db.session.commit()
        # #
        # p1 = PhieuKhamBenh(TrieuChung='ho', DuDoanBenh='ho',
        #                    BacSi_id=1, BenhNhan_id=1, HoaDon_id=1)
        # p2 = PhieuKhamBenh(TrieuChung='ho', DuDoanBenh='ho',
        #                    BacSi_id=1, BenhNhan_id=1, HoaDon_id=1)
        # p3 = PhieuKhamBenh(TrieuChung='ho', DuDoanBenh='ho',
        #                    BacSi_id=1, BenhNhan_id=1, HoaDon_id=1)
        # db.session.add_all([p1, p2, p3])
        # db.session.commit()

        # dv1 = DonVi(TenDonVi='Vien')
        # dv2 = DonVi(TenDonVi='Chai')
        # dv3 = DonVi(TenDonVi='Vy')
        # db.session.add_all([dv1, dv2, dv3])
        # db.session.commit()
        #
        # lt1 = LoaiThuoc(TenLoaiThuoc="Thuốc gây nghiện")
        # lt2 = LoaiThuoc(TenLoaiThuoc="Thuốc kháng sinh")
        # lt3 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị virút")
        # lt4 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị nấm")
        # lt5 = LoaiThuoc(TenLoaiThuoc="Thuốc chống viêm không steroid ")
        # lt6 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị bệnh Gút")
        # lt7 = LoaiThuoc(TenLoaiThuoc="Thuốc cấp cứu và chống độc")
        # lt8 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị ung thư ")
        # lt9 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị parkinson")
        # lt10 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị lao")
        # lt11 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị sốt rét")
        # lt12 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị đau nửa đầu")
        # lt13 = LoaiThuoc(TenLoaiThuoc="Thuốc tác động lên quá trình đông máu")
        # lt14 = LoaiThuoc(TenLoaiThuoc="Máu, chế phẩm máu, dung dịch cao phân tử")
        # lt15 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị bệnh mạch vành")
        # lt16 = LoaiThuoc(TenLoaiThuoc="Thuốc dùng cho chẩn đoán")
        # lt17 = LoaiThuoc(TenLoaiThuoc="Thuốc lợi tiểu")
        # lt18 = LoaiThuoc(TenLoaiThuoc="Thuốc chống loét dạ dày")
        # lt19 = LoaiThuoc(TenLoaiThuoc="Hooc môn ")
        # lt20 = LoaiThuoc(TenLoaiThuoc="Huyết thanh và globulin miễn dịch")
        # lt21 = LoaiThuoc(TenLoaiThuoc="Thuốc giãn cơ và tăng trương lực cơ")
        # lt22 = LoaiThuoc(TenLoaiThuoc="Sinh phẩm dùng chữa bệnh (trừ men tiêu hoá)")
        # lt23 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị rối loạn cương")
        # lt24 = LoaiThuoc(TenLoaiThuoc="Dung dịch truyền tĩnh mạch.")
        # lt25 = LoaiThuoc(TenLoaiThuoc="Thuốc làm co, dãn đồng tử và giảm nhãn áp")
        # lt26 = LoaiThuoc(TenLoaiThuoc="Thuốc thúc đẻ, cầm máu sau đẻ và chống đẻ non")
        # lt27 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị hen")
        # lt28 = LoaiThuoc(TenLoaiThuoc="Thuốc chống loạn nhịp")
        # lt29 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị tăng huyết áp")
        # lt30 = LoaiThuoc(TenLoaiThuoc="Thuốc điều trị hạ huyết áp")
        #
        # db.session.add_all([lt1,
        #                     lt2,
        #                     lt3,
        #                     lt4,
        #                     lt5,
        #                     lt6,
        #                     lt7,
        #                     lt8,
        #                     lt9,
        #                     lt10,
        #                     lt11,
        #                     lt12,
        #                     lt13,
        #                     lt14,
        #                     lt15,
        #                     lt16,
        #                     lt17,
        #                     lt18,
        #                     lt19,
        #                     lt20,
        #                     lt21,
        #                     lt22,
        #                     lt23,
        #                     lt24,
        #                     lt25,
        #                     lt26,
        #                     lt27,
        #                     lt28,
        #                     lt29,
        #                     lt30])
        # db.session.commit()
        #
        # t1 = Thuoc(TenThuoc="Paracetamol", SoLuongConLai=100, DonGia=20000, DonVi_id=1, LoaiThuoc_id=1)
        # t2 = Thuoc(TenThuoc="Tylenol", SoLuongConLai=112, DonGia=22000, DonVi_id=1, LoaiThuoc_id=2)
        # t3 = Thuoc(TenThuoc="Hapacol", SoLuongConLai=124, DonGia=20300, DonVi_id=2, LoaiThuoc_id=3)
        # t4 = Thuoc(TenThuoc="Efferalgant", SoLuongConLai=123, DonGia=30000, DonVi_id=1, LoaiThuoc_id=15)
        # t5 = Thuoc(TenThuoc="Ibuprofen", SoLuongConLai=222, DonGia=20111, DonVi_id=2, LoaiThuoc_id=16)
        # t6 = Thuoc(TenThuoc="Mobic", SoLuongConLai=234, DonGia=32111, DonVi_id=1, LoaiThuoc_id=17)
        # t7 = Thuoc(TenThuoc="Alexan", SoLuongConLai=234, DonGia=63444, DonVi_id=2, LoaiThuoc_id=25)
        # t8 = Thuoc(TenThuoc="Smecta", SoLuongConLai=123, DonGia=50000, DonVi_id=1, LoaiThuoc_id=22)
        # t9 = Thuoc(TenThuoc="Motilum", SoLuongConLai=344, DonGia=100000, DonVi_id=1, LoaiThuoc_id=21)
        # t10 = Thuoc(TenThuoc="Becberin", SoLuongConLai=234, DonGia=20000, DonVi_id=1, LoaiThuoc_id=20)
        # t11 = Thuoc(TenThuoc="Loratadine", SoLuongConLai=4675, DonGia=932874, DonVi_id=3, LoaiThuoc_id=19)
        # t12 = Thuoc(TenThuoc="Betadine", SoLuongConLai=456, DonGia=29000, DonVi_id=2, LoaiThuoc_id=18)
        # t13 = Thuoc(TenThuoc="Ketamine", SoLuongConLai=456, DonGia=2000, DonVi_id=2, LoaiThuoc_id=1)
        # t14 = Thuoc(TenThuoc="Natufib", SoLuongConLai=345, DonGia=20000, DonVi_id=1, LoaiThuoc_id=2)
        # t15 = Thuoc(TenThuoc="Optibac", SoLuongConLai=643, DonGia=87990, DonVi_id=1, LoaiThuoc_id=3)
        # t16 = Thuoc(TenThuoc="Acetaminophen", SoLuongConLai=3434, DonGia=80000, DonVi_id=1, LoaiThuoc_id=4)
        # t17 = Thuoc(TenThuoc="Panadol Extrat1", SoLuongConLai=234, DonGia=43000, DonVi_id=1, LoaiThuoc_id=5)
        # t18 = Thuoc(TenThuoc="V Rohto", SoLuongConLai=234, DonGia=20000, DonVi_id=2, LoaiThuoc_id=24)
        # t19 = Thuoc(TenThuoc="Panthenol", SoLuongConLai=234, DonGia=20000, DonVi_id=2, LoaiThuoc_id=22)
        # t20 = Thuoc(TenThuoc="Hidrasec", SoLuongConLai=234, DonGia=20000, DonVi_id=1, LoaiThuoc_id=14)
        # t21 = Thuoc(TenThuoc="Amoxicillin ", SoLuongConLai=1235, DonGia=320000, DonVi_id=3, LoaiThuoc_id=4)
        # t22 = Thuoc(TenThuoc="Neocodion", SoLuongConLai=6457, DonGia=983000, DonVi_id=3, LoaiThuoc_id=15)
        # t23 = Thuoc(TenThuoc="Omeprazol", SoLuongConLai=645, DonGia=20000, DonVi_id=3, LoaiThuoc_id=5)
        # t24 = Thuoc(TenThuoc="Docxycyclin", SoLuongConLai=453, DonGia=20000, DonVi_id=1, LoaiThuoc_id=14)
        # t25 = Thuoc(TenThuoc="Cefnidir ", SoLuongConLai=345, DonGia=12900, DonVi_id=3, LoaiThuoc_id=5)
        # t26 = Thuoc(TenThuoc="Cefpodoxime", SoLuongConLai=3545, DonGia=20000, DonVi_id=1, LoaiThuoc_id=7)
        # t27 = Thuoc(TenThuoc="Celecoxib", SoLuongConLai=5345, DonGia=89000, DonVi_id=3, LoaiThuoc_id=30)
        # t28 = Thuoc(TenThuoc="Piroxicam", SoLuongConLai=345, DonGia=99000, DonVi_id=1, LoaiThuoc_id=20)
        # t29 = Thuoc(TenThuoc="Prednisolon", SoLuongConLai=3455, DonGia=600000, DonVi_id=3, LoaiThuoc_id=2)
        # t30 = Thuoc(TenThuoc="Methylprednisolon", SoLuongConLai=3453, DonGia=3000000, DonVi_id=1, LoaiThuoc_id=18)
        # db.session.add_all([t1,
        #                     t2,
        #                     t3,
        #                     t4,
        #                     t5,
        #                     t6,
        #                     t7,
        #                     t8,
        #                     t9,
        #                     t10,
        #                     t11,
        #                     t12,
        #                     t13,
        #                     t14,
        #                     t15,
        #                     t16,
        #                     t17,
        #                     t18,
        #                     t19,
        #                     t20,
        #                     t21,
        #                     t22,
        #                     t23,
        #                     t24,
        #                     t25,
        #                     t26,
        #                     t27,
        #                     t28,
        #                     t29,
        #                     t30
        #                     ])
        # db.session.commit()
        #
        # ctpk1 = ChiTietPhieuKhamBenh(SoLuong=12, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=1, Thuoc_id=1)
        # ctpk2 = ChiTietPhieuKhamBenh(SoLuong=22, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=2, Thuoc_id=2)
        # ctpk3 = ChiTietPhieuKhamBenh(SoLuong=14, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=3, Thuoc_id=3)
        # ctpk4 = ChiTietPhieuKhamBenh(SoLuong=17, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=2, Thuoc_id=12)
        # ctpk5 = ChiTietPhieuKhamBenh(SoLuong=15, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=2, Thuoc_id=15)
        # ctpk6 = ChiTietPhieuKhamBenh(SoLuong=15, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=2, Thuoc_id=20)
        # ctpk7 = ChiTietPhieuKhamBenh(SoLuong=14, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=3, Thuoc_id=23)
        # ctpk8 = ChiTietPhieuKhamBenh(SoLuong=11, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=3, Thuoc_id=4)
        # ctpk9 = ChiTietPhieuKhamBenh(SoLuong=8, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=3, Thuoc_id=22)
        # ctpk10 = ChiTietPhieuKhamBenh(SoLuong=18, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=3, Thuoc_id=23)
        # ctpk11 = ChiTietPhieuKhamBenh(SoLuong=12, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=3, Thuoc_id=12)
        # ctpk12 = ChiTietPhieuKhamBenh(SoLuong=20, CachDung="Sang trua chieu",
        #                              PhieuKhamBenh_id=3, Thuoc_id=28)
        #
        # db.session.add_all([
        #                     ctpk2,
        #
        #                     ])
        # db.session.commit()
