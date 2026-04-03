package com.mann.mandir.controller;

import com.mann.mandir.constants.RestEndpointConstants;
import com.mann.mandir.dto.ApiResponse;
import com.mann.mandir.dto.domain.ChalisaDto;
import com.mann.mandir.dto.domain.ChalisaVerseDto;
import com.mann.mandir.dto.domain.MantraDto;
import com.mann.mandir.dto.domain.StotramDto;
import com.mann.mandir.dto.god.AartiDto;
import com.mann.mandir.service.GodService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping(RestEndpointConstants.GOD)
@Tag(name = "God", description = "Devotional content: Aarti, Chalisa, Stotrams, Mantras")
public class GodController {

    private final GodService godService;

    @GetMapping(RestEndpointConstants.AARTIS)
    @Operation(summary = "List all aartis", description = "Returns all aartis, optionally filtered by deity")
    public ResponseEntity<ApiResponse<List<AartiDto>>> getAllAartis(
            @RequestParam(required = false)
            @Parameter(description = "Filter by deity name") String deity,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {

        List<AartiDto> data = godService.getAartis(deity, page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping(RestEndpointConstants.AARTIS + "/{aartiId}")
    @Operation(summary = "Get aarti by ID")
    public ResponseEntity<ApiResponse<AartiDto>> getAartiById(@PathVariable String aartiId) {
        return ResponseEntity.ok(ApiResponse.ok(godService.getAartiById(aartiId)));
    }

    @GetMapping(RestEndpointConstants.AARTIS_BY_DEITIES)
    @Operation(summary = "List aarti deities")
    public ResponseEntity<ApiResponse<List<String>>> getAartiDeities() {
        return ResponseEntity.ok(ApiResponse.ok(godService.getAartiDeities()));
    }

    @GetMapping("/chalisas")
    @Operation(summary = "List all chalisas")
    public ResponseEntity<ApiResponse<List<ChalisaDto>>> getChalisas(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        List<ChalisaDto> data = godService.getChalisas(page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/chalisas/{deity}")
    @Operation(summary = "Get chalisa by deity")
    public ResponseEntity<ApiResponse<ChalisaDto>> getChalisaByDeity(@PathVariable String deity) {
        return ResponseEntity.ok(ApiResponse.ok(godService.getChalisaByDeity(deity)));
    }

    @GetMapping("/chalisas/{deity}/verses/{verseNumber}")
    @Operation(summary = "Get a specific chalisa verse")
    public ResponseEntity<ApiResponse<ChalisaVerseDto>> getChalisaVerse(
            @PathVariable String deity,
            @PathVariable int verseNumber) {
        return ResponseEntity.ok(ApiResponse.ok(godService.getChalisaVerse(deity, verseNumber)));
    }

    @GetMapping(RestEndpointConstants.STOTRAMS)
    @Operation(summary = "List all stotrams", description = "Returns stotrams, optionally filtered by deity")
    public ResponseEntity<ApiResponse<List<StotramDto>>> getStotrams(
            @RequestParam(required = false) String deity,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        List<StotramDto> data = godService.getStotrams(deity, page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping(RestEndpointConstants.STOTRAMS + "/{stotramId}")
    @Operation(summary = "Get stotram by ID")
    public ResponseEntity<ApiResponse<StotramDto>> getStotramById(@PathVariable String stotramId) {
        return ResponseEntity.ok(ApiResponse.ok(godService.getStotramById(stotramId)));
    }

    @GetMapping(RestEndpointConstants.MANTRAS + "/random")
    @Operation(summary = "Get a random mantra")
    public ResponseEntity<ApiResponse<MantraDto>> getRandomMantra() {
        return ResponseEntity.ok(ApiResponse.ok(godService.getRandomMantra()));
    }

    @GetMapping(RestEndpointConstants.MANTRAS)
    @Operation(summary = "Get mantras by deity")
    public ResponseEntity<ApiResponse<List<MantraDto>>> getMantras(
            @RequestParam(required = false) String deity,
            @RequestParam(defaultValue = "20") int limit) {
        return ResponseEntity.ok(ApiResponse.ok(godService.getMantras(deity, limit)));
    }
}
