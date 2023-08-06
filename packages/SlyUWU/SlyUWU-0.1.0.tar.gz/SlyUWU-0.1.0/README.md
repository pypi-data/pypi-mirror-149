# ![sly logo](https://raw.githubusercontent.com/dunkyl/SlyMeta/main/sly%20logo.svg) Sly Twitter for Python

> 🚧 **This library is an early work in progress! Breaking changes may be frequent.**

> 🐍 For Python 3.10+

## No-boilerplate, _async_ and _typed_ uwurandom-as-a-service access. 😸

```shell
pip install slyuwu
```

---

Example usage:

```python
import asyncio
from SlyTwitter import *

async def main():

    uwurand = await UWURandom()

    random = await uwurand.random(20)

    print(random) # :3 AAAAAAAAAAA gajhu
    assert len(random) == 20
    
asyncio.run(main())
```
