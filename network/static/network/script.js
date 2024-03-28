const post_textarea = document.querySelector("#post_textarea");

function adjustTextareaHeight() {
    const input = post_textarea.value;
    const numRows = countRows(input);
    if (numRows < 10) {
        post_textarea.rows = numRows + 1;
    }
}

function countRows(text) {
    // Split the text by newline characters and count the number of elements in the array
    return (text.match(/\n/g) || []).length + 1;
}

post_textarea.addEventListener('input', adjustTextareaHeight);

adjustTextareaHeight();