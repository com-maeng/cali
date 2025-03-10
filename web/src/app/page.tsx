import Image from "next/image";

import SearchBar from "@/ui/search-bar";

export default function Home() {
  return (
    <main className="w-full h-full flex flex-col items-center justify-start pt-[242px]">
      <Image
        src="/cali_logo.svg"
        alt="캘리"
        width={105}
        height={50}
        priority={true}
        className=""
      />
      <div className="mt-12">
        <SearchBar />
      </div>
    </main>
  );
}
