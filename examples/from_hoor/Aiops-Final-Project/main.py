from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, Response
from decoder import decode
from database import save_history, get_history
import logging
import uvicorn

app = FastAPI()

logging.basicConfig(filename="logs/app.log", level=logging.INFO)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware that logs incoming request and outgoing response to the DB."""
    try:
        # read request body (may be empty for GETs)
        body_bytes = await request.body()
        body_text = body_bytes.decode("utf-8") if body_bytes else None
    except Exception:
        body_text = None

    # run the request
    response = await call_next(request)

    # capture response body by draining the body iterator (works for JSONResponse and streaming)
    resp_body = None
    try:
        body_bytes = b""
        # response.body_iterator is an async iterator for streaming responses
        if hasattr(response, "body_iterator") and response.body_iterator is not None:
            async for chunk in response.body_iterator:
                body_bytes += chunk
        else:
            body_bytes = getattr(response, "body", b"") or b""

        try:
            resp_body = body_bytes.decode("utf-8") if body_bytes else None
        except Exception:
            resp_body = str(body_bytes)

        # recreate a Response with the same content so it can be returned to the client
        new_response = Response(content=body_bytes, status_code=response.status_code)
        # copy headers (avoid hop-by-hop headers if necessary)
        for name, value in response.headers.items():
            new_response.headers[name] = value
        response = new_response
    except Exception:
        resp_body = None

    # save into DB (non-blocking errors will be logged inside save_history)
    try:
        # If endpoint returned our old simple result (list) it will be in JSON body
        status = getattr(response, "status_code", None)
        # try to populate legacy fields when possible to stay compatible with init.sql
        legacy_input = None
        try:
            # request.query_params works for GET querystrings
            legacy_input = request.query_params.get("input")
        except Exception:
            legacy_input = None

        legacy_result = None
        # if we have a text response body, use it as the legacy result
        if isinstance(resp_body, str) and resp_body:
            legacy_result = resp_body

        # for GETs there's usually no request body; fall back to query string so the UI shows something
        request_body_to_store = body_text if body_text else (str(request.url.query) if request.url.query else None)

        save_history(
            input_str=legacy_input,
            result=legacy_result,
            method=request.method,
            path=str(request.url.path),
            query_string=str(request.url.query) if request.url.query else None,
            request_body=request_body_to_store,
            response_body=resp_body,
            status_code=status,
        )
    except Exception:
        logging.exception("Failed to save request/response to DB")

    return response


@app.get("/convert-measurements")
def convert(input: str = Query(...)):
    try:
        result = decode(input)
        # middleware will log request/response; no explicit DB write here to avoid duplicates
        logging.info(f"Decoded {input} -> {result}")
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"Error decoding {input}: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/history")
def history():
    return get_history()


if __name__ == "__main__":
    import sys
    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
