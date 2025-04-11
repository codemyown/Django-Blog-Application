import React, { useEffect, useState } from "react";
import { fetchPosts } from "../api";

const PostList = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetchPosts()
      .then((data) => {
        setPosts(Array.isArray(data) ? data : []);
      })
      .catch((err) => {
        console.error("Error fetching posts:", err);
        setPosts([]);
      });
  }, []);

  return (
    <div>
      <h2>All Posts</h2>
      {posts.map((post) => (
        <div key={post.id}>
          <h3>{post.title}</h3>
          <p>{post.content}</p>
          {post.image && <img src={post.image} alt={post.title} width="200" />}
          <hr />
        </div>
      ))}
    </div>
  );
};

export default PostList;
