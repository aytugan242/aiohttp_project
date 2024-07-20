import asyncio

import aiohttp
import json

async def main():
    session = aiohttp.ClientSession()
    response = await session.post(
        "http://127.0.0.1:8080/advertisements/",
        json={'header': 'header', 'owner': 'owner-2', 'description': 'description description description'},

    )
    print(response.status)
    print(await response.json())

    # response = await session.get(
    #     "http://127.0.0.1:8080/advertisements/1/",
    #
    # )
    # print(response.status)
    # print(await response.json())

    # response = await session.patch(
    #     "http://127.0.0.1:8080/advertisements/4/",
    #     json={
    #         'owner': 'owner_name'
    #     }
    #
    # )
    # print(response.status)
    # print(await response.json())
    #
    # response = await session.get(
    #     "http://127.0.0.1:8080/advertisements/4/",
    #
    # )
    # print(response.status)
    # print(await response.json())

    # response = await session.delete(
    #     "http://127.0.0.1:8080/advertisements/4/",
    # )
    # print(response.status)
    # print(await response.json())
    #
    # response = await session.get(
    #     "http://127.0.0.1:8080/advertisements/4/",
    # )
    # print(response.status)
    # print(await response.json())

    await session.close()


asyncio.run(main())
