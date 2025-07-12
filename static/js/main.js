// Skill Swap - Main JavaScript File

// Language translations
const translations = {
    en: {
        'skill-swap': 'Skill Swap',
        'tagline': 'Swap skills. Grow together.',
        'hero-title': 'Connect, Learn, and Grow with Skill Swap',
        'hero-subtitle': 'Join our community of learners and share your skills with others. Learn new abilities while teaching what you know best.',
        'get-started': 'Get Started',
        'learn-more': 'Learn More',
        'login': 'Login',
        'register': 'Register',
        'browse-users': 'Browse Users',
        'dashboard': 'Dashboard',
        'profile': 'Profile',
        'logout': 'Logout',
        'features': 'Features',
        'how-it-works': 'How It Works',
        'testimonials': 'Testimonials',
        'footer-text': '© 2025 Skill Swap Platform. Connect, Learn, Grow Together.',
        'name': 'Name',
        'email': 'Email',
        'password': 'Password',
        'location': 'Location',
        'availability': 'Availability',
        'submit': 'Submit',
        'or': 'or',
        'already-have-account': 'Already have an account?',
        'dont-have-account': 'Don\'t have an account?',
        'sign-up': 'Sign Up',
        'sign-in': 'Sign In'
    },
    hi: {
        'skill-swap': 'स्किल स्वैप',
        'tagline': 'कौशल बदलें। एक साथ बढ़ें।',
        'hero-title': 'स्किल स्वैप के साथ जुड़ें, सीखें और बढ़ें',
        'hero-subtitle': 'हमारे सीखने वाले समुदाय में शामिल हों और दूसरों के साथ अपने कौशल साझा करें। नई क्षमताएं सीखें जबकि आप जो सबसे अच्छा जानते हैं उसे सिखाएं।',
        'get-started': 'शुरू करें',
        'learn-more': 'और जानें',
        'login': 'लॉगिन',
        'register': 'रजिस्टर करें',
        'browse-users': 'उपयोगकर्ता ब्राउज़ करें',
        'dashboard': 'डैशबोर्ड',
        'profile': 'प्रोफ़ाइल',
        'logout': 'लॉगआउट',
        'features': 'विशेषताएं',
        'how-it-works': 'यह कैसे काम करता है',
        'testimonials': 'प्रशंसापत्र',
        'footer-text': '© 2025 स्किल स्वैप प्लेटफॉर्म। जुड़ें, सीखें, एक साथ बढ़ें।',
        'name': 'नाम',
        'email': 'ईमेल',
        'password': 'पासवर्ड',
        'location': 'स्थान',
        'availability': 'उपलब्धता',
        'submit': 'सबमिट करें',
        'or': 'या',
        'already-have-account': 'पहले से खाता है?',
        'dont-have-account': 'खाता नहीं है?',
        'sign-up': 'साइन अप करें',
        'sign-in': 'साइन इन करें'
    },
    gu: {
        'skill-swap': 'સ્કિલ સ્વેપ',
        'tagline': 'કૌશલ્ય બદલો. સાથે વૃદ્ધિ કરો.',
        'hero-title': 'સ્કિલ સ્વેપ સાથે જોડાઓ, શીખો અને વધો',
        'hero-subtitle': 'અમારા શીખનારાઓના સમુદાયમાં જોડાઓ અને અન્ય લોકો સાથે તમારા કૌશલ્ય શેર કરો. નવી ક્ષમતાઓ શીખો જ્યારે તમે જે શ્રેષ્ઠ જાણો છો તે શીખવો.',
        'get-started': 'શરૂ કરો',
        'learn-more': 'વધુ જાણો',
        'login': 'લોગિન',
        'register': 'નોંધણી કરો',
        'browse-users': 'યુઝર્સ બ્રાઉઝ કરો',
        'dashboard': 'ડેશબોર્ડ',
        'profile': 'પ્રોફાઇલ',
        'logout': 'લોગઆઉટ',
        'features': 'લક્ષણો',
        'how-it-works': 'તે કેવી રીતે કામ કરે છે',
        'testimonials': 'પ્રશંસાપત્રો',
        'footer-text': '© 2025 સ્કિલ સ્વેપ પ્લેટફ�ર્મ. જોડાઓ, શીખો, સાથે વૃદ્ધિ કરો.',
        'name': 'નામ',
        'email': 'ઇમેઇલ',
        'password': 'પાસવર્ડ',
        'location': 'સ્થાન',
        'availability': 'ઉપલબ્ધતા',
        'submit': 'સબમિટ કરો',
        'or': 'અથવા',
        'already-have-account': 'પહેલેથી ખાતું છે?',
        'dont-have-account': 'ખાતું નથી?',
        'sign-up': 'સાઇન અપ',
        'sign-in': 'સાઇન ઇન'
    }
};

// Current language
let currentLang = localStorage.getItem('skillswap-language') || 'en';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeLanguage();
    initializeScrollAnimations();
    initializeFormValidation();
    initializeNavbar();
    initializeParticles();
});

