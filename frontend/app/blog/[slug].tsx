"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_FLASK_URL;

export default function PostPage() {
  const [post, setPost] = useState(null);
  const router = useRouter();
  const { slug } = router.query;

  useEffect(() => {

      if (slug) {
        const fetchPost = async () => {
          try {
            const response = await fetch(`${API_URL}/blog/posts/${slug}`);
            if (!response.ok) {
              throw new Error("Error in fetching post");
            }
            const data = await response.json();
            setPost(data);
          } catch (error) {
            console.error(error);
          }
        };
        fetchPost();
    };
         
  }, [slug]);

  if (!post) return <p>Loading...</p>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="p-4 mb-4 bg-slate-500 shadow-lg">
        <h1 className="text-4xl font-bold">{post.title}</h1>
        <div dangerouslySetInnerHTML={{ __html: post.content }} />
        <h3 className="text-xl font-bold">By: {post.author}</h3>
        <p>{post.content}</p>
        {/* Link to post here*/}
      </div>
    </div>
  );
}
