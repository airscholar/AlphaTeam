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

        // Set the values of the hidden input fields in the form
        const formData = new FormData();
        formData.append('csv_file', csvFile);
        formData.append('option', option);

        // Submit the form
        const myHeaders = new Headers();

        $.ajax({
            url: "http://127.0.0.1:8000/api/v1/upload",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                const filename = result['filename'];
                const filename2 = result['filename2'];
                const option = result['option'];
                const filepath = result['filepath'];
                const full_path = result['full_path'];

                // Redirect to the home
                window.location.href = '/home?filename=' + filename + '&filename2=' + filename2 + '&option='
                    + option + '&filepath=' + filepath + '&full_path=' + full_path;
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log('error', errorThrown);
            }
        });

        let showSpinner = true; // Set this variable to true to display the spinner or false to hide it
        setSpinnerVisibility(showSpinner);


    });

    // Update the selected file name in the file input field
    $('#csv_file').on('change', function () {
        var filename = $(this).val().split('\\').pop();
        $('#noFile').text(filename);

        // Update the supported formats text with the selected file type
        $('#file-type').text(filename);
    });

});

function setSpinnerVisibility(visible) {
    let spinner = document.getElementById('spinner');
    spinner.style.display = visible ? 'flex' : 'none';
}

// Example usage
let showSpinner = false; // Set this variable to true to display the spinner or false to hide it
setSpinnerVisibility(showSpinner);

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

