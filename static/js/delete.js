document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
    const form = document.getElementById('deleteForm');
    const currentPath = window.location.pathname;
    let id;
    let basePath;
    
    // Check if we're on income pages
    if (currentPath.includes('/Income')) {
        if (currentPath.includes('edit-income')) {
            id = currentPath.split('/').pop();
        } else {
            const deleteButton = document.querySelector('[data-bs-target="#deleteModal"]');
            id = deleteButton.dataset.incomeId;
        }
        basePath = '/Income/income-delete/';
    } else {
        // Handle expense pages
        if (currentPath.includes('edit-expense')) {
            id = currentPath.split('/').pop();
        } else {
            const deleteButton = document.querySelector('[data-bs-target="#deleteModal"]');
            id = deleteButton.dataset.expenseId;
        }
        basePath = '/expense-delete/';
    }
    
    form.action = `${basePath}${id}`;
    form.submit();
});
