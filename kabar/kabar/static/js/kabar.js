function changeLanguage(targetId) {
  const buttons = document.querySelectorAll(".language-select-button");
  buttons.forEach((button) => {
    button.classList.remove("active-language");
  });
  const activeButton = document.getElementById(targetId);
  activeButton.classList.add("active-language");
}

document.addEventListener("DOMContentLoaded", function () {
  const slides = document.querySelectorAll(".article-image-slides");
  const slider = document.getElementById("page-article-slider-image-block");
  const prevButton = document.getElementById("article-slider-prev");
  const nextButton = document.getElementById("article-slider-next");

  if (slides && slider && prevButton && nextButton) {
    let index = 0;

    function showSlide(index) {
      const width = slides[index].clientWidth;
      slider.style.transform = `translateX(-${index * width}px)`;
      updateButtons();
    }

    function nextSlide() {
      if (index < slides.length - 1) {
        index++;
        showSlide(index);
      }
    }

    function prevSlide() {
      if (index > 0) {
        index--;
        showSlide(index);
      }
    }

    function updateButtons() {
      prevButton.disabled = index === 0;
      nextButton.disabled = index === slides.length - 1;
    }

    if (nextButton && prevButton) {
      nextButton.addEventListener("click", nextSlide);
      prevButton.addEventListener("click", prevSlide);
    }

    showSlide(index);
  }
});

const form = document.getElementById("survey-form");
if (form) {
  function submitForm(event) {
    event.preventDefault();
    const formBlock = document.getElementsByClassName(
      "survey-options-block"
    )[0];
    const submitButton = document.getElementById("submit-button");
    submitButton.innerHTML = "Отправлено";
    submitButton.style.background = "#8F9398";
    submitButton.style.cursor = "auto";
    submitButton.disabled = true;
    formBlock.classList.add("active");

    const percentages = document.getElementsByClassName("option-percentage");

    for (let i = 0; i < percentages.length; i++) {
      percentages[i].style.display = "block";
    }

    const radioButtons = document.getElementsByClassName("radio-survey");
    for (let i = 0; i < radioButtons.length; i++) {
      if (!radioButtons[i].checked) {
        radioButtons[i].style.display = "none";
        radioButtons[i].setAttribute("disabled", "");
      }
    }

    const labels = document.querySelectorAll(".survey-options label");

    labels.forEach((label) => {
      const percentage = label.getAttribute("data-percentage");
      label.style.setProperty("--target-width", percentage);
    });

    const radios = document.querySelectorAll(".radio-survey");

    radios.forEach((radio) => {
      radio.addEventListener("change", function () {
        labels.forEach((label) => {
          if (radio.id === label.getAttribute("for")) {
            label.classList.add("active");
          } else {
            label.classList.remove("active");
          }
        });
      });
    });
  }

  form.addEventListener("submit", submitForm);
}

const items = [
  { id: 1, text: "Январь" },
  { id: 2, text: "Февраль" },
  { id: 3, text: "Март" },
  { id: 4, text: "Апрель" },
  { id: 5, text: "Май" },
  { id: 6, text: "Июнь" },
  { id: 7, text: "Июль" },
  { id: 8, text: "Август" },
  { id: 9, text: "Сентябрь" },
  { id: 10, text: "Октябрь" },
  { id: 11, text: "Ноябрь" },
  { id: 12, text: "Декабрь" },
];

const years = Array.from(
  { length: new Date().getFullYear() - 2000 + 1 },
  (v, i) => ({
    id: i + 2000,
    text: (i + 2000).toString(),
  })
).reverse();

const days = Array.from({ length: 30 }, (v, i) => ({
  id: i + 1,
  text: (i + 1).toString(),
}));

const createSelect = (items, createParams) => {
  const {
    mainId = "customSelect",
    inputId = "input",
    optionsId = "options",
    popupId = "popup",
    selectedId = null,
    defaultText = "Choose",
    cssFontSize = "1em",
    cssArrowColor = "#1F334E",
    cssOptionsBackground = "#eee",
    cssDisabledColor = "#ccc",
    cssSelectedBackground = "linear-gradient(-30deg, rgba(128, 80, 50, 0.3), rgba(80, 50, 150, 0.5))",
    cssSelectedColor = "#000",
    cssHoverBackground = "#fff",
    cssHoverColor = "#000",
  } = createParams || {};
  const root = document.createElement("div");
  root.classList.add("select");
  root.setAttribute("id", mainId);
  root.setAttribute("data-input", `#${inputId}`);
  root.setAttribute("data-options", `#${optionsId}`);
  root.setAttribute("data-popup", `#${popupId}`);
  root.style.setProperty("--font-size", cssFontSize);
  root.style.setProperty("--arrow-color", cssArrowColor);
  root.style.setProperty("--options-bg", cssOptionsBackground);
  root.style.setProperty("--disabled-color", cssDisabledColor);
  root.style.setProperty("--selected-bg", cssSelectedBackground);
  root.style.setProperty("--selected-color", cssSelectedColor);
  root.style.setProperty("--hover-bg", cssHoverBackground);
  root.style.setProperty("--hover-color", cssHoverColor);
  if (selectedId) {
    root.setAttribute("data-id", selectedId);
  }

  const popup = document.createElement("div");
  popup.classList.add("select__popup");
  popup.setAttribute("id", popupId);
  const wrapper = document.createElement("div");
  wrapper.classList.add("select__wrapper");
  const input = document.createElement("div");
  input.classList.add("select__input");
  input.setAttribute("id", inputId);
  input.setAttribute("tabindex", 1);
  input.textContent = defaultText;
  wrapper.appendChild(input);
  const options = document.createElement("ul");
  options.classList.add("select__options");
  options.setAttribute("id", optionsId);
  for (const { id, text, disabled, children } of items) {
    const li = document.createElement("li");
    li.classList.add("select__element");
    const option = document.createElement("div");
    option.classList.add("select__option");
    if (disabled) {
      option.classList.add("select--disabled");
    }
    option.textContent = text;
    if (id) {
      option.setAttribute("data-id", id);
    }
    li.appendChild(option);

    if (children && children.length > 0) {
      const sub = document.createElement("ul");
      sub.classList.add("select__sub-options");
      for (const { id, text, disabled } of children) {
        const liSub = document.createElement("li");
        liSub.classList.add("select__element");
        const optionSub = document.createElement("div");
        optionSub.classList.add("select__option");
        if (disabled) {
          optionSub.classList.add("select--disabled");
        }
        optionSub.textContent = text;
        if (id) {
          optionSub.setAttribute("data-id", id);
        }
        liSub.appendChild(optionSub);
        sub.appendChild(liSub);
      }
      li.appendChild(sub);
    }

    options.appendChild(li);
  }
  wrapper.appendChild(options);

  root.appendChild(popup);
  root.appendChild(wrapper);
  return root;
};

