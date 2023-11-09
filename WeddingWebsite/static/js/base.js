const hamburger = document.querySelector(".hamburger");

const navbar = document.querySelector("nav");

const burger_top = document.querySelector(".burger_top")
const burger_middle = document.querySelector(".burger_middle")
const burger_bottom = document.querySelector(".burger_bottom")

hamburger.addEventListener("click", () => {
    burger_top.classList.toggle("x-out_burger_top");
    burger_middle.classList.toggle("x-out_burger_middle");
    burger_bottom.classList.toggle("x-out_burger_bottom");
    navbar.classList.toggle("visible");
});