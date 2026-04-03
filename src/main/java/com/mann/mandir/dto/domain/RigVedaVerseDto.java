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
public class RigVedaVerseDto {
    private int mandala;
    private int sukta;
    private int stanza;
    private String text;
    private String poet;
    private String deity;
    private String meter;
    private String poetCategory;
    private String deityCategory;
}