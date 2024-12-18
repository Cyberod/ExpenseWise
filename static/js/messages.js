
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.getElementById('messages');
    const closeBtn = messages.getElementsByClassName('close-btn');


    if (messages) {
        setTimeout(function() {
            const alerts = messages.getElementsByClassName('alert');
            Array.from(alerts).forEach(function(alert) {
                alert.style.transition = 'opacity 1s';
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 1000);
            });
        }, 10000);

        Array.from(closeBtn).forEach(function(btn) {
            btn.addEventListener('click', function() {
                const alert = btn.closest('.alert');
                alert.style.transition = 'opacity 1s';
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 1000);
            });
        });
    }
});
