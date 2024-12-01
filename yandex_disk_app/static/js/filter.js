function applyFilter() {
    const type = document.getElementById('filter-type').value;
    const params = new URLSearchParams(window.location.search);
    if (type) {
        params.set('type', type);
    } else {
        params.delete('type');
    }
    window.location.search = params.toString();
}