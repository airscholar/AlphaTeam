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
});

$(document).ready(function () {
    $('#example1').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example2').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example3').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example4').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example5').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example6').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example7').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example8').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example9').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example10').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example11').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example12').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example13').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example4').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example15').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example16').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example17').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example18').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example19').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});

$(document).ready(function () {
    $('#example20').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        "pageLength": 10, // Show 10 rows per page
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
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
});