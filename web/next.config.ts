import * as path from "path";

import * as dotenv from "dotenv";
import type { NextConfig } from "next";

const dotenvFile = process.env.DOTENV_FILE;

if (!dotenvFile) {
  throw new Error("DOTENV_FILE environment variable is not defined.");
}

dotenv.config({ path: path.resolve(__dirname, "..", dotenvFile) });

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
