document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#pwd_rpt').onkeyup = () => {
        // Initialize new request
        const pwd = document.querySelector('#pwd');
        const pwd_rpt = document.querySelector('#pwd_rpt');
        const good_color = "#66cc66";
        const bad_color = "#ff6666";
        if (pwd.value == pwd_rpt.value) {
            pwd_rpt.style.backgroundColor = good_color;

        } else {
            pwd_rpt.style.backgroundColor = bad_color;
        }

    };
    document.querySelector('#form').onsubmit = () => {
        // Initialize new request
        const request = new XMLHttpRequest();
        const user = document.querySelector('#user').value;
        const email = document.querySelector('#email').value;
        const pwd = document.querySelector('#pwd').value;
        const pwd_rpt = document.querySelector('#pwd_rpt').value;
        if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)))
        {
            alert("You have entered an invalid email address, retry!");
            document.querySelector('#email').value = '';
            return false;
        }

        if (pwd != pwd_rpt) {
            alert("Contraseñas no coinciden.")
            document.querySelector('#pwd').value = '';
            document.querySelector('#pwd_rpt').value = '';
            document.querySelector('#pwd_rpt').style.backgroundColor = '#ffffff';
            return false;
        }
        request.open('POST', '/signedup');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const response = JSON.parse(request.responseText);

            // Update the result div
            if (response.success) {
                //On success allowed to change the page
                alert("Perfil creado satisfactoriamentes \n  Usuario: "+user+ "\n  Email: "+email);

                window.location.href = "/";
                return true;
            } else {
                alert("User already in use");
                document.querySelector('#users').value = '';
                return false;
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('user', user);
        data.append('email', email);
        data.append('pwd', pwd);


        // Send request
        request.send(data);
        return false;
    };

});