document.getElementById("login-form").addEventListener("submit", function(e){
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch('/api/checklogin', {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCsrfToken()},
        body: JSON.stringify({username: username, password: password})
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
        .catch(error => {
            notify.innerText = "Server error";
        });
});