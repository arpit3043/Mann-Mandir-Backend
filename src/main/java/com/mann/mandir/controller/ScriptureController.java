package com.mann.mandir.controller;

import com.mann.mandir.constants.RestEndpointConstants;
import com.mann.mandir.dto.ApiResponse;
import com.mann.mandir.dto.domain.GitaChapterDto;
import com.mann.mandir.dto.domain.GitaVerseDto;
import com.mann.mandir.dto.domain.MahabharataParvaDto;
import com.mann.mandir.dto.domain.MahabharataVerseDto;
import com.mann.mandir.dto.domain.RamayanaKandaDto;
import com.mann.mandir.dto.domain.RamayanaVerseDto;
import com.mann.mandir.service.ScriptureService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping(RestEndpointConstants.SCRIPTURES)
@RequiredArgsConstructor
@Tag(name = "Scriptures", description = "Bhagavad Gita, Ramayana, Mahabharata")
public class ScriptureController {
    private final ScriptureService scriptureService;

    @GetMapping("/gita/chapters")
    @Operation(summary = "Get all 18 Gita chapters")
    public ResponseEntity<ApiResponse<List<GitaChapterDto>>> getGitaChapters() {
        return ResponseEntity.ok(ApiResponse.ok(scriptureService.getGitaChapters()));
    }

    @GetMapping("/gita/chapters/{chapterNumber}")
    @Operation(summary = "Get a specific Gita chapter")
    public ResponseEntity<ApiResponse<GitaChapterDto>> getGitaChapter(
            @PathVariable int chapterNumber) {
        return ResponseEntity.ok(ApiResponse.ok(scriptureService.getGitaChapter(chapterNumber)));
    }

    @GetMapping("/gita/chapters/{chapterNumber}/verses")
    @Operation(summary = "Get all verses in a Gita chapter")
    public ResponseEntity<ApiResponse<List<GitaVerseDto>>> getGitaVersesByChapter(
            @PathVariable int chapterNumber) {
        return ResponseEntity.ok(ApiResponse.ok(scriptureService.getGitaVersesByChapter(chapterNumber)));
    }

    @GetMapping("/gita/chapters/{chapterNumber}/verses/{verseNumber}")
    @Operation(summary = "Get a specific Gita verse with translations and commentaries")
    public ResponseEntity<ApiResponse<GitaVerseDto>> getGitaVerse(
            @PathVariable int chapterNumber,
            @PathVariable int verseNumber) {
        return ResponseEntity.ok(ApiResponse.ok(scriptureService.getGitaVerse(chapterNumber, verseNumber)));
    }

    @GetMapping("/ramayana/kandas")
    @Operation(summary = "Get all Ramayana Kandas (books)")
    public ResponseEntity<ApiResponse<List<RamayanaKandaDto>>> getRamayanaKandas() {
        return ResponseEntity.ok(ApiResponse.ok(scriptureService.getRamayanaKandas()));
    }

    @GetMapping("/ramayana/kandas/{kandaId}")
    @Operation(summary = "Get a specific Ramayana Kanda")
    public ResponseEntity<ApiResponse<RamayanaKandaDto>> getRamayanaKanda(
            @PathVariable String kandaId) {
        return ResponseEntity.ok(ApiResponse.ok(scriptureService.getRamayanaKanda(kandaId)));
    }

    @GetMapping("/ramayana/kandas/{kandaId}/sargas/{sarga}/verses")
    @Operation(summary = "Get verses from a Ramayana Sarga (chapter)")
    public ResponseEntity<ApiResponse<List<RamayanaVerseDto>>> getRamayanaVerses(
            @PathVariable String kandaId,
            @PathVariable int sarga,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        List<RamayanaVerseDto> data = scriptureService.getRamayanaVerses(kandaId, sarga, page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/ramayana/kandas/{kandaId}/sargas/{sarga}/verses/{verse}")
    @Operation(summary = "Get a specific Ramayana verse")
    public ResponseEntity<ApiResponse<RamayanaVerseDto>> getRamayanaVerse(
            @PathVariable String kandaId,
            @PathVariable int sarga,
            @PathVariable int verse) {
        return ResponseEntity.ok(ApiResponse.ok(scriptureService.getRamayanaVerse(kandaId, sarga, verse)));
    }

    @GetMapping("/mahabharata/parvas")
    @Operation(summary = "Get all 18 Mahabharata Parvas")
    public ResponseEntity<ApiResponse<List<MahabharataParvaDto>>> getMahabharataParvas() {
        return ResponseEntity.ok(ApiResponse.ok(scriptureService.getMahabharataParvas()));
    }

    @GetMapping("/mahabharata/parvas/{parvaNumber}")
    @Operation(summary = "Get a specific Mahabharata Parva")
    public ResponseEntity<ApiResponse<MahabharataParvaDto>> getMahabharataParva(
            @PathVariable int parvaNumber) {
        return ResponseEntity.ok(ApiResponse.ok(scriptureService.getMahabharataParva(parvaNumber)));
    }

    @GetMapping("/mahabharata/parvas/{parvaNumber}/chapters/{chapterNumber}/verses")
    @Operation(summary = "Get verses from a Mahabharata chapter")
    public ResponseEntity<ApiResponse<List<MahabharataVerseDto>>> getMahabharataVerses(
            @PathVariable int parvaNumber,
            @PathVariable int chapterNumber,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        List<MahabharataVerseDto> data = scriptureService.getMahabharataVerses(parvaNumber, chapterNumber, page, size);
        return ResponseEntity.ok(ApiResponse.ok(data,
                ApiResponse.PaginationMeta.of(page, size, data.size())));
    }

    @GetMapping("/mahabharata/parvas/{parvaNumber}/chapters/{chapterNumber}/verses/{verse}")
    @Operation(summary = "Get a specific Mahabharata verse")
    public ResponseEntity<ApiResponse<MahabharataVerseDto>> getMahabharataVerse(
            @PathVariable int parvaNumber,
            @PathVariable int chapterNumber,
            @PathVariable int verse) {
        return ResponseEntity.ok(ApiResponse.ok(
                scriptureService.getMahabharataVerse(parvaNumber, chapterNumber, verse)));
    }
}
