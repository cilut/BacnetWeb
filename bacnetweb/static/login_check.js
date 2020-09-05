document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        const user = document.querySelector('#user').value;
        const pwd = document.querySelector('#pwd').value;
        request.open('POST', '/login');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const response = JSON.parse(request.responseText);

            // Update the result div
            if (response.success) {
                //On success allowed to change the page
                window.location.href = "profile";
                return true;
            } else {
                alert("Datos erroneos, prueba de nuevo.");
                document.querySelector('#user').value = '';
                document.querySelector('#pwd').value = '';
                return false;
            }
        };

        // Add data to send with request
        const data = new FormData();
        data.append('user', user);
        data.append('pwd', pwd);

        // Send request
        request.send(data);
        return false;
    };

});