document.getElementById("change-password-form").addEventListener("submit", function(e){
    e.preventDefault();

    const old_password = document.getElementById("old_password").value;
    const new_password = document.getElementById("new_password").value;

    fetch('/api/change_password', {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCsrfToken()},
        body: JSON.stringify({old_password: old_password, new_password: new_password})
    })
    .then(res => res.json())
    .then(data => {
        const notify = document.getElementById("notify");
        if(data.success){
            window.location.href = "/home";
        } else {
            notify.innerText = data.message;
        }
    })
                    .catch(error =>
                {
                    notify.innerText = "Server error";
                });
});