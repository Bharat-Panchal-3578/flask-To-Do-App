const login_form = document.getElementById('login-form');
const message = document.getElementById('login-message');
const access_token = localStorage.getItem('access_token');

if (access_token) {
    window.location.href = '/dashboard/tasks';
}

if (login_form) {
    login_form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        const response = await fetch('/api/login',{method: 'POST',headers: {'Content-Type': 'application/json'}, body: JSON.stringify({username,password}) });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            localStorage.setItem('access_token',data.data.access_token);
            localStorage.setItem('refresh_token',data.data.refresh_token);
            window.location.href = '/dashboard/tasks';
        } else {
            message.textContent = data.message || "Login failed, try again.";
            message.style.color = 'red';
        }

        setTimeout(() => {
            message.textContent = '';
        },3000);
    });
}