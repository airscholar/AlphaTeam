$(document).ready(function () {
    $('table').each(function() {
         if (this.id === 'example-metrics') {
           const not_clean = true
        }
        else {
              const not_clean = false
         }
        $(this).DataTable({
            dom: 'Bfrtip',
            buttons: [
                'copyHtml5',
                'excelHtml5',
                'csvHtml5',
                'pdfHtml5'
            ],
            "pageLength": 10, // Show 10 rows per page
            "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]], // Customize page length menu
            "columnDefs": [{
                "targets": "_all",
                "render": function (data, type, row) {
                    if (not_clean) {
                        return data;
                    }
                    if (typeof data === 'number') {
                        return parseFloat(data.toFixed(6)); // Round to 6 decimal places for numbers
                    }
                    if (typeof data === 'string') {
                        if (data.length > 15 && data.startsWith('0x')) {
                            return data.slice(0, 6) + '...' + data.slice(-6);
                        } else if (!data.startsWith('0x')) {
                            return data.substring(0, 6); // Limit the length to 6 if the string doesn't start with '0x'
                        }
                        return data.substring(0, 12);
                    }
                    return data;
                }
            }]
        });
    });
});
