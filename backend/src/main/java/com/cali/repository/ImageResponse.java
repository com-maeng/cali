package com.cali.repository;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ImageResponse {
    private String artist;
    private String artwork;
    private byte[] image;
}
