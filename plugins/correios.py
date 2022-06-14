from api import send_message
import requests
import bs4

def get_objeto(objeto):
    url = "http://www2.correios.com.br/sistemas/rastreamento/newprint.cfm"
    headers = {'User-Agent': 'Nokia6630/1.0 (2.3.129) SymbianOS/8.0 Series60/2.6 Profile/MIDP-2.0 Configuration/CLDC-1.1'}
    data = { 'objetos' : objeto }
    output = requests.post(url, data, headers=headers)

    # Implementando um tratamento de erros basicão
    if output:
        ensopado = bs4.BeautifulSoup(output.content, "html.parser")

        # Este script explora a saída de impressão do SRO
        # Existe um <h4>Rastreamento</h4> quando acontece o erro de pacote não encontrado
        # Como a porra da API dos correios é paga e eles sequer têm a decência de retornar
        # um 404 quando não se acha o objeto, o jeito é esse: pescar
        if ensopado.find("body").find("h4") is not None:
            print("ops n tem")
        else:
            status = ""
            tabelita = ensopado.find("table", class_="listEvent sro").findAll("tr")

            # Corre todas as linhas da tabela
            # Por sorte, ao contrário da implementação do Aulete, estas tabelas têm
            # hierarquia lógica, parece... Muito conveniente, I must say...
            for evento in tabelita:
                # retorna um array contendo várias strings da primeira coluna
                localhora = evento.findAll("td")[0].findAll(text = True)
                # retorna um array contendo várias strings da segunda coluna
                natureza = evento.findAll("td")[1].findAll(text = True)

                # O lascado, agora, é que a porcaria da interface dos correios usa <label>
                # em alguns nomes de cidade. O que significa que o índice dois em diante é,
                # geralmente, uma bagunça... O jeito é concatená-los e arrancar os espaços
                # em branco...
                status += "`" + localhora[1].strip() + " " + localhora[0].strip() + "`"
                status += "\n"

                if len(natureza) > 3:
                    status += "*{} {}*".format(natureza[1].strip(), natureza[3].strip())
                else:
                    status += "*{}*".format(natureza[1].strip())
                status += "\n"

                if len(localhora) > 4:
                    status += "_" + localhora[3].strip() + "_"
                else:
                    status += "_" + localhora[2].strip() + "_"

                status += "\n\n"

    return status

def on_msg_received(msg, matches):
#    try:
    send_message(msg["chat"]["id"], get_objeto(matches.group(1)))
#    except Exception as e:
#        send_message(msg["chat"]["id"], f"ops n deu rsrsrs: {e}")
