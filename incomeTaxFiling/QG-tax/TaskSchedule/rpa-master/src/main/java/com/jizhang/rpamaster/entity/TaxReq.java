package com.jizhang.rpamaster.entity;


import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

@Data
@ApiModel
public class TaxReq {

    @ApiModelProperty(name = "id",hidden = false)
    private Long id;

    @ApiModelProperty(name = "类型",hidden = false)
    private String type;

    @ApiModelProperty(name = "id")
    private String declareId;

    @ApiModelProperty(name = "执行机器",hidden = true)
    private String execWorker;

    @ApiModelProperty(hidden = true)
    private Integer isSend;


    @Override
    public String toString() {
        return "TaxReq{" +
                "id=" + id +
                ", type='" + type + '\'' +
                ", declareId='" + declareId + '\'' +
                ", execWorker='" + execWorker + '\'' +
                ", isSend=" + isSend +
                '}';
    }
}
