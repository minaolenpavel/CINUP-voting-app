document.addEventListener('DOMContentLoaded', function() {
    var usernameElement = document.getElementById("username");
    var menu = document.getElementById("userMenu");

    function toggleMenu() {
        menu.style.display = menu.style.display === "block"? "none" : "block";
    }

    usernameElement.addEventListener('click', toggleMenu);

    // Hide the menu when clicking outside of it
    document.addEventListener('click', function(event) {
        var isClickInside = usernameElement.contains(event.target) || menu.contains(event.target);
        if (!isClickInside) {
            menu.style.display = "none";
        }
    });
});