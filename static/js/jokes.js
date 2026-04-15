function hideElement(name) {
    document.getElementById(name).classList.add("hidden");
}

function showElement(name) {
    document.getElementById(name).classList.remove("hidden");
}

function toggleElementById(id) {
    document.getElementById(id).classList.toggle("hidden");
}

function showLoadingScreen() {
    document.getElementById('loadingScreen').style.display = 'flex';
}

function hideLoadingScreen() {
    document.getElementById('loadingScreen').style.display = 'none';
}

function swapJoke(question, answer) {
    document.getElementById("joke-question").innerText = question;
    let answerEl = document.getElementById("joke-answer");
    answerEl.innerText = answer;

    let revealBtn = document.getElementById("reveal-btn");
    if (answer && answer.trim()) {
        answerEl.classList.add("hidden");
        if (!revealBtn) {
            revealBtn = document.createElement("button");
            revealBtn.id = "reveal-btn";
            revealBtn.onclick = revealAnswer;
            revealBtn.className = "mt-4 px-4 py-2 bg-amber-400 text-white text-sm font-semibold rounded-full shadow hover:bg-amber-500 transition";
            revealBtn.textContent = "Reveal";
            answerEl.parentElement.appendChild(revealBtn);
        } else {
            revealBtn.classList.remove("hidden");
        }
    } else {
        answerEl.classList.remove("hidden");
        if (revealBtn) revealBtn.classList.add("hidden");
    }
}

function revealAnswer() {
    showElement("joke-answer");
    let btn = document.getElementById("reveal-btn");
    if (btn) btn.classList.add("hidden");
}

function splitJoke(joke) {
    if (!joke.includes("?")) {
        return [joke, ""];
    }
    let parts = joke.split(/(\?)/);
    let question = parts.slice(0, parts.length - 1).join("");
    let answer = parts[parts.length - 1];
    return [question, answer];
}

async function countJokes2() {
    document.getElementById("joke-full").innerText = "";
    document.getElementById("joke-question").innerText = "";
    document.getElementById("joke-answer").innerText = "";
    document.getElementById("explanation").innerText = "";
    document.getElementById("joke-image").src = "";
    delete document.getElementById("joke-image").dataset.loaded;
    document.getElementById("joke-audio").src = "";
    hideElement("joke-explanation");
    hideElement("image-explanation");

    showLoadingScreen();
    const response = await fetch("/laugh");
    const data = await response.json();
    hideLoadingScreen();

    let joke = data["joke"];
    document.getElementById("joke-full").innerText = joke;
    let [question, answer] = splitJoke(joke);
    swapJoke(question, answer);
}

async function getExplanation() {
    let joke = document.getElementById("joke-full");
    let explanation = document.getElementById("explanation");

    if (joke && explanation.innerText === "") {
        showLoadingScreen();
        const safeJoke = encodeURIComponent(joke.innerText);
        const response = await fetch("/explain?joke=" + safeJoke);
        const data = await response.json();
        hideLoadingScreen();
        explanation.innerText = data["text"];
    }

    toggleElementById("joke-explanation");
}

function clearAudio() {
    document.getElementById("joke-audio").src = "";
}

async function getAudio() {
    let joke = document.getElementById("joke-full");
    let audio = document.getElementById("joke-audio");

    if (joke && (!audio.src || audio.src === window.location.href)) {
        showLoadingScreen();
        const safeJoke = encodeURIComponent(joke.innerText);
        const voice = document.getElementById("voice-select").value;
        const response = await fetch("/read?joke=" + safeJoke + "&voice=" + voice);
        const data = await response.json();
        hideLoadingScreen();
        audio.src = data["audio_path"];
    }

    if (!audio.paused) {
        audio.pause();
    } else {
        audio.play();
    }
}

async function getImage() {
    let joke = document.getElementById("joke-full");
    let image = document.getElementById("joke-image");

    if (joke && !image.dataset.loaded) {
        showLoadingScreen();
        const safeJoke = encodeURIComponent(joke.innerText);
        const response = await fetch("/draw?joke=" + safeJoke);
        const data = await response.json();
        image.src = data["image_url"];
        await new Promise(resolve => { image.onload = resolve; });
        image.dataset.loaded = "1";
        hideLoadingScreen();
        showElement("image-explanation");
    } else {
        toggleElementById("image-explanation");
    }
}
