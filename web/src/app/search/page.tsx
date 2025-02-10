"use client";

import Image from "next/image";
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
        "http://localhost:7700/indexes/hanja/search",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer x0tii5RDPBcoP7PX",
          },
          body: JSON.stringify({ q: value }),
        }
      );
      const data = await response.json();
      const dataList = data.hits
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
        <ul className={"w-full h-60 mt-[30px] bg-white"}>
          {listData.map((item, index) => (
            <li key={index} className="h-12 ml-6">
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
