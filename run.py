import os

import uvicorn

os.environ["DEVELOPMENT_MODE"] = "True"

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="localhost",
        port=5000,
        reload=os.environ["DEVELOPMENT_MODE"] == "True",
        debug=False,
        workers=1,
    )
