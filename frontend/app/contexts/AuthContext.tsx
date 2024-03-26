"use client";
import React, { createContext, useContext, useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface UserType {
  id: string;
  username: string;
  email: string;
}

interface AuthContextType {
  user: UserType | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState(null);
  const router = useRouter();
  const API_URL = process.env.NEXT_PUBLIC_FLASK_URL;

  useEffect(() => {
    console.log("User state updated:", user);
  }, [user]);

  const login = async (username: string, password: string) => {
    try {
      const response = await fetch(`${API_URL}/users/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error("Error in login");
      }
      const { access_token, user } = await response.json();

      localStorage.setItem("userToken", access_token);
      setUser(user);
      console.log("Logged in user AuthContext:", user);
    } catch (error) {
      console.error("Login Error: ", error);
    }
  };

  const refreshToken = async () => {
    try {
      const response = await fetch(`${API_URL}/users/refresh`, {
        method: "POST",
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Error in token refresh");
      }
    } catch (e) {
      console.error(e);
    }
  };

  const logout = async () => {
    try {
      const response = await fetch(`${API_URL}/users/logout`, {
        method: "POST",
        credentials: "include",
      });
      if (!response.ok) {
        throw new Error("Failed to log out");
      }
      localStorage.removeItem("userToken");
      setUser(null);
      router.push("/login");
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
};
