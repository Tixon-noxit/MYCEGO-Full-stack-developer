document.getElementById('download-selected').addEventListener('click', function () {
    const button = document.getElementById('download-selected');
    button.classList.add('uk-hidden');
    setTimeout(() => {
        button.classList.remove('uk-hidden');
    }, 5000);

    const selectedFiles = Array.from(document.querySelectorAll('input[name="selected_files"]:checked'))
        .map(checkbox => checkbox.value);

    if (selectedFiles.length === 0) {
        const modal = UIkit.modal("#modal-example");
        modal.show();
        return;
    }

    selectedFiles.forEach((file, index) => {
        setTimeout(() => {
            const a = document.createElement('a');
            a.href = file;
            a.target = '_blank';
            a.download = '';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }, 3000 * index);
    });
});