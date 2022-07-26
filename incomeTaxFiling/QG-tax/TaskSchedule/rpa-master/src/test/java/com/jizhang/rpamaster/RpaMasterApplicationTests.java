package com.jizhang.rpamaster;

import cn.hutool.http.HttpUtil;
import com.jizhang.rpamaster.dao.Mapper;
import com.jizhang.rpamaster.entity.TaxReq;
import com.jizhang.rpamaster.entity.WorkerEntity;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Arrays;
import java.util.List;

@SpringBootTest
class RpaMasterApplicationTests {

    @Autowired
    private Mapper mapper;

    @Test
    void contextLoads() {




        WorkerEntity idelWorker = mapper.getIdelWorker();

    }


    public static void main(String[] args) {

        String s = HttpUtil.get("https://www.baidu.com");
        System.out.println(s);
    }

}
