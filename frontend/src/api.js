const BASE_URL = process.env.REACT_APP_API_URL;

console.log("Calling API:", `${BASE_URL}/posts/`);

export const fetchPosts = async () => {
  const res = await fetch(`${BASE_URL}/posts/`);
  if (!res.ok) {
    console.warn("Failed to fetch posts:", res.status);
    return [];
  }
  return res.json();
};

export const registerUser = async (email, username, password) => {
  const formData = new FormData();
  formData.append("email", email);
  formData.append("username", username);
  formData.append("password", password);

  const res = await fetch(`${BASE_URL}/api/register/`, {
    method: "POST",
    body: formData,
  });

  return res.json(); // success or error
};

export const loginUser = async (username, password) => {
  const res = await fetch(`${BASE_URL}/api/token/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await res.json();

  console.log("Login response:", data); // ✅ Log the response

  if (res.ok && data.access) {
    console.log("Saving token:", data.access); // ✅ Confirm this logs
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
  } else {
    console.warn("Login failed:", data);
  }

  return data;
};

export const createPost = async (formData) => {
  const token = localStorage.getItem("access_token");
  console.log("Using token:", token); // ✅ Debug

  if (!token) {
    return { error: "User not authenticated. No access token found." };
  }

  const res = await fetch(`${BASE_URL}/posts/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`, // ✅ Bearer format is required
    },
    body: formData,
  });

  const data = await res.json();

  if (!res.ok) {
    console.error("Post creation failed:", data);
  }

  return data;
};
