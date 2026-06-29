"""
Build script: generates all pages with the new navigation structure
Usage: python build_site.py
"""

import os, re

BASE = "C:/Users/admin/WorkBuddy/2026-05-26-task-1/hongye-furniture-website"

# ── NAVIGATION DEFINITION ─────────────────────────────────────────────────────
# Each top-level item: (label_es, url, [dropdown_items])
# dropdown_items: (icon_type, label_es, url, label_key)
NAV_ITEMS = [
    ("Inicio", "/", []),
    ("Hoteles", "/hoteles/", [
        ("catalog", "Catálogo de muebles para hoteles", "/catalogo/hoteleria/", "hotel-catalog"),
        ("project", "Proyectos hoteleros",              "/proyectos/hoteleria/", "hotel-projects"),
    ]),
    ("Oficinas", "/oficinas/", [
        ("catalog", "Catálogo de muebles de oficina",   "/catalogo/oficinas/",  "office-catalog"),
        ("project", "Proyectos de oficinas",             "/proyectos/oficinas/", "office-projects"),
    ]),
    ("Salud", "/salud/", [
        ("catalog", "Catálogo de mobiliario para salud","/catalogo/salud/",     "health-catalog"),
        ("project", "Proyectos de salud",                "/proyectos/salud/",   "health-projects"),
    ]),
    ("Educación", "/educacion/", [
        ("catalog", "Catálogo de mobiliario escolar",   "/catalogo/educacion/", "edu-catalog"),
        ("project", "Proyectos educativos",              "/proyectos/educacion/","edu-projects"),
    ]),
    ("Residencial", "/residencial/", [
        ("catalog", "Catálogo residencial",             "/catalogo/residencial/","res-catalog"),
        ("project", "Proyectos residenciales",           "/proyectos/residencial/","res-projects"),
    ]),
    ("Fábrica", "/fabrica/", []),
    ("Recursos", "/recursos/", [
        ("blog",  "Blog",    "/recursos/blog/",   "blog"),
        ("video", "Videos",  "/recursos/videos/", "videos"),
    ]),
    ("Contacto", "/contacto/", []),
]

# SVG icons for dropdown items
ICONS = {
    "catalog": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    "project": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
    "blog":    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
    "video":   '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>',
}

def nav_html(active_url, depth=0):
    """Generate navbar HTML. depth=0 means root level, depth=1 means one folder deep, etc."""
    prefix = "../" * depth  # for asset paths

    items_html = ""
    for label, url, children in NAV_ITEMS:
        abs_url = url  # keep absolute-style paths for href
        has_drop = len(children) > 0
        is_active = active_url == url

        if has_drop:
            chevron = '<svg class="nav-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>'
            dd_items = ""
            for icon_key, dd_label, dd_url, _ in children:
                icon_svg = ICONS.get(icon_key, "")
                dd_items += f'''
        <a href="{dd_url}" class="nav-dropdown-item">
          <span class="dd-icon">{icon_svg}</span>
          {dd_label}
        </a>'''
            items_html += f'''
      <div class="nav-item">
        <a href="{url}" class="nav-link{" active" if is_active else ""}">{label} {chevron}</a>
        <div class="nav-dropdown">{dd_items}
        </div>
      </div>'''
        else:
            items_html += f'''
      <div class="nav-item">
        <a href="{url}" class="nav-link{" active" if is_active else ""}">{label}</a>
      </div>'''

    return f'''  <!-- ══ NAVBAR ══ -->
  <header class="navbar" id="navbar">
    <div class="nav-inner container-wide">
      <a href="/" class="logo">
        <img src="{prefix}images/logo-main.png" alt="Hongye Furniture Group - Fabricante de Muebles Comerciales" class="logo-img" width="120" height="44" />
      </a>
      <nav class="nav-links" id="navLinks">{items_html}
      </nav>
      <a href="/contacto/" class="nav-cta btn-primary">Solicitar Cotización</a>
      <div class="lang-switch">
        <button class="lang-btn lang-btn-active" id="langEs">ES</button>
        <button class="lang-btn" id="langEn">EN</button>
      </div>
      <button class="menu-toggle" id="menuToggle" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>'''

def footer_html(depth=0):
    prefix = "../" * depth
    return f'''  <!-- ══ FOOTER ══ -->
  <footer class="footer">
    <div class="container footer-top">
      <div class="footer-brand">
        <a href="/">
          <img src="{prefix}images/logo-white.png" alt="Hongye Furniture Group" class="footer-logo" width="120" height="44" onerror="this.style.display='none'" />
        </a>
        <p class="footer-tagline">Fabricante chino de muebles comerciales a medida con más de 40 años de experiencia.</p>
        <div class="footer-social">
          <a href="https://wa.me/8613800000000" target="_blank" rel="noopener" aria-label="WhatsApp" class="social-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
          </a>
          <a href="https://www.youtube.com/@hongyefurniture" target="_blank" rel="noopener" aria-label="YouTube" class="social-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-links">
        <div class="footer-col">
          <h4 class="footer-col-title">Productos</h4>
          <a href="/hoteles/" class="footer-link">Mobiliario Hotelero</a>
          <a href="/oficinas/" class="footer-link">Mobiliario de Oficina</a>
          <a href="/salud/" class="footer-link">Mobiliario de Salud</a>
          <a href="/educacion/" class="footer-link">Mobiliario Educativo</a>
          <a href="/residencial/" class="footer-link">Mobiliario Residencial</a>
        </div>
        <div class="footer-col">
          <h4 class="footer-col-title">Empresa</h4>
          <a href="/" class="footer-link">Inicio</a>
          <a href="/fabrica/" class="footer-link">Nuestra Fábrica</a>
          <a href="/catalogo/" class="footer-link">Catálogos</a>
          <a href="/proyectos/hoteleria/" class="footer-link">Proyectos</a>
        </div>
        <div class="footer-col">
          <h4 class="footer-col-title">Recursos</h4>
          <a href="/recursos/blog/" class="footer-link">Blog</a>
          <a href="/recursos/videos/" class="footer-link">Videos</a>
          <a href="/contacto/" class="footer-link">Solicitar Cotización</a>
        </div>
        <div class="footer-col">
          <h4 class="footer-col-title">Contacto</h4>
          <p class="footer-info">📧 info@hongyefurniture.com</p>
          <p class="footer-info">📱 +86 138-0000-0000</p>
          <p class="footer-info">📍 Guangdong, China</p>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container footer-bottom-inner">
        <p>&copy; 2025 Hongye Furniture Group Co., Ltd. Todos los derechos reservados.</p>
        <div class="footer-bottom-links">
          <a href="#">Política de Privacidad</a>
          <a href="#">Términos de Servicio</a>
        </div>
      </div>
    </div>
  </footer>'''

