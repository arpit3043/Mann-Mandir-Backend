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
class ChalisaDto {
    private String id;
    private String deity;
    private String title;
    private List<ChalisaVerseDto> verses;
    private int totalVerses;
}