const selectInit = ({ selector = ".select" }) => {
  const cssClassOpen = "select--open";
  const cssClassSelected = "select--selected";
  const cssClassDisabled = "select--disabled";
  const selectOption = ".select__option";
  const select = document.querySelector(selector);
  if (!select) return;
  const {
    input: selectorInput,
    popup: selectorPopup,
    options: selectorOptions,
  } = select.dataset;

  const input = select.querySelector(selectorInput);
  const popup = select.querySelector(selectorPopup);
  const options = select.querySelector(selectorOptions);
  const elements = select.querySelectorAll(selectOption);

  const span = document.createElement("span");
  document.body.appendChild(span);
  const width = [...document.querySelectorAll(".select__option")]
    .map(({ textContent }) => {
      span.textContent = textContent;
      span.classList.add("select__input");
      const width = span.clientWidth;
      span.textContent = "";
      return width;
    })
    .reduce(
      (accum, item) => (item > accum ? item : accum),
      Math.ceil(input.getBoundingClientRect().width)
    );
  document.body.removeChild(span);

  input.style.width = `${width}px`;
  options.style.width = `${width}px`;

  const toggleOptions = () => {
    select.classList.toggle(cssClassOpen);
    popup.classList.toggle(cssClassOpen);
    options.classList.toggle(cssClassOpen);
  };

  const selectItem = (event) => {
    const { target } = event;
    const { id } = target.dataset;
    const text = target.textContent;

    if (!target.classList.contains(cssClassDisabled)) {
      select.setAttribute("data-id", id);
      input.textContent = text;

      for (const element of [...elements]) {
        element.classList.remove(cssClassSelected);
      }

      target.classList.add(cssClassSelected);
    }
  };

  popup.addEventListener("click", toggleOptions);
  input.addEventListener("click", toggleOptions);
  options.addEventListener("click", toggleOptions);

  for (const element of [...elements]) {
    element.addEventListener("click", selectItem);
  }
};

const calendarBlock = document.getElementsByClassName("calendar-block");

let selectBox;

const windowWidth = window.innerWidth;
const firstSelectBox = document.getElementsByClassName("select-box")[0];
const secondSelectBox = document.getElementsByClassName("select-box")[1];

if (!secondSelectBox) {
  selectBox = firstSelectBox;
}

if (windowWidth > 1024) {
  if (!secondSelectBox) {
    selectBox = firstSelectBox;
  } else {
    selectBox = secondSelectBox;
  }
} else {
  selectBox = firstSelectBox;
}

if (selectBox) {
  if (selectBox.classList.contains("month-select-box")) {
    selectBox.appendChild(
      createSelect(days, {
        defaultText: "Число",
        mainId: "daysSelect",
        cssFontSize: "1.2rem",
        cssArrowColor: "#1F334E",
        cssOptionsBackground: "#F3F3F3",
        cssDisabledColor: "#666",
        cssSelectedBackground: "#1F334E",
        cssSelectedColor: "#fff",
        cssHoverBackground: "#1F334E",
        cssHoverColor: "#fff",
      })
    );
  }

  if (selectBox.classList.contains("month-select-box")) {
    selectBox.appendChild(
      createSelect(items, {
        defaultText: "Месяц",
        mainId: "monthSelect",
        cssFontSize: "1.2rem",
        cssArrowColor: "#1F334E",
        cssOptionsBackground: "#F3F3F3",
        cssDisabledColor: "#666",
        cssSelectedBackground: "#1F334E",
        cssSelectedColor: "#fff",
        cssHoverBackground: "#1F334E",
        cssHoverColor: "#fff",
      })
    );
  }

  if (selectBox.classList.contains("year-select-box")) {
    selectBox.appendChild(
      createSelect(years, {
        defaultText: "Год",
        mainId: "yearSelect",
        cssFontSize: "1.2rem",
        cssArrowColor: "#1F334E",
        cssOptionsBackground: "#F3F3F3",
        cssDisabledColor: "#666",
        cssSelectedBackground: "#1F334E",
        cssSelectedColor: "#fff",
        cssHoverBackground: "#1F334E",
        cssHoverColor: "#fff",
      })
    );
  }
}

selectInit({ selector: "#daysSelect" });
selectInit({ selector: "#monthSelect" });
selectInit({ selector: "#yearSelect" });

const addActive = (element) => {
  element.classList.add("active");
};

const daysPicker = document.getElementsByClassName("day-picker");

if (daysPicker.length) {
  for (let i = 0; i < daysPicker.length; i++) {
    daysPicker[i].addEventListener("click", function () {
      document.querySelectorAll(".day-picker").forEach((node) => {
        node.classList.remove("active");
      });

      addActive(daysPicker[i]);
    });
  }
}

const input = document.getElementsByClassName("search-input");

