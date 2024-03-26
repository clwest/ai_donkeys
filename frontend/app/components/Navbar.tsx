"use client";
import React, { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import Modal from "./Modal";
import AuthForm from "./Auth/AuthForm";
import { useAuth } from "../contexts/AuthContext";

interface User {
  username: string;
}

interface NavbarProps {
  user?: User | null;
}

const DropdownLink: React.FC<{
  title: string;
  links: Array<{ href: string; label: string }>;
}> = ({ title, links }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      <button onClick={() => setIsOpen(!isOpen)}>{title}</button>

      {isOpen && (
        <div className="absolute left-0 mt-2  w-48 bg-white rounded-md shadow-xl z-20">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

const Navbar: React.FC<NavbarProps> = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { user, logout } = useAuth();
  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <nav className="flex justify-center bg-slate-600 dark:bg-slate-700 dark:border-slate-600">
      <div className="grid h-full max-w-lg grid-cols-4 mx-auto font-bold">
        <Link
          href="/"
          className="inline-flex flex-col items-center justify-center px-5 hover:bg-slate-400 dark:hover:bg-slate-800"
        >
          Home
        </Link>
        <DropdownLink
          title="Blogs"
          links={[
            { href: "/blog", label: "Blogs" },
            { href: "/blog/ai", label: "AI" },
            { href: "/blog/blockchain", label: "Blockchain" },
            // Add more links as needed
          ]}
          className="inline-flex flex-col items-center justify-center px-5 hover:bg-slate-400 dark:hover:bg-slate-800"
        />
        <DropdownLink
          title="Images"
          links={[
            { href: "/images", label: "Images" },
            { href: "/blog/ai", label: "AI" },
            { href: "/blog/blockchain", label: "Blockchain" },
            // Add more links as needed
          ]}
          className="inline-flex flex-col items-center justify-center px-5 hover:bg-slate-400 dark:hover:bg-slate-800"
        />
        <Link
          href="/profile"
          className="inline-flex flex-col items-center justify-center px-5 hover:bg-slate-400 dark:hover:bg-gray-800"
        >
          Profile
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
