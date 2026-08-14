/* ─────────────────────────────────────────────────────────────
   PÁGINA PRINCIPAL - DASHBOARD DE GRÁFICAS (TEMA CLARO NATIVO)
   ───────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // Configuración de paleta de colores nativos nítidos y legibles
  const theme = {
    activo: '#10b981',        // Verde esmeralda
    vencido: '#ef4444',       // Rojo
    devuelto: '#3b82f6',      // Azul
    parcial: '#f59e0b',       // Amarillo/Ámbar
    gridColor: 'rgba(0, 0, 0, 0.06)',
    textColor: '#334155',     // Texto oscuro para alta legibilidad
    fontFamily: "'Inter', system-ui, sans-serif"
  };

  // ── 1. Gráfica de Estado de Préstamos (Doughnut) ──
  function initChartPrestamos() {
    const el = document.getElementById('chart-prestamos-data');
    const canvas = document.getElementById('chartPrestamos');
    if (!el || !canvas) return;

    try {
      const rawData = JSON.parse(el.textContent);
      const ctx = canvas.getContext('2d');

      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: rawData.labels || ['Activos', 'Vencidos', 'Devueltos', 'Parciales'],
          datasets: [{
            data: rawData.data || [0, 0, 0, 0],
            backgroundColor: [theme.activo, theme.vencido, theme.devuelto, theme.parcial],
            borderWidth: 2,
            borderColor: '#ffffff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 900 },
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                color: theme.textColor,
                font: { family: theme.fontFamily, size: 12, weight: '600' },
                padding: 16,
                usePointStyle: true,
                pointStyleWidth: 10
              }
            },
            tooltip: {
              backgroundColor: '#1e293b',
              titleColor: '#ffffff',
              bodyColor: '#e2e8f0',
              borderColor: '#334155',
              borderWidth: 1,
              padding: 10
            }
          },
          cutout: '70%'
        }
      });
    } catch (e) {
      console.error('Error iniciando chartPrestamos:', e);
    }
  }

  // ── 2. Gráfica de Stock por Categoría (Bar) ──
  function initChartCategorias() {
    const el = document.getElementById('chart-categorias-data');
    const canvas = document.getElementById('chartCategorias');
    if (!el || !canvas) return;

    try {
      const rawData = JSON.parse(el.textContent);
      const ctx = canvas.getContext('2d');

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: rawData.labels || [],
          datasets: [{
            label: 'Herramientas',
            data: rawData.data || [],
            backgroundColor: 'rgba(59, 130, 246, 0.85)',
            borderColor: '#2563eb',
            borderWidth: 1,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          animation: { duration: 900 },
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#1e293b',
              titleColor: '#ffffff',
              bodyColor: '#e2e8f0',
              borderColor: '#334155',
              borderWidth: 1,
              padding: 10
            }
          },
          scales: {
            x: {
              grid: { color: theme.gridColor },
              ticks: { color: theme.textColor, font: { family: theme.fontFamily, weight: '500' } }
            },
            y: {
              grid: { display: false },
              ticks: { color: '#0f172a', font: { family: theme.fontFamily, weight: '600' } }
            }
          }
        }
      });
    } catch (e) {
      console.error('Error iniciando chartCategorias:', e);
    }
  }

  // ── 3. Gráfica de Salud de Inventario (Pie) ──
  function initChartSalud() {
    const el = document.getElementById('chart-salud-data');
    const canvas = document.getElementById('chartSalud');
    if (!el || !canvas) return;

    try {
      const rawData = JSON.parse(el.textContent);
      const ctx = canvas.getContext('2d');

      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: rawData.labels || ['Disponible', 'En Préstamo', 'No disponible'],
          datasets: [{
            data: rawData.data || [0, 0, 0],
            backgroundColor: [theme.activo, theme.parcial, theme.vencido],
            borderWidth: 2,
            borderColor: '#ffffff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 900 },
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                color: theme.textColor,
                font: { family: theme.fontFamily, size: 12, weight: '600' },
                padding: 16,
                usePointStyle: true,
                pointStyleWidth: 10
              }
            },
            tooltip: {
              backgroundColor: '#1e293b',
              titleColor: '#ffffff',
              bodyColor: '#e2e8f0',
              borderColor: '#334155',
              borderWidth: 1,
              padding: 10
            }
          }
        }
      });
    } catch (e) {
      console.error('Error iniciando chartSalud:', e);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    initChartPrestamos();
    initChartCategorias();
    initChartSalud();
  });

})();

/* ── Modal ver producto ── */
function verProducto(sku, nombre, desc, stock, cat) {
  var vpSku    = document.getElementById('vpd-sku');
  var vpNombre = document.getElementById('vpd-nombre');
  var vpCat    = document.getElementById('vpd-cat');
  var vpStock  = document.getElementById('vpd-stock');
  var vpDesc   = document.getElementById('vpd-desc');
  var vpLink   = document.getElementById('vpd-link');

  if (vpSku)    vpSku.textContent    = sku;
  if (vpNombre) vpNombre.textContent = nombre;
  if (vpCat)    vpCat.textContent    = cat || '—';
  if (vpStock) {
    vpStock.textContent = stock;
    vpStock.style.color = stock === 0 ? '#ef4444' : stock < 3 ? '#f59e0b' : '#10b981';
  }
  if (vpDesc)  vpDesc.textContent  = desc || '—';
  if (vpLink)  vpLink.href         = '/inventario/' + encodeURIComponent(sku) + '/editar/';

  var modal = document.getElementById('modalVerProducto');
  if (modal) new bootstrap.Modal(modal).show();
}