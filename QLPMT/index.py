from datetime import date
from threading import Timer

from flask import render_template, request, redirect, session, jsonify, url_for
from QLPMT import app, dao, login
from flask_login import login_user, logout_user, current_user
from QLPMT.decorators import annonymous_user
import cloudinary.uploader


@app.route("/")
def index():
    return render_template('index.html')


# Dang ky kham truc tuyen
@app.route('/online-register', methods=['get', 'post'])
def online_register():
    err_msg = ''
    if request.method.__eq__('POST'):
        HoTen = request.form['name']
        GioiTinh = request.form['sex']
        NamSinh = request.form['year']
        DiaChi = request.form['address']
        if dao.count_patient() < dao.get_so_luong_benh_nhan_kham_trong_ngay():
            dao.online_register(HoTen=HoTen, GioiTinh=GioiTinh, NamSinh=NamSinh, DiaChi=DiaChi, DanhSachKham_id=1)
            err_msg = 'Đăng ký khám thành công'
        else:
            err_msg = 'Đăng ký không thành công vì vượt quá bệnh nhân khám trong ngày'
    return render_template('online_register.html', err_msg=err_msg)


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


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


@app.route('/list', methods=['get', 'post'])
def medical_list():
    if current_user.is_authenticated:
        err_msg = ''
        b = dao.load_BenhNhan()
        if request.method.__eq__('POST'):
            HoTen = request.form['name']
            GioiTinh = request.form['sex']
            NamSinh = request.form['year']
            DiaChi = request.form['address']
            if dao.count_patient() < dao.get_so_luong_benh_nhan_kham_trong_ngay():
                dao.online_register(HoTen=HoTen, GioiTinh=GioiTinh, NamSinh=NamSinh, DiaChi=DiaChi, DanhSachKham_id=1)
                err_msg = 'Đăng ký khám thành công'
                b = dao.load_BenhNhan()
            else:
                err_msg = 'Vượt quá bệnh nhân khám trong ngày'
        return render_template('list.html', err_msg=err_msg, benhnhan=b)
    return render_template('index.html')


@app.route('/medical-report', methods=['get', 'post'])
def medical_report():
    if current_user.is_authenticated:
        err_msg = ''
        if current_user.user_role == 'NURSE':
            if request.method.__eq__('POST'):
                render_template('list.html')
        else:
            err_msg = 'Y tá mới được phép lập danh sách khám'
            render_template('index.html', err_msg)
    else:
        render_template('index.html')



@app.route('/payment_bill', methods=['get', 'post'])
def payment_bill():
    err_msg = ''
    today = date.today()
    new_today_date = today.strftime("%d/%m/%Y")
    ngaykham = ''
    if request.method.__eq__('POST'):
        id = request.form['id']
        tienthuoc = 0
        ten = dao.get_name(id)
        sophieu = dao.count_bill(id)
        tienkham = dao.tien_kham()
        tongtienkham = sophieu * tienkham
        try:
            ngaykham = dao.get_date(id).strftime("%d/%m/%Y")
            arr_dongia_soluong = dao.get_don_gia_so_luong(id=id)
            for chitietphieukham, phieu, thuoc in arr_dongia_soluong:
                tienthuoc += chitietphieukham.SoLuong * thuoc.DonGia
        except:
            err_msg = 'Không tìm thấy phiếu khám bệnh của bệnh nhân'

        tongtien=tongtienkham+tienthuoc
        return render_template('payment_bill.html',
                           ten=ten,
                           ngaykham=ngaykham,
                           tongtienkham=tongtienkham,
                           tienthuoc=tienthuoc,
                           new_today_date=new_today_date,
                            tongtien=tongtien,
                               err_msg=err_msg)
    return render_template('payment_bill.html', new_today_date=new_today_date)

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    from QLPMT.admin import *
    app.run(debug=True)