def page_head(title, desc, keywords, canonical, img_path, depth=0):
    prefix = "../" * depth
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="https://www.hongyefurniture.com{canonical}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="robots" content="index, follow" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://www.hongyefurniture.com/{img_path}" />
  <meta property="og:url" content="https://www.hongyefurniture.com{canonical}" />
  <meta property="og:site_name" content="Hongye Furniture Group" />
  <meta property="og:locale" content="es_ES" />
  <link rel="stylesheet" href="{prefix}styles.css" />
  <link rel="stylesheet" href="{prefix}new-pages.css" />
  <link rel="stylesheet" href="{prefix}nav-shared.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
</head>
<body>'''

def nav_js():
    return '''  <script>
    // Mobile menu toggle
    const toggle = document.getElementById('menuToggle');
    const nav = document.getElementById('navLinks');
    if (toggle && nav) {
      toggle.addEventListener('click', () => {
        nav.classList.toggle('open');
        toggle.classList.toggle('open');
      });
    }
    // Mobile dropdown toggle
    document.querySelectorAll('.nav-item').forEach(item => {
      const link = item.querySelector('.nav-link');
      const drop = item.querySelector('.nav-dropdown');
      if (link && drop) {
        link.addEventListener('click', (e) => {
          if (window.innerWidth <= 900) {
            e.preventDefault();
            item.classList.toggle('open');
          }
        });
      }
    });
    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    if (navbar) {
      window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 20);
      });
    }
    // Lang buttons (placeholder)
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('lang-btn-active'));
        btn.classList.add('lang-btn-active');
      });
    });
  </script>'''

def page_hero(bg_img, alt, tag, h1, sub, cta_text, cta_url, depth=0):
    prefix = "../" * depth
    return f'''  <!-- Hero -->
  <section class="page-hero">
    <div class="page-hero-bg">
      <div class="page-hero-overlay"></div>
      <img src="{prefix}{bg_img}" alt="{alt}" class="page-hero-img" width="1920" height="600" />
    </div>
    <div class="container page-hero-content">
      <span class="hero-breadcrumb">{tag}</span>
      <h1 class="page-hero-title">{h1}</h1>
      <p class="page-hero-sub">{sub}</p>
      <div class="hero-actions">
        <a href="{cta_url}" class="btn-hero-primary">{cta_text}</a>
      </div>
    </div>
  </section>'''

# ── CATEGORY PAGE TEMPLATE ─────────────────────────────────────────────────────
def category_page(slug, label_es, title_full, desc, keywords, bg_img, hero_alt,
                  intro_text, catalog_desc, project_desc, depth=1):
    prefix = "../" * depth
    canonical = f"/{slug}/"
    head = page_head(title_full, desc, keywords, canonical, bg_img, depth)
    navbar = nav_html(f"/{slug}/", depth)
    hero = page_hero(bg_img, hero_alt, "Inicio / " + label_es,
                     label_es, intro_text,
                     "Solicitar Cotización", "/contacto/", depth)
    footer = footer_html(depth)
    js = nav_js()

    return f'''{head}
{navbar}
{hero}

  <!-- ══ INTRO ══ -->
  <section class="section">
    <div class="container">
      <div class="two-col-grid">
        <div class="col-text">
          <span class="section-tag">{label_es}</span>
          <h2 class="section-title">{title_full}</h2>
          <p class="section-desc">{intro_text}</p>
          <div class="two-cta-row">
            <a href="{prefix}catalogo/{slug if slug != "hoteles" else "hoteleria"}/" class="btn-primary">Ver Catálogo</a>
            <a href="{prefix}proyectos/{slug if slug != "hoteles" else "hoteleria"}/" class="btn-outline">Ver Proyectos</a>
          </div>
        </div>
        <div class="col-image">
          <img src="{prefix}{bg_img}" alt="{hero_alt}" loading="lazy" width="600" height="420" class="rounded-img" />
        </div>
      </div>
    </div>
  </section>

  <!-- ══ LINKS TO CATALOG & PROJECTS ══ -->
  <section class="section section-gray">
    <div class="container">
      <div class="card-pair-grid">
        <a href="{prefix}catalogo/{slug if slug != "hoteles" else "hoteleria"}/" class="feature-card">
          <div class="feature-card-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          </div>
          <h3 class="feature-card-title">Catálogo de Muebles</h3>
          <p class="feature-card-desc">{catalog_desc}</p>
          <span class="feature-card-link">Ver catálogo completo →</span>
        </a>
        <a href="{prefix}proyectos/{slug if slug != "hoteles" else "hoteleria"}/" class="feature-card">
          <div class="feature-card-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          </div>
          <h3 class="feature-card-title">Proyectos Realizados</h3>
          <p class="feature-card-desc">{project_desc}</p>
          <span class="feature-card-link">Ver casos de éxito →</span>
        </a>
      </div>
    </div>
  </section>

  <!-- ══ CTA ══ -->
  <section class="section cta-section section-dark">
    <div class="container cta-inner">
      <h2 class="cta-title">¿Listo para iniciar su proyecto?</h2>
      <p class="cta-desc">Contáctenos hoy y reciba una cotización gratuita en 24 horas.</p>
      <a href="/contacto/" class="btn-hero-primary">Solicitar Cotización Gratuita</a>
    </div>
  </section>

