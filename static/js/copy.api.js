function copySerialKey(){
    
    var serialKey = document.getElementById("serial-key");
    // Select the text field
    serialKey.select(); 
    serialKey.setSelectionRange(0, 99999); // For mobile devices

    // Copy the text inside the text field
    navigator.clipboard.writeText(serialKey.value);

    // Alert the copied text
    alert("Serial Key copied, ejoy :) => " + serialKey.value);

}