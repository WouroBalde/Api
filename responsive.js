// Détection du device
function initResponsive() {
    const isMobile = window.matchMedia("(max-width: 767px)").matches;
    
    if (isMobile) {
        // Optimisations pour mobile
        document.body.classList.add('mobile');
        initTouchEvents();
    } else {
        // Optimisations pour desktop
        document.body.classList.add('desktop');
    }
}

// Chargement différé des ressources
window.addEventListener('load', initResponsive);