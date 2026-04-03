package com.mann.mandir.dto.domain;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UpanishadVerseDto {
    private String upanishadId;
    private int chapter;
    private int verse;
    private String sanskrit;
    private String transliteration;
    private String translation;
    private String commentary;
}
