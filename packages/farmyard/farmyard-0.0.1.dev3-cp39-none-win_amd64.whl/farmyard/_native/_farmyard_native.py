

def version() -> str:
    ...


def sum_as_string(a: int, b: int) -> str:
    ...


# make sure this module cannot be imported!
raise ModuleNotFoundError("farmyard's rust extensions `_farmyard_native` were not found. It may not have been complied for your system?")
