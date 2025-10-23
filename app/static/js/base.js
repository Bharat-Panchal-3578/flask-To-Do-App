document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logout-btn');
    const accessToken = localStorage.getItem('access_token');

    // Show logout button if user is logged in
    if (accessToken) {
        logoutBtn.style.display = 'inline';
    } else {
        logoutBtn.style.display = 'none';
    }

    // Logout functionality
    logoutBtn.addEventListener('click', async () => {
        const refreshToken = localStorage.getItem('refresh_token');

        if (!refreshToken) {
            window.location.href = '/login';
            return;
        }

        try {
            const response = await fetch('/api/logout', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${refreshToken}`
                },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            const data = await response.json();

            if (data.status === 'success') {
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                window.location.href = '/login';
            } else {
                console.error(data.message || "Failed to log out.");
            }
        } catch (error) {
            console.error(error);
        }
    });
});
