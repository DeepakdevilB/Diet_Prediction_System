document.addEventListener('DOMContentLoaded', function () {
    const accordions = document.querySelectorAll('.accordion-header');

    accordions.forEach(acc => {
        acc.addEventListener('click', function () {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            content.classList.toggle('active');

            const arrow = this.querySelector('.arrow');
            if (content.classList.contains('active')) {
                arrow.textContent = '▲';
            } else {
                arrow.textContent = '▼';
            }
        });
    });
});
