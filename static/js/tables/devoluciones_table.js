/* ═══════════════════════════════════════════
   static/js/tables/devoluciones_table.js
   DataTable, Details & Actions for Devoluciones
  ═══════════════════════════════════════════ */
$(document).ready(function () {
  var childRows = {};

  // ─── PASO 1: extraer las filas de detalle ANTES de que DataTables
  //            las cuente como filas de datos (evita el warning TN/4).
  $('#devoluciones-table tbody tr.detail-row').each(function () {
    var id = $(this).attr('id');
    childRows[id] = $(this).clone();   // guardamos el nodo completo
    $(this).remove();                  // lo sacamos del DOM
  });

  // Extraer y remover la fila de estado vacío (evita warning TN/4)
  var emptyStateHtml = '';
  $('#devoluciones-table tbody tr').each(function () {
    if ($(this).find('td').length === 1 && $(this).find('td').attr('colspan')) {
      emptyStateHtml = $(this).find('td').html();
      $(this).remove();
    }
  });

  // ─── PASO 2: inicializar DataTable sobre el tbody ya limpio
  var table = $('#devoluciones-table').DataTable({
    responsive: true,
    dom: '<"row mb-3 align-items-center"<"col-md-6"B><"col-md-6"f>t<"row mt-3 align-items-center"<"col-md-6"i><"col-md-6"p>>',
    buttons: window.obtenerBotonesDataTable('devoluciones'),
    language: {
      url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
    },
    order: [],
    columnDefs: [
      // col 0 = chevron expand, col 4 = ítems count, col 6 = acciones
      { orderable: false, targets: [0, 4, 6] }
    ],
    pageLength: 10,
    lengthMenu: [[10, 25, 50, -1], [10, 25, 50, 'Todos']],
    drawCallback: function (settings) {
      if (settings.aiDisplay.length === 0 && emptyStateHtml) {
        $(this).find('.dataTables_empty').html(emptyStateHtml);
      }
      var tooltipTriggerList = this.api().table().container()
        .querySelectorAll('[data-bs-toggle="tooltip"]');
      [...tooltipTriggerList].forEach(function (el) {
        bootstrap.Tooltip.getOrCreateInstance(el);
      });
    }
  });

  // ─── PASO 3: manejar clic en el botón de expandir
  $('#devoluciones-table').on('click', '.btn-toggle-details', function (e) {
    e.preventDefault();
    var btn = $(this);
    var targetId = btn.attr('data-target-detail');
    var tr = btn.closest('tr');
    var row = table.row(tr);

    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass('shown');
      btn.find('.row-chevron').css('transform', 'rotate(0deg)');
    } else {
      var $detail = childRows[targetId];
      if ($detail) {
        row.child($detail.find('td').first().html()).show();
        row.child().find('td').attr('colspan', 7).css('padding', '0');
      }
      tr.addClass('shown');
      btn.find('.row-chevron').css('transform', 'rotate(90deg)');
    }
  });

  // ─── Clic delegado: Aceptar devolución
  $('#devoluciones-table').on('click', '.btn-aceptar-click', function (e) {
    e.preventDefault();
    var btn = $(this);
    abrirAceptar(btn.attr('data-pk'), btn.attr('data-prestamo-pk'), btn.attr('data-usuario'));
  });

  // ─── Clic delegado: Rechazar devolución
  $('#devoluciones-table').on('click', '.btn-rechazar-click', function (e) {
    e.preventDefault();
    var btn = $(this);
    abrirRechazar(btn.attr('data-pk'), btn.attr('data-prestamo-pk'), btn.attr('data-usuario'));
  });
});
