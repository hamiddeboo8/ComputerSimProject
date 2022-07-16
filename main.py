from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def __init__(self, service_rate, fault_prob):
        self.queue = []
        self.service_dist = 'exp'
        self.service_rate = service_rate
        self.fault_prob = fault_prob


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


num_of_instances = []
arrival_rate = 0
total_time = 0
max_wait = []

for i in range(4):
    input_line = input()
    if i == 0 or i == 3:
        input_line_arr = input_line.split(" ")
        if i == 0:
            num_of_instances = list(map(int, input_line_arr))
        else:
            max_wait = list(map(int, input_line_arr))
    else:
        if i == 1:
            arrival_rate = int(input_line)
        else:
            total_time = int(input_line)





