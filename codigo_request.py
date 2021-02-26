import json
from time import sleep
from os import environ
from igninterage import Igninterage
from lxml.html import fromstring

from gistman import GistMan

"""Envia automaticamente MP para quem postar CODIGO REQUEST no topico."""

URL = 'https://www.ignboards.com/'

MENSAGEM = environ['MENSAGEM']
FORUM_COOKIE = environ['FORUM_COOKIE']
TOPICO = environ['TOPICO']
GIST_TOKEN = environ['GIST_TOKEN']
CONF_FILE_ID = environ['CONF_FILE_ID']
TEMPO = 30

ign = Igninterage(URL, navegador='chrome')
ign.set_cookie(json.loads(FORUM_COOKIE))
gist = GistMan(GIST_TOKEN)


def topico_data(id_post):
    html = ign.interact_session.get(f'{URL}/posts/{id_post}/').content
    tree = fromstring(html)
    xpath_user = f'//*[@id="js-post-{id_post}"]'
    xpath_text = f'{xpath_user}/div/div[2]/div/div[1]/div/article/div[1]'
    my_username = tree.find_class('p-navgroup-linkText')[0].text_content()
    user = tree.xpath(xpath_user)[0].attrib['data-author']
    text = tree.xpath(xpath_text)[0].text_content().replace(f'@{my_username}', '').strip().lower()
    return text, user, id_post


def codigo_request():
    html = ign.interact_session.get(URL + 'account/alerts').content
    tree = fromstring(html)
    alerts = tree.find_class('contentRow-main contentRow-main--close')

    post_ids = [alert.xpath('a/@href')[1].split('/')[-2] for
                alert in alerts if 'replied to the thread ' + TOPICO in alert.text_content()]

    pedidos = [topico_data(post_id) for post_id in reversed(post_ids) if
               int(post_id) > int(gist.read(CONF_FILE_ID)['files']['cod_rec.data']['content'])]

    for pedido in pedidos:
        texto, nick, post_id = pedido
        gist.update(CONF_FILE_ID, 'cod_rec.data', post_id)
        if pedido[0] in ['codigo request', 'código request']:
            print(f'enviando para o user {nick}')
            ign.msg_privada('tá ná mão meu consagrado', MENSAGEM, nick, )
            sleep(TEMPO)
            return True


def main():
    if __name__ == '__main__':
        while True:
            print('rodando...')
            if not codigo_request():
                sleep(TEMPO)


def printa_seus_cookies_de_login():
    ign = Igninterage('https://www.ignboards.com/', navegador='chrome')
    ign.ign_login()
    print(json.dumps(ign.interact_session.cookies.get_dict()))


def cria_arquivo_de_configuracao(gist_token):
    print(GistMan(gist_token).create('cod_rec.data', '0')["id"])


if __name__ == '__main__':
    # printa_seus_cookies_de_login()
    # cria_arquivo_de_configuracao()
    main()
