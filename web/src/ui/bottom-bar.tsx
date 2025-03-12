import Link from "next/link";
import Image from "next/image";

export default function BottomBar() {
  return (
    <div className="w-[440px] h-[60px] flex justify-start items-center">
      <Link
        href="/"
        className="w-[110px] h-full flex justify-center items-center"
      >
        <Image src={"/home_icon.svg"} alt="" width={18} height={20} />
      </Link>
      <Link
        href="/search"
        className="w-[110px] h-full flex justify-center items-center"
      >
        <Image src={"/search_icon.svg"} alt="" width={20} height={20} />
      </Link>
      <Link
        href="/collection"
        className="w-[110px] h-full flex justify-center items-center"
      >
        <Image src={"/collection_icon.svg"} alt="" width={18} height={20} />
      </Link>
      <Link
        href="/profile"
        className="w-[110px] h-full flex justify-center items-center"
      >
        <Image src={"/user_icon.svg"} alt="" width={20} height={20} />
      </Link>
    </div>
  );
}
