import React, { useState } from "react";

interface FormData {
  title: string;
  content: string;
}

interface PostPageProps {
  post?: FormData;
  onSave: (data: FormData) => void;
}

const PostPage: React.FC<PostPageProps> = ({ post, onSave }) => {
  const [formData, setFormData] = useState<FormData>(
    post || { title: "", content: "" }
  );

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="">
      <form onSubmit={handleSubmit}>
        <input
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Title"
          className="w-full p-4 mb-2 flex border justify-center text-black text-center font-extrabold text-2xl"
        />
        <textarea
          name="content"
          value={formData.content}
          onChange={handleChange}
          placeholder="This is a story of a Donkey that lives on the internet"
          className="w-full p-2 mb-2 border text-black text-lg"
          rows="10"
        />
        <button
          type="submit"
          className="w-full p-2 mb-2 bg-slate-600 text-cyan-600 text-shadow font-extrabold text-lg rounded"
        >
          Publish  
        </button>
        <button
          type="submit"
          className="w-full p-2 mb-2 bg-slate-600 text-cyan-600 text-shadow font-extrabold text-lg rounded"
        >
          Save
        </button>
      </form>
    </div>
  );
};

export default PostPage;
