const textInput = document.getElementById("text-input")
const textDisplay = document.getElementById("text-display")
const sidebar = document.getElementById("sidebar")
const toggleBtn = document.getElementById("toggle-sidebar")
const customPrompt = document.getElementById("custom-prompt")
const aiResponse = document.getElementById("ai-response")

textInput.addEventListener("keydown",function(e) {
    if (e.key === "Enter" && !e.shiftKey){
        e.preventDefault()
        textDisplay.innerText = textInput.value
        textInput.style.display = "none"
        textDisplay.style.display = "block"
    }
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

document.addEventListener("selectionchange",function(){
    const selected = window.getSelection().toString().trim()

    if (selected.length <= 1) return

    const prompt = customPrompt.value || "请解释这个词或短语"

    aiResponse.innerText = "思考中..."

    fetch("/explain",{
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body:JSON.stringify({ text: selected, prompt: prompt })
    })
    .then(function(res) { return res.json() })
    .then(function(data) {
        aiResponse.innerText = data.explanation || data.error
    })
})