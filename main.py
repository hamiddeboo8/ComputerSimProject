import math
import random
from abc import ABC, abstractmethod
import numpy as np

random.seed(1)
np.random.seed(1)


# abstract classes
class Service(ABC):
    @abstractmethod
    def __init__(self, service_rate, fault_prob):
        self.service_dist = 'exp'
        self.service_rate = service_rate
        self.fault_prob = fault_prob
        self.inProgress = None

    @classmethod
    def addToQueue(cls, request, index, source):
        for i in range(len(cls.queue)):
            if type(request).priority < cls.queue[i][0][0].priority:
                cls.queue.insert(i, [(request, index), current_time, None, source])
                return
        cls.queue.append([(request, index), current_time, None, source])

    def serve(self, request, index, source):
        self.inProgress = [(request, index), current_time, None, source]
        if len(type(request).pipeline) - 1 == index:
            service_time = math.ceil(np.random.exponential(self.service_rate, 1)[0])
            type(self).mean.append(service_time)
            self.inProgress[2] = current_time + service_time
        else:
            Service.SpecifyHandleInstance(request, type(request).pipeline[index + 1], index + 1, self)

    def serve_back(self):
        # print("serve_back fired,", self.inProgress)
        if self.inProgress is None:
            return
        if self.inProgress[2] is None:
            service_time = math.ceil(np.random.exponential(self.service_rate, 1)[0])
            type(self).mean.append(service_time)
            self.inProgress[2] = current_time + service_time
            return
        if self.inProgress[2] > current_time:
            return
        if self.inProgress[3] is None:
            accepted_requests.append(self.inProgress[0][0])
            removeCurrent(self.inProgress[0][0].id)
        else:
            self.inProgress[3].serve_back()
        self.inProgress = None

    def fail(self):
        if self.inProgress is None:
            return
        if self.inProgress[3] is not None:
            self.inProgress[3].fail()
        else:
            failed_requests.append(self.inProgress[0][0])
            removeCurrent(self.inProgress[0][0].id)
        self.inProgress = None

    @classmethod
    def HandleProgress(cls):
        for instance in cls.instances:
            if instance.inProgress is not None \
                    and instance.inProgress[2] is not None \
                    and instance.inProgress[2] == current_time:
                instance.serve_back()

    @classmethod
    def EmptyQueues(cls):
        if not cls.queue:
            return
        else:
            free_instances = []
            for instance in cls.instances:
                if instance.inProgress is None:
                    free_instances.append(instance)
            while free_instances:
                if not cls.queue:
                    return
                out_queue = cls.queue.pop(0)
                idx = random.randint(0, len(free_instances) - 1)
                free_instances[idx].serve(out_queue[0][0], out_queue[0][1], out_queue[3])
                free_instances.pop(idx)

    @classmethod
    def SpecifyHandleInstance(cls, request, serviceType, index, source):
        free_instances = []
        for instance in serviceType.instances:
            if instance.inProgress is None:
                free_instances.append(instance)
        if free_instances:
            free_instances[random.randint(0, len(free_instances) - 1)].serve(request, index, source)
        else:
            serviceType.addToQueue(request, index, source)


class Request(ABC):
    __occurrence_prob_range = [0.0]
    __allRequests = []
    __ID = 0

    pipeline = []
    priority = 0
    max_wait = 0
    occurrence_prob = 0

    @abstractmethod
    def __init__(self, time):
        self.id = Request.__ID + 1
        self.time = -1
        Request.__ID += 1

    @classmethod
    def init(cls, self, priority, max_wait, occurrence_prob):
        type(self).priority = priority
        type(self).max_wait = max_wait
        type(self).occurrence_prob = occurrence_prob
        Request.__occurrence_prob_range.append(Request.__occurrence_prob_range[-1] + occurrence_prob)
        Request.__allRequests.append(type(self))

    def doRequest(self):
        self.time = current_time
        current_requests.append(self)
        Service.SpecifyHandleInstance(self, type(self).pipeline[0], 0, None)

    def time_out(self):
        for i in range(len(type(self).pipeline) - 1, -1, -1):
            temp = 0
            stage = type(self).pipeline[i]
            for instance in stage.instances:
                if instance is not None and instance.inProgress is not None and instance.inProgress[0][0].id == self.id:
                    instance.inProgress = None
                    temp = 1
                    break
            if temp == 1:
                continue

            idx = -1
            for k in range(len(stage.queue)):
                if stage.queue[k][0][0].id == self.id:
                    idx = k
                    break
            if idx != -1:
                stage.queue.pop(idx)
        timeout_requests.append(self)
        removeCurrent(self.id)

    @classmethod
    def get_occurrence_prob_range(cls):
        return cls.__occurrence_prob_range

    @classmethod
    def get_allRequests(cls):
        return cls.__allRequests


# services
class MobileAPI(Service):
    mean = []
    instances = []
    queue = []

    def __init__(self):
        Service.__init__(self, 2, 0.01)
        if not type(self).instances:
            type(self).queue = []
        type(self).instances.append(self)


