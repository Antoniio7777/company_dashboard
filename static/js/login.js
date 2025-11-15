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
        if(data.success){
            window.location.href = "/home";
        } else {
            document.getElementById("notify").innerText = data.message;
        }
    });
});