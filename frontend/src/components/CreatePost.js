import React, { useState } from "react";
import { createPost } from "../api";

const CreatePost = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);
    if (image) formData.append("image", image);

    const result = await createPost(formData);

    console.log("Post creation result:", result); // ✅ result is in scope
    alert(JSON.stringify(result, null, 2)); // ✅ only use it after it's defined

    if (result.id) {
      alert("✅ Post created!");
      setTitle("");
      setContent("");
      setImage(null);
    } else {
      alert(result.error || "❌ Failed to create post.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create New Post</h2>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title"
        required
      />
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Content"
        required
      />
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImage(e.target.files[0])}
      />

      <button type="submit">Create</button>
    </form>
  );
};

export default CreatePost;
