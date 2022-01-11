
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# List of domain names that are allowed to access the API
origins = ["*"]

# Add cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includes all routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>FastAPI - Tutorial</title>
            <link rel="icon" href="https://ufmmmw.dm.files.1drv.com/y4mqGPFwLkEdHv8neWQT2u2Je_MO6STFzrf3UPzVZV3NMhELKnwb4qizeWCr62wEEyJiNPCK1JwjBMSe02runDXvwe39soqsOtSsj_cYViwru89VXvuUj853rVLx3yByFt9PmtXDU-SijeKaEdETjZ1uNqBQUV0szbCzv-Ad7Q0qRYvG2MmWK5Xg_NUE24pQlpJ-OR9MUUFdIafyglmlMwErg/android-chrome-512x512.png?psid=1"/>
        </head>
        <body>
            <style>
            * {
                box-sizing: border-box;
            }
            body {
                display: flex;
                background-color: rgba(202, 160, 160, 0.096);
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0 auto;
                flex-direction: column;
            }
            ul {
                list-style: none;
                list-style-type: none;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            li {
                padding: 10px;
                margin: 10px auto;
                background-color: rgba(45, 142, 172, 0.308);
                width: 50%;
            }
            li:hover {
                background-color: rgba(45, 142, 172, 0.801);
            }
            a {
                color: black;
                font-weight: bold;
                text-decoration: none;
            }
            .container {
                background-color: rgba(45, 142, 172, 0.13);
                padding: 2rem 0;
                text-align: center;
                width: 75%;
            }
            img {
                width: 25%;
                height: auto;
            }
            </style>
            <div class="container">
            <img
                src="https://ufmmmw.dm.files.1drv.com/y4mqGPFwLkEdHv8neWQT2u2Je_MO6STFzrf3UPzVZV3NMhELKnwb4qizeWCr62wEEyJiNPCK1JwjBMSe02runDXvwe39soqsOtSsj_cYViwru89VXvuUj853rVLx3yByFt9PmtXDU-SijeKaEdETjZ1uNqBQUV0szbCzv-Ad7Q0qRYvG2MmWK5Xg_NUE24pQlpJ-OR9MUUFdIafyglmlMwErg/android-chrome-512x512.png?psid=1"
                alt="avatar"
            />
            <h1>FastAPI - Tutorial</h1>
            <ul>
                <a href="/docs"><li>Documentation</li></a>
                <a href="https://josue-lubaki.ca" target="_blank" rel="noopener noreferrer"><li>Portfolio</li></a>
                <a href="https://github.com/josue-lubaki" target="_blank" rel="noopener noreferrer"><li>GitHub</li></a>
            </ul>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/", response_class=HTMLResponse)
async def root():
    return generate_html_response()
