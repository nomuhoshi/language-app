const textInput = document.getElementById("text-input")
const textDisplay = document.getElementById("text-display")
const sidebar = document.getElementById("sidebar")
const toggleBtn = document.getElementById("toggle-sidebar")
const customPrompt = document.getElementById("custom-prompt")
const aiResponse = document.getElementById("ai-response")

function loadText() {
    const words = textInput.value.split(/(\s+)/)
    textDisplay.innerHTML = words.map(function(token) {
        if (token.trim() === "") return token
        return '<span class="word">' + token + "</span>"
    }).join("")

    textInput.style.display = "none"
    document.getElementById("load-btn").style.display = "none"
    textDisplay.style.display = "block"

    document.querySelectorAll(".word").forEach(function(span) {
        span.addEventListener("click", function() {
            const dragSelected = window.getSelection().toString().trim()
            if (dragSelected.length > 1) return
            document.querySelectorAll(".word").forEach(function(w) {
                w.classList.remove("selected")
            })
            this.classList.add("selected")
            triggerAI(this.innerText.trim())
        })
    })

    let debounceTimer = null
    function handleSelection() {
        const selected = window.getSelection().toString().trim()
        if (selected.length <= 1) return
        clearTimeout(debounceTimer)
        debounceTimer = setTimeout(function() {
            triggerAI(selected)
        }, 300)
    }
    textDisplay.addEventListener("mouseup",handleSelection)
    textDisplay.addEventListener("touchend",handleSelection)
}

textInput.addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault()
        loadText()
    }
})

document.getElementById("load-btn").addEventListener("click", function() {
    loadText()
})

toggleBtn.addEventListener("click",function() {
    if (sidebar.style.display === "none") {
        sidebar.style.display = "flex"
        toggleBtn.innerText = "收起"
    }else{
        sidebar.style.display = "none"
        toggleBtn.innerText = "展开"
    }
})

function triggerAI(selected) {
    if (!selected || selected.length <= 1) return
    const prompt = customPrompt.value || "请解释这个词或短语"
    const context = textDisplay.textContent
    aiResponse.innerText = "思考中..."

    fetch("/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ text: selected, prompt: prompt, context: context })
    })
    .then(function(res) { return res.json() })
    .then(function(data) {
        aiResponse.innerText = data.explanation || data.error
    })
}
