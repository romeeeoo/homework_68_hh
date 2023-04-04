$(document).ready(function () {

    let userChangeBtn = $("#id_user_update")

    console.log(userChangeBtn)

    $(userChangeBtn).click(function openModel (event) {
        event.preventDefault()
        $.ajax({
            url: $(this).attr("href"),
            method: "GET",
            dataType: 'JSON',
            // beforeSend: function () {
            //     $("#id-modalUserChange").modal("show");
            // },
            success: function (response, status) {
                $("#id-modalUserChange .modal-content").html(response.html_forms)
                console.log(response);
                console.log(status);
            },
            error: function (response, status) {
                console.log(status);
            },
        });
    })

    $("#id-modalUserChange").on("submit", "#id-profile-update-form", function performUpdate (event) {
        event.preventDefault()
        let form = $(this)
        let fd = new FormData(form[0]);
        $.ajax({
            url: form.attr("action"),
            data: fd,
            method: "POST",
            processData: false,
            contentType: false,
            // dataType: "JSON",
            success: function (response) {
                if (response.forms_are_valid) {
                    $('#general_profile_info').html(response.html_general_profile_info)
                    $('#id-modalUserChange').modal('hide');
                    // alert("User profile updated!");
                } else {
                    $("#id-modalUserChange .modal-content").html(response.html_forms)
                }
            }
        });
        // return false;
    });
})