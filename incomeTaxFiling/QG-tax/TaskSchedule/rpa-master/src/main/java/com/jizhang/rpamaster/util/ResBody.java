package com.jizhang.rpamaster.util;

import com.jizhang.rpamaster.constant.ResCode;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;


@ApiModel
@Data
public class ResBody<T> {

    @ApiModelProperty(name = "数据")
    private T data;

    @ApiModelProperty(name = "响应消息")
    private String msg;

    @ApiModelProperty(name = "响应码")
    private ResCode status = ResCode.SUCCESS;


    public ResBody(T data, String msg, ResCode code) {
        this.data = data;
        this.msg = msg;
        this.status = code;
    }

    public ResBody(T data, String msg) {
        this.data = data;
        this.msg = msg;
    }

    public ResBody(T data) {
        this.data = data;
    }

    public ResBody(String msg, ResCode code) {
        this.msg = msg;
        this.status = code;
    }

    public ResBody() {
    }

    public int getCode() {
        return status.code;
    }

    public static ResBody<?> SUCCESS(String msg) {
        return new ResBody<>(msg, ResCode.SUCCESS);
    }

    public static ResBody<?> SUCCESS() {
        return new ResBody<>();
    }

    public static ResBody<?> ERROR(String msg) {
        return new ResBody<>(msg, ResCode.ERROR);
    }

    public static ResBody<?> SUCCESS(Object data) {
        return new ResBody<>(data);
    }
}
