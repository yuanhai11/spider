package com.jizhang.rpamaster.dao;

import com.jizhang.rpamaster.entity.TaxReq;
import com.jizhang.rpamaster.entity.WorkerEntity;
import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface Mapper {


    @Insert("insert into z_list (id,company_id,sw_type)values(NULL,#{declareId},#{sw_type})")
    int saveDeclareData(@Param("declareId") String declareId, @Param("sw_type") String swType);


    @Delete("DELETE FROM z_list WHERE id = #{id}")
    int deleteById(@Param("id") Long id);

    @Update("update z_list set sw_type = #{type} where id = #{id}")
    int updateTypeById(@Param("id") Long id,@Param("type")String type);

    @Update("UPDATE c_list SET state=#{status}  WHERE computer=#{ip}")
    int updateWorkState(@Param("ip") String ip, @Param("status") String status);

    @Update("update c_list set state=2 where id = #{id}")
    void updateWorkerState2busy(@Param("id") Long id);

    @Select("select id,computer as ip, state, num from c_list where state = 1 limit 1")
    WorkerEntity getIdelWorker();

    @Select("select id ,sw_type as type, company_id as declareId  from z_list where sw_type = 2  order by id limit 1 ")
    TaxReq getTask();

    @Update("update z_list set exec_worker = #{ip} where id = #{id}")
    void updateTaskWorker(@Param("ip") String ip,@Param("id") Long id);


}
