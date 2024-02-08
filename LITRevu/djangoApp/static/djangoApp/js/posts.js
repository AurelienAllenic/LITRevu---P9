function confirmDelete() {
    let deleteButtons = document.querySelectorAll('.btn-danger');

    deleteButtons.forEach(button => {
        button.addEventListener('click', () => {
            let itemId = button.dataset.id;
            let itemType = button.dataset.type;
            let itemName = button.dataset.name;

            console.log('ID de l\'élément à supprimer:', itemId);
            console.log('Type de l\'élément:', itemType);
            console.log('Nom de l\'élément:', itemName);
            
            let modal = document.querySelector('.modal');
            modal.style.display = 'block';
            let questionDelete = document.querySelector('.question-delete');

            if (itemType === 'ticket') {
                questionDelete.textContent = 'Etes-vous sûr de vouloir supprimer ce ticket ?';
            } else {
                questionDelete.textContent = 'Etes-vous sûr de vouloir supprimer cette critique ?';
            }

            let titleDelete = document.querySelector('.title-delete');
            titleDelete.textContent = itemName;

            let validateButton = document.querySelector('.deleteYes');
            validateButton.addEventListener('click', () => {
                console.log(itemType);
                window.location.href = 'delete' + '/' + itemType + '/' + itemId;
            });
        });
    });
}

function handleClose() {
    let returnToPosts = document.querySelectorAll('.deleteNo');
    returnToPosts.forEach(button => {
        button.addEventListener('click', () => {
            let modal = document.getElementById('modal');
            modal.style.display = 'none';
        });
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    confirmDelete();
    handleClose();
});
