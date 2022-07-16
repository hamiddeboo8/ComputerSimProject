from abc import ABC, abstractmethod


# abstract classes
class Service(ABC):
    @abstractmethod
    def __init__(self, service_rate, fault_prob):
        self.queue = []
        self.service_dist = 'exp'
        self.service_rate = service_rate
        self.fault_prob = fault_prob


class Request(ABC):
    occurrence_prob_range = [0.0]
    allRequests = []

    @abstractmethod
    def __init__(self, priority, max_wait, occurrence_prob):
        self.priority = priority
        self.max_wait = max_wait
        self.occurrence_prob = occurrence_prob
        Request.occurrence_prob_range.append(Request.occurrence_prob_range[-1] + occurrence_prob)
        Request.allRequests.append(self)


# services
class MobileAPI(Service):
    instances = []

    def __init__(self):
        Service.__init__(self, 2, 0.01)
        MobileAPI.instances.append(self)


class WebAPI(Service):
    instances = []

    def __init__(self):
        Service.__init__(self, 3, 0.01)
        WebAPI.instances.append(self)


class RestaurantManagement(Service):
    instances = []

    def __init__(self):
        Service.__init__(self, 8, 0.02)
        RestaurantManagement.instances.append(self)


class CustomerManagement(Service):
    instances = []

    def __init__(self):
        Service.__init__(self, 5, 0.02)
        CustomerManagement.instances.append(self)


class OrderManagement(Service):
    instances = []

    def __init__(self):
        Service.__init__(self, 6, 0.03)
        OrderManagement.instances.append(self)


class DeliveryCommunication(Service):
    instances = []

    def __init__(self):
        Service.__init__(self, 9, 0.1)
        DeliveryCommunication.instances.append(self)


class Payments(Service):
    instances = []

    def __init__(self):
        Service.__init__(self, 12, 0.2)
        Payments.instances.append(self)


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


mapper_service_dict = {0: RestaurantManagement, 1: CustomerManagement, 2: OrderManagement, 3: DeliveryCommunication,
                       4: Payments, 5: MobileAPI, 6: WebAPI}
mapper_request_dict = {0: RegisterOrderMobile, 1: RegisterOrderWeb, 2: SendMessageDelivery, 3: RestaurantInfoMobile,
                       4: RestaurantInfoWeb, 5: DeliveryRequest, 6: OrderTracking}

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

for i in range(7):
    print(mapper_service_dict[i].instances)
