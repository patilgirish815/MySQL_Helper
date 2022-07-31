def get_items_from_source_that_are_not_in_dest(source, destination):
    return [item for item in source if item not in destination]

def compare_definitions(string1, string2):
    return True if string1 == string2 else False

