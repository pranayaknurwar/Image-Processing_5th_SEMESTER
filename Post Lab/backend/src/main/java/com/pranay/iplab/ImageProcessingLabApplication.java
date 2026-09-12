package com.pranay.iplab;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.beans.factory.annotation.Value;
@SpringBootApplication
public class ImageProcessingLabApplication {
 public static void main(String[] args){SpringApplication.run(ImageProcessingLabApplication.class,args);}
 @Bean
WebMvcConfigurer cors(@Value("${app.cors-origin:*}") String corsOrigin){
    return new WebMvcConfigurer(){
        public void addCorsMappings(CorsRegistry r){
            r.addMapping("/api/**")
             .allowedOrigins(corsOrigin)
             .allowedMethods("GET","POST","OPTIONS")
             .allowedHeaders("*");
        }
    };
}
}