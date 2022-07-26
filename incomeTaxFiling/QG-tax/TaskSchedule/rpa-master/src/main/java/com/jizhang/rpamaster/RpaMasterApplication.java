package com.jizhang.rpamaster;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import springfox.documentation.swagger2.annotations.EnableSwagger2;


@SpringBootApplication
@EnableSwagger2
@MapperScan("com.jizhang.rpamaster.dao")
public class RpaMasterApplication {

    public static void main(String[] args) {
        SpringApplication.run(RpaMasterApplication.class, args);
    }

}
