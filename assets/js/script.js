"use strict";

// element toggle function
const elementToggleFunc = function (elem) {
  elem.classList.toggle("active");
};

// sidebar variables
const sidebar = document.querySelector("[data-sidebar]");
const sidebarBtn = document.querySelector("[data-sidebar-btn]");

// sidebar toggle functionality for mobile
sidebarBtn.addEventListener("click", function () {
  elementToggleFunc(sidebar);
});

// mobile sidebar clicked by default
sidebarBtn.click();

// Generic continuous auto-scroll for horizontal marquee-style lists
function setupAutoScroll(listSelector, scrollSpeed) {
  const list = document.querySelector(listSelector);
  if (!list) return;

  const intervalDuration = 10; // smoothness
  let scrollPosition = list.scrollLeft;
  let scrolling = false;
  let interval = null;

  function getTotalWidth() {
    return list.scrollWidth - list.clientWidth;
  }

  function startScrolling() {
    if (scrolling) return;
    scrolling = true;
    interval = setInterval(() => {
      const totalWidth = getTotalWidth();
      if (totalWidth <= 0) return;

      scrollPosition += scrollSpeed;

      if (scrollPosition >= totalWidth) {
        scrollPosition = 0;
      }

      if (!scrolling) {
        clearInterval(interval);
        return;
      }

      list.scrollLeft = scrollPosition;
    }, intervalDuration);
  }

  function stopScrolling() {
    scrolling = false;
    if (interval) {
      clearInterval(interval);
      interval = null;
    }
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          startScrolling();
        } else {
          stopScrolling();
        }
      });
    },
    { threshold: 0 }
  );

  observer.observe(list);

  list.addEventListener("mouseenter", () => {
    stopScrolling();
  });

  list.addEventListener("mouseleave", () => {
    scrollPosition = list.scrollLeft;
    startScrolling();
  });

  // Keep our tracked position in sync if the user manually scrolls (touch, etc.)
  list.addEventListener("touchstart", () => {
    stopScrolling();
  });

  list.addEventListener("touchend", () => {
    scrollPosition = list.scrollLeft;
    startScrolling();
  });
}

// auto scrolling Tech Skills (Development Skills row)
setupAutoScroll(".technologies-list", 0.7);

// auto scrolling Technical Expertise cards
setupAutoScroll(".expertise-cards", 0.5);

// variables
const testimonialsItem = document.querySelectorAll("[data-testimonials-item]");
const modalContainer = document.querySelector("[data-modal-container]");
const modalCloseBtn = document.querySelector("[data-modal-close-btn]");
const overlay = document.querySelector("[data-overlay]");
const modalImg = document.querySelector("[data-modal-img]");
const modalTitle = document.querySelector("[data-modal-title]");
const modalText = document.querySelector("[data-modal-text]");

// modal toggle function
const testimonialsModalFunc = function () {
  modalContainer.classList.toggle("active");
  overlay.classList.toggle("active");
};

// add click event to all modal items
for (let i = 0; i < testimonialsItem.length; i++) {
  testimonialsItem[i].addEventListener("click", function () {
    modalImg.src = this.querySelector("[data-testimonials-avatar]").src;
    modalImg.alt = this.querySelector("[data-testimonials-avatar]").alt;
    modalTitle.innerHTML = this.querySelector(
      "[data-testimonials-title]"
    ).innerHTML;
    modalText.innerHTML = this.querySelector(
      "[data-testimonials-text]"
    ).innerHTML;

    testimonialsModalFunc();
  });
}

// add click event to modal close button
modalCloseBtn.addEventListener("click", testimonialsModalFunc);
overlay.addEventListener("click", testimonialsModalFunc);

// custom select variables
const select = document.querySelector("[data-select]");
const selectItems = document.querySelectorAll("[data-select-item]");
const selectValue = document.querySelector("[data-selecct-value]");
const filterBtn = document.querySelectorAll("[data-filter-btn]");

