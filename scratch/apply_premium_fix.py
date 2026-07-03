import os

CSS_APPEND = """
/* ═══════════════════════════════════════════════════════
   PREMIUM DESIGN OVERRIDES (FIXES)
   ═══════════════════════════════════════════════════════ */

/* 1. Unified Premium Dark Theme for Sidebar */
body.dark-mode aside {
  background: rgba(15, 23, 42, 0.65) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

body.dark-mode aside .dropdown-menu {
  background: rgba(15, 23, 42, 0.95) !important;
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
}

body.dark-mode aside .dropdown-item {
  color: rgba(255, 255, 255, 0.75) !important;
  transition: all 0.2s ease;
}

body.dark-mode aside .dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  color: #FFFFFF !important;
  padding-left: 1.5rem !important; /* Premium hover indent */
}

/* 2. Glassmorphism & Depth for Cards */
body.dark-mode .card {
  background: rgba(30, 41, 59, 0.4) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.05) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease !important;
}

body.dark-mode .card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

/* 3. KPI Number Enhancements */
.kpi-number, 
.extracted-style-216,
.extracted-style-219,
.extracted-style-221,
.extracted-style-223 {
  font-size: 3.2rem !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, #60a5fa, #c084fc, #f472b6);
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  line-height: 1.1 !important;
  margin: 0.5rem 0 !important;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

/* 4. Fix Sidebar Overlaps */
.nav-bottom {
  margin-top: auto !important;
  position: relative;
  z-index: 1050;
  background: inherit;
}

.aside-nav {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
  flex: 1;
}

/* Improve Notification Dropdown Z-Index & Positioning */
#aside-notif-panel {
  bottom: 60px !important; 
  z-index: 1100 !important;
  max-height: 60vh;
  overflow-y: auto;
  box-shadow: 0 -10px 40px rgba(0,0,0,0.5) !important;
}

.dropup .dropdown-menu {
  bottom: 100% !important;
  margin-bottom: 0.5rem !important;
  z-index: 1100 !important;
}
"""

with open('static/css/style.css', 'a', encoding='utf-8') as f:
    f.write(CSS_APPEND)

print("Premium styles appended successfully.")
