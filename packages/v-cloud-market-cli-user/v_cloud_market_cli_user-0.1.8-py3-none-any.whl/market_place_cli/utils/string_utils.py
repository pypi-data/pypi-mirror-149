def get_unit_num(resource_unit:str) -> str:
    index = resource_unit.find("-")
    return int(resource_unit[:index])

def get_container_memory(resource_unit:str) -> str:
    unit = get_unit_num(resource_unit)
    return str(unit) + "Gi"
