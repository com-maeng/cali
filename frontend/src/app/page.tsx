import Link from "next/link";
import Image from "next/image";

export default function Home() {
  return (
    <div className="w-[530] h-dvh flex justify-center items-center bg-[#f7f8f9]">
      <main className="w-full h-full flex flex-col items-center justify-center">
        <Image
          src="/cali_logo.svg"
          alt="캘리"
          width={111}
          height={54}
          priority={true}
          className=""
        />
        <div className="w-[80%] my-11">
          <Link href="/search" className="relative flex items-center h-12">
            <Image
              src="/search_logo.svg"
              alt="검색"
              width={22}
              height={22}
              className="absolute ml-5"
            />
            <input
              type="text"
              placeholder="한글 또는 한자를 입력하세요"
              className="w-full h-full py-3.5 pl-[54px] rounded-full border-none text-base placeholder:text-[#ADB5BD] shadow-[0_2px_8px_rgba(0,0,0,0.08)] focus:outline-none"
            />
          </Link>
          {/* <Link // Will be implemented later
            src="/camera_logo.svg"
            alt="카메라"
            width={22}
            height={22}
          ></Link> */}
        </div>
        <div className="top-[52.21vh] flex flex-col items-center w-full">
          <Image
            src="/home_deco_jeonseo.svg"
            alt="데코_전서체"
            width={50}
            height={50}
            className="mb-1"
          />
          <div className="text-[12px] text-gray-600">수레 차, 전서</div>
        </div>
      </main>
    </div>
  );
}
