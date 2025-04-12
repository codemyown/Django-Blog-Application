import React, { useState, useEffect } from "react";
import LoginForm from "./components/LoginForm";
import CreatePost from "./components/CreatePost";
import PostList from "./components/PostList";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [refreshPosts, setRefreshPosts] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const exp = localStorage.getItem("token_exp");
    const now = Math.floor(Date.now() / 1000);

    if (!token || now > exp) {
      alert(" Session expired. Please log in again.");
      localStorage.clear();
      setIsLoggedIn(false);
    } else {
      setIsLoggedIn(true);
    }
  }, []);

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        backgroundColor: "#121212",
        color: "#39ff14",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      }}
    >
      <div
        style={{
          flex: 1,
          padding: "2rem",
          borderRight: "2px solid #39ff14",
        }}
      >
        <h1 style={{ fontSize: "2rem", color: "#39ff14" }}>My Blog</h1>

        {!isLoggedIn ? (
          <>
            <h3 style={{ color: "#39ff14" }}>Login to continue</h3>
            <LoginForm onLogin={() => setIsLoggedIn(true)} />
          </>
        ) : (
          <>
            <h3 style={{ color: "#39ff14" }}>Create a New Post</h3>
            <CreatePost
              onPostCreated={() => setRefreshPosts((prev) => !prev)}
            />
          </>
        )}
      </div>

      <div
        style={{
          flex: 2,
          padding: "2rem",
          overflowY: "scroll",
          backgroundColor: "#1a1a1a",
        }}
      >
        <PostList refreshTrigger={refreshPosts} />
      </div>
    </div>
  );
}

export default App;