select.addEventListener("click", function () {
  elementToggleFunc(this);
});

// add event in all select items
for (let i = 0; i < selectItems.length; i++) {
  selectItems[i].addEventListener("click", function () {
    let selectedValue = this.innerText.toLowerCase();
    selectValue.innerText = this.innerText;
    elementToggleFunc(select);
    filterFunc(selectedValue);
  });
}

// filter variables
const filterItems = document.querySelectorAll("[data-filter-item]");

const filterFunc = function (selectedValue) {
  filterItems.forEach((item) => {
    const categories = item.dataset.category.split(" ");
    if (selectedValue === "all" || categories.includes(selectedValue)) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });
};

// add event in all filter button items for large screen
let lastClickedBtn = filterBtn[0];

for (let i = 0; i < filterBtn.length; i++) {
  filterBtn[i].addEventListener("click", function () {
    let selectedValue = this.innerText.toLowerCase();
    selectValue.innerText = this.innerText;
    filterFunc(selectedValue);

    lastClickedBtn.classList.remove("active");
    this.classList.add("active");
    lastClickedBtn = this;
  });
}

// contact form variables
const form = document.querySelector("[data-form]");
const formInputs = document.querySelectorAll("[data-form-input]");
const formBtn = document.querySelector("[data-form-btn]");

// add event to all form input field
for (let i = 0; i < formInputs.length; i++) {
  formInputs[i].addEventListener("input", function () {
    // check form validation
    if (form.checkValidity()) {
      formBtn.removeAttribute("disabled");
    } else {
      formBtn.setAttribute("disabled", "");
    }
  });
}

// Page navigation variables
const navigationLinks = document.querySelectorAll("[data-nav-link]");
const pages = document.querySelectorAll("[data-page]");

// Helper function to update active states
function updateActiveState(targetSection) {
  pages.forEach((page) => {
    page.classList.toggle("active", page.dataset.page === targetSection);
  });

  navigationLinks.forEach((link) => {
    const linkTarget =
      link.getAttribute("data-target-section") ||
      link.textContent.trim().toLowerCase();
    link.classList.toggle("active", linkTarget === targetSection);
  });

  // Scroll to the top when navigation occurs
  window.scrollTo(0, 0);
}

// Event listener for navigation links
navigationLinks.forEach((link) => {
  link.addEventListener("click", () => {
    const targetSection =
      link.getAttribute("data-target-section") ||
      link.textContent.trim().toLowerCase();
    updateActiveState(targetSection);
  });
});

// open certificates on click
function imgWindow() {
  window.open("image");
}

// copy email address
function copyEmail(e) {
  var email = document.querySelector(".email-text");
  var range = document.createRange();
  range.selectNode(email);
  window.getSelection().addRange(range);
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  e.target.innerText = "Copied";
  setTimeout(() => {
    e.target.innerText = "Copy";
  }, 300);
}

// Animated percentage bar
function increaseProgress(element, targetWidth) {
  var currentWidth = 0;
  var increment = 1;
  var interval = 10;

  var timer = setInterval(function () {
    currentWidth += increment;
    element.style.width = currentWidth + "%";
    if (currentWidth >= targetWidth) {
      clearInterval(timer);
    }
  }, interval);
}

function startAnimationOnScroll() {
  var progressFillElements = document.querySelectorAll(
    ".languages-progress-fill"
  );

  var options = {
    root: null,
    rootMargin: "0px",
    threshold: 0.5,
  };

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        var targetWidth = parseInt(entry.target.style.width);
        increaseProgress(entry.target, targetWidth);
        observer.unobserve(entry.target);
      }
    });
  }, options);

  progressFillElements.forEach(function (element) {
    observer.observe(element);
  });
}

startAnimationOnScroll();

