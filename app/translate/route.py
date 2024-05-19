from fastapi import APIRouter, Response
from translate.behaviour import meta_translate, meta_translate_get
from translate.pydantic_models import TranslateRequest

router = APIRouter()


@router.post(path="/translate", status_code=200)
async def translate(request: TranslateRequest) -> Response:
    return await meta_translate(request=request)


@router.get(path="/translate/{identifier}", status_code=200)
async def get_translate(identifier: str):
    return await meta_translate_get(identifier=identifier)
