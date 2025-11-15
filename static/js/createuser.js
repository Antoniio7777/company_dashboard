document.getElementById("create-form").addEventListener("submit", function(e){
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const canModify = document.getElementById("canModify").checked;
    const isAdmin = document.getElementById("isAdmin").checked;



    fetch("/api/adduser", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": getCsrfToken()},
        body: JSON.stringify({user: username, password: password, canModify: canModify, admin: isAdmin})
    })
    .then(res => res.json())
    .then(data => {
        const notify = document.getElementById("notify");
        notify.classList.remove("text-success", "text-danger");
        if(data.success) {
            notify.classList.add("text-success");
        }
        else {
            notify.classList.add("text-danger");
        }
            notify.innerText = data.message;
    })

});