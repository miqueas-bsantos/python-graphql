from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from .schemas import schema
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_route("/", GraphQLApp(schema=schema))
