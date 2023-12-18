#include <EEPROM.h>
#include <LinkedList.h>

#define TOTALGARRAFAS 4

struct Drink
{
    int id;
    char nome[20];
    float preco;
    int ingredientes[TOTALGARRAFAS];
};

int endereco = 0;
LinkedList<Drink> listaDeDrinks;
LinkedList<Drink> listaDeDrinksDaEEPROM;

Drink preencherDrink(const String &informacoes) {
    Drink novoDrink;

    // Encontrar os índices dos delimitadores
    int indiceEspaco1 = informacoes.indexOf(' ');
    int indiceEspaco2 = informacoes.indexOf(' ', indiceEspaco1 + 1);
    //int indiceEspaco3 = informacoes.indexOf(' ', indiceEspaco2 + 1);

    // Extrair os substrings
    String idStr = informacoes.substring(0, indiceEspaco1);
    novoDrink.id = idStr.toInt();

    String precoStr = informacoes.substring(indiceEspaco1 + 1, indiceEspaco2);
    novoDrink.preco = precoStr.toFloat();

    // Preencher o array de ingredientes
    for (int i = 0; i < TOTALGARRAFAS; i++) {
        int proximoIndice = informacoes.indexOf(' ', indiceEspaco2 + 1);
        String ingredienteStr = informacoes.substring(indiceEspaco2 + 1, proximoIndice);
        novoDrink.ingredientes[i] = ingredienteStr.toInt(); // (i == 0) ? : 0
        indiceEspaco2 = proximoIndice;
    }

    // Obter o restante da string como o nome
    String nomeStr = informacoes.substring(indiceEspaco2 + 1);
    //HARD*EST* CODE
      if (nomeStr == "Limonada Tropical com Pinga Azul")
        nomeStr = "Limon Trop c Pinga A";
      else if (nomeStr == "Cachaca Limonada Az")
        nomeStr = "Cachaca Limon Azul";
      else if (nomeStr == "Cachaca Limão Campari")
        nomeStr = "Cachaca Lim Campari";
    nomeStr.toCharArray(novoDrink.nome, 20);

    return novoDrink;
}


void adicionarDrinkALista(String informacoes) {
    Drink novoDrink = preencherDrink(informacoes);
    //Serial.println("informações": );
    //Serial.println(informacoes);
    listaDeDrinks.add(novoDrink);
}

void imprimirLista(LinkedList<Drink> lista) {
    for (int i = 0; i < lista.size(); i++) {
        Drink drinkAtual = lista.get(i);

        Serial.print("ID: ");
        Serial.println(drinkAtual.id);

        Serial.print("Preço: ");
        Serial.println(drinkAtual.preco, 2); // 2 casas decimais para o preço

        Serial.println("Ingredientes: ");
        for (int j = 0; j < TOTALGARRAFAS; j++) {
            Serial.print(drinkAtual.ingredientes[j]);
            Serial.println("");
        }

        Serial.print("Nome: ");
        Serial.println(drinkAtual.nome);

        Serial.println(); // Nova linha após os ingredientes

        Serial.println("--------------------");
    }
}

void enviaPraEEPROM()
{
  EEPROM.put(0, listaDeDrinks.size());

  for (int i = 0; i < listaDeDrinks.size(); i++) 
  {  
    EEPROM.put(0 + 2 + (i * sizeof(Drink)), listaDeDrinks.get(i));
    //EEPROM.put(endereco + 2 + (1 * sizeof(Drink)), newDrink2);
    //EEPROM.put(endereco + 2 + (2 * sizeof(Drink)), newDrink3);
  }
}

void readEEPROM(int qtdDrinks)
{
  EEPROM.get(0, qtdDrinks);

  for (int i = 0; i < qtdDrinks; i++)
  {
      Drink newDrink;
      EEPROM.get(0 + 2 + (i) * sizeof(Drink), newDrink);
      listaDeDrinksDaEEPROM.add(newDrink);
  }
}

void setup() {
    Serial.begin(115200);

    
}



void loop()
{
    if (Serial.available() > 0) 
    {
        String texto = Serial.readStringUntil('\n');
        texto.trim();
          if (texto == "INICIOU")
          { 
            listaDeDrinks.clear();
            Serial.println(texto);
          }
          else if (texto == "FINALIZOU")
          {
            Serial.println(texto);
            Serial.println("");
            imprimirLista(listaDeDrinks);
            enviaPraEEPROM();

            readEEPROM(listaDeDrinks.size());
            Serial.println("\nLISTA 2\n");
            imprimirLista(listaDeDrinksDaEEPROM);
          }
          else
          {
            adicionarDrinkALista(texto);
          }
        
        
        //Serial.println(listaDeDrinks.size());
        //imprimirLista();
    } 
    /*else if (listaDeDrinks.size() != 0) 
    {
        // Se a porta serial não tem mais dados e a lista não está vazia,
        // então imprima a lista e pare o loop.
        //imprimirLista();
        while (1) 
        {
            // Mantenha o loop bloqueado aqui ou adicione outra lógica conforme necessário.
        }
    }*/

//imprimirLista();
}