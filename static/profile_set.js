document.addEventListener('DOMContentLoaded', () => {

        document.querySelector('#form').onsubmit = () => {

            if (document.querySelector('#edit_btn').textContent.includes("Edit password & e-mail")) {
                let hiddens = document.querySelectorAll('.visible');
                hiddens.forEach(unhidde);

                function unhidde(item) {
                    item.hidden = false;
                    item.disabled = false;
                }

                let disables = document.querySelectorAll('.edit');
                disables.forEach(enable);

                function enable(item) {
                    item.disabled = false;
                }

                document.querySelector('#pwd').value = '';
                document.querySelector('#edit_btn').innerHTML = 'Save';
                return false;
            } else {
                // Initialize new request
                const request = new XMLHttpRequest();
                const user = document.querySelector('#user').value;
                const email = document.querySelector('#email').value;
                const pwd = document.querySelector('#pwd').value;
                const pwd_new = document.querySelector('#pwd_new').value;
                const pwd_rpt = document.querySelector('#pwd_rpt').value;
                //Comprobamos el formato corecto del email
                if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))) {
                    alert("You have entered an invalid email address, retry!");
                    document.querySelector('#email').value = '';
                    return false;
                }
                //Comprobamos que las dos contraseñas coinciden.
                if (pwd_new != pwd_rpt) {
                    alert("Passwords provided do not match.")
                    document.querySelector('#pwd').value = '';
                    document.querySelector('#pwd_new').value = '';
                    document.querySelector('#pwd_rpt').value = '';
                    document.querySelector('#pwd_rpt').style.backgroundColor = '#ffffff';
                    return false;
                }
                request.open('POST', '/update');

                // Callback function for when request completes
                request.onload = () => {

                    // Extract JSON data from request
                    const data = JSON.parse(request.responseText);

                    if (data.success) {
                        //On success allowed to change the page
                        let hiddens = document.querySelectorAll('.visible');
                        hiddens.forEach(unhidde);

                        function unhidde(item) {
                            item.hidden = true;
                            item.disabled = true;
                        }

                        let disables = document.querySelectorAll('.edit');
                        disables.forEach(enable);

                        function enable(item) {
                            item.disabled = true;
                        }


                        alert("Datos actualizados automaticamente. \n  Usuario: " + user + "\n  Email: " + email);
                        document.querySelector('#edit_btn').innerHTML = 'Edit password & e-mail';
                        document.querySelector('#pwd_new').value = '';
                        document.querySelector('#pwd_rpt    ').value = '';
                        document.querySelector('#pwd_rpt').style.backgroundColor = '#ffffff';
                        return false;
                    } else {
                        alert("Wrong current password.");
                        document.querySelector('#pwd').value = '';
                        document.querySelector('#pwd_new').value = '';
                        document.querySelector('#pwd_rpt    ').value = '';
                        document.querySelector('#pwd_rpt').style.backgroundColor = '#ffffff';
                        return false;
                    }
                }

                // Add data to send with request
                const data = new FormData();
                data.append('user', user);
                data.append('pwd', pwd);
                data.append('pwd_new', pwd_new);
                data.append('email', email);

                // Send request
                request.send(data);
                return false;
            }
        };

        document.querySelector('#pwd_rpt').onkeyup = () => {
            // Initialize new request
            const pwd_new = document.querySelector('#pwd_new');
            const pwd_rpt = document.querySelector('#pwd_rpt');
            const good_color = "#66cc66";
            const bad_color = "#ff6666";
            if (pwd_new.value == pwd_rpt.value) {
                pwd_rpt.style.backgroundColor = good_color;

            } else {
                pwd_rpt.style.backgroundColor = bad_color;
            }

        };
    }
);