class WebAPI(Service):
    mean = []
    instances = []
    queue = []

    def __init__(self):
        Service.__init__(self, 3, 0.01)
        if not type(self).instances:
            type(self).queue = []
        type(self).instances.append(self)


class RestaurantManagement(Service):
    mean = []
    instances = []
    queue = []

    def __init__(self):
        Service.__init__(self, 8, 0.02)
        if not type(self).instances:
            type(self).queue = []
        type(self).instances.append(self)


class CustomerManagement(Service):
    mean = []
    instances = []
    queue = []

    def __init__(self):
        Service.__init__(self, 5, 0.02)
        if not type(self).instances:
            type(self).queue = []
        type(self).instances.append(self)


class OrderManagement(Service):
    mean = []
    instances = []
    queue = []

    def __init__(self):
        Service.__init__(self, 6, 0.03)
        if not type(self).instances:
            type(self).queue = []
        type(self).instances.append(self)


class DeliveryCommunication(Service):
    mean = []
    instances = []
    queue = []

    def __init__(self):
        Service.__init__(self, 9, 0.1)
        if not type(self).instances:
            type(self).queue = []
        type(self).instances.append(self)


class Payments(Service):
    mean = []
    instances = []
    queue = []

    def __init__(self):
        Service.__init__(self, 12, 0.2)
        if not type(self).instances:
            type(self).queue = []
        type(self).instances.append(self)


# requests
class RegisterOrderMobile(Request):
    def __init__(self, time):
        if type(self).pipeline:
            super().__init__(time)
        if not type(self).pipeline:
            type(self).pipeline = [MobileAPI, OrderManagement, Payments]
            Request.init(self, 1, time, 0.2)


class RegisterOrderWeb(Request):
    def __init__(self, time):
        if type(self).pipeline:
            super().__init__(time)
        if not type(self).pipeline:
            type(self).pipeline = [WebAPI, OrderManagement, Payments]
            Request.init(self, 1, time, 0.1)


class SendMessageDelivery(Request):
    def __init__(self, time):
        if type(self).pipeline:
            super().__init__(time)
        if not type(self).pipeline:
            type(self).pipeline = [MobileAPI, CustomerManagement, DeliveryCommunication]
            Request.init(self, 2, time, 0.05)


class RestaurantInfoMobile(Request):
    def __init__(self, time):
        if type(self).pipeline:
            super().__init__(time)
        if not type(self).pipeline:
            type(self).pipeline = [MobileAPI, RestaurantManagement]
            Request.init(self, 2, time, 0.25)


class RestaurantInfoWeb(Request):
    def __init__(self, time):
        if type(self).pipeline:
            super().__init__(time)
        if not type(self).pipeline:
            type(self).pipeline = [WebAPI, RestaurantManagement]
            Request.init(self, 2, time, 0.15)


class DeliveryRequest(Request):
    def __init__(self, time):
        if type(self).pipeline:
            super().__init__(time)
        if not type(self).pipeline:
            type(self).pipeline = [WebAPI, RestaurantManagement, DeliveryCommunication]
            Request.init(self, 1, time, 0.2)


class OrderTracking(Request):
    def __init__(self, time):
        if type(self).pipeline:
            super().__init__(time)
        if not type(self).pipeline:
            type(self).pipeline = [MobileAPI, OrderManagement]
            Request.init(self, 2, time, 0.05)


# constants
mapper_service_dict = {0: RestaurantManagement, 1: CustomerManagement, 2: OrderManagement, 3: DeliveryCommunication,
                       4: Payments, 5: MobileAPI, 6: WebAPI}
mapper_request_dict = {0: RegisterOrderMobile, 1: RegisterOrderWeb, 2: SendMessageDelivery, 3: RestaurantInfoMobile,
                       4: RestaurantInfoWeb, 5: DeliveryRequest, 6: OrderTracking}

# variables
current_time = 0
arrival_table = []
current_requests = []
accepted_requests = []
failed_requests = []
timeout_requests = []


# functions
def generate_request_type():
    temp = random.random()
    for i in range(len(Request.get_occurrence_prob_range())):
        if Request.get_occurrence_prob_range()[i] > temp:
            temp2 = mapper_request_dict[i - 1](max_waits[i - 1])
            return temp2


def generate_arrival_data(rate, finish_time):
    last_start_time = 0
    result = []
    while last_start_time < finish_time:
        interArrival = np.random.poisson(1.0 / float(rate), 1)
        request = generate_request_type()
        if result:
            result.append((request, int(result[-1][1] + interArrival)))
        else:
            result.append((request, int(interArrival)))
        last_start_time = result[-1][1]
    if result[-1][1] >= finish_time:
        result.pop()
    return result


def handleQueues():
    for i in range(4, -3, -1):
        if i < 0:
            j = i + 7
        else:
            j = i
        mapper_service_dict[j].EmptyQueues()


