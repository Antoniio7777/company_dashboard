document.getElementById("create-form").addEventListener("submit", function(e){
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const role = document.getElementById("role").value.trim();

    fetch("/api/adduser", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCsrfToken()},
        body: JSON.stringify({username: username, password: password, role: role})
    })
    .then(res => res.json())
    .then(data => {
        const notify = document.getElementById("notify");
        notify.classList.remove("text-success", "text-danger");
        if(data.success) {
            notify.classList.add("text-success");
            loadUsers();
        }
        else {
            notify.classList.add("text-danger");
        }
        notify.innerText = data.message;
    });
});

    const userList = document.getElementById('user-list');
    const createForm = document.getElementById('create-form');
    const notifyDiv = document.getElementById('notify');

    function loadUsers() {

        fetch('/api/users', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(res => res.json())
        .then(data => {
            userList.innerHTML = '';

            if (data.success && data.users.length > 0) {
                data.users.forEach(user => {
                    const userElement = document.createElement('li');
                    userElement.className = 'list-group-item d-flex justify-content-between align-items-center gap-3';

                    userElement.innerHTML = `
                        <span class="fw-bold text-truncate" title="id">ID: ${user.id}</span>
                        <span class="fw-bold text-truncate" title="${user.user}">${user.user}</span>
                        <div class="d-flex align-items-center gap-2 flex-shrink-0">
                            <select class="form-select form-select-sm" style="width: 120px;" data-user-id="${user.id}">
                                <option value="user" ${user.role === 'user' ? 'selected' : ''}>User</option>
                                <option value="manager" ${user.role === 'manager' ? 'selected' : ''}>Manager</option>
                                <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Admin</option>
                            </select>
                            <button class="btn btn-sm btn-outline-success confirm-role-btn" title="Confirm Role Change" data-user-id="${user.id}"><i class="bi bi-check-lg"></i></button>
                            <button class="btn btn-sm btn-outline-secondary reset-password-btn" title="Reset Password" data-user-id="${user.id}"><i class="bi bi-key-fill"></i></button>
                            <button class="btn btn-sm btn-outline-danger" title="Delete User" data-user-id="${user.id}"><i class="bi bi-trash-fill"></i></button>
                        </div>
                    `;
                    userList.appendChild(userElement);
                });
            } else if (data.success && data.users.length === 0) {
                userList.innerHTML = '<li class="list-group-item text-muted">No users found.</li>';
            } else {
                userList.innerHTML = `<li class="list-group-item text-danger">Error: ${data.message}</li>`;
            }
        })
        .catch(error => {
            console.error('Error loading users:', error);
            userList.innerHTML = '<li class="list-group-item text-danger">Could not connect to the server.</li>';
        });
    }
    loadUsers();