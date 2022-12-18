 function SomeDeleteRowFunction(o, benhnhan) {
     let p=o.parentNode.parentNode;
     let answer = confirm(`${'Bạn có chắn chắn xóa bệnh nhân '}${benhnhan}`);
     if (answer) {
        p.parentNode.removeChild(p);
     }
}


function addMedToReport(element_id) {
    let not_included_med = document.getElementById("notIncludedMed");
    let patient_info = document.getElementById("patient_info")
    let medical_info = document.getElementById("medical_info")
    if (element_id == medical_info && findEmptyInputInDiv(medical_info) && not_included_med.value =='0')
            alert("Vui lòng điền đầy đủ các thông tin thuốc trong phiếu khám bệnh!!!");
    else if(element_id == patient_info && findEmptyInputInDiv(patient_info))
           alert("Vui lòng điền đầy đủ các thông tin bệnh nhân trong phiếu khám bệnh!!!");
    else if (element_id == patient_info && findEmptyInputInDiv(patient_info) == false
                && not_included_med.value =='0' && findEmptyInputInDiv(medical_info))
             alert("Vui lòng điền đầy đủ các thông tin thuốc trong phiếu khám bệnh hoặc chọn không kê khai thuốc!!!");
    else {
            fetch('/api/add-med-report', {
                method: "post",
                body: JSON.stringify({
                "report_date": document.getElementById("medicalDate").value,
                "patient_id": document.getElementById("patientID").value,
                "symptoms": document.getElementById("patientSymptoms").value,
                "diagnose": document.getElementById("doctorDiagnose").value,
                "med_name": document.getElementById("medicineName").value,
                "med_type": document.getElementById("medicineType").value,
                "med_quantity": +document.getElementById("medicineQuantity").value,
                "med_usage": document.getElementById("medicineUsage").value,
                "not_included_med": not_included_med.value
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                            console.info(data.toString().length)
                            console.info(data)
                            if (data.error === "no patient found")
                                alert(`Không tìm thấy bệnh nhân trong danh sách khám ngày ${document.getElementById("medicalDate").value}`)
                            else if (data.error === 'no medicine found')
                                alert("Không tồn tại thuốc")
                            else if (data.toString().length > 0) {
                                $("#medical_report_content").show()
                                alert("Thêm thành công!!!");
                                refreshMedReportContent();
                                document.getElementById("save_report").disabled=true;
                                document.getElementById("clear_report").disabled=true;
                                if (not_included_med.value != '1')
                                  resetValueMedReport(medical_info)
                                else
                                    not_included_med.disabled = true;
                            }
                            else
                                alert("Thêm thất bại!!!");
                        }).catch(err => console.error(err))
        }
}

function deleteMed(id) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch('/api/delete-med-report', {
            method: "delete",
            body: JSON.stringify({
            "id": id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            console.info(data);
            let c = document.getElementById(`medical_report_medicine${id}`);
            c.style.display = "none";
            refreshMedReportContent();
        }).catch(err => console.info(err))
    }
}

function findEmptyInputInDiv(element_id) {
    let empty = false
    $(element_id).find(':input').each(function() {
    switch(this.type) {
        case 'text':
            if ($(this).val() == "") {
                  empty = true;
            }
            console.info(empty)
            break;
        case 'number':
            if ($(this).val() == "" || $(this).val() == 0) {
                  empty = true;
            }
            console.info(empty)
            break;
    }
  });
  console.info(empty)
  return empty
}

function resetValueMedReport(element_id) {
  $(element_id).find(':input').each(function() {
    switch(this.type) {
        case 'text':
            $(this).val('');
            $(this).attr("disabled", false)
            break;
        case 'number':
            $(this).val('0');
            $(this).attr("disabled", false)
            break;
        case 'checkbox':
            $(this).val('0');
            this.checked = false;
            break;
    }
  });
}

function clearMedReportSession() {
    if (confirm("Bạn chắc chắn hủy phiếu khám bệnh không ") == true) {
        fetch('/api/clear-med-report').then(res => res.json()).then(data => {
                console.info(data)
                if (data.status === 204) {
                    alert("Hủy thành công!!!")
                    location.reload()
                    resetValueMedReport(patient_info)
                    resetValueMedReport(medical_info)
                }
                else {
                    alert("Hủy thất bại!!!")
                }
        }).catch(err => console.info(err))
    }
}

function refreshMedReportContent() {
    $("#medical_report_content").load(location.href + " #medical_report_content>*","");
}

function loadMedNameByType() {
     fetch('/api/load-med-name', {
            method: "post",
            body: JSON.stringify({
            "med_type": document.getElementById("medicineType").value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
                        console.info(data)
                        $("#medicineNames").load(location.href + " #medicineNames")
                    }).catch(err => console.error(err))
}

function showPatientMedicalReport() {
    let patient_id = document.getElementById("patientID").value;
    if (patient_id == "") {
            alert("Vui lòng nhập mã bệnh nhân để tiếp tục tra cứu");
            $('#medical_report_list').hide()
    }
    else {
    fetch('/api/load-patient-med-report', {
            method: "post",
            body: JSON.stringify({
                "patient_id": patient_id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
            }).then(res => res.json()).then(data => {
                    if (data.length > 0) {
                        let h = ''
                        $('#medical_report_list').toggle()
                        for(let i = 0; i< data.length; i++) {
                            h += `
                                    <tr>
                                        <td>${(i+1)}</td>
                                        <td id='${data[i].patient_id}'> ${data[i]["patient_name"]}</td>
                                        <td id='date${(i+1)}'>${data[i]["med_date"]}</td>
                                        <td>
                                            <input type="button" value="Xem" class="btn btn-primary" onclick=showPatientMedicalReportByDate(${data[i].patient_id},date${(i+1)})>
                                        </td>
                                    </tr>`
                        }
                         let d = document.getElementById('patient_medical_date');
                         d.innerHTML = h;
                    }
                    else
                        alert("Bệnh nhân không có phiếu khám bệnh!!!")
                }).catch(err => console.error(err))
    }
}

function showPatientMedicalReportByDate(patient_id,date) {
    console.info(patient_id)
    fetch('/api/show-patient-med-report', {
            method: "post",
            body: JSON.stringify({
                "patient_id": patient_id,
                "med_date": $(date).html()
            }),
            headers: {
                'Content-Type': 'application/json'
            }
            }).then(res => res.json()).then(data => {
                    let d0 = "";
                    let d1 = "";
                    let d2 = "";
                    console.info(data)
                    if (data.length > 0) {
                        $('#patient_medical_list_container').show()
                        for (let i = 0; i < data.length; i++){
                            if (data[i].medicine != undefined) {
                                if (data[i].medical_report != undefined)
                                     d1 += `
                                          </table>
                                         <h3>Phiếu khám bệnh</h3>
                                         <p class="fs-5">Ngày khám: ${data[i].medical_report.med_date}</p>
                                         <p class="fs-5">Họ tên: ${data[i].medical_report.patient_name}</p>
                                         <p class="fs-5">Triệu chứng: ${data[i].medical_report.symptoms}</p>
                                         <p class="fs-5">Dự đoán bệnh: ${data[i].medical_report.diagnose}</p>

                                            <table class="table table-bordered" style="max-width:500px">
                                                <tr>
                                                    <th>Thuốc</th>
                                                    <th>Loại</th>
                                                    <th>Đơn vị</th>
                                                    <th>Số lượng</th>
                                                    <th>Cách dùng</th>
                                                </tr>
                                                     <td>${data[i].medicine.med_name}</td>
                                                     <td>${data[i].medicine.med_type}</td>
                                                     <td>${data[i].medicine.med_unit}</td>
                                                     <td>${data[i].medicine.med_quantity}</td>
                                                     <td>${data[i].medicine.med_usage}</td>
                                                </tr>
                                     `
                                else {
                                      d1 += `
                                              <tr>
                                              <td>${data[i].medicine.med_name}</td>
                                              <td>${data[i].medicine.med_type}</td>
                                              <td>${data[i].medicine.med_unit}</td>
                                              <td>${data[i].medicine.med_quantity}</td>
                                              <td>${data[i].medicine.med_usage}</td>
                                             </tr>
                                      `
                                }
                            }
                            else {
                                 d0 += `
                                      <h3>Phiếu khám bệnh</h3>
                                         <p class="fs-5">Ngày khám: ${data[i].medical_report.med_date}</p>
                                         <p class="fs-5">Họ tên: ${data[i].medical_report.patient_name}</p>
                                         <p class="fs-5">Triệu chứng: ${data[i].medical_report.symptoms}</p>
                                         <p class="fs-5">Dự đoán bệnh: ${data[i].medical_report.diagnose}</p>
                                     <p class="fs-5">Không kê khai thuốc</p>
                                 `
                            }
                        }
                        let t0 = document.getElementById("patient_no_meds");
                        t0.innerHTML = d0;

                        let t1 = document.getElementById("patient_with_med");
                        t1.innerHTML = d1;
                    }
                }).catch(err => console.error(err))
}
function saveDataAfterRefresh() {
        fetch('/api/save-med-report', {
            method: "post",
            body: JSON.stringify({
            "report_date":  document.getElementById("medicalDate").value,
            "patient_id": document.getElementById("patientID").value,
            "symptoms": document.getElementById("patientSymptoms").value,
            "diagnose": document.getElementById("doctorDiagnose").value,
            "med_name": document.getElementById("medicineName").value,
            "med_type": document.getElementById("medicineType").value,
            "med_quantity": +document.getElementById("medicineQuantity").value,
            "med_usage": document.getElementById("medicineUsage").value,
            "not_included_med": document.getElementById("notIncludedMed").value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
                    console.info(data)
                    }).catch(err => console.error(err))
}

function checkBoxValue() {
    let not_included_med = document.getElementById("notIncludedMed");
    if (not_included_med.checked) {
        $("#medical_info :input").attr("disabled", true);
        $("#medical_info :input").val('')
        not_included_med.value = '1';
    } else {
        $("#medical_info :input").attr("disabled", false);
        not_included_med.value = '0';
    }
    console.info(not_included_med.value)
}

function searchKeyWordTable() {
  let input, filter, table, tr, td, i, j, txtValue;
  input = document.getElementById("keyword");
  filter = input.value.toUpperCase();
  table = document.getElementById("meds-table");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    for (j = 0; j < 3; j++) {
        td = tr[i].getElementsByTagName("td")[j]
        if (td) {
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
            break;
          } else {
            tr[i].style.display = "none";
          }
        }
    }
  }
}