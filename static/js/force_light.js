// Force Unfold Admin to always use light mode
// This runs before Alpine.js initializes to prevent any flash of dark mode
(function() {
    // Remove dark class immediately
    document.documentElement.classList.remove('dark');
    
    // Override the Alpine persist storage so theme always reads as 'light'
    try {
        localStorage.setItem('_x_adminTheme', '"light"');
    } catch(e) {}

    // Watch for any mutations that try to add 'dark' class back
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                if (document.documentElement.classList.contains('dark')) {
                    document.documentElement.classList.remove('dark');
                }
            }
        });
    });

    observer.observe(document.documentElement, { attributes: true });
})();
