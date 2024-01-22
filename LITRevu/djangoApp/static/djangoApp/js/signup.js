function handleClose(){
    let cross = document.querySelector('.cross');
    cross.addEventListener('click', () => {
        window.location.href = "/";
    })
}
document.addEventListener('DOMContentLoaded', (event) => {
    handleClose();
});