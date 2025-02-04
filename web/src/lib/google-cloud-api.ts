import { Storage, Bucket, File } from "@google-cloud/storage";

export async function getHanjaImageFiles(
  hanja: {
    hun: string;
    eum: string;
  },
  style: "seal" | "clerical" | "regular" | "semi-cursive" | "cursive",
  pageToken: string | null
): Promise<{
  files: File[] | null;
  nextPageToken: string | null;
}> {
  const storage: Storage = new Storage({
    keyFilename: process.env.SERVICE_ACCOUNT_KEY_NAME + ".json",
  });
  const hanjaBucketName: string = process.env.HANJA_BUCKET || "";
  const bucket: Bucket = storage.bucket(hanjaBucketName);

  let files: File[] | null = null;
  let nextPageToken: string | null = null;

  try {
    const [fetchedFiles, nextQuery] = await bucket.getFiles({
      matchGlob: [hanja.hun, hanja.eum, style].join("/") + "/" + "*.webp",
      autoPaginate: false, // To limit maximum number of the results
      maxResults: 12,
      ...(pageToken ? { pageToken: pageToken } : {}),
    });

    files = fetchedFiles;
    nextPageToken = nextQuery?.pageToken || null;
  } catch (error) {
    console.error("Error fetching files: ", error);
  } finally {
    return { files, nextPageToken };
  }
}
