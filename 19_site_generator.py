import json
import os

import jinja2
import markdown


def load_config(filepath):
    with open(filepath, "r", encoding='utf-8') as input_file:
        raw_json_data = json.load(input_file)
    return raw_json_data


def get_sub_menu_items(json_data, main_menu_item):
    sub_menu_items = \
        [x for x in json_data['articles'] if x['topic'] == main_menu_item]
    return sub_menu_items


def get_menu_structure(json_data):
    main_level_menu = json_data['topics']
    right_menu_structure = []
    for item in main_level_menu:
        sub_menu_items = get_sub_menu_items(json_data, item['slug'])
        item.update({'articles': sub_menu_items})
        right_menu_structure.append(item)
    return right_menu_structure


def render_articles_pages_to_file(tpl_path, json_data):
    path, filename = os.path.split(tpl_path)
    for article in json_data['articles']:
        with open('articles/' + article['source'], "r",
                  encoding='utf-8') as input_file:
            md_text = input_file.read()
            html_text = markdown.markdown(md_text, extensions=[
                'markdown.extensions.codehilite'])
            context = {
                'article': html_text
            }
            html = jinja2.Environment(loader=jinja2.FileSystemLoader(
                path)).get_template(filename).render(context)
            with open('articles/' + article['source'] + '.html', 'w',
                      encoding='utf-8') as output_file:
                output_file.write(html)


def render_index_page_to_file(tpl_path, json_data):
    path, filename = os.path.split(tpl_path)
    main_menu = get_menu_structure(json_data)
    context = {
        'main_menu': main_menu
    }
    html = jinja2.Environment(autoescape=True, trim_blocks=True,
                              loader=jinja2.FileSystemLoader(
                                  path)).get_template(filename).render(context)
    with open('index.html', 'w', encoding='utf-8') as output_file:
        output_file.write(html)


def generate_static_site(config_file):
    json_data = load_config(config_file)
    render_index_page_to_file('templates/index.html', json_data)
    render_articles_pages_to_file('templates/article.html', json_data)


if __name__ == '__main__':
    print('Generate site from MD articles...')
    generate_static_site('config.json')
    print('done.')

