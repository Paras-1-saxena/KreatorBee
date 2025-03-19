// Sidebar Toggler on Mobile

const sidebar = document.querySelector('.sidebar');
const hamburger = document.querySelector('.hamburger');
const backdrop = document.querySelector('.backdrop');

hamburger.addEventListener('click', () => {
     sidebar.classList.add('d-block');
     sidebar.classList.remove('d-none');
     backdrop.classList.add('d-block');
     backdrop.classList.remove('d-none');
});

backdrop.addEventListener('click', () => {
    sidebar.classList.add('d-none');
    sidebar.classList.remove('d-block');
    backdrop.classList.add('d-none');
    backdrop.classList.remove('d-block');
});