from datetime import date, datetime
from threading import Timer
from flask import render_template, request, redirect, session, jsonify, url_for, make_response, flash
from QLPMT import app, dao, login
from flask_login import login_user, logout_user, current_user, login_required
from QLPMT.decorators import annonymous_user, requires_access_level
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
                err_msg = 'Đăng ký khám thất bại vì vượt quá bệnh nhân khám trong ngày'
            b = dao.load_BenhNhan(DanhSachKham_id=DanhSachKham_id)
        return render_template('medical_list.html', err_msg=err_msg,
                               benhnhan=b,
                               new_today_date=new_today_date)
    return render_template('index.html')


####################################################


# Phieu kham benh

@app.route('/medical-report', methods=['get', 'post'])
@login_required
def medical_report():
    today = date.today()
    new_today_date = today.strftime("%d/%m/%Y")
    key = app.config['MEDICAL_REPORT_KEY']
    key2 = app.config['MEDICAL_REPORT_MEDICINE_KEY']
    medical_reports = session.get(key)
    medical_report_medicine = session.get(key2)
    med_type = dao.load_med_type()
    med_info = dao.load_med_info()
    med_name = dao.load_med_name()
    if request.method.__eq__('POST'):
        try:
            dao.add_payment(payment_id=int(medical_reports.get('patient_id')))
            dao.add_medical_report(ngaykham=medical_reports.get('report_date'),
                                   mabenhnhan=int(medical_reports.get('patient_id')),
                                   trieuchung=medical_reports.get('symptoms'),
                                   dudoanbenh=medical_reports.get('diagnose'))
            for key in medical_report_medicine.keys():
                data = medical_report_medicine[key]
                dao.add_detail_medical_report(tenloaithuoc=data.get('med_type'),
                                              tenthuoc=data.get('med_name'),
                                              soluong=int(data.get('med_quantity')),
                                              cachdung=data.get('med_usage'))
                dao.update_med_amount(med_name=data.get('med_name'), amount=data.get('med_quantity'))
            flash('Lưu phiếu khám bệnh thành công!!!')
            session.pop('medical_reports', None)
            session.pop('medical_report_medicine', None)
            session.pop('medical_report_save', None)
            return redirect('/medical-report')
        except Exception as ex:
            print(ex)
            flash('Lưu phiếu khám bệnh thất bại!!!')
    return render_template('medical_report.html', med_info=med_info, med_type=med_type, med_name=med_name, new_today_date=new_today_date)


@app.route('/api/load-med-name', methods=['post'])
def load_med_name_by_type():
    key = app.config['MEDICAL_NAME_KEY']
    med_name = session.get(key)
    data = request.json
    med_type = data['med_type']
    temp = dao.load_med_name(med_type=med_type)
    print(temp)
    print("do dai: ", len(temp))
    result = []
    if len(temp) != 0:
        for item in temp:
            result.append({
                'med_name': item.TenThuoc
            })
            med_name = result
    else:
        med_name = {}
    session[key] = med_name
    print(len(med_name))
    res = make_response(jsonify(med_name), 200)
    return res


@app.route('/api/save-med-report', methods=['post'])
def load_save_medical_report():
    key = app.config['MEDICAL_REPORT_SAVE_KEY']
    data = request.json
    not_included_med = data['not_included_med']
    if not_included_med == 'on':
        not_included_med = '0'
    medical_report_save = {
        "report_date": data['report_date'],
        "patient_id": data['patient_id'],
        "symptoms": data['symptoms'],
        "diagnose": data['diagnose'],
        "med_name": data['med_name'],
        "med_type": data['med_type'],
        "med_quantity": data['med_quantity'],
        "med_usage": data['med_usage'],
        "not_included_med": not_included_med
    }
    medical_report_save = {k: v for k, v in medical_report_save.items() if v is not None}
    session[key] = medical_report_save
    res = make_response(jsonify(medical_report_save), 200)
    return res


