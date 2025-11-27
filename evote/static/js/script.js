//for automatic letter display 
const words = ["Online Voting System", " e-Vote Campus."];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const speed = 150; // Typing speed
    const display = document.getElementById("display");

    function typeEffect() {
      const currentWord = words[wordIndex];
      let text = currentWord.substring(0, charIndex);
      display.textContent = text;

      if (!isDeleting && charIndex < currentWord.length) {
        charIndex++;
        setTimeout(typeEffect, speed);
      } else if (isDeleting && charIndex > 0) {
        charIndex--;
        setTimeout(typeEffect, speed / 2);
      } else {
        isDeleting = !isDeleting;
        if (!isDeleting) {
          wordIndex = (wordIndex + 1) % words.length;
        }
        setTimeout(typeEffect, 1000);
      }
    }

    typeEffect();