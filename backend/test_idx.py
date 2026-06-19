from financial_intelligence.idx_client import IDXClient

client = IDXClient()

emitens = client.get_emiten()

print(type(emitens))
print(len(emitens))
print(emitens[:3])