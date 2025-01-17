package com.cali.gcp;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.cali.repository.ImageResponse;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.Blob;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class GcsService {

    private final Storage gcsClient;
    private final int IMG_LIMIT = 12;

    public List<ImageResponse> getImages(String folderPath, int offset) {
        String bucketName = System.getenv("HANJA_BUCKET");
        List<ImageResponse> images = new ArrayList<>();
        Iterable<Blob> blobsIterable = gcsClient.list(bucketName).iterateAll();
        for (Blob blob : blobsIterable) {
            if (blob.getName().startsWith(folderPath) && blob.getName().endsWith(".webp")) {
                byte[] imageBytes = blob.getContent();
                String imageString = blob.getName();
                String lastSegment = imageString.substring(imageString.lastIndexOf("/") + 1);

                String[] artistArtwork = lastSegment.split("_");
                String artist = artistArtwork[0];
                String artwork = artistArtwork[1];

                ImageResponse imageResponse = new ImageResponse();
                imageResponse.setArtist(artist);
                imageResponse.setArtwork(artwork);
                imageResponse.setImage(imageBytes);
                images.add(imageResponse);
            }
        }
        return paginate(images, offset);
    }

    public List<ImageResponse> paginate(List<ImageResponse> imgs, int offset) {
        List<ImageResponse> resImgs = new ArrayList<>();

        int blobSize = imgs.size();
        if (offset >= blobSize) {
            return resImgs;
        }

        int endIdx = Math.min(offset + IMG_LIMIT, blobSize);
        for (int i = offset; i < endIdx; i++) {
            resImgs.add(imgs.get(i));
        }

        return resImgs;
    }

}
