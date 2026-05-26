document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const nav = document.querySelector('nav');
    const navLinks = document.querySelectorAll('nav a');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            nav.classList.toggle('active');
        });
    }

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (link.classList.contains('user-toggle')) return;
            hamburger.classList.remove('active');
            nav.classList.remove('active');
        });
    });

    document.addEventListener('click', function(event) {
        if (hamburger && nav) {
            if (!hamburger.contains(event.target) && !nav.contains(event.target)) {
                hamburger.classList.remove('active');
                nav.classList.remove('active');
            }
        }
    });

    const userToggle = document.querySelector('.user-toggle');
    const userDropdown = document.querySelector('.user-dropdown');

    if (userToggle && userDropdown) {
        userToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            userDropdown.classList.toggle('active');
        });

        document.addEventListener('click', function(e) {
            if (!userDropdown.contains(e.target)) {
                userDropdown.classList.remove('active');
            }
        });
    }

    // Fetch logged-in user information and dynamically update the page
    fetch('/api/user-info')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                // 1. Update navigation username toggle elements
                const userToggles = document.querySelectorAll('.user-toggle');
                userToggles.forEach(userToggle => {
                    userToggle.innerHTML = `${data.name} &#9662;`;
                });

                // 2. Update My Account profile name elements
                const profileNames = document.querySelectorAll('.profile-name');
                profileNames.forEach(profileName => {
                    profileName.textContent = data.name;
                });

                // 3. Populate first name and last name input fields
                const firstNameInput = document.getElementById('firstName');
                const lastNameInput = document.getElementById('lastName');
                if (firstNameInput || lastNameInput) {
                    const nameParts = data.name.split(' ');
                    if (firstNameInput) {
                        firstNameInput.value = nameParts[0] || '';
                    }
                    if (lastNameInput) {
                        lastNameInput.value = nameParts.slice(1).join(' ') || '';
                    }
                }

                // 4. Populate other input/form fields
                const nameInput = document.getElementById('name');
                if (nameInput) nameInput.value = data.name;

                const orgNameInput = document.getElementById('orgName');
                if (orgNameInput) orgNameInput.value = data.name;

                const businessNameInput = document.getElementById('businessName');
                if (businessNameInput) businessNameInput.value = data.name;

                const emailInput = document.getElementById('email');
                if (emailInput) emailInput.value = data.email;

                const phoneInput = document.getElementById('phone');
                if (phoneInput) phoneInput.value = data.phone;

                const cityInput = document.getElementById('city');
                if (cityInput) cityInput.value = data.city;

                const pincodeInput = document.getElementById('pincode');
                if (pincodeInput) pincodeInput.value = data.pincode;
            }
        })
        .catch(err => console.error('Error fetching user info:', err));
});
