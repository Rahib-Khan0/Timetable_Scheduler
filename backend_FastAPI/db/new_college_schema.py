# async def create_college_schema(engine, schema_name: str):
#     async with engine.begin() as conn:
#         await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}";'))
#         await conn.run_sync(Base.metadata.create_all, schema=schema_name)
