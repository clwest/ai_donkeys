"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_FLASK_URL;

interface FormData {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  password: string;
  confirmPassword: string;
}

const RegisterForm: React.FC = () => {
  const router = useRouter();
  const [data, setData] = useState<FormData>({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    date_of_birth: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const registerUser = async (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    const { confirmPassword, ...userData } = data;
    if (userData.password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/users/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        throw new Error("Error in register");
      }
      console.log(response);
      const userInfo = await response.json();
      console.log(userInfo);
      router.push("/login");
    } catch (error) {
      console.error("Registration Error: ", error);
    }
  };

  return (
    <>
      <div className="flex flex-col justify-center items-center h-screen bg-gray-600 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <h2 className="mt-10 text-2xl font-bold leading-9 tracking-tight text-center text-slate-400">
            Register Account
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" onSubmit={registerUser}>
            <div>
              <label
                htmlFor="name"
                className="block text-lg font-medium leading-6 text-slate-400 sr-only"
              >
                Username
              </label>
              <div className="mt-2">
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  value={data.username}
                  onChange={handleChange}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-4 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-slate-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-lg font-medium leading-6 text-slate-400 sr-only"
              >
                Email address
              </label>
              <div className="mt-2">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={data.email}
                  onChange={handleChange}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-4 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-4 focus:ring-inset focus:ring-slate-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>
            <div>
              <label
                htmlFor="first_name"
                className="block text-lg font-medium leading-6 text-slate-400 sr-only"
              >
                First Name
              </label>
              <div className="mt-2">
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  required
                  value={data.first_name}
                  onChange={handleChange}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-4 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-slate-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="last_name"
                className="block text-lg font-medium leading-6 text-slate-400 sr-only"
              >
                Last Name
              </label>
              <div className="mt-2">
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  required
                  value={data.last_name}
                  onChange={handleChange}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-4 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-slate-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>
            <div>
              <label
                htmlFor="date_of_birth"
                className="block text-lg font-medium leading-6 text-slate-400 sr-only"
              >
                Date of Birth
              </label>
              <div className="mt-2">
                <input
                  id="date_of_birth"
                  name="date_of_birth"
                  type="date"
                  required
                  value={data.date_of_birth}
                  onChange={handleChange}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-4 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-slate-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label
                  htmlFor="password"
                  className="block text-lg font-medium leading-6 text-slate-400"
                >
                  Password
                </label>
                <div className="text-sm"></div>
              </div>
              <div className="mt-2">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={data.password}
                  onChange={handleChange}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-4 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-slate-600 sm:text-sm sm:leading-6"
                />
              </div>
              <div className="flex items-center justify-between">
                <label
                  htmlFor="password"
                  className="block text-lg font-medium leading-6 text-slate-400"
                >
                  Confirm Password
                </label>
                <div className="text-sm"></div>
              </div>
              <div className="mt-2">
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  required
                  value={data.confirmPassword}
                  onChange={handleChange}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-4 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-slate-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-slate-400 px-3 py-1.5 text-sm font-semibold leading-6 text-slate-300 shadow-sm hover:bg-slate-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-600"
              >
                Register
              </button>
            </div>
            <Link
              className="mt-3 text-sm text-right text-amber-500"
              href={"/login"}
            >
              Already have an account? <span className="underline">Login</span>
            </Link>
          </form>
        </div>
      </div>
    </>
  );
};

export default RegisterForm;
