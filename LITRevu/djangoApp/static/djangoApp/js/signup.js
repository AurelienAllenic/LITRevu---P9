function handleClose(){
    let cross = document.getElementById('returnHome');
    cross.addEventListener('click', () => {
        window.location.href = "/";
    })
}
document.addEventListener('DOMContentLoaded', (event) => {
    handleClose();
});