{footer}
{js}
</body>
</html>'''

# ── CATALOG / PROJECTS LISTING PAGE ───────────────────────────────────────────
def listing_page(page_type, cat_slug, cat_label, title, desc, keywords, bg_img, alt, depth=2):
    """page_type: 'catalogo' or 'proyectos'"""
    prefix = "../" * depth
    url_slug = cat_slug  # hoteleria / oficinas / salud / educacion / residencial
    canonical = f"/{page_type}/{url_slug}/"

    type_label = "Catálogo" if page_type == "catalogo" else "Proyectos"
    type_label_full = "Catálogo de Muebles" if page_type == "catalogo" else "Proyectos Realizados"
    breadcrumb = f"Inicio / {cat_label} / {type_label}"

    head = page_head(title, desc, keywords, canonical, bg_img, depth)
    navbar = nav_html(f"/{cat_label.lower()}/", depth)
    footer = footer_html(depth)
    js = nav_js()

    if page_type == "catalogo":
        content = f'''  <!-- ══ CATALOG INTRO ══ -->
  <section class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">{cat_label}</span>
        <h2 class="section-title">{title}</h2>
        <p class="section-desc">{desc}</p>
      </div>
      <!-- Catalog items placeholder grid -->
      <div class="catalog-grid">
        <div class="catalog-item-placeholder">
          <div class="catalog-thumb">
            <img src="{prefix}images/productos/{url_slug}/placeholder-1.jpg"
              onerror="this.parentElement.style.background='linear-gradient(135deg,#1a2a3a,#2c4050)'"
              alt="{cat_label} - producto 1" loading="lazy" width="400" height="300" />
          </div>
          <div class="catalog-info">
            <h4>Producto {cat_label} 01</h4>
            <p>Fabricación a medida · Precio directo de fábrica</p>
          </div>
        </div>
        <div class="catalog-item-placeholder">
          <div class="catalog-thumb" style="background:linear-gradient(135deg,#1a2a3a,#2c4050)"></div>
          <div class="catalog-info"><h4>Producto {cat_label} 02</h4><p>Personalización total de materiales y acabados</p></div>
        </div>
        <div class="catalog-item-placeholder">
          <div class="catalog-thumb" style="background:linear-gradient(135deg,#1a3a2a,#2c5040)"></div>
          <div class="catalog-info"><h4>Producto {cat_label} 03</h4><p>Certificaciones internacionales ISO · CE · SGS</p></div>
        </div>
        <div class="catalog-item-placeholder">
          <div class="catalog-thumb" style="background:linear-gradient(135deg,#2a1a3a,#4a2c50)"></div>
          <div class="catalog-info"><h4>Producto {cat_label} 04</h4><p>Envío internacional a más de 50 países</p></div>
        </div>
        <div class="catalog-item-placeholder">
          <div class="catalog-thumb" style="background:linear-gradient(135deg,#3a2a1a,#504030)"></div>
          <div class="catalog-info"><h4>Producto {cat_label} 05</h4><p>Muestra física disponible bajo pedido</p></div>
        </div>
        <div class="catalog-item-placeholder catalog-cta-card">
          <div class="catalog-cta-content">
            <h4>¿No encuentra lo que busca?</h4>
            <p>Diseñamos y fabricamos según sus especificaciones exactas.</p>
            <a href="/contacto/" class="btn-primary">Solicitar Diseño a Medida</a>
          </div>
        </div>
      </div>
    </div>
  </section>'''
    else:
        content = f'''  <!-- ══ PROJECTS LISTING ══ -->
  <section class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">{cat_label}</span>
        <h2 class="section-title">{title}</h2>
        <p class="section-desc">{desc}</p>
      </div>
      <div class="projects-grid">
        <div class="project-card project-featured">
          <div class="project-thumb" style="background:linear-gradient(135deg,#1a2a3a,#2c4050)"></div>
          <div class="project-info">
            <span class="project-tag">{cat_label}</span>
            <h3>Proyecto Destacado 01</h3>
            <p>Proyecto de amueblamiento completo entregado con éxito. Más detalles próximamente.</p>
            <div class="project-meta"><span>📍 Latinoamérica</span></div>
          </div>
        </div>
        <div class="project-card">
          <div class="project-thumb" style="background:linear-gradient(135deg,#1a3040,#2c4a5e)"></div>
          <div class="project-info">
            <span class="project-tag">{cat_label}</span>
            <h3>Proyecto 02</h3>
            <p>En actualización — estamos cargando los detalles del proyecto.</p>
          </div>
        </div>
        <div class="project-card">
          <div class="project-thumb" style="background:linear-gradient(135deg,#2a1a10,#4a3020)"></div>
          <div class="project-info">
            <span class="project-tag">{cat_label}</span>
            <h3>Proyecto 03</h3>
            <p>Próximamente — caso de éxito en preparación.</p>
          </div>
        </div>
      </div>
    </div>
  </section>'''

    return f'''{head}
{navbar}
  <!-- Hero -->
  <section class="page-hero page-hero-sm">
    <div class="page-hero-bg">
      <div class="page-hero-overlay"></div>
      <img src="{prefix}{bg_img}" alt="{alt}" class="page-hero-img" width="1920" height="400" />
    </div>
    <div class="container page-hero-content">
      <nav class="breadcrumb-nav" aria-label="breadcrumb">
        <a href="/">Inicio</a>
        <span>›</span>
        <a href="/{url_slug if url_slug not in ("hoteleria",) else "hoteles"}/">{cat_label}</a>
        <span>›</span>
        <span>{type_label}</span>
      </nav>
      <h1 class="page-hero-title">{title}</h1>
    </div>
  </section>

