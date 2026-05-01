package com.mann.mandir.controller;

import com.mann.mandir.constants.RestEndpointConstants;
import com.mann.mandir.dto.ApiResponse;
import com.mann.mandir.dto.domain.VedaDto;
import com.mann.mandir.dto.domain.MantraDto;
import com.mann.mandir.dto.domain.RigVedaVerseDto;
import com.mann.mandir.dto.domain.UpanishadDto;
import com.mann.mandir.dto.domain.UpanishadVerseDto;
import com.mann.mandir.service.VedaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping({RestEndpointConstants.VEDAS, "/veda"})
@RequiredArgsConstructor
@Tag(name = "Vedas", description = "Rig Veda, Yajur Veda, Sama Veda, Atharva Veda, Upanishads")
public class VedaController {

    private final VedaService vedaService;

    @GetMapping
    @Operation(summary = "Get all 4 Vedas with metadata")
    public ResponseEntity<ApiResponse<List<VedaDto>>> getAllVedas() {
        return ResponseEntity.ok(ApiResponse.ok(vedaService.getAllVedas()));
    }

    @GetMapping("/{vedaId}")
    @Operation(summary = "Get metadata for a specific Veda",
            description = "vedaId: rig | yajur | sama | atharva")
    public ResponseEntity<ApiResponse<VedaDto>> getVeda(@PathVariable String vedaId) {
        return ResponseEntity.ok(ApiResponse.ok(vedaService.getVeda(vedaId)));
    }

    @GetMapping("/rig/mandalas/{mandala}/verses")
    @Operation(summary = "Get Rig Veda verses by Mandala (1-10)")
    public ResponseEntity<ApiResponse<List<RigVedaVerseDto>>> getRigVedaByMandala(
            @PathVariable int mandala,
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "20") int size) {
        List<RigVedaVerseDto> data = vedaService.getRigVedaByMandala(mandala, page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/rig/mandalas/{mandala}/suktas/{sukta}/stanzas/{stanza}")
    @Operation(summary = "Get a specific Rig Veda verse (mandala/sukta/stanza)")
    public ResponseEntity<ApiResponse<RigVedaVerseDto>> getRigVedaVerse(
            @PathVariable int mandala,
            @PathVariable int sukta,
            @PathVariable int stanza) {
        return ResponseEntity.ok(ApiResponse.ok(vedaService.getRigVedaVerse(mandala, sukta, stanza)));
    }

    @GetMapping("/rig/search/deity/{deity}")
    @Operation(summary = "Search Rig Veda verses by deity (devata)")
    public ResponseEntity<ApiResponse<List<RigVedaVerseDto>>> getRigVedaByDeity(
            @PathVariable String deity,
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "20") int size) {
        List<RigVedaVerseDto> data = vedaService.getRigVedaByDeity(deity, page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/rig/search/poet/{poet}")
    @Operation(summary = "Search Rig Veda verses by poet (rishi)")
    public ResponseEntity<ApiResponse<List<RigVedaVerseDto>>> getRigVedaByPoet(
            @PathVariable String poet,
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "20") int size) {
        List<RigVedaVerseDto> data = vedaService.getRigVedaByPoet(poet, page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/yajur/mantras")
    @Operation(summary = "Get Yajur Veda mantras (paginated)")
    public ResponseEntity<ApiResponse<List<MantraDto>>> getYajurVedaMantras(
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "20") int size) {
        List<MantraDto> data = vedaService.getYajurVedaMantras(page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/sama/mantras")
    @Operation(summary = "Get Sama Veda mantras (paginated)")
    public ResponseEntity<ApiResponse<List<MantraDto>>> getSamaVedaMantras(
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "20") int size) {
        List<MantraDto> data = vedaService.getSamaVedaMantras(page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/atharva/mantras")
    @Operation(summary = "Get Atharva Veda mantras (paginated)")
    public ResponseEntity<ApiResponse<List<MantraDto>>> getAtharvaVedaMantras(
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "20") int size) {
        List<MantraDto> data = vedaService.getAtharvaVedaMantras(page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/mantras/random")
    @Operation(summary = "Get a random Vedic mantra")
    public ResponseEntity<ApiResponse<MantraDto>> getRandomVedicMantra() {
        return ResponseEntity.ok(ApiResponse.ok(vedaService.getRandomVedicMantra()));
    }

    @GetMapping("/mantras/search")
    @Operation(summary = "Search mantras across all Vedas by deity")
    public ResponseEntity<ApiResponse<List<MantraDto>>> searchMantras(
            @RequestParam String deity,
            @RequestParam(defaultValue = "20") int limit) {
        return ResponseEntity.ok(ApiResponse.ok(vedaService.searchMantras(deity, limit)));
    }

    @GetMapping(RestEndpointConstants.UPANISHADS)
    @Operation(summary = "Get list of all major Upanishads")
    public ResponseEntity<ApiResponse<List<UpanishadDto>>> getUpanishads() {
        return ResponseEntity.ok(ApiResponse.ok(vedaService.getUpanishads()));
    }

    @GetMapping("/upanishads/{upanishadId}")
    @Operation(summary = "Get a specific Upanishad",
            description = "upanishadId: isha | kena | katha | mundaka | mandukya | chandogya | brihadaranyaka | ...")
    public ResponseEntity<ApiResponse<UpanishadDto>> getUpanishad(
            @PathVariable String upanishadId) {
        return ResponseEntity.ok(ApiResponse.ok(vedaService.getUpanishad(upanishadId)));
    }

    @GetMapping("/upanishads/{upanishadId}/chapters/{chapter}/verses")
    @Operation(summary = "Get verses from an Upanishad chapter")
    public ResponseEntity<ApiResponse<List<UpanishadVerseDto>>> getUpanishadVerses(
            @PathVariable String upanishadId,
            @PathVariable int chapter,
            @RequestParam(defaultValue = "0")  int page,
            @RequestParam(defaultValue = "20") int size) {
        List<UpanishadVerseDto> data = vedaService.getUpanishadVerses(upanishadId, chapter, page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/upanishads/{upanishadId}/chapters/{chapter}/verses/{verse}")
    @Operation(summary = "Get a specific Upanishad verse")
    public ResponseEntity<ApiResponse<UpanishadVerseDto>> getUpanishadVerse(
            @PathVariable String upanishadId,
            @PathVariable int chapter,
            @PathVariable int verse) {
        return ResponseEntity.ok(ApiResponse.ok(
                vedaService.getUpanishadVerse(upanishadId, chapter, verse)));
    }
}
