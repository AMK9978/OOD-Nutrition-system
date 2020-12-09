from requests import Session
from zeep import Client, Transport
from random import randint


class PaymentGatewayAdapter(object):
    def __init__(self):
        pass

    def create_client(self, web_service) -> Client:
        session = Session()
        session.headers = {}
        transport = Transport(session=session)
        transport.session.headers = {}  # DON'T REMOVE THIS LINE.YOU BLOCK FROM SAMAN BANK IF REMOVE THIS LINE
        return Client(web_service, transport=transport)

    def sep_request_token(self, amount, wage, additional_data: ['', '']):
        client = self.create_client('https://sep.shaparak.ir/payments/initpayment.asmx?wsdl')
        res_num = self.sep_generate_reservation_number()
        response = client.service.RequestToken(
            'saman mid',
            res_num,
            amount,
            0, 0, 0, 0, 0, 0,
            additional_data[0],
            additional_data[1],
            wage
        )
        token = str(response)
        return token, res_num

    def sep_verify_transaction(self, ref_num):
        client = self.create_client('https://sep.shaparak.ir/payments/referencepayment.asmx?wsdl')
        result = client.service.verifyTransaction(
            ref_num,
            'saman mid'
        )
        return result

    def sep_reverse_transaction(self, ref_num):
        client = self.create_client('https://sep.shaparak.ir/payments/referencepayment.asmx?wsdl')
        result = client.service.reverseTransaction(
            ref_num,
            "saman mid",
            "saman mid",
            "saman password"
        )
        return result

    def sep_generate_reservation_number(self):
        return randint(11111111111111, 99999999999999)