// Theme Management
function initializeTheme() {
    const savedTheme = localStorage.getItem('skillswap-theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
        updateThemeIcon();
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('skillswap-theme', newTheme);
    updateThemeIcon();
    
    // Add smooth transition effect
    document.body.style.transition = 'all 0.3s ease';
    setTimeout(() => {
        document.body.style.transition = '';
    }, 300);
}

function updateThemeIcon() {
    const themeToggle = document.querySelector('.theme-toggle i');
    const currentTheme = document.documentElement.getAttribute('data-theme');
    
    if (themeToggle) {
        themeToggle.className = currentTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Language Management
function initializeLanguage() {
    const languageSelect = document.querySelector('.language-selector select');
    if (languageSelect) {
        languageSelect.value = currentLang;
        languageSelect.addEventListener('change', changeLanguage);
    }
    
    updateLanguage();
}

function changeLanguage(event) {
    currentLang = event.target.value;
    localStorage.setItem('skillswap-language', currentLang);
    updateLanguage();
}

function updateLanguage() {
    const elementsToTranslate = document.querySelectorAll('[data-translate]');
    
    elementsToTranslate.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[currentLang] && translations[currentLang][key]) {
            if (element.tagName === 'INPUT' && element.type === 'submit') {
                element.value = translations[currentLang][key];
            } else if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
                element.placeholder = translations[currentLang][key];
            } else {
                element.textContent = translations[currentLang][key];
            }
        }
    });
    
    // Update document title
    if (translations[currentLang]['skill-swap']) {
        document.title = translations[currentLang]['skill-swap'];
    }
}

// Scroll Animations
function initializeScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                    showFieldError(input, 'This field is required');
                } else {
                    input.classList.remove('error');
                    hideFieldError(input);
                }
                
                // Email validation
                if (input.type === 'email' && input.value.trim()) {
                    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailPattern.test(input.value)) {
                        isValid = false;
                        input.classList.add('error');
                        showFieldError(input, 'Please enter a valid email address');
                    }
                }
                
                // Password validation
                if (input.type === 'password' && input.value.trim()) {
                    if (input.value.length < 6) {
                        isValid = false;
                        input.classList.add('error');
                        showFieldError(input, 'Password must be at least 6 characters');
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
            
            input.addEventListener('input', function() {
                if (input.classList.contains('error')) {
                    validateField(input);
                }
            });
        });
    });
}

function validateField(input) {
    const value = input.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // Required field validation
    if (input.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    
    // Email validation
    if (input.type === 'email' && value) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    }
    
    // Password validation
    if (input.type === 'password' && value) {
        if (value.length < 6) {
            isValid = false;
            errorMessage = 'Password must be at least 6 characters';
        }
    }
    
    if (isValid) {
        input.classList.remove('error');
        hideFieldError(input);
    } else {
        input.classList.add('error');
        showFieldError(input, errorMessage);
    }
}

function showFieldError(input, message) {
    hideFieldError(input); // Remove existing error
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.cssText = `
        color: #ef4444;
        font-size: 0.875rem;
        margin-top: 0.25rem;
        opacity: 0;
        transform: translateY(-10px);
        transition: all 0.3s ease;
    `;
    
    input.parentNode.appendChild(errorElement);
    
    // Animate in
    setTimeout(() => {
        errorElement.style.opacity = '1';
        errorElement.style.transform = 'translateY(0)';
    }, 10);
}

function hideFieldError(input) {
    const existingError = input.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

// Navbar Management
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    let lastScrollY = window.scrollY;
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollY = currentScrollY;
    });
}

// Particle Animation (for hero section)
function initializeParticles() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles-container';
    particlesContainer.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        pointer-events: none;
        z-index: 1;
    `;
    
    hero.appendChild(particlesContainer);
    
    // Create particles
    for (let i = 0; i < 50; i++) {
        createParticle(particlesContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    const size = Math.random() * 4 + 2;
    const startX = Math.random() * window.innerWidth;
    const duration = Math.random() * 20 + 10;
    
    particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background: radial-gradient(circle, var(--primary-color), transparent);
        border-radius: 50%;
        left: ${startX}px;
        top: 100%;
        opacity: 0.6;
        animation: floatUp ${duration}s linear infinite;
    `;
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
        // Create new particle
        createParticle(container);
    }, duration * 1000);
}

// Add CSS for particle animation
const style = document.createElement('style');
style.textContent = `
    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0.6;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    .form-control.error {
        border-color: #ef4444;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
    }
`;
document.head.appendChild(style);

// Utility Functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        opacity: 0;
        transform: translateX(100px);
        transition: all 0.3s ease;
    `;
    
    // Set background color based on type
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#3b82f6',
        warning: '#f59e0b'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

function addLoadingState(button) {
    const originalText = button.textContent;
    button.innerHTML = '<span class="loading"></span> Loading...';
    button.disabled = true;
    
    return function removeLoadingState() {
        button.textContent = originalText;
        button.disabled = false;
    };
}

// Export functions for use in other scripts
window.SkillSwap = {
    showNotification,
    addLoadingState,
    updateLanguage,
    toggleTheme
};