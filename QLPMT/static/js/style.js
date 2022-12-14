 function SomeDeleteRowFunction(o, benhnhan) {
     let p=o.parentNode.parentNode;
     let answer = confirm(`${'Bạn có chắn chắn xóa bệnh nhân '}${benhnhan}`);
     if (answer) {
        p.parentNode.removeChild(p);
     }
}
function addMedToReport(element_id) {
    let report_date = document.getElementById("medicalDate").value;
    let patient_id = document.getElementById("patientID").value;
    let symptoms = document.getElementById("patientSymptoms").value;
    let diagnose = document.getElementById("doctorDiagnose").value;
    let med_name = document.getElementById("medicineName").value;
    let med_type = document.getElementById("medicineType").value;
    let med_quantity = +document.getElementById("medicineQuantity").value;
    let med_usage = document.getElementById("medicineUsage").value;
    let not_included_med = document.getElementById("notIncludedMed").value;
    let patient_info = document.getElementById("patient_info")
    let medical_info = document.getElementById("medical_info")
    console.info(element_id)
    if (element_id == medical_info && findEmptyInputInDiv(medical_info) && not_included_med =='0')
            alert("Vui lòng điền đầy đủ các thông tin thuốc trong phiếu khám bệnh!!!");
    else if(element_id == patient_info && findEmptyInputInDiv(patient_info))
           alert("Vui lòng điền đầy đủ các thông tin bệnh nhân trong phiếu khám bệnh!!!");
    else if (element_id == patient_info && findEmptyInputInDiv(patient_info) == false && not_included_med =='0')
             alert("Vui lòng điền đầy đủ các thông tin thuốc trong phiếu khám bệnh hoặc chọn không kê khai thuốc!!!");
    else {
            fetch('/api/add-med-report', {
                method: "post",
                body: JSON.stringify({
                "report_date": report_date,
                "patient_id": patient_id,
                "symptoms": symptoms,
                "diagnose": diagnose,
                "med_name": med_name,
                "med_type": med_type,
                "med_quantity": med_quantity,
                "med_usage": med_usage
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                            console.info(data)
                            if (Object.keys(data).length > 0) {
                                alert("Thêm thành công!!!");
                                resetValueMedReport(medical_info)
                                refreshMedReportContent();
                            }
                            else {
                                alert("Thêm thất bại (Không tồn tại thông tin bệnh nhân hoặc thuốc) !!!")
                            }
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
            let c = document.getElementById(`med_report${id}`);
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
                if (data.status != 500) {
                    alert("Hủy thành công!!!")
                    resetValueMedReport(patient_info)
                    resetValueMedReport(medical_info)
                    location.reload()
                }
                else {
                    alert("Hủy thất bại!!!")
                }
        }).catch(err => console.info(err))
    }
}

function refreshMedReportContent() {
    $("#med_report_content").load(location.href + " #med_report_content");
     $("#notIncludedMedDiv").load(location.href + " #notIncludedMedDiv");
}

function loadMedNameByType() {
    let med_type = document.getElementById("medicineType").value;
    let select =  document.getElementById("medicineNames")
     fetch('/api/load-med-name', {
            method: "post",
            body: JSON.stringify({
            "med_type": med_type
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
    if (patient_id == "")
        alert("Vui lòng nhập mã bệnh nhân để tiếp tục tra cứu");
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
                if (data.toString().length > 0) {
                    if ($("#med_report_list").css('display') != 'none')
                        $("#patient_medical_date").load(location.href + " #patient_medical_date");
                    loadPatientMedicalReportToTable(data)
                    $("#med_report_list").toggle();
                }
                else
                    alert("Không tồn tại mã bệnh nhân!!!")
                }).catch(err => console.error(err))
    }
}

function showPatientMedicalReportByDate(date) {
    let med_date = $(date).html();
    console.info(med_date)
    let patient_id = document.getElementById("patientID").value;
    console.info(med_date)
    fetch('/api/show-patient-med-report', {
            method: "post",
            body: JSON.stringify({
                "patient_id": patient_id,
                "med_date": med_date
            }),
            headers: {
                'Content-Type': 'application/json'
            }
            }).then(res => res.json()).then(data => {
                    let d0 = "";
                    let d1 = "";
                    let d2 = "";
                    for (let i = 0; i < data.length; i++){
                        if (data[i].med_name == undefined) {
                             d0 += `
                                        <p class="fs-5">Phiếu khám: ${(i+1)}</p>
                                        <p class="fs-5">Ngày khám: ${data[i].med_date}</p>
                                        <p class="fs-5">Triệu chứng: ${data[i].symptoms}</p>
                                        <p class="fs-5">Dự đoán bệnh: ${data[i].diagnose}</p>
                             `
                        }
                        else {
                            d1 += `     <p class="fs-5">Phiếu khám: ${(i+1)}</p>
                                        <p class="fs-5">Ngày khám: ${data[i].med_date}</p>
                                        <p class="fs-5">Triệu chứng: ${data[i].symptoms}</p>
                                        <p class="fs-5">Dự đoán bệnh: ${data[i].diagnose}</p>
                                        <table class="table table-bordered" style="max-width:400px">
                                                <tr>
                                                    <th>Thuốc</th>
                                                    <th>Loại</th>
                                                    <th>Đơn vị</th>
                                                    <th>Số lượng</th>
                                                    <th>Cách dùng</th>
                                                </tr>
                                                <tr>
                                                    <td>${data[i].med_name}</td>
                                                    <td>${data[i].med_type}</td>
                                                    <td>${data[i].med_unit}</td>
                                                    <td>${data[i].med_quantity}</td>
                                                    <td>${data[i].med_usage}</td>
                                                </tr>
                                        </table>
                            `
                        }
                    }
                    let t0 = document.getElementById("patient_no_meds");
                    t0.innerHTML = d0;

                    let t1 = document.getElementById("patient_with_med");
                    t1.innerHTML = d1;
                }).catch(err => console.error(err))
}

function loadPatientMedicalReportToTable(data) {
            for (let i = 0; i < data.length; i++) {
            tr = $('<tr/>');
            tr.append("<td>" + (i+1) + "</td>");
            tr.append("<td>" + data[i].patient_name + "</td>");
            tr.append("<td " + 'id="date' + (i+1) +'"' + ">" + data[i].med_date + "</td>");
            tr.append("<td>" +  '<input type="button" value="Xem" class="btn btn-primary"'
            + 'Onclick="' + 'showPatientMedicalReportByDate('+ 'date' + (i+1) + ')"'
            + '/>' + "</td")
            $('#patient_medical_date').append(tr);
            }
}

function saveDataAfterRefresh() {
    let report_date = document.getElementById("medicalDate").value;
    let patient_id = document.getElementById("patientID").value;
    let symptoms = document.getElementById("patientSymptoms").value;
    let diagnose = document.getElementById("doctorDiagnose").value;
    let med_name = document.getElementById("medicineName").value;
    let med_type = document.getElementById("medicineType").value;
    let med_quantity = +document.getElementById("medicineQuantity").value;
    let med_usage = document.getElementById("medicineUsage").value;
    let not_included_med = document.getElementById("notIncludedMed").value;
        fetch('/api/save-med-report', {
            method: "post",
            body: JSON.stringify({
            "report_date": report_date,
            "patient_id": patient_id,
            "symptoms": symptoms,
            "diagnose": diagnose,
            "med_name": med_name,
            "med_type": med_type,
            "med_quantity": med_quantity,
            "med_usage": med_usage,
            "not_included_med": not_included_med
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
    for (j = 0; j < 2; j++) {
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