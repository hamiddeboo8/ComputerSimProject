import random
from abc import ABC, abstractmethod
import numpy as np


# abstract classes
class Service(ABC):
    instances = []
    queue = []

    @abstractmethod
    def __init__(self, service_rate, fault_prob):
        self.service_dist = 'exp'
        self.service_rate = service_rate
        self.fault_prob = fault_prob
        self.inProgress = None

        if not type(self).instances:
            type(self).queue = []
        type(self).instances.append(self)

    @classmethod
    def addToQueue(cls, request, index, source):
        for i in range(len(cls.queue)):
            if request.priority < cls.queue[i][0][0].priority:
                cls.queue.append([(request, index), current_time, None, source])
                return
        cls.queue.append([(request, index), current_time, None, source])

    def serve(self, request, index, source):
        self.inProgress = [(request, index), current_time, None, source]
        if len(request.pipeline) - 1 == index:
            service_time = np.random.exponential(self.service_rate, 1)
            self.inProgress[2] = current_time + service_time
        else:
            Service.SpecifyHandleInstance(request, request.pipeline[index + 1], index + 1, self)

    def serve_back(self):
        if self.inProgress is None:
            return
        if self.inProgress[2] is None:
            service_time = np.random.exponential(self.service_rate, 1)
            self.inProgress[2] = current_time + service_time
            return
        if self.inProgress[2] > current_time:
            return
        temp = self.inProgress
        self.inProgress = None
        if temp[3] is None:
            return
        temp[3].serve_back()

    @classmethod
    def HandleProgress(cls):
        for instance in cls.instances:
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
                out_queue = cls.queue.pop()
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
            serviceType.addToQueue(request, index, None, source)


class Request(ABC):
    occurrence_prob_range = [0.0]
    allRequests = []

    @abstractmethod
    def __init__(self, priority, max_wait, occurrence_prob):
        self.pipeline = []
        self.priority = priority
        self.max_wait = max_wait
        self.occurrence_prob = occurrence_prob
        Request.occurrence_prob_range.append(Request.occurrence_prob_range[-1] + occurrence_prob)
        Request.allRequests.append(self)

    def doRequest(self):
        Service.SpecifyHandleInstance(self, self.pipeline[0], 0, None)


# services
class MobileAPI(Service):
    def __init__(self):
        Service.__init__(self, 2, 0.01)


class WebAPI(Service):
    def __init__(self):
        Service.__init__(self, 3, 0.01)


class RestaurantManagement(Service):
    def __init__(self):
        Service.__init__(self, 8, 0.02)


class CustomerManagement(Service):
    def __init__(self):
        Service.__init__(self, 5, 0.02)


class OrderManagement(Service):
    def __init__(self):
        Service.__init__(self, 6, 0.03)


class DeliveryCommunication(Service):
    def __init__(self):
        Service.__init__(self, 9, 0.1)


class Payments(Service):
    def __init__(self):
        Service.__init__(self, 12, 0.2)


# requests
class RegisterOrderMobile(Request):
    def __init__(self, max_wait):
        self.pipeline = [MobileAPI, OrderManagement, Payments]
        Request.__init__(self, 1, max_wait, 0.2)


class RegisterOrderWeb(Request):
    def __init__(self, max_wait):
        self.pipeline = [WebAPI, OrderManagement, Payments]
        Request.__init__(self, 1, max_wait, 0.1)


class SendMessageDelivery(Request):
    def __init__(self, max_wait):
        self.pipeline = [MobileAPI, CustomerManagement, DeliveryCommunication]
        Request.__init__(self, 2, max_wait, 0.05)


class RestaurantInfoMobile(Request):
    def __init__(self, max_wait):
        self.pipeline = [MobileAPI, RestaurantManagement]
        Request.__init__(self, 2, max_wait, 0.25)


class RestaurantInfoWeb(Request):
    def __init__(self, max_wait):
        self.pipeline = [WebAPI, RestaurantManagement]
        Request.__init__(self, 2, max_wait, 0.15)


class DeliveryRequest(Request):
    def __init__(self, max_wait):
        self.pipeline = [WebAPI, RestaurantManagement, DeliveryCommunication]
        Request.__init__(self, 1, max_wait, 0.2)


class OrderTracking(Request):
    def __init__(self, max_wait):
        self.pipeline = [MobileAPI, OrderManagement]
        Request.__init__(self, 2, max_wait, 0.05)


# constants
mapper_service_dict = {0: RestaurantManagement, 1: CustomerManagement, 2: OrderManagement, 3: DeliveryCommunication,
                       4: Payments, 5: MobileAPI, 6: WebAPI}
mapper_request_dict = {0: RegisterOrderMobile, 1: RegisterOrderWeb, 2: SendMessageDelivery, 3: RestaurantInfoMobile,
                       4: RestaurantInfoWeb, 5: DeliveryRequest, 6: OrderTracking}


# functions
def generate_request_type():
    temp = random.random()
    for i in range(len(Request.occurrence_prob_range)):
        if Request.occurrence_prob_range[i] > temp:
            return type(Request.allRequests[i - 1])


def generate_arrival_data(rate, finish_time):
    last_start_time = 0
    result = []
    while last_start_time < finish_time:
        interArrival = np.random.poisson(1.0 / float(rate), 1)
        request_type = generate_request_type()
        if result:
            result.append((request_type, int(result[-1][1] + interArrival)))
        else:
            result.append((request_type, int(interArrival)))
        last_start_time = result[-1][1]
    if result[-1][1] >= finish_time:
        result.pop()
    return result


def handleQueues():
    for i in range(4, -3):
        if i < 0:
            j = i + 7
        else:
            j = i
        mapper_service_dict[j].EmptyQueues()


def handleProgressed():
    for i in range(4, -3):
        if i < 0:
            j = i + 7
        else:
            j = i
        mapper_service_dict[j].HandleProgress()


def isIdle():
    if arrival_table[idx_over_arrival][1] == current_time:
        return False
    for i in range(7):
        if mapper_service_dict[i].queue:
            return False
    for i in range(7):
        for instance in mapper_service_dict[i].instances:
            if instance is not None:
                return False
    return True


# inputs
num_of_instances = []
arrival_rate = 0
total_time = 0
max_waits = []

# variables
current_time = 0
arrival_table = []

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
# print(Request.allRequests)
# print(Request.occurrence_prob_range)

# for arrive in arrival_table:
#    arrive[0].putInQueue(arrive[1])


while current_time <= total_time:
    if isIdle():
        current_time = arrival_table[idx_over_arrival][1]
    else:
        while arrival_table[idx_over_arrival][1] == current_time:
            arrival_table[idx_over_arrival][0].doRequest()
            idx_over_arrival += 1
        handleProgressed()
        handleQueues()
