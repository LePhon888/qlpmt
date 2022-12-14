from datetime import date, datetime
from threading import Timer

from flask import render_template, request, redirect, session, jsonify, url_for, make_response
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
        NgayKhamDsKham = dao.get_date_in_danhsachkham().strftime("%d/%m/%Y")
        if new_today_date != NgayKhamDsKham:
            dao.add_danhsachkham(ngaykham=today)
            DanhSachKham_id = dao.get_id_danhsachkham()
        b = dao.load_BenhNhan(DanhSachKham_id=DanhSachKham_id)

        if request.method.__eq__('POST'):
            # Kiểm tra ngày khám của danh sách khám
            # Nếu ngày khám hiện tại khác ngày khám của danh sách khám trước đó
            # thì thêm danh sách khám mới và cập nhật số lượng bệnh nhân lại
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


# Phieu kham benh
@app.route('/medical-report', methods=['get', 'post'])
def medical_report():
    key = app.config['MEDICAL_REPORT_KEY']
    med_report = session.get(key)
    med_type = dao.load_med_type()
    med_info = dao.load_med_info()
    med_name = dao.load_med_name()
    err_msg = ''
    # if current_user.is_authenticated:
    #     err_msg = ''
    #     if current_user.user_role == 'NURSE':
    #         if request.method.__eq__('POST'):
    #             render_template('list.html')
    #     else:
    #         err_msg = 'Y tá mới được phép lập danh sách khám'
    #         render_template('index.html', err_msg)
    # else:
    #     render_template('index.html')
    if request.method.__eq__('POST'):
        try:
            for k in med_report:
                data = med_report[k]
                dao.add_medical_report(ngaykham=data.get('report_date'),
                                       mabenhnhan=int(data.get('patient_id')),
                                       trieuchung=data.get('symptoms'),
                                       dudoanbenh=data.get('diagnose'))
                dao.add_detial_medical_report(tenloaithuoc=data.get('med_type'),
                                              tenthuoc=data.get('med_name'),
                                              soluong=int(data.get('med_quantity')),
                                              cachdung=data.get('med_usage'))
                dao.update_med_amount(med_name=data.get('med_name'), amount=data.get('med_quantity'))
                err_msg = "Lưu phiếu khám bệnh thành công!!!"
        except:
            err_msg = 'Hệ thống đang có lỗi! Vui lòng quay lại sau!'
    return render_template('medical_report.html', med_info=med_info, med_type=med_type, med_name=med_name,
                           err_msg=err_msg)


@app.route('/api/load-med-name', methods=['post'])
def load_med_name_by_type():
    key = app.config['MEDICAL_NAME_KEY']
    med_name = session.get(key)
    data = request.json
    med_type = data['med_type']
    print(med_type)
    result = []
    filter = dao.load_med_name(med_type=med_type)
    print(filter)
    for item in filter:
        result.append({
            'med_name': item.TenThuoc
        })
        med_name = result
    session[key] = med_name
    print(len(med_name))
    res = make_response(jsonify(med_name), 200)
    return res


@app.route('/api/save-med-report', methods=['post'])
def load_save_med_report():
    key = app.config['MEDICAL_REPORT_SAVE_KEY']
    data = request.json
    report_date = data['report_date']
    patient_id = data['patient_id']
    symptoms = data['symptoms']
    diagnose = data['diagnose']
    med_name = data['med_name']
    med_type = data['med_type']
    med_quantity = data['med_quantity']
    med_usage = data['med_usage']
    not_included_med = data['not_included_med']
    if not_included_med == 'on':
        not_included_med = '0'
    med_report_save = {
        "report_date": report_date,
        "patient_id": patient_id,
        "symptoms": symptoms,
        "diagnose": diagnose,
        "med_name": med_name,
        "med_type": med_type,
        "med_quantity": med_quantity,
        "med_usage": med_usage,
        "not_included_med": not_included_med
    }
    med_report_save = {k: v for k, v in med_report_save.items() if v is not None}
    session[key] = med_report_save
    res = make_response(jsonify(med_report_save), 200)
    return res


@app.route('/api/load-patient-med-report', methods=['post'])
def load_med_report():
    data = request.json
    patient_id = data['patient_id']
    temp_list = []
    filter = dao.get_medical_date_of_patient(patient_id=patient_id)
    for id in range((len(filter))):
        for item in filter:
            temp_list.append({

                'med_date': item.PhieuKhamBenh.NgayKham.strftime("%d/%m/%Y"),
                'patient_name': item.BenhNhan.HoTen
            })
    res = []
    [res.append(x) for x in temp_list if x not in res]
    res = make_response(jsonify(res), 200)
    return res


