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

// 21


$(document).ready(function () {
    $('#example21').DataTable({
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
    $('#example22').DataTable({
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
    $('#example23').DataTable({
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
    $('#example24').DataTable({
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
    $('#example25').DataTable({
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
    $('#example26').DataTable({
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
    $('#example27').DataTable({
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
    $('#example28').DataTable({
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
    $('#example29').DataTable({
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
    $('#example30').DataTable({
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

// 31

$(document).ready(function () {
    $('#example31').DataTable({
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
    $('#example32').DataTable({
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
    $('#example33').DataTable({
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
    $('#example34').DataTable({
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
    $('#example35').DataTable({
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
    $('#example36').DataTable({
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
    $('#example37').DataTable({
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
    $('#example38').DataTable({
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
    $('#example39').DataTable({
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
    $('#example40').DataTable({
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

// 41

$(document).ready(function () {
    $('#example41').DataTable({
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
    $('#example42').DataTable({
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
    $('#example43').DataTable({
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
    $('#example44').DataTable({
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
    $('#example45').DataTable({
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
    $('#example46').DataTable({
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
    $('#example47').DataTable({
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
    $('#example48').DataTable({
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
    $('#example49').DataTable({
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
    $('#example50').DataTable({
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

// 51

$(document).ready(function () {
    $('#example51').DataTable({
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
    $('#example52').DataTable({
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
    $('#example53').DataTable({
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
    $('#example54').DataTable({
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
    $('#example55').DataTable({
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
    $('#example56').DataTable({
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
    $('#example57').DataTable({
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
    $('#example58').DataTable({
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
    $('#example59').DataTable({
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
    $('#example60').DataTable({
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

// 61

$(document).ready(function () {
    $('#example61').DataTable({
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
    $('#example62').DataTable({
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
    $('#example63').DataTable({
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
    $('#example64').DataTable({
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
    $('#example65').DataTable({
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
    $('#example66').DataTable({
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
    $('#example67').DataTable({
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
    $('#example68').DataTable({
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
    $('#example69').DataTable({
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
    $('#example70').DataTable({
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

// 71

$(document).ready(function () {
    $('#example71').DataTable({
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
    $('#example72').DataTable({
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
    $('#example73').DataTable({
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
    $('#example74').DataTable({
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
    $('#example75').DataTable({
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
    $('#example76').DataTable({
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
    $('#example77').DataTable({
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
    $('#example78').DataTable({
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
    $('#example79').DataTable({
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
    $('#example80').DataTable({
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

// 81

$(document).ready(function () {
    $('#example81').DataTable({
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
    $('#example82').DataTable({
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
    $('#example83').DataTable({
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
    $('#example84').DataTable({
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
    $('#example85').DataTable({
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
    $('#example86').DataTable({
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
    $('#example87').DataTable({
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
    $('#example88').DataTable({
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
    $('#example89').DataTable({
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
    $('#example90').DataTable({
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