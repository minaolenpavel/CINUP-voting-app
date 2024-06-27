function msgDisappears(){
    var messageLists = document.getElementsByClassName("messageList");
    for (var i = 0; i < messageLists.length; i++) {
        messageLists[i].style.display = 'none';
    }
}
setTimeout(msgDisappears, 3000);