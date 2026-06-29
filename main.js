// Hongye Furniture Group - Main JavaScript

document.addEventListener('DOMContentLoaded', () => {

  // ========================================
  // Navbar Scroll Effect
  // ========================================
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 20) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }, { passive: true });
  }

  // ========================================
  // Mobile Menu Toggle
  // ========================================
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const spans = menuToggle.querySelectorAll('span');
      if (navLinks.classList.contains('open')) {
        spans[0].style.transform = 'rotate(45deg) translateY(7px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translateY(-7px)';
      } else {
        spans[0].style.transform = '';
        spans[1].style.opacity = '';
        spans[2].style.transform = '';
      }
    });

    // Close on link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
      });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!navbar.contains(e.target)) {
        navLinks.classList.remove('open');
      }
    });
  }

  // ========================================
  // Hero Banner Carousel (CSS background swap)
  // ========================================
  const heroSection = document.querySelector('.hero');
  if (heroSection) {
    let isSlide1 = true;
    let autoplayTimer = null;

    function nextSlide() {
      isSlide1 = !isSlide1;
      heroSection.classList.toggle('slide-2', !isSlide1);
    }

    function prevSlide() {
      isSlide1 = !isSlide1;
      heroSection.classList.toggle('slide-2', !isSlide1);
    }

    function startAutoplay() {
      stopAutoplay();
      autoplayTimer = setInterval(nextSlide, 5000);
    }
    function stopAutoplay() {
      if (autoplayTimer) { clearInterval(autoplayTimer); autoplayTimer = null; }
    }

    heroSection.addEventListener('mouseenter', stopAutoplay);
    heroSection.addEventListener('mouseleave', startAutoplay);

    startAutoplay();
  }

  // ========================================
  // Scroll Animations
  // ========================================
  const animateOnScroll = () => {
    const elements = document.querySelectorAll(
      '.cat-card, .project-card, .why-feature, .process-step, ' +
      '.cert-badge, .value-card, .factory-card, .timeline-item, ' +
      '.cert-detail-card, .group-card, .prod-space-card, .prod-item, ' +
      '.edu-card, .res-card, .service-card-dark, .faq-group'
    );

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });

    elements.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(24px)';
      el.style.transition = `opacity 0.5s ease ${(i % 8) * 0.06}s, transform 0.5s ease ${(i % 8) * 0.06}s`;
      observer.observe(el);
    });
  };

  animateOnScroll();

  // ========================================
  // Stats Counter Animation
  // ========================================
  const statNums = document.querySelectorAll('.stat-num, .ov-num');
  statNums.forEach(el => {
    const text = el.textContent;
    const num = parseFloat(text.replace(/[^0-9.]/g, ''));
    const suffix = text.replace(/[0-9.]/g, '');
    if (!isNaN(num)) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            animateCount(el, num, suffix, 1200);
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.5 });
      observer.observe(el);
    }
  });

  function animateCount(el, target, suffix, duration) {
    const start = 0;
    const step = target / (duration / 16);
    let current = start;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = (Number.isInteger(target) ? Math.round(current) : current.toFixed(1)) + suffix;
    }, 16);
  }

  // ========================================
  // Products Page: Category Nav Active State
  // ========================================
  const catNavItems = document.querySelectorAll('.cat-nav-item');
  const prodSections = document.querySelectorAll('.prod-section');

  if (catNavItems.length && prodSections.length) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          catNavItems.forEach(item => {
            item.classList.remove('active-cat');
            if (item.getAttribute('href') === '#' + id) {
              item.classList.add('active-cat');
            }
          });
        }
      });
    }, { threshold: 0.4 });

    prodSections.forEach(sec => sectionObserver.observe(sec));

    catNavItems.forEach(item => {
      item.addEventListener('click', (e) => {
        catNavItems.forEach(i => i.classList.remove('active-cat'));
        item.classList.add('active-cat');
      });
    });
  }

  // ========================================
  // FAQ Accordion
  // ========================================
  window.toggleFaq = function(btn) {
    const item = btn.closest('.faq-item');
    const answer = item.querySelector('.faq-a');
    const isOpen = answer.classList.contains('open');

    // Close all
    document.querySelectorAll('.faq-a').forEach(a => a.classList.remove('open'));
    document.querySelectorAll('.faq-q').forEach(q => q.classList.remove('open'));

    if (!isOpen) {
      answer.classList.add('open');
      btn.classList.add('open');
    }
  };

  // ========================================
  // Contact Form
  // ========================================
  window.handleSubmit = function(e) {
    e.preventDefault();
    const form = document.getElementById('contactForm');
    const successDiv = document.getElementById('formSuccess');
    const submitBtn = document.getElementById('submitBtn');

    if (!form) return;

    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;

    setTimeout(() => {
      form.style.display = 'none';
      if (successDiv) {
        successDiv.style.display = 'block';
        successDiv.style.animation = 'fadeIn 0.4s ease';
      }
    }, 1200);
  };

  // ========================================
  // Smooth Scroll for Anchor Links
  // ========================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const navbarH = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--navbar-h')) || 72;
        const offset = 16;
        const top = target.getBoundingClientRect().top + window.scrollY - navbarH - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  // ========================================
  // Active Nav Link
  // ========================================
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

});

// ========================================
// CSS Keyframes (injected)
// ========================================
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }
`;
document.head.appendChild(style);
