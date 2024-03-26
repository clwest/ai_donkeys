import { useEffect, useState } from "react";

export function LikeDislikeComponent({ imageId }) {
  const [likes, setLikes] = useState(0);
  const [dislikes, setDislikes] = useState(0);

  const handleLike = async () => {
    try {
      await fetch(`/api/huggingface/image/database`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ imageId }),
      });
      setLikes((prev) => prev + 1);
    } catch (error) {
      console.error("Failed to like", error);
    }
  };

  const handleDislike = async () => {
    try {
      await fetch(`/api/huggingface/image/database`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ imageId }),
      });
      setDislikes((prev) => prev + 1);
    } catch (error) {
      console.error("Failed to dislike", error);
    }
  };

  return (
    <div>
      <button onClick={handleLike}>👍 ({likes})</button>
      <button onClick={handleDislike}>👎 ({dislikes})</button>
    </div>
  );
}