if (input.length > 0) {
  for (let i = 0; i < input.length; i++) {
    input[i].addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        let newLoc;
        if (location.href.includes("index.html")) {
          const index = "index.html";
          newLoc = location.href.replace(
            index,
            "pages/search_page.html?search=" + input[i].value
          );
        } else {
          let url = location.href;
          let parts = url.split("/");
          let baseUrl = parts.slice(0, parts.length - 1).join("/") + "/";

          newLoc = baseUrl + "search_page.html?search=" + input[i].value;
        }

        location.href = newLoc;
      }
    });
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const datePicker = document.getElementById("input-date-picker");
  const calendar = document.getElementById("drop-down-calendar");
  let indexShowCalendar = 0;
  const relativeBlock = document.getElementsByClassName("relative-block")[0];

  if (datePicker) {
    datePicker.addEventListener("click", function (event) {
      event.stopPropagation();
      if (indexShowCalendar % 2 === 0) {
        calendar.hidden = false;
        relativeBlock.classList.add("active");
        indexShowCalendar--;
      } else {
        calendar.hidden = true;
        relativeBlock.classList.remove("active");
        indexShowCalendar++;
      }
    });

    document.addEventListener("click", function (event) {
      if (
        !datePicker.contains(event.target) &&
        !calendar.contains(event.target)
      ) {
        calendar.hidden = true;
        relativeBlock.classList.remove("active");
        if (indexShowCalendar % 2 !== 0) {
          indexShowCalendar++;
        }
      }
    });
  }
});

if (location.href.includes("central_asia_page")) {
  document.addEventListener("DOMContentLoaded", function () {
    updateCategoryButtons();
    setupMoreButton();
    setupAddCategoryButton();

    function updateCategoryButtons() {
      let buttons = document.querySelectorAll(".category-button");
      let sectionBlock = document.getElementsByClassName("section-block")[0];

      buttons.forEach(function (button) {
        button.addEventListener("click", function () {
          if (!button.disabled) {
            let sectionTitle = document.createElement("h3");
            sectionTitle.className = "section-title";
            sectionTitle.innerText = button.textContent.trim();

            sectionBlock.appendChild(sectionTitle);

            button.disabled = true;
            button.classList.add("active-category");
            button.classList.remove("not-active-category-button");

            addRemoveButtons();
          }
        });
      });
    }

    function addRemoveButtons() {
      let sectionBlock = document.getElementsByClassName("section-block")[0];

      if (sectionBlock) {
        let sectionTitles =
          sectionBlock.getElementsByClassName("section-title");

        if (sectionTitles == undefined) {
          return;
        }

        if (sectionTitles.length > 1) {
          for (let i = 0; i < sectionTitles.length; i++) {
            let sectionTitle = sectionTitles[i];

            if (!sectionTitle.querySelector(".remove-category-button")) {
              let removeButton = document.createElement("button");
              removeButton.className = "remove-category-button";
              removeButton.innerHTML = "&#x2716;";

              removeButton.addEventListener("click", function () {
                let parentSectionTitle = this.parentElement;
                let buttonText = parentSectionTitle.innerText
                  .trim()
                  .toLowerCase();

                sectionBlock.removeChild(parentSectionTitle);

                updateButtonState(buttonText);
                addRemoveButtons();
              });
              sectionTitle.appendChild(removeButton);
            }
          }
        } else {
          for (let i = 0; i < sectionTitles.length; i++) {
            let existingButton = sectionTitles[i].querySelector(
              ".remove-category-button"
            );
            if (existingButton) {
              sectionTitles[i].removeChild(existingButton);
            }
          }
        }
      } else {
        return;
      }
    }

    function updateButtonState(buttonText) {
      let buttons = document.querySelectorAll(".category-button");
      buttons.forEach(function (button) {
        let buttonInnerText = button.innerText.toLowerCase().trim();
        let targetText = buttonText.toLowerCase().replace("✖", "").trim();

        if (buttonInnerText === targetText) {
          button.disabled = false;
          button.classList.add("not-active-category-button");
          button.classList.remove("active-category");
        }
      });
    }

    function setupMoreButton() {
      let moreButton = document.querySelector(".more-category-button");
      let extraCategories = document.querySelector(".extra-categories");

      if (moreButton && extraCategories) {
        moreButton.addEventListener("click", function () {
          if (
            extraCategories.style.display === "none" ||
            extraCategories.style.display === ""
          ) {
            extraCategories.style.display = "flex";
            moreButton.innerText = "Скрыть";
            moreButton.classList.add("hide-button");
          } else {
            extraCategories.style.display = "none";
            moreButton.innerText = "еще 1";
            moreButton.classList.remove("hide-button");
          }
        });
      }
    }

    function setupAddCategoryButton() {
      let addCategoryButton = document.getElementById("add-category-button");
      let searchInput = document.getElementById("category-search-input");

      if (addCategoryButton && searchInput) {
        addCategoryButton.addEventListener("click", function () {
          if (searchInput.classList.contains("open")) {
            searchInput.classList.remove("open");
          } else {
            searchInput.classList.add("open");
          }
        });
      }
    }
    addRemoveButtons();
  });
}

const moreCategoryPopup = document.getElementsByClassName(
  "more-category-popup"
)[0];

const moreCategoryLink = document.getElementById("more-category-link");
const moreCategoryList =
  document.getElementsByClassName("more-category-list")[0];

if (moreCategoryLink && moreCategoryPopup) {
  moreCategoryLink.addEventListener("click", function () {
    if (moreCategoryList.style.display == "block") {
      moreCategoryPopup.style.display = "none";
      moreCategoryList.style.display = "none";
    } else {
      moreCategoryList.style.display = "block";
      moreCategoryPopup.style.display = "block";
    }
  });
  moreCategoryPopup.addEventListener("click", function () {
    if (moreCategoryList.style.display == "block") {
      moreCategoryPopup.style.display = "none";
      moreCategoryList.style.display = "none";
    } else {
      moreCategoryList.style.display = "block";
      moreCategoryPopup.style.display = "block";
    }
  });
}

