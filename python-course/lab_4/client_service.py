from client import Client


class ClientService:
    clients = []

    @classmethod
    def create_client(cls, client_id):
        if cls.get_client_by_client_id(client_id):
            raise Exception("Client already exists.")

        client = Client(client_id)
        cls.clients.append(client)
        return client

    @classmethod
    def get_clients(cls):
        return cls.clients

    @classmethod
    def get_client_by_client_id(cls, client_id):
        for client in cls.clients:
            if client.id == client_id:
                return client
