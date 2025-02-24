"use client";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { useState } from "react";

export default function Search() {
  const router = useRouter();
  const [userInput, setUserInput] = useState("");
  const [listData, setListData] = useState<string[]>([]);

  const handleUserInputChange = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = e.target.value;

    if (value === "") {
      setUserInput("");
      setListData([]);
      return;
    }

    setUserInput(value);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_APP_URL}/search/complete?q=${value}`,
        {
          method: "POST",
        }
      );
      const data = await response.json();
      const dataList = data
        .slice(0, 5) // Top 5
        .map(
          (obj: { hanja_id: number; hanja_hun_eum: string }) =>
            obj.hanja_hun_eum
        );

      setListData(dataList);
    } catch (error) {
      console.error("Error calling search API: ", error);
    }
  };

  const handleBackClick = () => {
    if (window.history.length > 1) {
      router.back(); // Go to previous page
    } else {
      router.push("/"); // Go to root URL
    }
  };

  return (
    <div className="w-full h-full flex flex-col justify-start items-start">
      <div className="w-full flex items-center justify-start">
        <Image
          src="/back_arrow.svg"
          width={10}
          height={18}
          alt="뒤로가기"
          className="ml-4"
          onClick={handleBackClick}
        />
        <div className="flex w-full items-center h-12 ml-4 mr-4">
          <Image
            src="/search_logo.svg"
            alt="검색"
            width={20}
            height={20}
            className="absolute ml-3.5"
          />
          <input
            type="text"
            value={userInput}
            onChange={handleUserInputChange}
            placeholder="한글 또는 한자를 입력하세요"
            className="w-full h-full py-3.5 pl-12 rounded-full border-none text-base placeholder:text-[#ADB5BD] shadow-[0_2px_8px_rgba(0,0,0,0.08)] focus:outline-none"
            autoFocus
          />
        </div>
      </div>
      {listData.length > 0 && (
        <div className={"w-full h-60 mt-[30px] bg-white flex-col"}>
          {listData.map((item, index) => (
            <Link
              key={index}
              href={`${process.env.NEXT_PUBLIC_APP_URL}/search/${item}`}
              className="h-12 ml-6 block"
            >
              {item}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
