from fastapi import HTTPException

async def exception_service(func, *args, **kwargs):
    """Единый обработчик ошибок для роутов."""
    try:
        result = await func(*args, **kwargs)
        if isinstance(result, str):
            result = {"message": result}
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
