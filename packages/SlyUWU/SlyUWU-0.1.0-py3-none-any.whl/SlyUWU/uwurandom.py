from SlyAPI import WebAPI

class UWURandom(WebAPI):
    base_url = 'https://uwurandom.bs2k.me/nya'
    
    def __init__(self):
        super().__init__(None)

    async def of_length(self, l: int) -> str:
        """
            Get UWU random text.
        """
        return await self.get_text(f'/{l}')
   