{content}

  <!-- ══ CTA ══ -->
  <section class="section cta-section section-dark">
    <div class="container cta-inner">
      <h2 class="cta-title">¿Tiene un proyecto en mente?</h2>
      <p class="cta-desc">Hablemos. Cotización gratuita en 24 horas.</p>
      <a href="/contacto/" class="btn-hero-primary">Contactar Ahora</a>
    </div>
  </section>

{footer}
{js}
</body>
</html>'''

# ── GENERATE ALL PAGES ─────────────────────────────────────────────────────────

pages = []

# 1. CATEGORY MAIN PAGES
categories = [
    {
        "slug": "hoteles",
        "label_es": "Hoteles",
        "title_full": "Mobiliario Hotelero a Medida",
        "desc": "Fabricante de mobiliario hotelero a medida: habitaciones, lobbies, restaurantes y spa. Precio directo de fábrica, envío internacional. Hongye Furniture Group.",
        "keywords": "mobiliario hotelero a medida, muebles hotel cinco estrellas, fabricante muebles hoteleros China, mobiliario habitaciones hotel, lobby hotel muebles",
        "bg_img": "images/productos/hotel/mobiliario-hotelero-lujo-lobby.jpg",
        "hero_alt": "Mobiliario hotelero de lujo fabricado a medida por Hongye Furniture Group",
        "intro_text": "Equipamos hoteles de lujo en más de 50 países con mobiliario fabricado a medida. Desde habitaciones estándar hasta suites presidenciales, lobbies y restaurantes — soluciones completas de amueblamiento directo de fábrica.",
        "catalog_desc": "Explore nuestra colección completa de muebles para hoteles: camas, armarios, escritorios, sillas, sofás y más.",
        "project_desc": "Vea proyectos hoteleros reales entregados en Asia, Oriente Medio, Europa y Latinoamérica.",
        "depth": 1,
    },
    {
        "slug": "oficinas",
        "label_es": "Oficinas",
        "title_full": "Mobiliario de Oficina Corporativo a Medida",
        "desc": "Muebles de oficina corporativos a medida: escritorios ejecutivos, salas de reuniones, coworking y recepción. Fabricante directo en China. Hongye Furniture Group.",
        "keywords": "muebles oficina corporativa, escritorios ejecutivos medida, sala reuniones muebles, mobiliario coworking, fabricante muebles oficina China",
        "bg_img": "images/productos/oficina/mobiliario-oficina-moderna-coworking.jpg",
        "hero_alt": "Mobiliario de oficina corporativa moderna fabricado a medida por Hongye Furniture",
        "intro_text": "Diseñamos y fabricamos mobiliario de oficina para empresas multinacionales, startups y espacios de coworking. Escritorios a medida, sistemas de almacenaje, salas de juntas y zonas de recepción con identidad corporativa.",
        "catalog_desc": "Escritorios, sillas ejecutivas, mesas de reunión, estanterías y sistemas de almacenamiento a medida.",
        "project_desc": "Proyectos de amueblamiento de oficinas corporativas en Asia, Europa y Latinoamérica.",
        "depth": 1,
    },
    {
        "slug": "salud",
        "label_es": "Salud",
        "title_full": "Mobiliario Médico y de Salud a Medida",
        "desc": "Mobiliario médico certificado para hospitales, clínicas y centros de cuidado. Materiales de grado médico, fácil desinfección. Hongye Furniture Group.",
        "keywords": "mobiliario médico hospital, muebles clínica a medida, mobiliario centros salud, muebles grado médico China, fabricante mobiliario sanitario",
        "bg_img": "images/productos/salud/mobiliario-medico-hospital-clinica.jpg",
        "hero_alt": "Mobiliario médico para hospitales y clínicas fabricado por Hongye Furniture Group",
        "intro_text": "Proveemos soluciones de mobiliario especializado para hospitales, clínicas, residencias de mayores y centros de rehabilitación. Materiales de grado médico, superficies antibacterianas y diseño ergonómico para entornos de salud.",
        "catalog_desc": "Mobiliario de salas de espera, consultorios, habitaciones de paciente y zonas de enfermería.",
        "project_desc": "Proyectos de equipamiento de hospitales y centros médicos en múltiples países.",
        "depth": 1,
    },
    {
        "slug": "educacion",
        "label_es": "Educación",
        "title_full": "Mobiliario Educativo para Escuelas y Universidades",
        "desc": "Fabricante de mobiliario educativo: aulas, bibliotecas, laboratorios y dormitorios universitarios. Resistente, ergonómico y a medida. Hongye Furniture Group.",
        "keywords": "mobiliario educativo aulas, muebles biblioteca universidad, mobiliario escolar a medida, fabricante muebles educativos China, muebles laboratorio escuela",
        "bg_img": "images/productos/educacion/mobiliario-educativo-universidad.jpg",
        "hero_alt": "Mobiliario educativo para aulas y universidades fabricado por Hongye Furniture Group",
        "intro_text": "Equipamos escuelas, colegios y universidades con mobiliario educativo duradero y ergonómico. Aulas, bibliotecas, laboratorios, residencias universitarias y salas de docentes — diseño funcional para entornos de aprendizaje.",
        "catalog_desc": "Mesas y sillas de aula, estanterías de biblioteca, mobiliario de laboratorio y dormitorios universitarios.",
        "project_desc": "Proyectos educativos completos para universidades y colegios en Latinoamérica y el mundo.",
        "depth": 1,
    },
    {
        "slug": "residencial",
        "label_es": "Residencial",
        "title_full": "Mobiliario Residencial de Lujo para Villas y Proyectos",
        "desc": "Muebles de lujo para villas, apartamentos premium y proyectos residenciales. Fabricación a medida, materiales premium. Hongye Furniture Group.",
        "keywords": "muebles residenciales lujo, mobiliario villas a medida, muebles apartamentos premium, fabricante muebles lujo China, mobiliario desarrollos residenciales",
        "bg_img": "images/productos/residencial/salon-lujo-villa-moderno.jpg",
        "hero_alt": "Mobiliario de lujo para villas y residencias premium fabricado por Hongye Furniture",
        "intro_text": "Creamos ambientes residenciales exclusivos con mobiliario de lujo fabricado a medida. Salones, dormitorios, cocinas y espacios exteriores para villas privadas, penthouses y desarrollos inmobiliarios de alto standing.",
        "catalog_desc": "Sofás, camas, armarios, mesas de comedor y cocinas a medida para residencias de lujo.",
        "project_desc": "Proyectos de amueblamiento de villas y apartamentos de lujo en todo el mundo.",
        "depth": 1,
    },
]

for cat in categories:
    html = category_page(**cat)
    path = os.path.join(BASE, cat["slug"], "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    pages.append(path)
    print(f"  Created: {cat['slug']}/index.html")

# 2. CATALOG SUB-PAGES
catalog_pages = [
    ("hoteleria", "Hoteles", "Catálogo de Muebles para Hoteles | Hongye Furniture",
     "Catálogo completo de mobiliario hotelero a medida: habitaciones, suites, lobby y restaurante.",
     "catálogo muebles hotel, mobiliario hotelero precio, muebles habitación hotel a medida",
     "images/productos/hotel/habitacion-hotel-cinco-estrellas-bangkok.png",
     "Catálogo de mobiliario hotelero - habitaciones de hotel cinco estrellas"),
    ("oficinas", "Oficinas", "Catálogo de Muebles de Oficina | Hongye Furniture",
     "Catálogo de mobiliario de oficina corporativa: escritorios, salas de juntas y áreas colaborativas.",
     "catálogo muebles oficina, escritorios corporativos precio, sillas ejecutivas a medida",
     "images/productos/oficina/escritorios-ejecutivos-madera.jpg",
     "Catálogo de mobiliario de oficina - escritorios ejecutivos"),
    ("salud", "Salud", "Catálogo de Mobiliario Médico | Hongye Furniture",
     "Catálogo de mobiliario médico certificado para hospitales, clínicas y centros de salud.",
     "catálogo muebles médicos, mobiliario hospital precio, sillas consulta médica",
     "images/productos/salud/consultorio-medico-mobiliario.png",
     "Catálogo de mobiliario médico - consultorios y hospitales"),
    ("educacion", "Educación", "Catálogo de Mobiliario Educativo | Hongye Furniture",
     "Catálogo de muebles escolares y universitarios: aulas, bibliotecas y laboratorios.",
     "catálogo muebles escolares, mobiliario educativo precio, sillas aula a medida",
     "images/productos/educacion/salon-clases-mobiliario-escolar.png",
     "Catálogo de mobiliario educativo - aulas y universidades"),
    ("residencial", "Residencial", "Catálogo Mobiliario Residencial de Lujo | Hongye Furniture",
     "Catálogo de muebles de lujo para villas y apartamentos premium: sala, dormitorio y cocina.",
     "catálogo muebles residenciales lujo, mobiliario villa precio, sofás lujo a medida",
     "images/productos/residencial/salon-elegante-muebles-premium.jpg",
     "Catálogo de mobiliario residencial de lujo - villas y apartamentos"),
]

for slug, label, title, desc, kw, img, alt in catalog_pages:
    html = listing_page("catalogo", slug, label, title, desc, kw, img, alt, depth=2)
    path = os.path.join(BASE, "catalogo", slug, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    pages.append(path)
    print(f"  Created: catalogo/{slug}/index.html")

# 3. PROJECTS SUB-PAGES
project_pages = [
    ("hoteleria", "Hoteles", "Proyectos Hoteleros Realizados | Hongye Furniture",
     "Casos de éxito: proyectos de amueblamiento hotelero completo en más de 30 países.",
     "proyectos hoteleros, casos éxito muebles hotel, amueblamiento hotel completo",
     "images/proyectos/proyecto-hotel-dubai-muebles.jpg",
     "Proyecto de amueblamiento hotelero - hotel de lujo en Dubai"),
    ("oficinas", "Oficinas", "Proyectos de Oficinas Realizados | Hongye Furniture",
     "Proyectos de amueblamiento de oficinas corporativas en Asia, Europa y Latinoamérica.",
     "proyectos oficinas corporativas, amueblamiento oficina completo, casos éxito muebles oficina",
     "images/proyectos/proyecto-oficina-corporativa-singapur.jpg",
     "Proyecto de mobiliario de oficina corporativa en Singapur"),
    ("salud", "Salud", "Proyectos de Mobiliario Médico | Hongye Furniture",
     "Proyectos de equipamiento de hospitales y centros médicos en múltiples países.",
     "proyectos mobiliario médico, equipamiento hospital completo, casos éxito muebles salud",
     "images/productos/salud/mobiliario-medico-hospital-clinica.jpg",
     "Proyecto de mobiliario médico - centro de salud equipado"),
    ("educacion", "Educación", "Proyectos Educativos Realizados | Hongye Furniture",
     "Proyectos de equipamiento de campus universitarios y colegios en Latinoamérica y el mundo.",
     "proyectos educativos, equipamiento universidad completo, casos éxito muebles escuela",
     "images/proyectos/proyecto-universidad-latinoamerica.jpg",
     "Proyecto de mobiliario educativo - universidad latinoamericana"),
    ("residencial", "Residencial", "Proyectos Residenciales de Lujo | Hongye Furniture",
     "Proyectos de amueblamiento de villas y apartamentos de lujo en todo el mundo.",
     "proyectos residenciales lujo, amueblamiento villa completo, casos éxito muebles lujo",
     "images/productos/residencial/comedor-muebles-lujo-residencial.jpg",
     "Proyecto de mobiliario residencial de lujo - villa premium"),
]

for slug, label, title, desc, kw, img, alt in project_pages:
    html = listing_page("proyectos", slug, label, title, desc, kw, img, alt, depth=2)
    path = os.path.join(BASE, "proyectos", slug, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    pages.append(path)
    print(f"  Created: proyectos/{slug}/index.html")

# 4. FABRICA PAGE
fabrica_html = f'''{page_head(
    "Nuestra Fábrica | Hongye Furniture Group - 350.000m² en China",
    "Visite la fábrica de Hongye Furniture Group: 350.000m² con tecnología CNC, 40.000m² de sala de exposición y certificaciones ISO/CE/FSC/SGS. Fabricación directa.",
    "fábrica muebles China, fabricante directo muebles, visita fábrica muebles Guangdong, producción muebles comerciales",
    "/fabrica/",
    "images/fabrica/sala-exposicion-muebles-comerciales.jpg",
    1
)}
{nav_html("/fabrica/", 1)}
  <section class="page-hero">
    <div class="page-hero-bg">
      <div class="page-hero-overlay"></div>
      <img src="../images/fabrica/sala-exposicion-muebles-comerciales.jpg" alt="Fábrica de muebles Hongye Furniture Group - sala de exposición de 40.000m²" class="page-hero-img" width="1920" height="600" />
    </div>
    <div class="container page-hero-content">
      <span class="hero-breadcrumb">Inicio / Fábrica</span>
      <h1 class="page-hero-title">Nuestra Fábrica</h1>
      <p class="page-hero-sub">350.000m² de producción · 40.000m² de sala de exposición · Más de 40 años de excelencia</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="two-col-grid">
        <div class="col-text">
          <span class="section-tag">Fábrica Propia</span>
          <h2 class="section-title">Fabricación Directa sin Intermediarios</h2>
          <p class="section-desc">Hongye Furniture Group opera sus propias instalaciones de fabricación en Guangdong, China. Con más de 350.000m² de planta industrial y tecnología de última generación, producimos directamente para nuestros clientes en todo el mundo.</p>
          <ul class="feature-list">
            <li>✓ 350.000m² planta de producción propia</li>
            <li>✓ 40.000m² sala de exposición</li>
            <li>✓ Más de 2.000 trabajadores especializados</li>
            <li>✓ CNC de alta precisión · Laser · Acabado 5 ejes</li>
            <li>✓ Certificaciones ISO 9001 · CE · FSC · SGS</li>
            <li>✓ Control de calidad en 12 etapas</li>
          </ul>
        </div>
        <div class="col-image">
          <img src="../images/fabrica/sala-exposicion-muebles-comerciales.jpg" alt="Sala de exposición de 40.000m² de Hongye Furniture Group" loading="lazy" width="600" height="420" class="rounded-img" />
        </div>
      </div>
    </div>
  </section>

  <section class="section section-gray">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Instalaciones</span>
        <h2 class="section-title">Tecnología de Fabricación de Vanguardia</h2>
      </div>
      <div class="stats-grid">
        <div class="stat-card"><span class="stat-num">350,000㎡</span><span class="stat-label">Planta de producción</span></div>
        <div class="stat-card"><span class="stat-num">40,000㎡</span><span class="stat-label">Sala de exposición</span></div>
        <div class="stat-card"><span class="stat-num">40+</span><span class="stat-label">Años de experiencia</span></div>
        <div class="stat-card"><span class="stat-num">2,000+</span><span class="stat-label">Empleados especializados</span></div>
        <div class="stat-card"><span class="stat-num">10,000+</span><span class="stat-label">Proyectos completados</span></div>
        <div class="stat-card"><span class="stat-num">50+</span><span class="stat-label">Países de destino</span></div>
      </div>
    </div>
  </section>

  <section class="section cta-section section-dark">
    <div class="container cta-inner">
      <h2 class="cta-title">¿Le gustaría visitar nuestra fábrica?</h2>
      <p class="cta-desc">Organizamos visitas guiadas para clientes B2B. Contáctenos para programar su visita.</p>
      <a href="/contacto/" class="btn-hero-primary">Programar Visita a Fábrica</a>
    </div>
  </section>

