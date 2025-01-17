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

    public List<ImageResponse> getImages(String folderPath) {
        String bucketName = System.getenv("HANJA_BUCKET");
        List<ImageResponse> images = new ArrayList<>();

        Iterable<Blob> blobs = gcsClient.list(bucketName).iterateAll();
        for (Blob blob : blobs) {
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
        return images;
    }

}
