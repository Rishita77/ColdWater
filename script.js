function showHome() {
    hideAllPages();
    document.getElementById('landing-page').classList.remove('hidden');
}

function showAbout() {
    hideAllPages();
    document.getElementById('about-page').classList.remove('hidden');
}

function showContact() {
    hideAllPages();
    document.getElementById('contact-page').classList.remove('hidden');
}

function showLogin() {
    hideAllPages();
    document.getElementById('login-page').classList.remove('hidden');
}

function showSignup() {
    hideAllPages();
    document.getElementById('signup-page').classList.remove('hidden');
}

function showDashboard() {
    hideAllPages();
    document.getElementById('dashboard-page').classList.remove('hidden');
}

function hideAllPages() {
    document.getElementById('landing-page').classList.add('hidden');
    document.getElementById('about').classList.add('hidden');
    document.getElementById('contact').classList.add('hidden');
    document.getElementById('login-page').classList.add('hidden');
    document.getElementById('signup-page').classList.add('hidden');
    document.getElementById('dashboard-page').classList.add('hidden');
}

document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Signup successful! Redirecting to dashboard...');
    showDashboard();
});

document.querySelector('#login-page button').addEventListener('click', function() {
    alert('Login successful! Redirecting to dashboard...');
    showDashboard();
});