{footer_html(1)}
{nav_js()}
</body>
</html>'''

with open(os.path.join(BASE, "fabrica", "index.html"), "w", encoding="utf-8") as f:
    f.write(fabrica_html)
print("  Created: fabrica/index.html")

# 5. CONTACTO PAGE
contacto_html = f'''{page_head(
    "Contacto y Cotización Gratuita | Hongye Furniture Group",
    "Solicite una cotización gratuita para muebles comerciales. Respondemos en 24 horas por WhatsApp, email o formulario. Hongye Furniture Group.",
    "cotización muebles comerciales, contacto fabricante muebles China, presupuesto mobiliario hotel, solicitar cotización muebles",
    "/contacto/",
    "images/fabrica/linea-ensamblaje-muebles-fabrica.jpg",
    1
)}
{nav_html("/contacto/", 1)}
  <section class="page-hero page-hero-sm">
    <div class="page-hero-bg">
      <div class="page-hero-overlay"></div>
      <img src="../images/fabrica/linea-ensamblaje-muebles-fabrica.jpg" alt="Contacte con Hongye Furniture Group para cotización de muebles comerciales" class="page-hero-img" width="1920" height="400" />
    </div>
    <div class="container page-hero-content">
      <span class="hero-breadcrumb">Inicio / Contacto</span>
      <h1 class="page-hero-title">Solicitar Cotización</h1>
      <p class="page-hero-sub">Respondemos en menos de 24 horas</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="contact-grid">
        <div class="contact-form-col">
          <h2 class="section-title">Cuéntenos su Proyecto</h2>
          <p class="section-desc">Complete el formulario y nuestro equipo le contactará con una propuesta personalizada.</p>
          <form class="contact-form" action="#" method="post">
            <div class="form-row">
              <div class="form-group">
                <label for="nombre">Nombre *</label>
                <input type="text" id="nombre" name="nombre" placeholder="Su nombre completo" required />
              </div>
              <div class="form-group">
                <label for="empresa">Empresa</label>
                <input type="text" id="empresa" name="empresa" placeholder="Nombre de su empresa" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="email">Email *</label>
                <input type="email" id="email" name="email" placeholder="correo@empresa.com" required />
              </div>
              <div class="form-group">
                <label for="whatsapp">WhatsApp / Teléfono</label>
                <input type="tel" id="whatsapp" name="whatsapp" placeholder="+1 000 000 0000" />
              </div>
            </div>
            <div class="form-group">
              <label for="categoria">Categoría de Muebles</label>
              <select id="categoria" name="categoria">
                <option value="">Seleccione una categoría</option>
                <option value="hoteles">Mobiliario Hotelero</option>
                <option value="oficinas">Mobiliario de Oficina</option>
                <option value="salud">Mobiliario de Salud</option>
                <option value="educacion">Mobiliario Educativo</option>
                <option value="residencial">Mobiliario Residencial</option>
                <option value="otro">Otro</option>
              </select>
            </div>
            <div class="form-group">
              <label for="mensaje">Descripción del Proyecto *</label>
              <textarea id="mensaje" name="mensaje" rows="5" placeholder="Describa su proyecto: tipo de espacio, cantidad aproximada de piezas, presupuesto estimado, plazos..." required></textarea>
            </div>
            <button type="submit" class="btn-primary btn-full">Enviar Consulta</button>
          </form>
        </div>
        <div class="contact-info-col">
          <h3>Contacto Directo</h3>
          <div class="contact-method">
            <div class="cm-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
            </div>
            <div>
              <strong>WhatsApp</strong>
              <a href="https://wa.me/8613800000000" target="_blank" rel="noopener">+86 138-0000-0000</a>
            </div>
          </div>
          <div class="contact-method">
            <div class="cm-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            </div>
            <div>
              <strong>Email</strong>
              <a href="mailto:info@hongyefurniture.com">info@hongyefurniture.com</a>
            </div>
          </div>
          <div class="contact-method">
            <div class="cm-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            </div>
            <div>
              <strong>Dirección</strong>
              <p>Guangdong Province, China</p>
            </div>
          </div>
          <div class="contact-faq">
            <h4>Preguntas Frecuentes</h4>
            <details class="faq-item">
              <summary>¿Cuál es el MOQ mínimo?</summary>
              <p>No hay MOQ mínimo estricto. Trabajamos desde proyectos de una sola pieza hasta pedidos de miles de unidades.</p>
            </details>
            <details class="faq-item">
              <summary>¿Cuánto tiempo tarda la producción?</summary>
              <p>Generalmente entre 30 y 60 días dependiendo del volumen y complejidad del proyecto.</p>
            </details>
            <details class="faq-item">
              <summary>¿Pueden enviar a cualquier país?</summary>
              <p>Sí, enviamos a más de 50 países con soporte logístico completo puerta a puerta.</p>
            </details>
          </div>
        </div>
      </div>
    </div>
  </section>

