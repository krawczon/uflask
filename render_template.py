def render_template(*args, **kwargs):

    file = open(args[0], "r")
    content = file.read()
    formated_content = content.format(**kwargs)
    file.close()

    return formated_content
