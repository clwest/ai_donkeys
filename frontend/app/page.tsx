import { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import poker from "../public/poker.png";
import study from "../public/study.png";
import SearchBar from "./components/SearchBar";
import Navbar from "./components/Navbar";

export const metadata: Metadata = {
  title: "Donkey Betz",
};

export default async function Home() {
  return (
    <div>
      <main className="container flex flex-col min-h-screen w-screen">
        {/* <header>
          <div className="flex items-center justify-between w-full h-16 mt-5"></div>
        </header> */}

        <div className="p-4 text-xl italic font-extrabold text-center text-cyan-500">
          <Image src={study} alt="study" width={350} height={350} />
        </div>

        <div className="container flex items-center justify-between space-x-3 mt-7 flex-co"></div>
      </main>
    </div>
  );
}
