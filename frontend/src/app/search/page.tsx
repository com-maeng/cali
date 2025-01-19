"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";

export default function Search() {
  const router = useRouter();

  const handleBackClick = (e) => {
    if (window.history.length > 1) {
      router.back(); // Go to previous page
    } else {
      router.push("/"); // Go to root URL
    }
    console.log(window.history.length);
  };

  return (
    <div className="w-[530] h-dvh flex justify-start items-start bg-[#f7f8f9]">
      <div className="w-full flex items-center justify-start">
        <Image
          src="/back_arrow.svg"
          width={10}
          height={18}
          alt="뒤로가기"
          className="ml-[22px]"
          onClick={handleBackClick}
        />
        <div className="flex w-full items-center h-12 ml-6 mr-4">
          <Image
            src="/search_logo.svg"
            alt="검색"
            width={20}
            height={20}
            className="absolute ml-3.5"
          />
          <input
            type="text"
            placeholder="한글 또는 한자를 입력하세요"
            className="w-full h-full py-3.5 pl-12 rounded-full border-none text-base placeholder:text-[#ADB5BD] shadow-[0_2px_8px_rgba(0,0,0,0.08)] focus:outline-none"
          />
        </div>
      </div>
    </div>
  );
}
