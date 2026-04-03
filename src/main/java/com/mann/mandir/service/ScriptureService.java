package com.mann.mandir.service;

import com.mann.mandir.dto.domain.GitaChapterDto;
import com.mann.mandir.dto.domain.GitaVerseDto;
import com.mann.mandir.dto.domain.MahabharataParvaDto;
import com.mann.mandir.dto.domain.MahabharataVerseDto;
import com.mann.mandir.dto.domain.RamayanaKandaDto;
import com.mann.mandir.dto.domain.RamayanaVerseDto;

import java.util.List;

public interface ScriptureService {
    List<GitaChapterDto> getGitaChapters();
    GitaChapterDto getGitaChapter(int chapterNumber);
    List<GitaVerseDto> getGitaVersesByChapter(int chapterNumber);
    GitaVerseDto getGitaVerse(int chapterNumber, int verseNumber);
    List<RamayanaKandaDto> getRamayanaKandas();
    RamayanaKandaDto getRamayanaKanda(String kandaId);
    List<RamayanaVerseDto> getRamayanaVerses(String kandaId, int sarga, int page, int size);
    RamayanaVerseDto getRamayanaVerse(String kandaId, int sarga, int verse);
    List<MahabharataParvaDto> getMahabharataParvas();
    MahabharataParvaDto getMahabharataParva(int parvaNumber);
    List<MahabharataVerseDto> getMahabharataVerses(int parvaNumber, int chapterNumber, int page, int size);
    MahabharataVerseDto getMahabharataVerse(int parvaNumber, int chapterNumber, int verse);
}
