import levrt
from levrt import Cr, annot, ctx
from levrt.annot.cats import Attck


@annot.meta(
    desc="Hello",
    params=[annot.Param("name", "person name")],
    cats=[Attck.Reconnaissance],
)
def hello(name: str = "world") -> Cr:
    @levrt.remote
    def entry():
        ctx.set(msg=f"Hello, {name}!")

    return Cr("alpine:latest", entry=entry())


__lev__ = annot.meta([hello])