@app.route('/api/load-patient-med-report', methods=['post'])
def load_medical_report():
    data = request.json
    patient_id = int(data['patient_id'])
    temp = []
    patient_all_id = dao.get_all_patient_by_id(patient_id)
    print(len(patient_all_id))
    print(patient_all_id)
    for item in patient_all_id:
        temp += dao.get_medical_date_of_patient(int(item.id))
    print(temp)
    result = []
    added = set()
    for item in temp:
        if item.PhieuKhamBenh.NgayKham.strftime("%d/%m/%Y") not in added:
            result.append({
                'med_date': item.PhieuKhamBenh.NgayKham.strftime("%d/%m/%Y"),
                'patient_name': item.BenhNhan.HoTen,
                'patient_id': item.BenhNhan.id
            })
            added.add(item.PhieuKhamBenh.NgayKham.strftime("%d/%m/%Y"))
    print(result)
    res = make_response(jsonify(result), 200)
    return res


@app.route('/api/show-patient-med-report', methods=['post'])
def show_patient_medical_report_by_date():
    data = request.json
    patient_id = data['patient_id']
    med_date = data['med_date']
    temp = dao.get_medical_date_of_patient(patient_id=patient_id)
    result = []
    for item in temp:
        if item.PhieuKhamBenh.NgayKham.strftime("%d/%m/%Y") == med_date:
            dt = dao.load_detail_medical_report(item.PhieuKhamBenh.id)
            if len(dt) > 0:
                for d in dt:
                    if dt.index(d) == 0:
                        result.append({
                            "medical_report": {
                                "id": d.ChiTietPhieuKhamBenh.phieukhambenh.id,
                                "med_date": d.ChiTietPhieuKhamBenh.phieukhambenh.NgayKham.strftime("%d/%m/%Y"),
                                "patient_name": d.ChiTietPhieuKhamBenh.phieukhambenh.benhnhan.HoTen,
                                "symptoms": d.ChiTietPhieuKhamBenh.phieukhambenh.TrieuChung,
                                "diagnose": d.ChiTietPhieuKhamBenh.phieukhambenh.DuDoanBenh,
                                "med_included": 1
                            },
                            "medicine": {
                                "med_name": d.ChiTietPhieuKhamBenh.thuoc.TenThuoc,
                                "med_type": d.ChiTietPhieuKhamBenh.thuoc.loaithuoc.TenLoaiThuoc,
                                "med_unit": d.ChiTietPhieuKhamBenh.thuoc.donvi.TenDonVi,
                                "med_quantity": d.ChiTietPhieuKhamBenh.SoLuong,
                                "med_usage": d.ChiTietPhieuKhamBenh.CachDung
                            }
                        })
                    else:
                        result.append({
                            "medicine": {
                                "med_name": d.ChiTietPhieuKhamBenh.thuoc.TenThuoc,
                                "med_type": d.ChiTietPhieuKhamBenh.thuoc.loaithuoc.TenLoaiThuoc,
                                "med_unit": d.ChiTietPhieuKhamBenh.thuoc.donvi.TenDonVi,
                                "med_quantity": d.ChiTietPhieuKhamBenh.SoLuong,
                                "med_usage": d.ChiTietPhieuKhamBenh.CachDung
                            }
                        })
            else:
                result.append({
                    "medical_report": {
                        "id": item.PhieuKhamBenh.id,
                        "patient_name": item.PhieuKhamBenh.benhnhan.HoTen,
                        "med_date": item.PhieuKhamBenh.NgayKham.strftime("%d/%m/%Y"),
                        "symptoms": item.PhieuKhamBenh.TrieuChung,
                        "diagnose": item.PhieuKhamBenh.DuDoanBenh,
                    }
                })
    res = make_response(jsonify(result), 200)
    return res

