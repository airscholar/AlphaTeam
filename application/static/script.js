$(function () {
    var form = $('#upload-form');
    var progressBar = $('#progress-bar');

    form.on('submit', function (event) {
        event.preventDefault();

        // Get the CSV file and the selected option
        var csvFile = $('#csv_file')[0].files[0];
        var option = $('#dropdown-menu').val();

        // Validate the CSV file and the selected option
        if (!csvFile || !csvFile.size) {
            alert('Please select a CSV file.');
            return;
        }

        if (option === 'option1') {
            alert('Please Select Dataset Type.');
            return;
        }

        // Create a FormData object to send the data
        var formData = new FormData();
        formData.append('csv_file', csvFile);
        formData.append('option', option);

        // Send the data using AJAX
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            xhr: function () {
                var xhr = new XMLHttpRequest();
                xhr.upload.addEventListener('progress', function (event) {
                    if (event.lengthComputable) {
                        var percent = Math.round((event.loaded / event.total) * 100);
                        progressBar.val(percent);
                    }
                }, false);
                return xhr;
            },
            beforeSend: function () {
                progressBar.show();
                progressBar.val(0);
            },
            success: function (response) {
                // Redirect the user to the success page
                window.location.href = '/home';
            },
            error: function (jqXHR, textStatus, errorThrown) {
                // Handle errors
                console.log('Error:', errorThrown);
            },
            complete: function () {
                // Hide the progress bar
                progressBar.hide();
            }
        });
    });

    // Update the selected file name in the file input field
    $('#csv_file').on('change', function () {
        var filename = $(this).val().split('\\').pop();
        $('#noFile').text(filename);

        // Update the supported formats text with the selected file type
        $('#file-type').text(filename);
    });

});
