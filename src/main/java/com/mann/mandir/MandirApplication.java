package com.mann.mandir;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;

@SpringBootApplication
@EnableCaching
public class MandirApplication {

	public static void main(String[] args) {
		SpringApplication.run(MandirApplication.class, args);
	}
}
