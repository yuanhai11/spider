package com.jizhang.rpamaster.controller;


import com.jizhang.rpamaster.dao.Mapper;
import com.jizhang.rpamaster.entity.TaxReq;
import com.jizhang.rpamaster.entity.WorkerEntity;
import com.jizhang.rpamaster.task.MsgConsumer;
import com.jizhang.rpamaster.task.MsgProducer;
import com.jizhang.rpamaster.task.SendManager;
import com.jizhang.rpamaster.util.ResBody;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.ObjectUtils;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("api")
@Api(description = "rpa 调度控制", tags = "rpa")
@Slf4j
public class ReceiveTaskController {

    @Autowired
    private Mapper mapper;

    @Autowired
    private SendManager sendManager;


    @Autowired
    private MsgProducer producer;

    @Autowired
    private MsgConsumer consumer;

    @GetMapping
    @ApiOperation("测试接口")
    public String Hello() {

        return "hello,RPA!";

    }

    @PostMapping
    @ApiOperation("存入账号信息")
    public ResBody<?> save(@RequestBody TaxReq req) {

        if (StringUtils.isEmpty(req.getDeclareId()) || StringUtils.isEmpty(req.getType())) {
            return ResBody.ERROR("数据缺失！！！");
        }

        log.info("receive - {}:{}", req.getDeclareId(), req.getType());
        int i = mapper.saveDeclareData(req.getDeclareId(), req.getType());
        if (i == 1) {
            return ResBody.SUCCESS("保存成功");
        } else {
            return ResBody.ERROR("数据错误");
        }
    }


    @PostMapping("delete")
    @ApiModelProperty("删除已经完成的数据")
    public ResBody<?> deleteFinished(@RequestBody TaxReq req) {
        if (ObjectUtils.isEmpty(req.getId())) {
            return ResBody.ERROR("数据缺失，id 为空！");
        }
        log.info("接收到删除信息为：{}", req);
        int i = mapper.deleteById(req.getId());
        if (i == 1) {
            return ResBody.SUCCESS("删除成功！");
        } else {
            return ResBody.ERROR("数据错误！");
        }
    }

    @PostMapping("updateStatus")
    @ApiModelProperty("更新 work computer 状态")
    public ResBody<?> updateWorkStatus(@RequestBody WorkerEntity worker) {

        if (StringUtils.isEmpty(worker.getIp()) || StringUtils.isEmpty(worker.getState())) {
            return ResBody.ERROR("数据缺失");
        }
        log.info("接受到更新work信息为：{}", worker);
        int i = mapper.updateWorkState(worker.getIp(), worker.getState());
        if (i == 1) {
            return ResBody.SUCCESS("更新成功！");
        } else {
            return ResBody.ERROR("失败！");
        }
    }

    @GetMapping("start")
    @ApiModelProperty("启动消息分发线程")
    public ResBody<?> startRunner() {
        if (!sendManager.isRunning()) {
            sendManager.start();
            Thread thread = new Thread(producer, "producer");
            Thread t2 = new Thread(consumer, "sender");

            thread.start();
            t2.start();
            log.info("runner start!!");
            return ResBody.SUCCESS();
        } else {
            log.error("已经启动了！！");
            return ResBody.ERROR("已经启动了！！");
        }


    }

    @GetMapping("stop")
    @ApiModelProperty("停止")
    public ResBody<?> stopRunner() {
        if (sendManager.isRunning()) {
            sendManager.cancel();
            log.info("runner stopped!!");
            return ResBody.SUCCESS();
        } else {
            return ResBody.ERROR("没有启动！！");
        }
    }


    @PostMapping("updateType")
    @ApiModelProperty("更新type")
    public ResBody<?> updateSwType(@RequestBody TaxReq req) {
        if (ObjectUtils.isEmpty(req.getId()) || StringUtils.isEmpty(req.getType())) {
            return ResBody.ERROR("id 或 type 不可以为空！");
        }
        log.info("更新id:{} 为 type:{}", req.getId(), req.getType());
        int i = mapper.updateTypeById(req.getId(), req.getType());
        if (i == 0) {
            return ResBody.ERROR("数据错误，没有 id:{" + req.getId() + "}的数据");
        }
        return ResBody.SUCCESS("成功！");
    }

}
