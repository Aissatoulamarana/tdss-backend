import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DeclarationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Gérer la connexion, par exemple, l'ajout au groupe WebSocket
        self.group_name = 'declarations'  # Nom du groupe pour la diffusion
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Nettoyage lors de la déconnexion du WebSocket
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Recevoir des messages du client (si nécessaire)
        pass

    async def status_update(self, event):
        # Envoyer une mise à jour de statut aux clients connectés
        await self.send(text_data=json.dumps(event['message']))
