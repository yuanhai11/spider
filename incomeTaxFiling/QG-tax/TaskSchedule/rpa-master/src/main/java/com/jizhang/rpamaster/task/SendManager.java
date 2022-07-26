package com.jizhang.rpamaster.task;


import com.jizhang.rpamaster.entity.TaxReq;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.concurrent.LinkedBlockingDeque;

/**
 * 管理发送任务
 */
@Component
public class SendManager {

    private volatile boolean running = false;


    public final LinkedBlockingDeque<TaxReq> taskQueue = new LinkedBlockingDeque<>(1);


    public void cancel() {
        running = false;
    }

    public Boolean isRunning() {
        return running;
    }

    public void start() {
        running = true;
    }


}
