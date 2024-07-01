function copyToClipboard() {
    const keyElement = document.getElementById('accessKey');
    const key = keyElement.innerText;
    navigator.clipboard.writeText(key).then(function() {
        alert('Clé copiée!');
    }, function(err) {
        alert('Erreur lors de la copie: ' + err);
    });
}
