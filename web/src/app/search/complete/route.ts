import { request } from "http";

import { NextRequest, NextResponse } from "next/server";

interface MeilisearchSearchResult {
  hits: string[];
  query: string;
  processingTimeMs: number;
  limit: number;
  offset: number;
  estimatedTotalHits: number;
}

export async function POST(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const query = searchParams.get("q");

  if (!query) {
    return NextResponse.json(
      { error: 'Query parameter "q" is required' },
      { status: 400 }
    );
  }

  const data = JSON.stringify({
    q: query,
  });
  const options = {
    hostname: process.env.MEILI_HOST,
    port: process.env.MEILI_PORT,
    path: "/indexes/hanja/search",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.MEILI_MASTER_KEY}`,
    },
  };

  try {
    const result = await new Promise<MeilisearchSearchResult>(
      (resolve, reject) => {
        const req = request(options, (res) => {
          let responseData = "";

          res.on("data", (chunk) => {
            responseData += chunk;
          });
          res.on("end", () => {
            if (
              res.statusCode &&
              res.statusCode >= 200 &&
              res.statusCode < 300
            ) {
              resolve(JSON.parse(responseData));
            } else {
              reject(new Error(`HTTP error! status: ${res.statusCode}`));
            }
          });
        });

        req.on("error", (error) => {
          reject(error);
        });
        req.write(data);
        req.end();
      }
    );

    return NextResponse.json(result.hits);
  } catch (error) {
    return NextResponse.json(
      { error: (error as Error)?.message },
      { status: 500 }
    );
  }
}
