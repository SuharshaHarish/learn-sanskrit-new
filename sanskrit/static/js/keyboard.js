const Keyboard = {
  elements: {
    main: null,
    keysContainer: null,
    keys: []
  },

  eventHandlers: {
    oninput: null,
    onclose: null
  },

  properties: {
    value: "",
    capsLock: false
  },

  init() {
    // Create main elements
    this.elements.main = document.createElement("div");
    this.elements.keysContainer = document.createElement("div");

    // Setup main elements
    this.elements.main.classList.add("keyboard", "keyboard--hidden");
    this.elements.keysContainer.classList.add("keyboard__keys");
    this.elements.keysContainer.appendChild(this._createKeys());

    this.elements.keys = this.elements.keysContainer.querySelectorAll(
      ".keyboard__key"
    );

    // Add to DOM
    this.elements.main.appendChild(this.elements.keysContainer);
    document.body.appendChild(this.elements.main);

    // Automatically use keyboard for elements with .use-keyboard-input
    console.log(document.activeElement);

    document.querySelectorAll(".use-keyboard-input").forEach(element => {
      element.addEventListener("focus", () => {
        console.log(this);
        this.open(element.value, currentValue => {
          element.value = currentValue;
        });
      });
    });
  },

  _createKeys() {
    const fragment = document.createDocumentFragment();

    const keyLayout = [
      "०",
      "१",
      "२",
      "३",
      "४",
      "५",
      "६",
      "७",
      "८",
      "९",
      "अ",
      "आ",
      "इ",
      "ई",
      "उ",
      "ऊ",
      "ऋ",
      "ॠ",
      "ऌ",
      "ॡ",
      "ए",
      "ऐ",
      "ओ",
      "औ",
      "ं",
      "ः",
      "्",
      "ा",
      "ि",
      "ी",
      "ु",
      "ू",
      "ृ",
      "ॄ",
      "ॢ",
      "ॣ",
      "े",
      "ै",
      "ो",
      "ौ",
      "enter",
      "क",
      "ख",
      "ग",
      "घ",
      "ङ",
      "च",
      "छ",
      "ज",
      "झ",
      "ञ",
      "ट",
      "ठ",
      "ड",
      "ढ",
      "ण",
      "त",
      "थ",
      "द",
      "ध",
      "न",
      "प",
      "फ",
      "ब",
      "भ",
      "म",
      "य",
      "र",
      "ल",
      "व",
      "श",
      "ष",
      "स",
      "ह",
      "backspace",
      "क्ष",
      "त्र",
      "ज्ञ",
      "श्र",
      "space",
      "।",
      "॥",
      "ऽ",
      "ॐ",
      "done"
    ];

    // Creates HTML for an icon
    const createIconHTML = icon_name => {
      return `<i class="material-icons">${icon_name}</i>`;
    };

    keyLayout.forEach(key => {
      const keyElement = document.createElement("button");
      const insertLineBreak =
        ["backspace", "p", "enter", "?"].indexOf(key) !== -1;

      // Add attributes/classes
      keyElement.setAttribute("type", "button");
      keyElement.classList.add("keyboard__key");

      switch (key) {
        case "backspace":
          keyElement.classList.add("keyboard__key--wide");
          keyElement.innerHTML = createIconHTML("backspace");

          keyElement.addEventListener("click", () => {
            this.properties.value = this.properties.value.substring(
              0,
              this.properties.value.length - 1
            );
            this._triggerEvent("oninput");
          });

          break;

        case "caps":
          keyElement.classList.add(
            "keyboard_key--wide",
            "keyboard_key--activatable"
          );
          keyElement.innerHTML = createIconHTML("keyboard_capslock");

          keyElement.addEventListener("click", () => {
            this._toggleCapsLock();
            keyElement.classList.toggle(
              "keyboard__key--active",
              this.properties.capsLock
            );
          });

          break;

        case "enter":
          keyElement.classList.add("keyboard__key--wide");
          keyElement.innerHTML = createIconHTML("keyboard_return");

          keyElement.addEventListener("click", () => {
            this.properties.value += "\n";
            this._triggerEvent("oninput");
          });

          break;

        case "space":
          keyElement.classList.add("keyboard__key--extra-wide");
          keyElement.innerHTML = createIconHTML("space_bar");

          keyElement.addEventListener("click", () => {
            this.properties.value += " ";
            this._triggerEvent("oninput");
          });

          break;

        case "done":
          keyElement.classList.add("keyboard_key--wide", "keyboard_key--dark");
          keyElement.innerHTML = createIconHTML("check_circle");

          keyElement.addEventListener("click", () => {
            this.close();
            this._triggerEvent("onclose");
          });

          break;

        default:
          keyElement.textContent = key.toLowerCase();

          keyElement.addEventListener("click", () => {
            this.properties.value += this.properties.capsLock
              ? key.toUpperCase()
              : key.toLowerCase();
            this._triggerEvent("oninput");
          });

          break;
      }

      fragment.appendChild(keyElement);

      if (insertLineBreak) {
        fragment.appendChild(document.createElement("br"));
      }
    });

    return fragment;
  },

  _triggerEvent(handlerName) {
    if (typeof this.eventHandlers[handlerName] == "function") {
      this.eventHandlers[handlerName](this.properties.value);
    }
  },

  _toggleCapsLock() {
    this.properties.capsLock = !this.properties.capsLock;

    for (const key of this.elements.keys) {
      if (key.childElementCount === 0) {
        key.textContent = this.properties.capsLock
          ? key.textContent.toUpperCase()
          : key.textContent.toLowerCase();
      }
    }
  },

  open(initialValue, oninput, onclose) {
    this.properties.value = initialValue || "";
    this.eventHandlers.oninput = oninput;
    this.eventHandlers.onclose = onclose;
    this.elements.main.classList.remove("keyboard--hidden");
  },

  close() {
    this.properties.value = "";
    this.eventHandlers.oninput = oninput;
    this.eventHandlers.onclose = onclose;
    this.elements.main.classList.add("keyboard--hidden");
  }
};

// window.addEventListener("DOMContentLoaded", function() {
//   Keyboard.init();
// });
