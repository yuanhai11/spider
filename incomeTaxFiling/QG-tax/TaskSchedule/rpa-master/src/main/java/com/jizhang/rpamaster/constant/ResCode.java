package com.jizhang.rpamaster.constant;

public enum ResCode {
    ERROR(1, "数据错误"),
    SUCCESS(0,"成功！");


    public int code;

    public String msg;

    ResCode(int code, String msg) {
        this.code = code;
        this.msg = msg;
    }


}
