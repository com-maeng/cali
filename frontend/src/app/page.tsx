import Image from 'next/image';

export default function Home() {
  return (
    <div className="w-full min-h-screen flex justify-center items-center">
      <div className="w-[100vw] h-[100vh]">
        <main className="w-full h-full flex flex-col items-center">
          <Image 
            src="/cali_logo.svg" 
            alt="캘리" 
            width={111}
            height={54}
            priority={true}
            className="mt-[29.31vh]"
          />
          <div className="absolute top-[39.4vh] w-[80%]">
            <div className="relative flex items-center">
              <input 
                type="text"
                placeholder="한글 또는 한자를 입력하세요"
                className="w-full py-[1.4vh] px-[5vh] rounded-full border-none text-[1.6vh] placeholder:text-[#ADB5BD] shadow-[0_2px_8px_rgba(0,0,0,0.08)] focus:outline-none"
              />
              <div className="absolute left-[2vh]">
                <Image 
                  src="/search_logo.svg" 
                  alt="검색" 
                  width={22}
                  height={22}
                />
              </div>
              {/* <div className="absolute right-[2vh]">
                <Image 
                  src="/camera_logo.svg" 
                  alt="카메라" 
                  width={22}
                  height={22}
                />
              </div> */}
            </div>
          </div>
          <div className="absolute top-[52.21vh] flex flex-col items-center w-full">
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
    </div>
  );
}
