"use client";
import { useState, useEffect } from "react";


export default function CryptoCards() {
  const [articles, setArticles] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  const fetchArticles = async () => {
    try {
      const res = await fetch("/api/cryptonews/regulations");
      const articleInfo = await res.json();

      setArticles(articleInfo);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, []);

  const nextArticles = () => {
    setCurrentIndex((currentIndex + 3) % articles.length);
  };

  const prevArticles = () => {
    setCurrentIndex((currentIndex - 3 + articles.length) % articles.length);
  };

  return (
    <div className="relative">
      <h1 className="mt-3 text-4xl text-center font-extrabold p-2 text-cyan-700">
        News
      </h1>
      <button
        onClick={prevArticles}
        className="mt-5 font-extrabold text-lg text-cyan-500"
      >
        Previous
      </button>
      <button
        onClick={nextArticles}
        className="mt-5 font-extrabold text-lg absolute right-0 text-cyan-500"
      >
        Next
      </button>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {articles
          .slice(currentIndex, currentIndex + 3)
          .map((article, index) => (
            <div
              key={index}
              className="bg-slate-700 p-4 rounded-lg shadow-lg mb-4 card-body border border-spacing-1 border-cyan-300"
            >
              <h3 className="text-lg font-bold mt-2 text-cyan-400 card">
                {article.source}
              </h3>
              <a
                href={article.news}
                className="text-cyan-300"
                target="_blank"
                rel="noopener noreferrer"
              >
                <img
                  src={article.image}
                  alt={article.title}
                  className="w-full h-40 object-cover rounded"
                />
                <h2 className="text-xl font-bold mt-2 text-cyan-300">
                  {article.title}
                </h2>
                <h5 className="text-cyan-500">
                  {article.date}
                  <br />
                  {article.sentiment}
                </h5>
                Read more
              </a>
            </div>
          ))}
      </div>
    </div>
  );
}
