const form = document.querySelector('form');

form.addEventListener('submit', (e) => {
	e.preventDefault();

	const file = document.querySelector('#csv_file').files[0];

	if (file && file.size) {
		const fileSize = file.size / 1024 / 1024;
		if (fileSize > 10) {
			alert('The file size is too large. Please select a file that is smaller than 10MB.');
			return;
		}
	}
	else {
		alert('Please select a file.');
		return;
	}


	// Submit the form using AJAX
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append('csv_file', file);
    xhr.open('POST', '/upload');
    xhr.onload = function() {
        const response = JSON.parse(xhr.responseText);
        alert(response.message);
    };
    xhr.send(formData);

    return false;
});

$('#csv_file').bind('change', function () {
	var filename = $("#csv_file").val();
	if (/^\s*$/.test(filename)) {
	  $(".file-upload").removeClass('active');
	  $("#noFile").text("No file chosen..."); 
	}
	else {
	  $(".file-upload").addClass('active');
	  $("#noFile").text(filename.replace("C:\\fakepath\\", "")); 
	}
  });
  