const languagesArr = ["Рус", "Кыр", "Eng", "Tr", "中文", "العربية"];

const languages = Array.from({ length: languagesArr.length }, (v, i) => ({
  id: i + 1,
  text: languagesArr[i],
}));

const languageSelect = document.querySelector(".language-select");
const languageSelectList = document.querySelector(".language-select-list");
let currentLanguage = languages[0];
languageSelect.textContent = currentLanguage.text;

function updateLanguageList() {
  languageSelectList.innerHTML = "";
  languages
    .filter((lang) => lang.text !== currentLanguage.text)
    .forEach((lang) => {
      const li = document.createElement("li");
      li.textContent = lang.text;
      li.addEventListener("click", () => {
        currentLanguage = lang;
        languageSelect.textContent = currentLanguage.text;
        updateLanguageList();
      });
      languageSelectList.appendChild(li);
    });
}

updateLanguageList();

languageSelect.addEventListener("click", () => {
  if (!languageSelect.classList.contains("active")) {
    languageSelectList.style.display = "flex";
    languageSelect.classList.add("active");
  } else {
    languageSelectList.style.display = "none";
    languageSelect.classList.remove("active");
  }
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".language-select-block")) {
    languageSelectList.style.display = "none";
    languageSelect.classList.remove("active");
  }
});

const burgerButton = document.getElementById("hamburger-button");
const searchButton = document.getElementById("search-button");
const closeBurger = document.getElementById("close-burger-button");
const closeSearch = document.getElementById("close-search-button");

if (burgerButton) {
  burgerButton.addEventListener("click", function () {
    document.getElementsByClassName("burger-pop-up-block")[0].style.display =
      "block";
  });

  closeBurger.addEventListener("click", function () {
    document.getElementsByClassName("burger-pop-up-block")[0].style.display =
      "none";
  });

  searchButton.addEventListener("click", function () {
    document.getElementsByClassName("search-pop-up-block")[0].style.display =
      "block";
  });

  closeSearch.addEventListener("click", function () {
    document.getElementsByClassName("search-pop-up-block")[0].style.display =
      "none";
  });
}

function getRandomDate() {
  const months = [
    { name: "Января", days: 31 },
    { name: "Февраля", days: 28 },
    { name: "Марта", days: 31 },
    { name: "Апреля", days: 30 },
    { name: "Мая", days: 31 },
    { name: "Июня", days: 30 },
    { name: "Июля", days: 31 },
    { name: "Августа", days: 31 },
    { name: "Сентября", days: 30 },
    { name: "Октября", days: 31 },
    { name: "Ноября", days: 30 },
    { name: "Декабря", days: 31 },
  ];

  const randomMonthIndex = Math.floor(Math.random() * months.length);
  const randomMonth = months[randomMonthIndex];
  const randomDay = Math.floor(Math.random() * randomMonth.days) + 1;

  return `${randomDay} ${randomMonth.name}`;
}

