document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form_new_pass').onsubmit = () => {
        // Initialize new request
        const pwd_new = document.querySelector('#pwd_new').value;
        const pwd_rpt = document.querySelector('#pwd_rpt').value;
        if (pwd_new != pwd_rpt) {
            alert('Password provided mismatch.');
            document.querySelector('#pwd_new').value = '';
            document.querySelector('#pwd_rpt').value = '';
            document.querySelector('#pwd_rpt').style.backgroundColor = '#ffffff';
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

});