from abc import ABC, abstractmethod

from entities.service import Service

class PredictionConverter(ABC):
    
    @abstractmethod
    def convert_prediction(self, result) -> list:
        pass

class PredictionConverterA(PredictionConverter):
    
    def convert_prediction(self, result):
        svcsequence_count = dict((x,result.count(x)) for x in set(result))
        svc_count = {}
        for i in svcsequence_count:
            svcs = str(i).split(',')
            for svc in svcs:
                if svc in svc_count.keys():
                    svc_count[svc] = svc_count[svc] + svcsequence_count[i]
                else:
                    svc_count[svc] = svcsequence_count[i]
        services = []
        for svc in svc_count:
            service = Service(svc, svc_count[svc], 'sock-shop')
            services.append(service)
        return services