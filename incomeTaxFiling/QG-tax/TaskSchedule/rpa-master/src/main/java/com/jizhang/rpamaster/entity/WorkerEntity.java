package com.jizhang.rpamaster.entity;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

@Data
@ApiModel
public class WorkerEntity {

    @ApiModelProperty(name = "worker_id", hidden = true)
    private Long id;

    @ApiModelProperty(name = "ip 地址")
    private String ip;

    @ApiModelProperty(name = "状态")
    private String state;

    @Override
    public String toString() {
        return "WorkerEntity{" +
                "ip='" + ip + '\'' +
                ", status='" + state + '\'' +
                '}';
    }

    @ApiModelProperty(name = "hashMapping", hidden = true)
    private String num;

}
