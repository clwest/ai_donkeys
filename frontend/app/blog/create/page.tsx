"use client";
import React from "react";
import BlogForm from "../../components/BlogForm";

const API_URL = process.env.NEXT_PUBLIC_FLASK_URL;
export default function CreatePostPage() {
  const handleSave = async (postData) => {
    try {
      const token = localStorage.getItem("userToken");
      console.log("Token is: ", token);
      const response = await fetch(`${API_URL}/blog/posts`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(postData),
      });
      console.log("The response is: ", response);
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Server Response: ", errorData);
        throw new Error(
          `Error in saving post: ${errorData.message} || 'Unknown error'`
        );
      }
      const data = await response.json();
      console.log("Post Saved successfully: ", data);
    } catch (error) {
      console.error("Error in handleSave: ", error);
    }
  };

  return (
    <div>
      <header>
        <div className="flex items-center justify-between w-full h-16 mt-5"></div>
      </header>
      <h1 className="text-center font-extrabold text-cyan-600 text-3xl">
        Create a new post
      </h1>
      <BlogForm onSave={handleSave} />
    </div>
  );
}
