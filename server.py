import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError

from models import Base, Session, Advertisement, engine

app = web.Application()


async def orm_context(app: web.Application):
    print("Start")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("Shut down")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

def get_error(error_cls, error_description):
    return error_cls(
        text=json.dumps({"error": error_description}), content_type="application/json"
    )

async def get_advertisement(advertisement_id: int, session: Session):
    advertisement = await session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise get_error(web.HTTPNotFound, "advertisement not found")
    return advertisement


async def add_advertisement(advertisement: Advertisement, session: Session):
    session.add(advertisement)
    try:
        await session.commit()
    except IntegrityError:
        error = get_error(web.HTTPConflict, "advertisement already exists")
        raise error
    return advertisement

class AdvertisementView(web.View):

    @property
    def session(self):
        return self.request.session

    @property
    def advertisement_id(self):
        return int(self.request.match_info["advertisement_id"])

    async def get(self):
        advertisement = await get_advertisement(self.advertisement_id, self.session)
        return web.json_response(advertisement.json)

    async def post(self):
        json_data = await self.request.json()
        advertisement = Advertisement(**json_data)
        advertisement = await add_advertisement(advertisement, self.session)
        return web.json_response({"id": advertisement.id})

    async def patch(self):
        json_data = await self.request.json()
        advertisement = await get_advertisement(self.advertisement_id, self.session)
        for field, value in json_data.items():
            setattr(advertisement, field, value)
        advertisement = await add_advertisement(advertisement, self.session)
        return web.json_response({"id": advertisement.id})

    async def delete(self):
        advertisement = await get_advertisement(self.advertisement_id, self.session)
        await self.session.delete(advertisement)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.post("/advertisements/", AdvertisementView),
        web.get(r"/advertisements/{advertisement_id:d+}/", AdvertisementView),
        web.patch(r"/advertisements/{advertisement_id:d+}/", AdvertisementView),
        web.delete(r"/advertisements/{advertisement_id:d+}/", AdvertisementView),
    ]
)

web.run_app(app)
