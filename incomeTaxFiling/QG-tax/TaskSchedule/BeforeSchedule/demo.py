import json
import traceback
try:
    message_str = "{\"orgName\":\"zj\",\"taskId\":\"111111\",\"orgType\":\"个税\",\"requestParams\":{\"data\":{\"password\":\"zlcw1003\",\"taxStaffRpaVOS\":[{\"mob\":\"18658158810\",\"otherCertificateNumber\":\"\",\"entryDate\":\"None\",\"remark\":\"None\",\"employedType\":\"雇员\",\"quitDate\":\"None\",\"nationality\":\"中国\",\"certificateNumber\":\"321183199406112217\",\"identifyDate\":\"2021-12\",\"name\":\"段文轩\",\"birthCountry\":\"\",\"taxRelatedMatters\":\"\",\"departureDate\":\"None\",\"employedDate\":\"2018-10-22\",\"certificateType\":\"居民身份证\",\"status\":\"正常\"}],\"loginname\":\"91330101MA2CF0NL1Y\",\"staffSalaryVOS\":[{\"insurance\":0,\"accumulationFund\":0,\"certificateNumber\":\"321183199406112217\",\"medicalInsurance\":0,\"unemploymentInsurance\":0,\"identifyDate\":\"2021-12\",\"currentIncome\":0,\"name\":\"段文轩\",\"certificateType\":\"居民身份证\"}]}},\"taskType\":\"个税申报\"}"

    message_dict = json.loads(message_str)
    print(message_dict)
    print(type(message_dict))
    # task_id = message_dict['taskId']
    city = message_dict['orgName']

    content = str(message_dict['requestParams'])
    print(content)
    a = 1/0
except Exception as e:
    print(traceback.format_exc())


