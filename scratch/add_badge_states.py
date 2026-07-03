import os

CSS_APPEND = """
/* ═══════════════════════════════════════════════════════
   BADGE STATES (REPAIRED FROM CORRUPTED HTML)
   ═══════════════════════════════════════════════════════ */

.state-Administrador {
  background: rgba(152, 71, 62, 0.15) !important;
  color: #f87171 !important;
  border: 1px solid rgba(248, 113, 113, 0.3) !important;
}

.state-vencido {
  background: rgba(220, 38, 38, 0.15) !important;
  color: #f87171 !important;
  border: 1px solid rgba(248, 113, 113, 0.3) !important;
}

.state-devuelto {
  background: rgba(5, 150, 105, 0.15) !important;
  color: #34d399 !important;
  border: 1px solid rgba(52, 211, 153, 0.3) !important;
}

.badge {
  font-family: var(--font-ui, 'Inter', sans-serif);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
"""

with open('static/css/style.css', 'a', encoding='utf-8') as f:
    f.write(CSS_APPEND)
