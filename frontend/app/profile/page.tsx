"use client";
import React from "react";
import Link from "next/link";
import { useAuth } from "../contexts/AuthContext";
import ProfileBot from "../components/ProfileBot";

export default function Profile() {
  const { user } = useAuth();
  return (
    <main className="container flex flex-col min-h-screen">
      {/* <header>
        <div className="flex items-center justify-between w-full h-16 mt-5"></div>
      </header> */}
      <p className="p-5 text-xl italic font-extrabold text-center text-slate-400">
        This is where chatbots, saved blogs and favorited stuff will live.
      </p>
      <div>
        <section className="flex justify-center space-x-10">
          <div className="flex flex-col items-center">
            <h2 className="text-3xl italic font-extrabold text-center text-cyan-700">
              Blogs
            </h2>
            <Link href="/blog/create">
              <button className="w-18 p-2 mb-2 mt-5 bg-slate-600 text-cyan-600 text-shadow font-extrabold text-lg rounded">
                Create Post
              </button>
            </Link>
          </div>
          <div className="flex flex-col items-center">
            <h2 className="text-3xl italic font-extrabold text-center text-cyan-700">
              ChatBots
            </h2>
            <Link href="/chatbots">
              <button className="w-18 p-2 mb-2 mt-5 bg-slate-600 text-cyan-600 text-shadow font-extrabold text-lg rounded">
                ChatBots
              </button>
            </Link>
          </div>
        </section>
      </div>
      <section className="flex flex-col items-center justify-between min-h-screen px-24 py-5">
        <ProfileBot />
      </section>
    </main>
  );
}