// Loading Animation
window.addEventListener("DOMContentLoaded", (event) => {
  const imageContainers = document.querySelectorAll(".project-img");
  imageContainers.forEach((container) => {
    const image = container.querySelector("img");
    image.addEventListener("load", function () {
      container.classList.remove("loading");
    });
  });
});

// Age Counter Animation
function calculateAge(birthDate) {
  const birth = new Date(birthDate);
  const today = new Date();
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();

  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
    age--;
  }

  return age;
}

document.getElementById("age").textContent = `${calculateAge(
  "2006-12-24"
)} years old`;

// Motto Animation
const text = Array.from({ length: 20 }, () =>
  Array.from({ length: 16 }, () => Math.round(Math.random())).join("")
);
text.push("Hello, World !");

const mottoElement = document.getElementById("motto");
let index = 0;

function flipmotto() {
  mottoElement.textContent = text[index];

  if (text[index] === "Hello, World !") {
    clearInterval(intervalId);
  }

  index = (index + 1) % text.length;
}

const intervalId = setInterval(flipmotto, 100);

// Expanding About Text
function toggleText() {
  var moreText = document.getElementById("more");
  var btnText = document.getElementById("toggle-button");

  if (moreText.style.display === "none") {
    moreText.style.display = "block";
    btnText.innerHTML = "&uarr; &nbsp; &nbsp; Hide text &nbsp; &nbsp; &uarr;";
  } else {
    moreText.style.display = "none";
    btnText.innerHTML = "&darr; &nbsp; &nbsp; Show more &nbsp; &nbsp; &darr;";
  }
}

// Turn image alt text into title

document.addEventListener("DOMContentLoaded", function () {
  const items = document.querySelectorAll(".technologies-item");

  items.forEach((item) => {
    const image = item.querySelector("img");
    const titleText = image.alt;
    const titleDiv = document.createElement("div");
    titleDiv.className = "image-title";
    titleDiv.textContent = titleText;
    item.appendChild(titleDiv);
  });
});

// Lazy Loading on scroll for Projects

document.addEventListener("DOMContentLoaded", function () {
  let projectItems = document.querySelectorAll(".project-item");

  let observer = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          let img = entry.target.querySelector("img");
          img.src = img.getAttribute("data-src");
          img.classList.remove("loading");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  projectItems.forEach((item) => {
    observer.observe(item);
  });
});

// Universal click/tap "press" animation — works reliably for both mouse
// clicks and touch taps (plain CSS :active is unreliable on many mobile
// browsers, especially iOS Safari, unless a touch listener is bound).
document.addEventListener("DOMContentLoaded", function () {
  const pressableSelectors = [
    ".navbar-link",
    ".filter-item button",
    ".filter-select",
    ".select-item button",
    ".pagination-button",
    ".social-item .social-link",
    ".copy-button",
    ".form-btn",
    ".info_more-btn",
    ".expertise-nav-btn",
    ".more",
    ".modal-close-btn",
    ".project-buttons a",
    ".certificate-container",
  ].join(", ");

  const pressableEls = document.querySelectorAll(pressableSelectors);

  pressableEls.forEach((el) => {
    el.style.cursor = "pointer";

    const press = () => el.classList.add("btn-press");
    const release = () => el.classList.remove("btn-press");

    // Pointer events cover mouse, touch, and pen uniformly.
    el.addEventListener("pointerdown", press);
    el.addEventListener("pointerup", release);
    el.addEventListener("pointerleave", release);
    el.addEventListener("pointercancel", release);

    // Fallback for browsers without full Pointer Events support.
    el.addEventListener("touchstart", press, { passive: true });
    el.addEventListener("touchend", release);
    el.addEventListener("touchcancel", release);
    el.addEventListener("mousedown", press);
    el.addEventListener("mouseup", release);
  });
});

// Enables :active / :hover states to register reliably on iOS Safari,
// which otherwise ignores them unless a touch listener exists on the page.
document.addEventListener("touchstart", function () {}, { passive: true });
