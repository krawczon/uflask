def render_template(template_name, **context):
    template_path = f'templates/{template_name}'

    with open(template_path, 'r') as file:
        template_content = file.read()

    rendered_content = template_content

    for key, value in context.items():
        placeholder = f'{{{{ {key} }}}}'
        rendered_content = rendered_content.replace(placeholder, str(value))

    return f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'+rendered_content
