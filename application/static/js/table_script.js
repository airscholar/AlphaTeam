$(document).ready(function () {
    $('table').each(function () {
        // disablle cleaning if the table is the global metrics table
        if (this.id === 'global-metrics') {
            console.log('global metrics table')
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
                        if (typeof data === 'string') {
                            if (data.length > 6) {
                                if (data.startsWith('0') || data.startsWith('1') || data.startsWith('2') || data.startsWith('3') || data.startsWith('4') || data.startsWith('5') || data.startsWith('6') || data.startsWith('7') || data.startsWith('8') || data.startsWith('9')) {
                                    return data.substring(0, 7); // Limit the length to 6 if the string doesn't start with '0x'
                                }
                            }
                        }
                        return data;
                    }
                }]
            });
        } else {
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
        }

    });
});
