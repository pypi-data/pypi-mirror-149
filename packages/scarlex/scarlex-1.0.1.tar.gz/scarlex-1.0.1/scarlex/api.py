from typing import Any, ClassVar, Dict, List, Optional, Tuple, Union

import aiohttp

__all__: Tuple[str, ...] = ("ApiClient",)


class ApiResponse:
    __slots__: Tuple[str, ...] = ("message", "status", "json")

    def __init__(self, response: Dict[str, Any]) -> None:
        self.json: Dict[str, Any] = response
        self.message: Union[Dict[str, Any], str] = response.get("message")
        self.status: int = response.get("code")

    @property
    def by(self) -> Optional[List[Dict[str, Any]]]:
        if isinstance(self.message, dict):
            return self.message.get("developers")
        return
        
    def __repr__(self) -> str:
        return f"<Scarlex.ApiResponse status={self.status}>"


class ApiClient:
    r"""A client class for connecting to scarlex api.
    
    Parameters
    ----------
    name: str
        Name of user trying to connect to api.
    password: str
        Password of the user trying to connect to api."""
    __slots__: Tuple[str, ...] = ("name", "password")

    BASE: ClassVar[str] = "https://scarlex.org/api/v1/"

    def __init__(self, name: str, password: str) -> None:
        self.name = name
        self.password = password

    def __repr__(self) -> str:
        return f"<Scarlex.ApiClient name={self.name!r}>"

    async def make_request(self, path: str) -> ApiResponse:
        """A function which makes request to specified endpoint of the client.

        Parameters
        ----------
        path: str
            Endpoint to which request is being made on api.

        Returns
        -------
        ApiResponse
            Response object for the request made to the api.
        """
        async with aiohttp.ClientSession() as session:
            response = await (
                await session.get(self.BASE + path, auth=aiohttp.BasicAuth(self.name, self.password))
            ).json()
        return ApiResponse(response=response)

    async def get_all_endpoints(self) -> ApiResponse:
        """Function for getting all the available api endpoints.

        Returns
        -------
        ApiResponse
            Response object for the request made to 'json' endpoint.
        """
        return await self.make_request("json")
        
