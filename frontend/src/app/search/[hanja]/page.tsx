import Image from "next/image";
import Link from "next/link";

export default async function Page() {
  const hanjaImageWidth = 105;
  const hanjaImageHeight = 105;

  return (
    <div className="w-full h-full flex flex-col items-center justify-start">
      <Link href="/" className="w-[51px] h-6 mt-12">
        <Image
          src="/cali_logo_small.svg"
          alt="캘리"
          width={51}
          height={24}
          priority={true}
        />
      </Link>
      <Link
        href="/search"
        className="w-[calc(100%-32px)] relative flex items-center h-12 mt-3 mx-4"
      >
        <Image
          src="/search_logo.svg"
          alt="검색"
          width={20}
          height={20}
          className="absolute ml-5"
        />
        <input
          type="text"
          placeholder="한글 또는 한자를 입력하세요"
          className="w-full h-full py-3.5 pl-[54px] rounded-full border-none text-base placeholder:text-[#ADB5BD] shadow-[0_2px_8px_rgba(0,0,0,0.08)] focus:outline-none"
        />
      </Link>
      <div className="w-full h-10 mt-2 flex justify-center">
        <button className="h-10 w-1/5 flex justify-center items-center border-b-2 border-[#212529] font-bold">
          <span>전서</span>
        </button>
        <button className="h-10 w-1/5 flex justify-center items-center border-b-2 border-[#DEE2E6]">
          <span>예서</span>
        </button>
        <button className="h-10 w-1/5 flex justify-center items-center border-b-2 border-[#DEE2E6]">
          <span>해서</span>
        </button>
        <button className="h-10 w-1/5 flex justify-center items-center border-b-2 border-[#DEE2E6]">
          <span>행서</span>
        </button>
        <button className="h-10 w-1/5 flex justify-center items-center border-b-2 border-[#DEE2E6]">
          <span>초서</span>
        </button>
      </div>
      <div className="w-[343px] mt-5 grid grid-cols-3 gap-x-[14px] gap-y-[22px]">
        <div className="w-full h-[133px] flex flex-col items-center">
          <Image
            src="/hanja_image_placeholder.png"
            alt="한자 이미지 땜빵" // Replace this
            width={hanjaImageWidth}
            height={hanjaImageHeight}
            priority={true}
          />
          <span className="mt-3">사신비</span>
        </div>
        <div className="w-full h-[133px] flex flex-col items-center">
          <Image
            src="/hanja_image_placeholder.png"
            alt="한자 이미지 땜빵" // Replace this
            width={hanjaImageWidth}
            height={hanjaImageHeight}
            priority={true}
          />
          <span className="mt-3">사신비</span>
        </div>
        <div className="w-full h-[133px] flex flex-col items-center">
          <Image
            src="/hanja_image_placeholder.png"
            alt="한자 이미지 땜빵" // Replace this
            width={hanjaImageWidth}
            height={hanjaImageHeight}
            priority={true}
          />
          <span className="mt-3">사신비</span>
        </div>
        <div className="w-full h-[133px] flex flex-col items-center">
          <Image
            src="/hanja_image_placeholder.png"
            alt="한자 이미지 땜빵" // Replace this
            width={hanjaImageWidth}
            height={hanjaImageHeight}
            priority={true}
          />
          <span className="mt-3">사신비</span>
        </div>
      </div>
    </div>
  );
}
