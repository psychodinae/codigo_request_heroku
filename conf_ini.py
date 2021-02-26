import json

from igninterage import Igninterage

from gistman import GistMan


def printa_seus_cookies_de_login():
    ignc = Igninterage('https://www.ignboards.com/', navegador='chrome')
    ignc.ign_login()
    print(json.dumps(ignc.interact_session.cookies.get_dict()))


def cria_arquivo_de_configuracao(gist_token):
    print(GistMan(gist_token).create('cod_rec.data', '0')["id"])