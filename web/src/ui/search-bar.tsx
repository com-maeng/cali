import Link from "next/link";
import Image from "next/image";

export default function SearchBar() {
  return (
    <div className="w-[400px] h-14 border border-[#C7C7CC] rounded-lg ">
      <Link href="/search" className="relative flex items-center h-full w-full">
        <Image
          src="/search_logo.svg"
          alt="검색"
          width={20}
          height={20}
          className="absolute ml-[22px]"
        />
        <input
          type="text"
          placeholder="한글 또는 한자를 입력하세요"
          className="outline-none w-full h-full pl-16 placeholder:text-[#717171] placeholder:text-lg bg-inherit"
        />
      </Link>
      {/* <Link // Will be implemented later
            src="/camera_logo.svg"
            alt="카메라"
            width={22}
            height={22}
          ></Link> */}
    </div>
  );
}
