package com.mann.mandir.config;

import com.mann.mandir.constants.RestEndpointConstants;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenApiConfig {

    @Value("${server.port:8080}")
    private int port;

    @Bean
    public OpenAPI mandirOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Mann Mandir API")
                        .version("1.0.0")
                        .description("A comprehensive REST API for Hindu spiritual content — "
                                + "Aarti, Chalisa, Stotrams, Mantras, Bhagavad Gita, Ramayana, "
                                + "Mahabharata, Vedas, and Upanishads.")
                        .contact(new Contact()
                                .name("Mann Mandir")
                                .email("api@mannmandir.com"))
                        .license(new License()
                                .name("MIT")
                                .url("https://opensource.org/licenses/MIT")))
                .servers(List.of(
                        new Server()
                                .url("http://localhost:" + port + RestEndpointConstants.BASE_URL)
                                .description("Local Development"),
                        new Server()
                                .url("https://api.mannmandir.com" + RestEndpointConstants.BASE_URL)
                                .description("Production")));
    }
}
