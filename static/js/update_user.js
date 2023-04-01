$(document).ready(function () {

    let userChangeBtn = $("#id_user_update")

    console.log(userChangeBtn)

    $(userChangeBtn).click(function (event) {
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

    $("#id-modalUserChange").on("submit", "#id-profile-update-form", function () {
        // event.preventDefault()
        let form = $(this)
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            method: "POST",
            dataType: "JSON",
            success: function (response) {
                if (response.forms_are_valid) {
                    alert("User profile updated!");
                }
                else {
                    $("#id-modalUserChange .modal-content").html(response.html_forms)
                }
            }
        });
        return false;
    });
})