def handleProgressed():
    for ii in range(4, -3, -1):
        if ii < 0:
            jj = ii + 7
        else:
            jj = ii
        mapper_service_dict[jj].HandleProgress()


def isIdle():
    if idx_over_arrival < len(arrival_table) and arrival_table[idx_over_arrival][1] == current_time:
        return False
    for i in range(7):
        if mapper_service_dict[i].queue:
            return False
    for i in range(7):
        for instance in mapper_service_dict[i].instances:
            if instance.inProgress is not None:
                return False
    return True


def handleFaults():
    instancesServing = []
    for i in range(7):
        for instance in mapper_service_dict[i].instances:
            if instance.inProgress is not None and instance.inProgress[2] is not None:
                instancesServing.append(instance)

    for instance in instancesServing:
        temp = random.random()
        if temp < instance.fault_prob:
            instance.fail()


def checkTimeOuts():
    for req in current_requests:
        #print(current_time, req.time)
        if current_time - req.time > type(req).max_wait:
            #print(req.time)
            req.time_out()


def showDebug():
    res = ""
    for i in range(7):
        res += str(mapper_service_dict[i]) + ":\n"
        res += "\t" + str(mapper_service_dict[i].queue) + "\n"
        res += "\tinstances:\n"
        for instance in mapper_service_dict[i].instances:
            res += "\t\t" + str(instance.inProgress) + "\n"
        res += "\n"
    res += "----------------------------------------------------------------------------------------------\n"
    return res


def removeCurrent(id):
    idx = 0
    for i in range(len(current_requests)):
        if current_requests[i].id == id:
            idx = i
            break
    current_requests.pop(idx)


# inputs
num_of_instances = []
arrival_rate = 0
total_time = 0
max_waits = []

for i in range(4):
    input_line = input()
    if i == 0 or i == 3:
        input_line_arr = input_line.split(" ")
        if i == 0:
            num_of_instances = list(map(int, input_line_arr))
        else:
            max_waits = list(map(int, input_line_arr))
    else:
        if i == 1:
            arrival_rate = int(input_line)
        else:
            total_time = int(input_line)

for i in range(7):
    for j in range(num_of_instances[i]):
        mapper_service_dict[i]()

for i in range(7):
    mapper_request_dict[i](max_waits[i])

arrival_table = generate_arrival_data(arrival_rate, total_time)
idx_over_arrival = 0
log = ""
# print(Request.allRequests)
# print(Request.occurrence_prob_range)

# for arrive in arrival_table:
#    arrive[0].putInQueue(arrive[1])

try:
    while current_time <= total_time:
        if isIdle():
            if idx_over_arrival < len(arrival_table):
                current_time = arrival_table[idx_over_arrival][1]
            else:
                break
        else:
            addition = 0
            while idx_over_arrival < len(arrival_table) and arrival_table[idx_over_arrival][1] == current_time:
                arrival_table[idx_over_arrival][0].doRequest()
                idx_over_arrival += 1
                addition += 1
            #print(addition)
            #print(len(failed_requests) + len(timeout_requests) + len(accepted_requests) + len(current_requests), end="\t")
            #print(len(timeout_requests), end="\t")
            #print(len(accepted_requests), end="\t")
            #print(len(current_requests))

            checkTimeOuts()
            handleProgressed()
            handleFaults()
            handleQueues()
            log += "* t = " + str(current_time) + "\n"
            log += showDebug()
            current_time += 1
finally:
    """a1 = a2 = a3 = a4 = a5 = a6 = a7 = 0
    for req in timeout_requests:
        if type(req) == RegisterOrderMobile:
            a1 += 1
        if type(req) == RegisterOrderWeb:
            a2 += 1
        if type(req) == SendMessageDelivery:
            a3 += 1
        if type(req) == RestaurantInfoMobile:
            a4 += 1
        if type(req) == RestaurantInfoWeb:
            a5 += 1
        if type(req) == DeliveryRequest:
            a6 += 1
        if type(req) == OrderTracking:
            a7 += 1
    print(a1, a2, a3, a4, a5, a6, a7)"""
    print(len(arrival_table))
    arrival_txt = ""
    for x in arrival_table:
        arrival_txt += str(x[1]) + ", " + str(x[0]) + "\n"
    with open("arrival.txt", 'w') as f:
        f.write(arrival_txt)
    with open("log.txt", 'w') as f:
        f.write(log)
    with open("accepted.txt", 'w') as f:
        f.write(str(len(accepted_requests)) + "\n" + str(accepted_requests))
    with open("failed.txt", 'w') as f:
        f.write(str(len(failed_requests)) + "\n" + str(failed_requests))
    with open("timeout.txt", 'w') as f:
        f.write(str(len(timeout_requests)) + "\n" + str(timeout_requests))
    with open("pending.txt", 'w') as f:
        f.write(str(len(current_requests)) + "\n" + str(current_requests))
