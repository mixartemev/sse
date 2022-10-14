const evtSource = new EventSource("http://127.0.0.1:8000/sse")
const data = document.getElementById("data")

evtSource.onopen = (e) => console.log("Connected.")

evtSource.onmessage = (event) => data.textContent = event.data

evtSource.addEventListener("ping", (event) => data.textContent = `ping: ${event.data}`)

evtSource.onerror = (err) => console.error("EventSource failed:", err)