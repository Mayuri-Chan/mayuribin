import asyncio
import uvloop

from mayuribin.mayuribin import MayuriBin

if __name__ == "__main__":
    uvloop.install()
    asyncio.run(MayuriBin().run())
