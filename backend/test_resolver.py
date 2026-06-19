from financial_intelligence.idx_resolver import IDXResolver


resolver = IDXResolver()

result = resolver.resolve(
    "Mahaka"
)

print(result)