import React, { useState, useEffect } from "react";

function App() {
  const [chatId, setChatId] = useState(null);
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  // Create chat session on load
  useEffect(() => {
    fetch("http://backend:5050/create_chat", {
      method: "POST"
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to create chat");
        return res.json();
      })
      .then((data) => {
        setChatId(data.chat_id);
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  // Send query
  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);
    setResponse(null);

    fetch("http://localhost:5050/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chatId, query: question })
    })
      .then((res) => {
        if (!res.ok) throw new Error("Query failed");
        return res.json();
      })
      .then((data) => {
        setResponse(data);
      })
      .catch((err) => {
        setError(err.message);
      });
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>RC Chatbot Test</h1>

      {chatId ? (
        <p>Connected! Chat ID: {chatId}</p>
      ) : error ? (
        <p> {error}</p>
      ) : (
        <p>Connecting...</p>
      )}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask me something"
          style={{ width: "300px", marginRight: "10px" }}
        />
        <button type="submit" disabled={!chatId}>
          Ask
        </button>
      </form>

      {response && (
        <div style={{ marginTop: "2rem" }}>
          <p>
            <strong>Answer:</strong> {response.response || "No answer returned."}
          </p>

          {response.sources && response.sources.length > 0 && (
            <div>
              <strong>Sources:</strong>
              <ul>
                {response.sources.map((src, idx) => (
                  <li key={idx}>
                    <a href={src} target="_blank" rel="noopener noreferrer">
                      {src}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <details style={{ marginTop: "1rem" }}>
            <summary>Raw JSON</summary>
            <pre>{JSON.stringify(response, null, 2)}</pre>
          </details>
        </div>
      )}
    </div>
  );
}

export default App;
