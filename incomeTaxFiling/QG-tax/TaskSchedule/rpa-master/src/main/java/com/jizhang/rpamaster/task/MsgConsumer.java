package com.jizhang.rpamaster.task;


import cn.hutool.http.HttpUtil;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jizhang.rpamaster.dao.Mapper;
import com.jizhang.rpamaster.entity.TaxReq;
import com.jizhang.rpamaster.entity.WorkerEntity;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.HashMap;

@Component
@Slf4j
public class MsgConsumer implements Runnable {

    @Autowired
    private SendManager manager;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private Mapper mapper;

    @SneakyThrows
    @Override
    public void run() {
        while (manager.isRunning()) {
            WorkerEntity idelWorker = mapper.getIdelWorker();
            if (idelWorker == null) {
                Thread.sleep(5000);
                log.info("没有worker可用");
                continue;
            }
            TaxReq take = manager.taskQueue.take();

            HashMap<String, Object> param = new HashMap<>();

            param.put("sw_type", take.getType());
            param.put("company_id", take.getDeclareId());
            param.put("id", take.getId());
            String url = "http://" + idelWorker.getIp() + ":3333";
            try {
                mapper.updateWorkState(idelWorker.getIp(), "2");
                HttpUtil.createPost(url).body(objectMapper.writeValueAsBytes(param)).timeout(10 * 1000).execute();
                log.info("发送{} 到 worker:{}成功", take, idelWorker.getIp());
            } catch (Exception e) {
                mapper.updateWorkState(idelWorker.getIp(), "0");
                log.error("发送{} 到work:{}失败,更新worker 为 不可用（state = 0 ）！", take, idelWorker.getIp());
                e.printStackTrace();
            }
            Thread.sleep(1000);


        }
    }
}
