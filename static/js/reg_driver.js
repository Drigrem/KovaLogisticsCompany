const openModalButton = document.getElementById('open_modal');
const modal = document.getElementById('reg_modal');
const closeModal = document.getElementById('reg_modal_close')

openModalButton.addEventListener('click', () => {
    reg_modal.style.display = 'block';
    console.log('Хуй');
});

closeModal.addEventListener('click', () => {
    reg_modal.style.display = 'none';
    console.log('пизда');
})