@app.route('/api/show-patient-med-report', methods=['post'])
def show_patient_med_report_by_date():
    data = request.json
    patient_id = data['patient_id']
    med_date = data['med_date']
    print(patient_id)
    print("Ngay:", med_date)
    temp_list = []
    filter = dao.load_all_medical_report(patient_id=patient_id, med_date=med_date)
    print(filter)
    print(len(filter))
    for id in range((len(filter))):
        for item in filter:
            if item.PhieuKhamBenh.NgayKham.strftime("%d/%m/%Y") == med_date:
                if not isinstance(item.Thuoc, type(None)):
                    temp_list.append({
                        "med_date": med_date,
                        "symptoms": item.PhieuKhamBenh.TrieuChung,
                        "diagnose": item.PhieuKhamBenh.DuDoanBenh,
                        "med_name": item.Thuoc.TenThuoc,
                        "med_type": item.LoaiThuoc.TenLoaiThuoc,
                        "med_unit": item.DonVi.TenDonVi,
                        "med_quantity": item.ChiTietPhieuKhamBenh.SoLuong,
                        "med_usage": item.ChiTietPhieuKhamBenh.CachDung
                    })
                else:
                    temp_list.append({
                        "med_date": med_date,
                        "symptoms": item.PhieuKhamBenh.TrieuChung,
                        "diagnose": item.PhieuKhamBenh.DuDoanBenh
                    })

    res = []
    [res.append(x) for x in temp_list if x not in res]
    print(res)
    res = make_response(jsonify(res), 200)
    return res


@app.route('/api/clear-med-report')
def clear_med_report_session():
    key = app.config['MEDICAL_REPORT_KEY']
    key2 = app.config['MEDICAL_REPORT_SAVE_KEY']
    try:
        del session[key]
        del session[key2]
        return jsonify({'status': 204})
    except:
        return jsonify({'status': 404})


@app.route('/api/add-med-report', methods=['post'])
def add_med_to_report():
    key = app.config['MEDICAL_REPORT_KEY']
    med_report = session[key] if key in session else {}
    data = request.json
    patient_id = data['patient_id']
    patient_name = dao.get_patient_name(patient_id)
    report_date = data['report_date']
    med_name = data['med_name']
    med_quantity = data['med_quantity']
    symptoms = data['symptoms']
    diagnose = data['diagnose']
    med_type = data['med_type']
    med_unit = dao.get_med_unit(med_name)
    med_usage = data['med_usage']

    if patient_name is None:
        med_report.clear()
        print(med_report)
        print(patient_name)
    else:
        if any(d['patient_id'] != patient_id for d in med_report.values()):
            med_report.clear()
        if any(d['patient_id'] == patient_id for d in med_report.values()):
            if any(d['med_name'] == '' for d in med_report.values()):
                med_report.clear()
        if any(d['med_name'] == med_name for d in med_report.values()):
            dict = ','.join([str(item) for item in (key for key in med_report if med_name in med_report[key].values())])
            print('phat hien co trung')
            print(dict)
            result = int(med_report[dict]["med_quantity"]) + med_quantity
            med_report[dict]["med_quantity"] = str(result)
        else:
            id = str(len(med_report) + 1)
            med_report[id] = {
                "id": id,
                "report_date": report_date,
                "patient_id": patient_id,
                "patient_name": patient_name,
                "symptoms": symptoms,
                "diagnose": diagnose,
                "med_name": med_name,
                "med_type": med_type,
                "med_unit": med_unit,
                "med_quantity": med_quantity,
                "med_usage": med_usage
            }
    session[key] = med_report
    print(med_report)
    print(len(med_report))
    # med_report.clear()
    res = make_response(jsonify(med_report), 200)
    return res


@app.route('/api/delete-med-report', methods=['delete'])
def delete_med_in_report():
    key = app.config['MEDICAL_REPORT_KEY']
    med_report = session.get(key)
    data = request.json
    id = str(data['id'])
    pos = int(id)
    if med_report and id in med_report:
        print(med_report.keys())
        del med_report[id]
        temp_dict = {}
        for key in list(med_report.keys()):
            if int(key) > pos:
                print('gia tri cua keys la: ', key)
                for i in range(pos, len(med_report) + 1):
                    new_key = i
                    print('day la lan thu: ' + str(i) + ' gia tri cua new key: ', new_key)
                    if int(key) > new_key:
                        temp_dict[key] = str(new_key)
                        print('day la lan thu: ' + str(i) + ' gia tri cua temp dict: ', temp_dict)
        for old, new in temp_dict.items():
            print('gia tri cua old: ', old)
            med_report[new] = med_report.pop(str(old))
            med_report[new]["id"] = str(new)
    session[key] = med_report
    print(med_report)
    res = make_response(jsonify(med_report), 200)
    return res




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
