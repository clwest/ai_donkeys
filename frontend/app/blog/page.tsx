"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_FLASK_URL;
export default function BlogPage() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch(`${API_URL}/blog/posts`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error("Error in fetching posts");
        }
        const data = await response.json();
        console.log(data);
        setPosts(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchPosts();
  }, []);

  return (
    <div>
      <header>
        <div className="flex items-center justify-between w-full h-16 mt-5"></div>
      </header>
      <div className="max-w-2xl mx-auto">
        {posts.map((post) => (
          <div key={post.id} className="p-4 mb-4 bg-slate-600 shadow-lg">
            <Link href={`/blog/${post.slug}`}>
              <h2 className="text-2xl font-bold text-center text-cyan-500">
                {post.title}
              </h2>
            </Link>
            <h3 className="text-xl font-bold text-center text-cyan-500">
              By: {post.author}
            </h3>
            <p>{post.summary}</p>
            {/* Link to post here*/}
          </div>
        ))}
      </div>
    </div>
  );
}
