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
    })
                    .catch(error =>
                {
                    notify.innerText = "Server error";
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
                        <span class="fw-bold text-truncate" title="${user.username}">${user.username}</span>
                        <div class="d-flex align-items-center gap-2 flex-shrink-0">
                            <select class="form-select form-select-sm" style="width: 120px;" data-user-id="${user.id}">
                                <option value="user" ${user.role === 'user' ? 'selected' : ''}>User</option>
                                <option value="manager" ${user.role === 'manager' ? 'selected' : ''}>Manager</option>
                                <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Admin</option>
                            </select>
                            <button class="btn btn-sm btn-outline-success confirm-role-btn" title="Confirm Role Change" data-user-id="${user.id}"><i class="bi bi-check-lg"></i></button>
                            <button class="btn btn-sm btn-outline-secondary reset-password-btn" title="Reset Password" data-user-id="${user.id}"><i class="bi bi-key-fill"></i></button>
                            <button class="btn btn-sm btn-outline-danger delete-user-btn" title="Delete User" data-user-id="${user.id}"><i class="bi bi-trash-fill"></i></button>
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
            userList.innerHTML = '<li class="list-group-item text-danger">Server error</li>';
        });
    }

    loadUsers();

    document.getElementById("user-list").addEventListener('click', function(e) {
        const roleBtn = e.target.closest(".confirm-role-btn");
        const deleteBtn = e.target.closest(".delete-user-btn");
        const passwordBtn = e.target.closest(".reset-password-btn");

        if (roleBtn) {
            const userId = roleBtn.getAttribute("data-user-id");
            const newRole = document.querySelector(`select[data-user-id="${userId}"]`).value;

                        if (!confirm("Are you sure you want to change this user role?")) return;

            fetch(`/api/users/${userId}/role`, {
                method: "PATCH",
                headers: {"Content-Type": "application/json", "X-CSRFToken": getCsrfToken()},
                body: JSON.stringify({role: newRole})
            })
                .then(res => res.json())
                .then(data =>{
                    const notifyList = document.getElementById("list-notify");
                    if(data.success){
                        notifyList.classList.add("text-success");
                        notifyList.innerText = data.message;
                    }
                    else{
                        notifyList.classList.add("text-danger");
                        notifyList.innerText = data.message;
                    }
                })
                .catch(error =>
                {
                    notifyList.innerText = "Server error";
                });
        }

        if (passwordBtn) {
            const userId = passwordBtn.getAttribute("data-user-id");

            if (!confirm("Are you sure you want to reset this user password?")) return;

            fetch(`/api/users/${userId}/reset_password`, {
                method: "PATCH",
                headers: {"Content-Type": "application/json", "X-CSRFToken": getCsrfToken()},
            })
                .then(res => res.json())
                .then(data =>{
                    const notifyList = document.getElementById("list-notify");
                    if(data.success){
                        document.getElementById('new-password-display').classList.remove('d-none');
                        document.getElementById("new-pass").innerText=data.password;
                    }
                    else{
                        notifyList.classList.add("text-danger");
                        notifyList.innerText = data.message;
                    }
                })
                .catch(error =>
                {
                    notifyList.innerText = "Server error";
                });
        }

        if (deleteBtn) {
            const userId = deleteBtn.getAttribute("data-user-id");

            if (!confirm("Are you sure you want to delete this user?")) return;

            fetch(`/api/users/${userId}/delete`, {
                method: "DELETE",
                headers: {"Content-Type": "application/json", "X-CSRFToken": getCsrfToken()},
            })
                .then(res => res.json())
                .then(data =>{
                    const notifyList = document.getElementById("list-notify");
                    if(data.success){
                        notifyList.classList.add("text-success");
                        notifyList.innerText = data.message;
                        loadUsers();
                    }
                    else{
                        notifyList.classList.add("text-danger");
                        notifyList.innerText = data.message;
                    }
                })
                .catch(error =>
                {
                    notifyList.innerText = "Server error";
                });
        }

    });

        const copyButton = document.getElementById('copy-pass-link');
        copyButton.addEventListener('click', function(e) {
    const password = document.getElementById('new-pass').innerText;
    navigator.clipboard.writeText(password)
        .then(() => {
            copyButton.innerText="Copied!"
        });
});