@app.route('/api/clear-med-report')
def clear_medical_report_session():
    key = app.config['MEDICAL_REPORT_KEY']
    key1 = app.config['MEDICAL_REPORT_SAVE_KEY']
    key2 = app.config['MEDICAL_REPORT_MEDICINE_KEY']
    if key in session:
        del session[key]
    if key1 in session:
        del session[key1]
    if key2 in session:
        del session[key2]
    session.pop('medical_reports', None)
    session.pop('medical_report_medicine', None)
    session.pop('medical_report_save', None)
    return jsonify({'status': 204})


@app.route('/api/add-med-report', methods=['post'])
def add_med_to_report():
    key = app.config['MEDICAL_REPORT_KEY']
    key2 = app.config['MEDICAL_REPORT_MEDICINE_KEY']
    medical_reports = session[key] if key in session else {}
    medical_report_medicine = session[key2] if key2 in session else {}
    data = request.json
    patient_id = data['patient_id']
    med_name = data['med_name']
    med_quantity = data['med_quantity']
    not_included_med = data['not_included_med']
    print(not_included_med)
    patient_name = dao.get_patient_name(patient_id)
    med_unit = dao.get_med_unit(med_name)
    if patient_name is None:
        return jsonify({"error": 'no patient found'})
    elif med_unit is None and not_included_med != '1':
        return jsonify({"error": "no medicine found"})
    else:
        if any(d['med_name'] == med_name for d in medical_report_medicine.values()):
            dict_key = ','.join([str(item) for item in (key for key in medical_report_medicine if
                                                        med_name in medical_report_medicine[key].values())])
            result = int(medical_report_medicine[dict_key]["med_quantity"]) + med_quantity
            medical_report_medicine[dict_key]["med_quantity"] = str(result)
        else:
            id = str(len(medical_report_medicine) + 1)
            print(medical_reports.values())
            if patient_id not in medical_reports.values():
                if med_unit is not None:
                    medical_reports = {
                        "report_date": data['report_date'],
                        "patient_id": patient_id,
                        "patient_name": patient_name,
                        "symptoms": data['symptoms'],
                        "diagnose": data['diagnose'],
                    }
                    medical_report_medicine[id] = {
                        "id": id,
                        "med_name": med_name,
                        "med_type": data['med_type'],
                        "med_unit": med_unit,
                        "med_quantity": med_quantity,
                        "med_usage": data['med_usage']
                    }
                else:
                    medical_reports = {
                        "report_date": data['report_date'],
                        "patient_id": patient_id,
                        "patient_name": patient_name,
                        "symptoms": data['symptoms'],
                        "diagnose": data['diagnose'],
                    }
            else:
                medical_report_medicine[id] = {
                    "id": id,
                    "med_name": med_name,
                    "med_type": data['med_type'],
                    "med_unit": med_unit,
                    "med_quantity": med_quantity,
                    "med_usage": data['med_usage']
                }
        session[key] = medical_reports
        session[key2] = medical_report_medicine
        print(medical_report_medicine)
        print(medical_reports)
    return jsonify({"data": 204})


@app.route('/api/delete-med-report', methods=['delete'])
def delete_med_in_report():
    key = app.config['MEDICAL_REPORT_MEDICINE_KEY']
    medical_report_medicine = session.get(key)
    data = request.json
    id = str(data['id'])
    pos = int(id)
    if medical_report_medicine and id in medical_report_medicine:
        del medical_report_medicine[id]
        temp_dict = {}
        for key in list(medical_report_medicine.keys()):
            if int(key) > pos:
                for i in range(pos, len(medical_report_medicine) + 1):
                    new_key = i
                    if int(key) > new_key:
                        temp_dict[key] = str(new_key)
    for old, new in temp_dict.items():
        medical_report_medicine[new] = medical_report_medicine.pop(str(old))
        medical_report_medicine[new]["id"] = str(new)
    session[key] = medical_report_medicine
    res = make_response(jsonify(medical_report_medicine), 200)
    return res

###################################################


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