if (
  location.href.includes("index_news_page") ||
  location.href.includes("press_conference_announce_page") ||
  location.href.includes("search_page") ||
  location.href.includes("press_centre_page")
) {
  const itemsArr = [];

let itemsPerPage;
let listContainer;
if (document.getElementsByClassName("index-news-page")[0]) {
  itemsPerPage = 7;
  listContainer = document.getElementById("indexNewsList");
  for (let i = 1; i <= 20; i++) {
    itemsArr.push(` <li class="index-news-list-item">
                <img src="../assets/images/news/laptop.jfif" alt="laptop" />

                <div class="news-info">
                  <h4 class="news-info-title">
                    <a href="./material_page.html">
                      Ранние пташки. В Бишкеке предложили перенести начало
                      занятий в школах из-за пробок Ранние пташки. В Бишкеке
                      предложили перенести начало занятий в школах из-за пробок
                    </a>
                  </h4>

                  <div class="news-data-block-inner">
                    <span class="news-date news-info-item">
                      <svg
                        width="11"
                        height="12"
                        viewBox="0 0 11 12"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M2.4 5.4H3.6V6.6H2.4V5.4ZM10.8 2.4V10.8C10.8 11.46 10.26 12 9.6 12H1.2C0.88174 12 0.576515 11.8736 0.351472 11.6485C0.126428 11.4235 0 11.1183 0 10.8L0.00599999 2.4C0.00599999 1.74 0.534 1.2 1.2 1.2H1.8V0H3V1.2H7.8V0H9V1.2H9.6C10.26 1.2 10.8 1.74 10.8 2.4ZM1.2 3.6H9.6V2.4H1.2V3.6ZM9.6 10.8V4.8H1.2V10.8H9.6ZM7.2 6.6H8.4V5.4H7.2V6.6ZM4.8 6.6H6V5.4H4.8V6.6Z"
                          fill="#555555"
                        />
                      </svg>
                      02 января 2024
                    </span>
                    <div class="vl"></div>
                    <span class="news-time news-info-item">
                      <svg
                        width="13"
                        height="12"
                        viewBox="0 0 13 12"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <g clip-path="url(#clip0_4759_3792)">
                          <path
                            d="M6.7998 6.49951V4.49951M11.2998 2.99951L10.2998 1.99951M5.7998 0.999512H7.7998M6.7998 10.4995C4.59067 10.4995 2.7998 8.70865 2.7998 6.49951C2.7998 4.29037 4.59067 2.49951 6.7998 2.49951C9.00894 2.49951 10.7998 4.29037 10.7998 6.49951C10.7998 8.70865 9.00894 10.4995 6.7998 10.4995Z"
                            stroke="#555555"
                            stroke-width="1.2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          />
                        </g>
                        <defs>
                          <clipPath id="clip0_4759_3792">
                            <rect
                              width="12"
                              height="12"
                              fill="#555555"
                              transform="translate(0.799805 -0.000488281)"
                            />
                          </clipPath>
                        </defs>
                      </svg>
                      12:45
                    </span>
                    <div class="vl"></div>
                    <span class="news-views news-info-item">
                      <svg
                        width="14"
                        height="10"
                        viewBox="0 0 14 10"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M13.2244 4.86711C13.2058 4.82445 12.7508 3.81547 11.7347 2.79938C10.7919 1.85766 9.17207 0.734375 6.79973 0.734375C4.42738 0.734375 2.80754 1.85766 1.86472 2.79938C0.848631 3.81547 0.393631 4.82281 0.375037 4.86711C0.356341 4.90911 0.34668 4.95457 0.34668 5.00055C0.34668 5.04652 0.356341 5.09198 0.375037 5.13398C0.393631 5.17609 0.848631 6.18508 1.86472 7.20117C2.80754 8.14289 4.42738 9.26562 6.79973 9.26562C9.17207 9.26562 10.7919 8.14289 11.7347 7.20117C12.7508 6.18508 13.2058 5.17773 13.2244 5.13398C13.2431 5.09198 13.2528 5.04652 13.2528 5.00055C13.2528 4.95457 13.2431 4.90911 13.2244 4.86711ZM6.79973 8.60938C5.08363 8.60938 3.58519 7.98484 2.34543 6.75383C1.82574 6.23731 1.38596 5.64621 1.04058 5C1.38586 4.3539 1.82566 3.76296 2.34543 3.24672C3.58519 2.01516 5.08363 1.39062 6.79973 1.39062C8.51582 1.39062 10.0143 2.01516 11.254 3.24672C11.7738 3.76296 12.2136 4.3539 12.5589 5C12.2105 5.66773 10.4638 8.60938 6.79973 8.60938ZM6.79973 2.48438C6.30218 2.48438 5.81581 2.63191 5.40212 2.90833C4.98843 3.18475 4.66599 3.57764 4.47559 4.03731C4.28519 4.49698 4.23537 5.00279 4.33244 5.49077C4.4295 5.97876 4.66909 6.427 5.02091 6.77882C5.37273 7.13063 5.82097 7.37022 6.30895 7.46729C6.79693 7.56435 7.30274 7.51454 7.76241 7.32413C8.22208 7.13373 8.61497 6.8113 8.89139 6.39761C9.16781 5.98391 9.31535 5.49754 9.31535 5C9.31448 4.33308 9.04916 3.69373 8.57758 3.22214C8.106 2.75056 7.46664 2.48524 6.79973 2.48438ZM6.79973 6.85938C6.43198 6.85938 6.07248 6.75033 5.76671 6.54601C5.46094 6.3417 5.22262 6.05131 5.08189 5.71155C4.94115 5.3718 4.90433 4.99794 4.97608 4.63725C5.04782 4.27657 5.22491 3.94526 5.48495 3.68522C5.74499 3.42518 6.0763 3.2481 6.43698 3.17635C6.79766 3.10461 7.17152 3.14143 7.51128 3.28216C7.85103 3.42289 8.14143 3.66121 8.34574 3.96699C8.55005 4.27276 8.6591 4.63225 8.6591 5C8.6591 5.49314 8.4632 5.96608 8.1145 6.31478C7.7658 6.66348 7.29286 6.85938 6.79973 6.85938Z"
                          fill="#555555"
                          stroke="#555555"
                          stroke-width="0.5"
                        />
                      </svg>
                      6000
                    </span>
                    <div class="vl"></div>
                    <span class="news-comments news-info-item">
                      <svg
                        width="11"
                        height="12"
                        viewBox="0 0 11 12"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M3.55469 9.90088C4.21543 10.282 4.98207 10.5 5.79963 10.5C8.28491 10.5 10.2998 8.48528 10.2998 6C10.2998 3.51472 8.28509 1.5 5.7998 1.5C3.31452 1.5 1.2998 3.51472 1.2998 6C1.2998 6.81756 1.51783 7.58419 1.8989 8.24494L1.90038 8.2475C1.93704 8.31107 1.95553 8.34313 1.96391 8.37343C1.97181 8.402 1.97401 8.4277 1.97199 8.45728C1.96982 8.48906 1.95911 8.52201 1.93715 8.58789L1.55273 9.74113L1.55225 9.74264C1.47114 9.98596 1.43059 10.1076 1.4595 10.1887C1.4847 10.2594 1.54065 10.3152 1.61133 10.3404C1.69221 10.3692 1.81333 10.3288 2.05558 10.2481L2.05859 10.247L3.21183 9.86255C3.27749 9.84066 3.31087 9.82956 3.3426 9.82739C3.37218 9.82537 3.39769 9.82804 3.42627 9.83594C3.45665 9.84433 3.48872 9.86283 3.55262 9.89969L3.55469 9.90088Z"
                          stroke="#555555"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                      </svg>

                      0
                    </span>
                    <div class="vl"></div>
                    <span class="news-category news-info-item">спорт</span>
                  </div>
                </div>
              </li>`);
  }
} else if (
  document.getElementsByClassName("press-conferense-announce-page")[0]
) {
  itemsPerPage = 2;
  listContainer = document.getElementById("announceList");
  for (let i = 1; i <= 20; i++) {
    itemsArr.push(`<li class="announce-list-item">
      <h3 class="section-title">${getRandomDate()}</h3>
      <div class="announce-block">
        <span class="news-time news-info-item">
          <div class="vl"></div>
          <svg width="13" height="12" viewBox="0 0 13 12" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g clip-path="url(#clip0_4759_3792)">
              <path d="M6.7998 6.49951V4.49951M11.2998 2.99951L10.2998 1.99951M5.7998 0.999512H7.7998M6.7998 10.4995C4.59067 10.4995 2.7998 8.70865 2.7998 6.49951C2.7998 4.29037 4.59067 2.49951 6.7998 2.49951C9.00894 2.49951 10.7998 4.29037 10.7998 6.49951C10.7998 8.70865 9.00894 10.4995 6.7998 10.4995Z" stroke="#555555" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
            </g>
            <defs>
              <clipPath id="clip0_4759_3792">
                <rect width="12" height="12" fill="#555555" transform="translate(0.799805 -0.000488281)"/>
              </clipPath>
            </defs>
          </svg>
          12:00
        </span>
        <div class="announce-title">
          Последствия незаконных действий отдельных должностных лиц судебного департамента физических лиц, действиями которых нанесен ущерб Федерации профсоюзов КР
        </div>
        <ul class="participants-list">
          Участники:
          <li class="participants-list-item">— Полковник милиции в отставке, председатель совета ветеранов МВД КР Жоошбаев Султанбек Жоошбаевич</li>
          <li class="participants-list-item">— Полковник милиции в отставке, председатель совета ветеранов МВД КР Жоошбаев Султанбек Жоошбаевич</li>
          <li class="participants-list-item">— Полковник милиции в отставке, председатель совета ветеранов МВД КР Жоошбаев Султанбек Жоошбаевич</li>
          <li class="participants-list-item">— Полковник милиции в отставке, председатель совета ветеранов МВД КР Жоошбаев Султанбек Жоошбаевич</li>
        </ul>
      </div>
    </li>`);
  }
} else if (document.getElementsByClassName("search-news-page")[0]) {
  itemsPerPage = 8;
  listContainer = document.getElementById("searchResultList");
  for (let i = 1; i <= 20; i++) {
    itemsArr.push(`
     <li class="index-news-list-item">
                <img src="../assets/images/news/laptop.jfif" alt="laptop" />

                <div class="news-info">
                  <h4 class="news-info-title">
                    <a class="news-info-link" href="./material_page.html">
                      Поздравление президента кыргызской республики Садыра
                      <span class="found-word">Жапаров</span>а с Днем финансовых и экономических
                      работников Поздравление президента кыргызской респуублики
                    </a>
                  </h4>

                  <div class="news-data-block-inner">
                    <span class="news-info-item"> Президент </span>
                    <div class="vl"></div>
                    <span class="news-info-item"> Jenny kiaa </span>
                    <div class="vl"></div>
                    <span class="news-date news-info-item">
                      <svg
                        width="11"
                        height="12"
                        viewBox="0 0 11 12"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M2.4 5.4H3.6V6.6H2.4V5.4ZM10.8 2.4V10.8C10.8 11.46 10.26 12 9.6 12H1.2C0.88174 12 0.576515 11.8736 0.351472 11.6485C0.126428 11.4235 0 11.1183 0 10.8L0.00599999 2.4C0.00599999 1.74 0.534 1.2 1.2 1.2H1.8V0H3V1.2H7.8V0H9V1.2H9.6C10.26 1.2 10.8 1.74 10.8 2.4ZM1.2 3.6H9.6V2.4H1.2V3.6ZM9.6 10.8V4.8H1.2V10.8H9.6ZM7.2 6.6H8.4V5.4H7.2V6.6ZM4.8 6.6H6V5.4H4.8V6.6Z"
                          fill="#555555"
                        />
                      </svg>
                      02 января 2024
                    </span>
                    <div class="vl"></div>
                    <span class="news-views news-info-item">
                      <svg
                        width="13"
                        height="12"
                        viewBox="0 0 13 12"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <g clip-path="url(#clip0_4759_3792)">
                          <path
                            d="M6.7998 6.49951V4.49951M11.2998 2.99951L10.2998 1.99951M5.7998 0.999512H7.7998M6.7998 10.4995C4.59067 10.4995 2.7998 8.70865 2.7998 6.49951C2.7998 4.29037 4.59067 2.49951 6.7998 2.49951C9.00894 2.49951 10.7998 4.29037 10.7998 6.49951C10.7998 8.70865 9.00894 10.4995 6.7998 10.4995Z"
                            stroke="#555555"
                            stroke-width="1.2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          />
                        </g>
                        <defs>
                          <clipPath id="clip0_4759_3792">
                            <rect
                              width="12"
                              height="12"
                              fill="#555555"
                              transform="translate(0.799805 -0.000488281)"
                            />
                          </clipPath>
                        </defs>
                      </svg>
                      12:45
                    </span>
                    <div class="vl"></div>
                    <span class="news-views news-info-item">
                      <svg
                        width="14"
                        height="10"
                        viewBox="0 0 14 10"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M13.2244 4.86711C13.2058 4.82445 12.7508 3.81547 11.7347 2.79938C10.7919 1.85766 9.17207 0.734375 6.79973 0.734375C4.42738 0.734375 2.80754 1.85766 1.86472 2.79938C0.848631 3.81547 0.393631 4.82281 0.375037 4.86711C0.356341 4.90911 0.34668 4.95457 0.34668 5.00055C0.34668 5.04652 0.356341 5.09198 0.375037 5.13398C0.393631 5.17609 0.848631 6.18508 1.86472 7.20117C2.80754 8.14289 4.42738 9.26562 6.79973 9.26562C9.17207 9.26562 10.7919 8.14289 11.7347 7.20117C12.7508 6.18508 13.2058 5.17773 13.2244 5.13398C13.2431 5.09198 13.2528 5.04652 13.2528 5.00055C13.2528 4.95457 13.2431 4.90911 13.2244 4.86711ZM6.79973 8.60938C5.08363 8.60938 3.58519 7.98484 2.34543 6.75383C1.82574 6.23731 1.38596 5.64621 1.04058 5C1.38586 4.3539 1.82566 3.76296 2.34543 3.24672C3.58519 2.01516 5.08363 1.39062 6.79973 1.39062C8.51582 1.39062 10.0143 2.01516 11.254 3.24672C11.7738 3.76296 12.2136 4.3539 12.5589 5C12.2105 5.66773 10.4638 8.60938 6.79973 8.60938ZM6.79973 2.48438C6.30218 2.48438 5.81581 2.63191 5.40212 2.90833C4.98843 3.18475 4.66599 3.57764 4.47559 4.03731C4.28519 4.49698 4.23537 5.00279 4.33244 5.49077C4.4295 5.97876 4.66909 6.427 5.02091 6.77882C5.37273 7.13063 5.82097 7.37022 6.30895 7.46729C6.79693 7.56435 7.30274 7.51454 7.76241 7.32413C8.22208 7.13373 8.61497 6.8113 8.89139 6.39761C9.16781 5.98391 9.31535 5.49754 9.31535 5C9.31448 4.33308 9.04916 3.69373 8.57758 3.22214C8.106 2.75056 7.46664 2.48524 6.79973 2.48438ZM6.79973 6.85938C6.43198 6.85938 6.07248 6.75033 5.76671 6.54601C5.46094 6.3417 5.22262 6.05131 5.08189 5.71155C4.94115 5.3718 4.90433 4.99794 4.97608 4.63725C5.04782 4.27657 5.22491 3.94526 5.48495 3.68522C5.74499 3.42518 6.0763 3.2481 6.43698 3.17635C6.79766 3.10461 7.17152 3.14143 7.51128 3.28216C7.85103 3.42289 8.14143 3.66121 8.34574 3.96699C8.55005 4.27276 8.6591 4.63225 8.6591 5C8.6591 5.49314 8.4632 5.96608 8.1145 6.31478C7.7658 6.66348 7.29286 6.85938 6.79973 6.85938Z"
                          fill="#555555"
                          stroke="#555555"
                          stroke-width="0.5"
                        />
                      </svg>
                      6000
                    </span>
                    <div class="vl"></div>
                    <span class="news-comments news-info-item">
                      <svg
                        width="11"
                        height="12"
                        viewBox="0 0 11 12"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M3.55469 9.90088C4.21543 10.282 4.98207 10.5 5.79963 10.5C8.28491 10.5 10.2998 8.48528 10.2998 6C10.2998 3.51472 8.28509 1.5 5.7998 1.5C3.31452 1.5 1.2998 3.51472 1.2998 6C1.2998 6.81756 1.51783 7.58419 1.8989 8.24494L1.90038 8.2475C1.93704 8.31107 1.95553 8.34313 1.96391 8.37343C1.97181 8.402 1.97401 8.4277 1.97199 8.45728C1.96982 8.48906 1.95911 8.52201 1.93715 8.58789L1.55273 9.74113L1.55225 9.74264C1.47114 9.98596 1.43059 10.1076 1.4595 10.1887C1.4847 10.2594 1.54065 10.3152 1.61133 10.3404C1.69221 10.3692 1.81333 10.3288 2.05558 10.2481L2.05859 10.247L3.21183 9.86255C3.27749 9.84066 3.31087 9.82956 3.3426 9.82739C3.37218 9.82537 3.39769 9.82804 3.42627 9.83594C3.45665 9.84433 3.48872 9.86283 3.55262 9.89969L3.55469 9.90088Z"
                          stroke="#555555"
                          stroke-width="1.2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                      </svg>

                      0
                    </span>
                  </div>
                </div>
              </li>
    `);
  }
} else if (document.getElementsByClassName("press-centre-page")[0]) {
  itemsPerPage = 7;
  listContainer = document.getElementById("pressCentreList");
  for (let i = 1; i <= 20; i++) {
    itemsArr.push(`
    <li class="index-news-list-item">
                <img src="../assets/images/news/laptop.jfif" alt="laptop" />

                <div class="news-info">
                  <h4 class="news-info-title">
                    <a href="./material_page.html">
                      Последствия незаконных действий отдельных должностных лиц судебного департамента и физических лиц, действиями которых нанесен ущерб Федерации профсоюзов КР
                      <img src="../assets/vectors/icons/youtube.svg" alt="video" class="title-icon">
                    </a>
                  </h4>

                  <div class="news-data-block-inner">
                    <span class="news-date news-info-item">
                      <svg
                        width="11"
                        height="12"
                        viewBox="0 0 11 12"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M2.4 5.4H3.6V6.6H2.4V5.4ZM10.8 2.4V10.8C10.8 11.46 10.26 12 9.6 12H1.2C0.88174 12 0.576515 11.8736 0.351472 11.6485C0.126428 11.4235 0 11.1183 0 10.8L0.00599999 2.4C0.00599999 1.74 0.534 1.2 1.2 1.2H1.8V0H3V1.2H7.8V0H9V1.2H9.6C10.26 1.2 10.8 1.74 10.8 2.4ZM1.2 3.6H9.6V2.4H1.2V3.6ZM9.6 10.8V4.8H1.2V10.8H9.6ZM7.2 6.6H8.4V5.4H7.2V6.6ZM4.8 6.6H6V5.4H4.8V6.6Z"
                          fill="#555555"
                        />
                      </svg>
                      02 января 2024
                    </span>
                    <div class="vl"></div>
                    <span class="news-time news-info-item">
                      <svg
                        width="13"
                        height="12"
                        viewBox="0 0 13 12"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <g clip-path="url(#clip0_4759_3792)">
                          <path
                            d="M6.7998 6.49951V4.49951M11.2998 2.99951L10.2998 1.99951M5.7998 0.999512H7.7998M6.7998 10.4995C4.59067 10.4995 2.7998 8.70865 2.7998 6.49951C2.7998 4.29037 4.59067 2.49951 6.7998 2.49951C9.00894 2.49951 10.7998 4.29037 10.7998 6.49951C10.7998 8.70865 9.00894 10.4995 6.7998 10.4995Z"
                            stroke="#555555"
                            stroke-width="1.2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          />
                        </g>
                        <defs>
                          <clipPath id="clip0_4759_3792">
                            <rect
                              width="12"
                              height="12"
                              fill="#555555"
                              transform="translate(0.799805 -0.000488281)"
                            />
                          </clipPath>
                        </defs>
                      </svg>
                      12:45
                    </span>
                  </div>
                </div>
              </li>
    `);
  }
}

let currentPage = 1;

function displayItems(page) {
  listContainer.innerHTML = "";
  const start = (page - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  const itemsToShow = itemsArr.slice(start, end);
  listContainer.innerHTML = itemsToShow.join("");
}

function setupPagination() {
  const paginationContainer = document.getElementById("paginationNumbers");
  paginationContainer.innerHTML = "";
  const totalPages = Math.ceil(itemsArr.length / itemsPerPage);

  if (totalPages > 1) {
    const firstPageButton = document.createElement("button");
    firstPageButton.textContent = 1;
    if (currentPage === 1) {
      firstPageButton.classList.add("active");
    }
    firstPageButton.addEventListener("click", () => {
      currentPage = 1;
      displayItems(currentPage);
      setupPagination();
    });
    paginationContainer.appendChild(firstPageButton);
  }

  if (totalPages > 5) {
    if (currentPage > 4) {
      paginationContainer.appendChild(document.createTextNode("..."));
    }

    const startPage = Math.max(currentPage - 2, 2);
    const endPage = Math.min(currentPage + 2, totalPages - 1);

    for (let i = startPage; i <= endPage; i++) {
      const button = document.createElement("button");
      button.textContent = i;
      if (i === currentPage) {
        button.classList.add("active");
      }
      button.addEventListener("click", () => {
        currentPage = i;
        displayItems(currentPage);
        setupPagination();
      });
      paginationContainer.appendChild(button);
    }

    if (currentPage < totalPages - 3) {
      paginationContainer.appendChild(document.createTextNode("..."));
    }
  } else {
    for (let i = 2; i <= totalPages - 1; i++) {
      const button = document.createElement("button");
      button.textContent = i;
      if (i === currentPage) {
        button.classList.add("active");
      }
      button.addEventListener("click", () => {
        currentPage = i;
        displayItems(currentPage);
        setupPagination();
      });
      paginationContainer.appendChild(button);
    }
  }

  if (totalPages > 1) {
    const lastPageButton = document.createElement("button");
    lastPageButton.textContent = totalPages;
    if (currentPage === totalPages) {
      lastPageButton.classList.add("active");
    }
    lastPageButton.addEventListener("click", () => {
      currentPage = totalPages;
      displayItems(currentPage);
      setupPagination();
    });
    paginationContainer.appendChild(lastPageButton);
  }
}

document.querySelector(".pagination-prev").addEventListener("click", () => {
  if (currentPage > 1) {
    currentPage--;
    displayItems(currentPage);
    setupPagination();
  }
});

document.querySelector(".pagination-next").addEventListener("click", () => {
  const totalPages = Math.ceil(itemsArr.length / itemsPerPage);
  if (currentPage < totalPages) {
    currentPage++;
    displayItems(currentPage);
    setupPagination();
  }
});

displayItems(currentPage);
setupPagination();
}

if (location.href.includes("search_page")) {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const searchValue = urlParams.get("search");

  const sectionTitle = document.getElementsByClassName("section-title")[0];
  const searchPageInput = document.getElementById("search-page-input");

  if (searchValue) {
    sectionTitle.innerHTML = "Результаты поиска: " + searchValue;
    searchPageInput.placeholder = searchValue;
  } else {
    searchPageInput.placeholder = "Найти";
  }

  let title = document.querySelectorAll(".news-info-link");
  let regex = new RegExp(searchValue, "gi");
  let text;

  title.forEach((item) => {
    text = item.textContent.replace(regex, function (match) {
      return '<span class="found-word">' + match + "</span>";
    });
    item.innerHTML = text;
  });
}

const videoPlayButtons = document.querySelectorAll(".video-play-button");
if(videoPlayButtons.length > 0){
  videoPlayButtons.forEach(button => {
    button.addEventListener('click', function() {
      let parentSlide;
      let image;
      if(location.href.includes("material_video_page") || location.href.includes("news")){
        parentSlide = button.closest('.video-block');
        image = parentSlide.querySelector('.video-thumbnail');
      }else{
        parentSlide = button.closest('.swiper-slide');
        console.log(parentSlide);
        image = parentSlide.querySelector('.swiper-media');
      }
      
      const iframe = parentSlide.querySelector('.material-videos');
      iframe.setAttribute('src', iframe.getAttribute('src') + "?autoplay=true");
      const darkFilter = parentSlide.querySelector('.darker-filter');
      darkFilter.style.display = 'none';

      image.style.display = 'none';
      button.style.display = 'none';

      iframe.style.display = 'block';
    });
  });
}

const partnerSwiper = new Swiper(".partner-container", {
  direction: "horizontal",
  loop: true,
  speed: 400,
  spaceBetween: 60,
  initialSlide: 0,
  slidesPerView: 2,
  breakpoints: {
    1024: {
      slidesPerView: 5,
      slidesPerGroup: 1,
    },
    480: {
      slidesPerView: 3,
    },
  },

  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

const lateNewsSwiper = new Swiper(".late-news-slider", {
  direction: "horizontal",
  loop: true,
  speed: 400,
  spaceBetween: 0,
  initialSlide: 2,
  slidesPerView: 1,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});

const photoSwiper = new Swiper(".photo-swiper", {
  direction: "horizontal",
  loop: true,
  speed: 400,
  spaceBetween: 0,
  initialSlide: 2,
  slidesPerView: 1,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});

const materialSlider = new Swiper(".material-slider", {
  direction: "horizontal",
  speed: 400,
  spaceBetween: 100,
  initialSlide: 0,
  slidesPerView: 1,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});
