package com.mann.mandir.dto.god;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AartiDto {
    private String id;
    private String name;
    private String deity;
    private String devanagari;
    private String transliteration;
    private String translation;
    private String language;
    private String audioUrl;
    private List<String> verses;
}
