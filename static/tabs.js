document.addEventListener('DOMContentLoaded', function () {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    function activateTab(btn) {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(tc => tc.classList.remove('active'));
        btn.classList.add('active');
        const targetId = btn.dataset.tab;
        if (targetId) {
            const el = document.getElementById(targetId);
            if (el) el.classList.add('active');
        }
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            // If data-tab is present, treat as an in-page tab and prevent navigation
            if (btn.dataset.tab) {
                e.preventDefault();
                activateTab(btn);
            }
            // Otherwise allow the normal navigation (external page)
        });
    });

    // Activate a tab based on URL hash (e.g., #tab-produtos) if present
    if (window.location.hash) {
        const hash = window.location.hash.replace('#', '');
        const btn = document.querySelector(`.tab-btn[data-tab="${hash}"]`);
        if (btn) activateTab(btn);
    }

    // If no tab content is active, activate the first internal tab
    if (!document.querySelector('.tab-content.active')) {
        const first = document.querySelector('.tab-btn[data-tab]');
        if (first) activateTab(first);
    }
});
