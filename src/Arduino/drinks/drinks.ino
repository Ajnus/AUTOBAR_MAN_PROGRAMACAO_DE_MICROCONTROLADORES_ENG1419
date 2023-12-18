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

void preencherDrinks(const char *informacoes, Drink drinks[], int numDrinks) {
    const char *delimiter = ",";
    char copiaInformacoes[strlen(informacoes) + 1];
    strcpy(copiaInformacoes, informacoes);

    char *token = strtok(copiaInformacoes, delimiter);
    int contador = 0;

    while (token != NULL && contador < numDrinks) {
        drinks[contador].id = atoi(token);

        token = strtok(NULL, delimiter);
        drinks[contador].preco = atof(token);

        // Preencher o array de ingredientes
        for (int i = 0; i < 4; i++) {
            token = strtok(NULL, delimiter);
            drinks[contador].ingredientes[i] = (token != NULL) ? atoi(token) : 0;
        }

        token = strtok(NULL, delimiter);
        strcpy(drinks[contador].nome, token);

        token = strtok(NULL, delimiter);
        contador++;
    }
}


LinkedList<Drink> listaDeDrinks;

void setup() {
  Serial.begin(115200);

}

void loop() {
  //Serial.println("HELLO THERE");
  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    texto.trim();
    Serial.println(texto);
  }
 
  //delay(3000);

}