{footer_html(1)}
{nav_js()}
</body>
</html>'''

with open(os.path.join(BASE, "contacto", "index.html"), "w", encoding="utf-8") as f:
    f.write(contacto_html)
print("  Created: contacto/index.html")

# 6. RECURSOS PAGES
recursos_main = f'''{page_head(
    "Recursos | Blog y Videos de Muebles Comerciales | Hongye Furniture",
    "Centro de recursos de Hongye Furniture: artículos de blog sobre tendencias en muebles comerciales y videos de fábrica y proyectos.",
    "blog muebles comerciales, videos fábrica muebles China, tendencias mobiliario hotelero",
    "/recursos/",
    "images/fabrica/taller-produccion-muebles-cnc.jpg",
    1
)}
{nav_html("/recursos/", 1)}
  <section class="page-hero page-hero-sm">
    <div class="page-hero-bg">
      <div class="page-hero-overlay"></div>
      <img src="../images/fabrica/taller-produccion-muebles-cnc.jpg" alt="Centro de recursos Hongye Furniture - blog y videos" class="page-hero-img" width="1920" height="400" />
    </div>
    <div class="container page-hero-content">
      <span class="hero-breadcrumb">Inicio / Recursos</span>
      <h1 class="page-hero-title">Recursos</h1>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="card-pair-grid">
        <a href="/recursos/blog/" class="feature-card">
          <div class="feature-card-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></div>
          <h3 class="feature-card-title">Blog</h3>
          <p class="feature-card-desc">Artículos sobre tendencias en mobiliario comercial, guías de diseño y consejos para proyectos.</p>
          <span class="feature-card-link">Leer artículos →</span>
        </a>
        <a href="/recursos/videos/" class="feature-card">
          <div class="feature-card-icon"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg></div>
          <h3 class="feature-card-title">Videos</h3>
          <p class="feature-card-desc">Videos de nuestra fábrica, proceso de fabricación, sala de exposición y proyectos terminados.</p>
          <span class="feature-card-link">Ver videos →</span>
        </a>
      </div>
    </div>
  </section>
{footer_html(1)}
{nav_js()}
</body>
</html>'''

with open(os.path.join(BASE, "recursos", "index.html"), "w", encoding="utf-8") as f:
    f.write(recursos_main)
print("  Created: recursos/index.html")

# Blog page
blog_html = f'''{page_head(
    "Blog sobre Muebles Comerciales | Hongye Furniture Group",
    "Artículos y guías sobre tendencias en mobiliario hotelero, de oficina, educativo y residencial de lujo. Expertos en fabricación a medida.",
    "blog muebles comerciales, tendencias mobiliario hotelero, guía muebles oficina, artículos fabricante muebles China",
    "/recursos/blog/",
    "images/fabrica/taller-produccion-muebles-cnc.jpg",
    2
)}
{nav_html("/recursos/", 2)}
  <section class="page-hero page-hero-sm">
    <div class="page-hero-bg">
      <div class="page-hero-overlay"></div>
      <img src="../../images/fabrica/taller-produccion-muebles-cnc.jpg" alt="Blog Hongye Furniture - artículos sobre muebles comerciales" class="page-hero-img" width="1920" height="400" />
    </div>
    <div class="container page-hero-content">
      <nav class="breadcrumb-nav"><a href="/">Inicio</a> <span>›</span> <a href="/recursos/">Recursos</a> <span>›</span> <span>Blog</span></nav>
      <h1 class="page-hero-title">Blog</h1>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Artículos</span>
        <h2 class="section-title">Últimas Publicaciones</h2>
        <p class="section-desc">Conocimiento experto sobre diseño, fabricación y tendencias en mobiliario comercial.</p>
      </div>
      <div class="blog-grid">
        <article class="blog-card">
          <div class="blog-thumb" style="background:linear-gradient(135deg,#1a2a3a,#2c4050)"></div>
          <div class="blog-content">
            <span class="blog-tag">Hoteles</span>
            <h3>Tendencias en Mobiliario Hotelero 2025</h3>
            <p>Las nuevas tendencias en diseño de habitaciones de hotel y cómo influyen en la elección de mobiliario...</p>
            <span class="blog-date">Próximamente</span>
          </div>
        </article>
        <article class="blog-card">
          <div class="blog-thumb" style="background:linear-gradient(135deg,#1a3a2a,#2c5040)"></div>
          <div class="blog-content">
            <span class="blog-tag">Oficinas</span>
            <h3>Cómo Elegir Muebles para tu Oficina Corporativa</h3>
            <p>Guía práctica para seleccionar el mobiliario ideal según el estilo de trabajo y la cultura de empresa...</p>
            <span class="blog-date">Próximamente</span>
          </div>
        </article>
        <article class="blog-card">
          <div class="blog-thumb" style="background:linear-gradient(135deg,#2a1a3a,#4a2c50)"></div>
          <div class="blog-content">
            <span class="blog-tag">Fábrica</span>
            <h3>Por Qué Comprar Muebles Directamente del Fabricante</h3>
            <p>Ventajas de trabajar directamente con fábrica: precio, personalización, calidad y tiempos de entrega...</p>
            <span class="blog-date">Próximamente</span>
          </div>
        </article>
      </div>
    </div>
  </section>
{footer_html(2)}
{nav_js()}
</body>
</html>'''

with open(os.path.join(BASE, "recursos", "blog", "index.html"), "w", encoding="utf-8") as f:
    f.write(blog_html)
print("  Created: recursos/blog/index.html")

# Videos page
videos_html = f'''{page_head(
    "Videos de Fábrica y Proyectos | Hongye Furniture Group",
    "Videos de la fábrica Hongye Furniture, proceso de fabricación de muebles comerciales, sala de exposición y proyectos terminados en todo el mundo.",
    "videos fábrica muebles China, proceso fabricación muebles comerciales, videos proyectos hoteleros",
    "/recursos/videos/",
    "images/fabrica/linea-ensamblaje-muebles-fabrica.jpg",
    2
)}
{nav_html("/recursos/", 2)}
  <section class="page-hero page-hero-sm">
    <div class="page-hero-bg">
      <div class="page-hero-overlay"></div>
      <img src="../../images/fabrica/linea-ensamblaje-muebles-fabrica.jpg" alt="Videos Hongye Furniture - proceso de fabricación de muebles" class="page-hero-img" width="1920" height="400" />
    </div>
    <div class="container page-hero-content">
      <nav class="breadcrumb-nav"><a href="/">Inicio</a> <span>›</span> <a href="/recursos/">Recursos</a> <span>›</span> <span>Videos</span></nav>
      <h1 class="page-hero-title">Videos</h1>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">YouTube</span>
        <h2 class="section-title">Videos de Nuestra Fábrica y Proyectos</h2>
        <p class="section-desc">Vea en primera persona cómo fabricamos muebles comerciales de alta calidad.</p>
      </div>
      <div class="videos-grid">
        <div class="video-card">
          <div class="video-thumb" style="background:linear-gradient(135deg,#1a2a3a,#2c4050)">
            <div class="video-play-btn"><svg width="40" height="40" viewBox="0 0 24 24" fill="white"><polygon points="5 3 19 12 5 21 5 3"/></svg></div>
          </div>
          <h4>Tour por la Fábrica Hongye Furniture</h4>
          <p>Recorra nuestras instalaciones de 350.000m² en Guangdong, China.</p>
        </div>
        <div class="video-card">
          <div class="video-thumb" style="background:linear-gradient(135deg,#1a3040,#2c4a5e)">
            <div class="video-play-btn"><svg width="40" height="40" viewBox="0 0 24 24" fill="white"><polygon points="5 3 19 12 5 21 5 3"/></svg></div>
          </div>
          <h4>Proceso de Fabricación de Muebles Hoteleros</h4>
          <p>Del diseño a la entrega: cómo producimos mobiliario para hoteles de lujo.</p>
        </div>
        <div class="video-card">
          <div class="video-thumb" style="background:linear-gradient(135deg,#2a1a10,#4a3020)">
            <div class="video-play-btn"><svg width="40" height="40" viewBox="0 0 24 24" fill="white"><polygon points="5 3 19 12 5 21 5 3"/></svg></div>
          </div>
          <h4>Proyectos Destacados 2024-2025</h4>
          <p>Una selección de los mejores proyectos de amueblamiento entregados.</p>
        </div>
      </div>
      <div class="section-cta-center">
        <a href="https://www.youtube.com/@hongyefurniture" target="_blank" rel="noopener" class="btn-primary">Ver más en YouTube →</a>
      </div>
    </div>
  </section>
{footer_html(2)}
{nav_js()}
</body>
</html>'''

with open(os.path.join(BASE, "recursos", "videos", "index.html"), "w", encoding="utf-8") as f:
    f.write(videos_html)
print("  Created: recursos/videos/index.html")

print(f"\n✅ All {len(pages) + 9} pages generated successfully!")
