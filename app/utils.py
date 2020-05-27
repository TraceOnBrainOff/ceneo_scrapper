#funkcja do ekstrkcji składowych opinii
def extract_element(dom_tree, tag, tag_class, child=None):
    try:
        if child:
            return dom_tree.find(tag,tag_class).find(child).get_text().strip()
        else:
            return dom_tree.find(tag,tag_class).get_text().strip()
    except AttributeError:
        return None

#funkcja do usuwania znaków formatujacych
def remove_whitespaces(string):
    try:
        return string.replace("\n", ", ").replace("\r", ", ")
    except AttributeError:
        pass
