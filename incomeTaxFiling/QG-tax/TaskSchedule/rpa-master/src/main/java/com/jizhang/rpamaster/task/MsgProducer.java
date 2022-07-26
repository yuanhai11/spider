package com.jizhang.rpamaster.task;


import com.jizhang.rpamaster.dao.Mapper;
import com.jizhang.rpamaster.entity.TaxReq;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

import java.util.List;

@Slf4j
@Component
public class MsgProducer implements Runnable {

    @Autowired
    private SendManager manager;
    @Autowired
    private Mapper mapper;

    @SneakyThrows
    @Override
    public void run() {
        while (manager.isRunning()) {
            TaxReq task = mapper.getTask();
            if (ObjectUtils.isEmpty(task)) {
                Thread.sleep(5000);
                continue;
            }
            manager.taskQueue.put(task);
            log.info("<<<put {} to queue finished!", task);

            Thread.sleep(1000);
        }
    }

}
