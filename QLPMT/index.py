from datetime import date
from threading import Timer

from flask import render_template, request, redirect, session, jsonify, url_for
from QLPMT import app, dao, login
from flask_login import login_user, logout_user, current_user, login_required
from QLPMT.decorators import annonymous_user
import cloudinary.uploader


@app.route("/")
def index():
    return render_template('index.html')


# Dang ky kham truc tuyen
@app.route('/online-register', methods=['get', 'post'])
def online_register():
    err_msg = ''
    today = date.today()
    new_today_date = today.strftime("%d/%m/%Y")
    DanhSachKham_id = dao.get_id_danhsachkham()
    if request.method.__eq__('POST'):
        DanhSachKham_id = dao.get_id_danhsachkham()
        NgayKhamDsKham = dao.get_date_in_danhsachkham().strftime("%d/%m/%Y")
        if new_today_date != NgayKhamDsKham:
            dao.add_danhsachkham(ngaykham=today)
            DanhSachKham_id = dao.get_id_danhsachkham()
        HoTen = request.form['name']
        GioiTinh = request.form['sex']
        NamSinh = request.form['year']
        DiaChi = request.form['address']
        if dao.count_patient_by_id(DanhSachKham_id=DanhSachKham_id) < dao.get_so_luong_benh_nhan_kham_trong_ngay():
            dao.online_register(HoTen=HoTen,
                                GioiTinh=GioiTinh,
                                NamSinh=NamSinh,
                                DiaChi=DiaChi,
                                DanhSachKham_id=DanhSachKham_id)
            err_msg = 'Đăng ký khám thành công'
        else:
            err_msg = 'Đăng ký không thành công vì vượt quá bệnh nhân khám trong ngày'
    return render_template('online_register.html',
                           err_msg=err_msg, )


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        type = request.form['optradio']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['image'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password,
                             avatar=avatar,
                             type=type)

                return redirect('/login')
            except:
                err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/medical_list/', defaults={'id': None}, methods=['get', 'post'])
@app.route('/medical_list/<int:id>', methods=['get', 'post'])
@login_required
def medical_list(id):
    err_msg = ''
    if current_user.is_authenticated:
        try:
            if id:
                dao.delete_patient(id=id)
        except:
            pass
        today = date.today()
        new_today_date = today.strftime("%d/%m/%Y")
        DanhSachKham_id = dao.get_id_danhsachkham()
        if request.method.__eq__('POST'):
            # Kiểm tra ngày khám của danh sách khám
            # Nếu ngày khám hiện tại khác ngày khám của danh sách khám trước đó
            # thì thêm danh sách khám mới và cập nhật số lượng bệnh nhân lại
            DanhSachKham_id = dao.get_id_danhsachkham()
            NgayKhamDsKham = dao.get_date_in_danhsachkham().strftime("%d/%m/%Y")
            if new_today_date != NgayKhamDsKham:
                dao.add_danhsachkham(ngaykham=today)
                DanhSachKham_id = dao.get_id_danhsachkham()
            HoTen = request.form['name']
            GioiTinh = request.form['sex']
            NamSinh = request.form['year']
            DiaChi = request.form['address']
            if dao.count_patient_by_id(DanhSachKham_id=DanhSachKham_id) < \
                    dao.get_so_luong_benh_nhan_kham_trong_ngay():
                dao.online_register(HoTen=HoTen, GioiTinh=GioiTinh,
                                    NamSinh=NamSinh, DiaChi=DiaChi,
                                    DanhSachKham_id=DanhSachKham_id)
                err_msg = 'Đăng ký khám thành công'
            else:
                err_msg = 'Vượt quá bệnh nhân khám trong ngày'
        b = dao.load_BenhNhan(DanhSachKham_id=DanhSachKham_id)
        return render_template('medical_list.html', err_msg=err_msg,
                               benhnhan=b,
                               new_today_date=new_today_date)
    return render_template('index.html')


@app.route('/medical-report', methods=['get', 'post'])
@login_required
def medical_report():
    if current_user.is_authenticated:
        err_msg = ''
        if current_user.user_role == 'NURSE':
            if request.method.__eq__('POST'):
                render_template('medical_list.html')
        else:
            err_msg = 'Y tá mới được phép lập danh sách khám'
            render_template('index.html', err_msg)
    else:
        render_template('index.html')


@app.route('/payment_bill', methods=['get', 'post'])
@login_required
def payment_bill():
    err_msg = ''
    today = date.today()
    new_today_date = today.strftime("%d/%m/%Y")
    ngaykham = ''
    tongtienkham = 0
    if request.method.__eq__('POST'):
        id = request.form['id']
        tienthuoc = 0
        tongtien = 0
        ten = ''
        try:
            ten = dao.get_name(id)
            sophieu = dao.count_bill(id)
            tienkham = dao.tien_kham()
            tongtienkham = sophieu * tienkham
            try:
                ngaykham = dao.get_date(id).strftime("%d/%m/%Y")
                arr_dongia_soluong = dao.get_don_gia_so_luong(id=id)
                for chitietphieukham, phieu, thuoc in arr_dongia_soluong:
                    tienthuoc += chitietphieukham.SoLuong * thuoc.DonGia
                tongtien = tongtienkham + tienthuoc
            except:
                err_msg = 'Không tìm thấy phiếu khám bệnh của bệnh nhân'
        except:
            err_msg = 'Không tìm thấy bệnh nhân trong hệ thống'

        return render_template('payment_bill.html',
                               ten=ten,
                               ngaykham=ngaykham,
                               tongtienkham=tongtienkham,
                               tienthuoc=tienthuoc,
                               new_today_date=new_today_date,
                               tongtien=tongtien,
                               err_msg=err_msg)
    return render_template('payment_bill.html', new_today_date=new_today_date)


@app.route('/login', methods=['get', 'post'])
@annonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user=user)
            n = request.args.get("next")
            return redirect(n if n else '/')

    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


if __name__ == "__main__":
    from QLPMT.admin import *

    app.run(debug=True)
