
function signupNavigation() {
    let signup = document.getElementById('signup');
    signup.addEventListener('click', () => {
        window.location.href = "/signup";
    })
}

document.addEventListener('DOMContentLoaded', (event) => {
    signupNavigation();
});