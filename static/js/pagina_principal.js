/* ─────────────────────────────────────────────────────────────
   PÁGINA PRINCIPAL - DASHBOARD DE GRÁFICAS (CHART.JS)
   ───────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // Configuración de colores globales acordes al diseño de la app
  const colors = {
    activo: '#1D9E75',      // Verde Esmeralda / Sage
    vencido: '#98473E',     // Rojo / Rust
    devuelto: '#5b8dee',    // Azul primario
    parcial: '#c4900a',     // Amarillo / Warning
    optimo: '#1D9E75',
    stockBajo: '#c4900a',
    sinStock: '#98473E',
    gridColor: 'rgba(255, 255, 255, 0.08)',
    textColor: '#a3aed0'
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
            backgroundColor: [colors.activo, colors.vencido, colors.devuelto, colors.parcial],
            borderWidth: 2,
            borderColor: '#1e2430'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                color: colors.textColor,
                font: { family: 'Inter', size: 12 },
                padding: 16,
                usePointStyle: true
              }
            },
            tooltip: {
              backgroundColor: '#1b202e',
              titleColor: '#fff',
              bodyColor: '#a3aed0',
              borderColor: 'rgba(255, 255, 255, 0.1)',
              borderWidth: 1,
              padding: 12
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
            label: 'Stock total',
            data: rawData.data || [],
            backgroundColor: 'rgba(91, 141, 238, 0.85)',
            borderColor: '#5b8dee',
            borderWidth: 1,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y', // Barras horizontales
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#1b202e',
              titleColor: '#fff',
              bodyColor: '#a3aed0',
              borderColor: 'rgba(255, 255, 255, 0.1)',
              borderWidth: 1,
              padding: 12
            }
          },
          scales: {
            x: {
              grid: { color: colors.gridColor },
              ticks: { color: colors.textColor }
            },
            y: {
              grid: { display: false },
              ticks: { color: colors.textColor }
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
          labels: rawData.labels || ['Óptimo', 'Stock Bajo', 'Sin Stock'],
          datasets: [{
            data: rawData.data || [0, 0, 0],
            backgroundColor: [colors.optimo, colors.stockBajo, colors.sinStock],
            borderWidth: 2,
            borderColor: '#1e2430'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                color: colors.textColor,
                font: { family: 'Inter', size: 12 },
                padding: 16,
                usePointStyle: true
              }
            },
            tooltip: {
              backgroundColor: '#1b202e',
              titleColor: '#fff',
              bodyColor: '#a3aed0',
              borderColor: 'rgba(255, 255, 255, 0.1)',
              borderWidth: 1,
              padding: 12
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
    vpStock.style.color = stock === 0 ? 'var(--rust)' : stock < 3 ? '#c4900a' : 'var(--sage)';
  }
  if (vpDesc)  vpDesc.textContent  = desc || '—';
  if (vpLink)  vpLink.href         = '/inventario/' + encodeURIComponent(sku) + '/editar/';

  var modal = document.getElementById('modalVerProducto');
  if (modal) new bootstrap.Modal(modal).show();
}