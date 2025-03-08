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
      <div className="w-full h-14 flex items-center justify-start border-b border-[#C7C7CC]">
        <Image
          src="/back_arrow.svg"
          width={12}
          height={20}
          alt="뒤로가기"
          className="ml-6"
          onClick={handleBackClick}
        />
        <div className="flex w-full items-center h-full ml-[27px]">
          <input
            type="text"
            value={userInput}
            onChange={handleUserInputChange}
            placeholder="한글 또는 한자를 입력하세요"
            className="w-full h-full border-none text-base placeholder:text-[#717171] focus:outline-none bg-inherit"
            autoFocus
          />
          {/* TODO: Add `x` button */}
        </div>
      </div>
      {listData.length > 0 && (
        <div className={"w-full h-[280]px mt-2 flex-col px-6"}>
          {listData.map((item, index) => (
            <Link
              key={index}
              href={`${process.env.NEXT_PUBLIC_APP_URL}/search/${item}`}
              className="w-full h-14 flex justify-start items-center"
            >
              <Image
                src="/search_logo.svg"
                alt="Search icon"
                width={20}
                height={20}
                className="inline"
              />
              <span className="w-[18px] text-lg ml-5">{item.slice(0, 1)}</span>
              <span className="text-lg ml-3">{item.slice(1)}</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
