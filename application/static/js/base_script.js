function setSpinnerVisibility(visible) {
    let spinner = document.getElementById('spinner');
    spinner.style.display = visible ? 'flex' : 'none';
}

// Example usage
let showSpinner = false; // Set this variable to true to display the spinner or false to hide it
setSpinnerVisibility(showSpinner);

$(document).ready(function () {
    $('#example1').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]] // Customize page length menu
    });
});

$(document).ready(function () {
    $('#example').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]] // Customize page length menu
    });
});

document.querySelectorAll('.fetch-spinner').forEach(function (element) {
    element.addEventListener('click', function (event) {
        // Prevent the default behavior of the link
        event.preventDefault();

        // Show the spinner when the link is clicked
        setSpinnerVisibility(true);

        // Get the href attribute of the link
        var url = this.getAttribute('href');

        // Set a delay before navigating to the new page
        setTimeout(function () {
            window.location.href = url;
        }, 2000); // 2000 milliseconds (2 seconds) delay
    });
});

$(document).ready(function () {
    // Initialize DataTables
    var table = $('#example').DataTable();
    $('#download_csv').on('click', function () {
        var csv = '';
        var headers = [];
        var rows = [];

        // Get the table headers
        $('#example thead th').each(function () {
            headers.push($(this).text().trim());
        });

        // Get all table rows, including pagination
        table.rows().every(function () {
            rows.push(this.data());
        });

        // Combine the headers and rows into a CSV string
        csv += headers.join(',') + '\n';
        $.each(rows, function (index, row) {
            csv += row.join(',') + '\n';
        });

        // Create a temporary link element to trigger the download
        var link = document.createElement('a');
        link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
        link.setAttribute('download', 'metrics_data.csv');
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
});

function validateLayout() {
    var layout = document.getElementById('dropdown-menu').value;
    if (layout === 'option1') {
        alert('Please select a layout option.');
        return false;
    }

    return true;
}