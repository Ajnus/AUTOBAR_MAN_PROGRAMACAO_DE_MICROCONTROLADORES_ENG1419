#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>
#include <RotaryEncoder.h>
#include <GFButton.h>
#include <EEPROM.h>
#include <LinkedList.h>
#include <Stepper.h>

#define TOTALGARRAFAS 4
#define QTDUSUARIOS 5
#define TEMPO_DE_ESPERA 10000
#define velmotor 4
#define mla 5
#define mlb 6
#define e1 8
#define e2 9
#define e3 10
#define e4 11
#define passosPorGiro 32

int vel = 0;
const int pinoSensor = 7; // PINO DIGITAL UTILIZADO PELO SENSOR
bool estadoSensor = LOW;

// Inicialização dos componentes
hd44780_I2Cexp lcd;
RotaryEncoder encoder(2, 3);
GFButton botao(A1);
Stepper mp(passosPorGiro, e1, e3, e2, e4);

// Variáveis globais
struct Drink
{
    int id;
    char nome[20];
    int ingredientes[TOTALGARRAFAS];
    float preco;
};
const String nomes[5] = {"Ricardo", "Gralha", "Jam", "Guilherme", "Jan"};
int usuarioSelecionado = 0;
Drink bebidaSelecionada;
int posicaoAnterior = 0;
int tela = 0;
int posicaoEncoder_tela1 = 0;
int posicaoEncoder_tela2 = 0;
int posicaoEncoder_tela3 = 0;
float tamanhoRecipiente = 0;
int endereco = 0;
int zerou = 0;

//-------- BOMBA ----------
unsigned long instanteAnteriorDeDeteccao = 0;

int porta_digital_bomba[] = {47, 49, 51, 53};
float constanteBomba[] = {20, 22, 25, 25};
float volumes[3] = {};
int indice_porta_bomba = 0;
bool estado = false;

//-------- MIXER---------
bool estado_mixer = false;

/*
Drink newDrink1;
Drink newDrink2;
Drink newDrink3;
Drink newDrink4;
Drink newDrink5;
*/

LinkedList<Drink> listaDeDrinks;

// funcoes Auxiliares

Drink preencherDrink(const String &informacoes)
{
    Drink novoDrink;

    // Encontrar os índices dos delimitadores
    int indiceEspaco1 = informacoes.indexOf(' ');
    int indiceEspaco2 = informacoes.indexOf(' ', indiceEspaco1 + 1);
    // int indiceEspaco3 = informacoes.indexOf(' ', indiceEspaco2 + 1);

    // Extrair os substrings
    String idStr = informacoes.substring(0, indiceEspaco1);
    novoDrink.id = idStr.toInt();

    String precoStr = informacoes.substring(indiceEspaco1 + 1, indiceEspaco2);
    novoDrink.preco = precoStr.toFloat();

    // Preencher o array de ingredientes
    for (int i = 0; i < TOTALGARRAFAS; i++)
    {
        int proximoIndice = informacoes.indexOf(' ', indiceEspaco2 + 1);
        String ingredienteStr = informacoes.substring(indiceEspaco2 + 1, proximoIndice);
        novoDrink.ingredientes[i] = ingredienteStr.toInt(); // (i == 0) ? : 0
        indiceEspaco2 = proximoIndice;
    }

    // Obter o restante da string como o nome
    String nomeStr = informacoes.substring(indiceEspaco2 + 1);
    // HARD*EST* CODE
    if (nomeStr == "Limonada Tropical com Pinga Azul")
        nomeStr = "Limon Trop c Pinga A";
    else if (nomeStr == "Cachaca Limonada Az")
        nomeStr = "Cachaca Limon Azul";
    else if (nomeStr == "Cachaca Limão Campari")
        nomeStr = "Cachaca Lim Campari";
    nomeStr.toCharArray(novoDrink.nome, 20);

    return novoDrink;
}

void adicionarDrinkALista(String informacoes)
{
    Drink novoDrink = preencherDrink(informacoes);
    // Serial.println("informações": );
    // Serial.println(informacoes);
    listaDeDrinks.add(novoDrink);
}

void imprimirLista()
{
    for (int i = 0; i < listaDeDrinks.size(); i++)
    {
        Drink drinkAtual = listaDeDrinks.get(i);

        Serial.print("ID: ");
        Serial.println(drinkAtual.id);

        Serial.print("Preço: ");
        Serial.println(drinkAtual.preco, 2); // 2 casas decimais para o preço

        Serial.println("Ingredientes: ");
        for (int j = 0; j < TOTALGARRAFAS; j++)
        {
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
    Serial.println("ENVIAPRAEEPROM LISTADEDDRINKS SIZE:");
    Serial.println(listaDeDrinks.size());
    

    for (int i = 0; i < listaDeDrinks.size(); i++)
    {
        EEPROM.put(0 + 2 + (i * sizeof(Drink)), listaDeDrinks.get(i));
        // EEPROM.put(endereco + 2 + (1 * sizeof(Drink)), newDrink2);
        // EEPROM.put(endereco + 2 + (2 * sizeof(Drink)), newDrink3);
    }
}

/*
void readEEPROM()
{
  int qtdDrinks;
  int endereco = 0;

    EEPROM.get(endereco, qtdDrinks);

    for (int i = 0; i < qtdDrinks; i++)
    {
        Drink newDrink;
        EEPROM.get(endereco + 2 + (i) * sizeof(Drink), newDrink);
        listaDeDrinksDaEEPROM.add(newDrink);
    }
}
*/


void pedidoConcluido(int posicao);
void tickDoEncoder()
{
    encoder.tick();
}

/*
void insere()
{
    newDrink1.id = 1;
    strcpy(newDrink1.nome, "Pina Colada");
    newDrink1.ingredientes[0] = 30;
    newDrink1.ingredientes[1] = 20;
    newDrink1.ingredientes[2] = 30;
    newDrink1.ingredientes[3] = 20;
    newDrink1.preco = 15;

    newDrink2.id = 2;
    strcpy(newDrink2.nome, "Margarita");
    newDrink2.ingredientes[0] = 10;
    newDrink2.ingredientes[1] = 10;
    newDrink2.ingredientes[2] = 10;
    newDrink2.ingredientes[3] = 70;
    newDrink2.preco = 15;

    newDrink3.id = 3;
    strcpy(newDrink3.nome, "Martini");
    newDrink3.ingredientes[0] = 10;
    newDrink3.ingredientes[1] = 30;
    newDrink3.ingredientes[2] = 10;
    newDrink3.ingredientes[3] = 50;
    newDrink3.preco = 15;

    EEPROM.put(endereco, 3);
    EEPROM.put(endereco + 2 + (0 * sizeof(Drink)), newDrink1);
    EEPROM.put(endereco + 2 + (1 * sizeof(Drink)), newDrink2);
    EEPROM.put(endereco + 2 + (2 * sizeof(Drink)), newDrink3);
}
*/

void le()
{
    int qtd;
    int endereco = 0;

    EEPROM.get(endereco, qtd);
    for (int i = 0; i < qtd; i++)
    {
        Drink newDrink;
        EEPROM.get(endereco + 2 + (i) * sizeof(Drink), newDrink);
        listaDeDrinks.add(newDrink);
    }
}

// Inicialização do AutoBar Man
void inicial()
{
    lcd.setCursor(0, 0);
    lcd.print("--------------------");
    lcd.setCursor(0, 1);
    lcd.print("  Seja bem-vindo!   ");
    lcd.setCursor(0, 2);
    lcd.print("  Auto BarMan 1.0   ");
    lcd.setCursor(0, 3);
    lcd.print("--------------------");
    delay(1000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Selecione seu nome:");
    lcd.setCursor(0, 1);
    lcd.print(">");
}

// Seleciona o usuário
void selecionaUsuario(int posicao)
{
    if (posicao > posicaoAnterior)
    {
        posicaoEncoder_tela1 = (posicaoEncoder_tela1 + 1) % 5;
        if (posicaoEncoder_tela1 > QTDUSUARIOS)
        {
            posicaoEncoder_tela1 = 0;
        }
    }
    else if (posicao < posicaoAnterior)
    {
        posicaoEncoder_tela1 = (posicaoEncoder_tela1 - 1) % 5;
        if (posicaoEncoder_tela1 < 0)
        {
            posicaoEncoder_tela1 = QTDUSUARIOS;
        }
    }
    // Serial.print(abs(posicaoEncoder));
    tela = 0;
    lcd.setCursor(0, 0);
    lcd.print("Selecione seu nome:");
    lcd.setCursor(0, 1);
    lcd.print(nomes[abs(posicaoEncoder_tela1)]);
    lcd.setCursor(0, 1);
    lcd.print("                    "); // Espaços em branco para limpar a linha
    lcd.setCursor(0, 1);
    lcd.print(">");
    lcd.print(nomes[abs(posicaoEncoder_tela1)]);
    botao.setPressHandler(bebidaPredefinida);
    usuarioSelecionado = posicaoEncoder_tela1;
}

// Seleciona bebida
void bebidaPredefinida(int posicao)
{
    if (posicao > posicaoAnterior)
    {
        posicaoEncoder_tela2 = (posicaoEncoder_tela2 + 1);
        if (posicaoEncoder_tela2 >= listaDeDrinks.size())
        {
            posicaoEncoder_tela2 = 0;
        }
    }
    else if (posicao < posicaoAnterior)
    {
        posicaoEncoder_tela2 = (posicaoEncoder_tela2 - 1);
        if (posicaoEncoder_tela2 <= 0)
        {
            posicaoEncoder_tela2 = listaDeDrinks.size();
        }
    }
    // posicaoEncoder = posicaoEncoder % listaDeDrinks.size();;

    if (tela == 2)
    {
        lcd.clear();
    }
    lcd.clear();
    tela = 3;
    lcd.setCursor(0, 0);
    lcd.print("Qual bebida deseja?");
    lcd.setCursor(0, 1);
    lcd.print("                    "); // Espaços em branco para limpar a linha
    lcd.setCursor(0, 1);
    lcd.print(">");
    lcd.print(listaDeDrinks.get(abs(posicaoEncoder_tela2)).nome);
    botao.setPressHandler(qtdRecipiente);
    bebidaSelecionada = listaDeDrinks.get(abs(posicaoEncoder_tela2));
}

// Seleciona tamanho do recipiente do cliente
void qtdRecipiente(int posicao)
{
    if (posicao > posicaoAnterior)
    {
        posicaoEncoder_tela3 = posicaoEncoder_tela3 + 50;
        if (posicaoEncoder_tela3 > 300)
        {
            posicaoEncoder_tela3 = 50;
        }
    }
    else if (posicao < posicaoAnterior)
    {
        posicaoEncoder_tela3 = posicaoEncoder_tela3 - 50;
        if (posicaoEncoder_tela3 < 50)
        {
            posicaoEncoder_tela3 = 300;
        }
    }

    if (tela == 3)
    {
        lcd.clear();
    }

    // Serial.println(posicaoEncoder);
    // Serial.println(posicao);
    tela = 4;
    lcd.setCursor(0, 0);
    lcd.print("Qual o tamanho do");
    lcd.setCursor(0, 1);
    lcd.print("seu recipiente?");
    lcd.setCursor(0, 3);
    lcd.print(posicaoEncoder_tela3);
    lcd.print(" ml");
    lcd.print("           ");
    botao.setPressHandler(pedidoConcluido);
    tamanhoRecipiente = posicaoEncoder_tela3;
}

// Insere liquido
void insereLiquido()
{
    estadoSensor = digitalRead(pinoSensor);
    if (estadoSensor == LOW)
    {
        if (estado == true)
        { //
            if (indice_porta_bomba == 0)
            {
                digitalWrite(porta_digital_bomba[indice_porta_bomba], LOW);
                Serial.print("ligou bomba do indice: ");
                Serial.println(indice_porta_bomba);
                Serial.println(((volumes[indice_porta_bomba] / constanteBomba[indice_porta_bomba]) * 1000));
                if (millis() > instanteAnteriorDeDeteccao + (volumes[indice_porta_bomba] / constanteBomba[indice_porta_bomba]) * 1000)
                {
                    instanteAnteriorDeDeteccao = millis();
                    digitalWrite(porta_digital_bomba[indice_porta_bomba], HIGH);
                    Serial.println("desligou bomba do indice ");
                    Serial.println(indice_porta_bomba);
                    indice_porta_bomba = indice_porta_bomba + 1;
                    Serial.println("novo indice");
                    Serial.println(indice_porta_bomba);
                }
            }
            if (indice_porta_bomba < 4 && indice_porta_bomba > 0)
            {
                digitalWrite(porta_digital_bomba[indice_porta_bomba], LOW);
                Serial.print("ligou bomba do indice: ");
                Serial.println(indice_porta_bomba);
                Serial.println(((volumes[indice_porta_bomba] / constanteBomba[indice_porta_bomba]) * 1000));
                if (millis() > instanteAnteriorDeDeteccao + (volumes[indice_porta_bomba] / constanteBomba[indice_porta_bomba]) * 1000)
                {
                    instanteAnteriorDeDeteccao = millis();
                    digitalWrite(porta_digital_bomba[indice_porta_bomba], HIGH);
                    Serial.println("desligou bomba do indice ");
                    Serial.println(indice_porta_bomba);
                    indice_porta_bomba = indice_porta_bomba + 1;
                    Serial.println("novo indice");
                    Serial.println(indice_porta_bomba);
                    if (indice_porta_bomba == 4)
                    {
                        indice_porta_bomba = 0;
                        estado = false;
                        estado_mixer = true;
                        if (estado_mixer == true)
                        {
                            vel = 55;
                            analogWrite(velmotor, vel);

                            motorPasso(500, 1, 1, 1000);

                            digitalWrite(mlb, HIGH);
                            digitalWrite(mla, LOW);

                            delay(2000);

                            vel = 35;
                            analogWrite(velmotor, vel);

                            delay(5000);

                            digitalWrite(mlb, LOW);
                            digitalWrite(mla, LOW);

                            delay(1000);

                            motorPasso(500, -1, 1, 3000);
                            estado_mixer == false;
                        }
                    }
                }
            }
        }
    }
    else
    {
        estado == false;
        digitalWrite(47, HIGH);
        digitalWrite(49, HIGH);
        digitalWrite(51, HIGH);
        digitalWrite(53, HIGH);
    }
}

// Pedido concluido
void pedidoConcluido(int posicao)
{
    lcd.clear();
    tela = 5;
    lcd.setCursor(0, 0);
    lcd.print("Aguarde...");
    lcd.setCursor(0, 1);
    lcd.print("Preparando bebida!");
    Serial.println("----------------------");
    Serial.println(nomes[usuarioSelecionado]);
    Serial.println(bebidaSelecionada.nome);
    Serial.println(tamanhoRecipiente);
    // Serial.println("----------");
    // Serial.println(bebidaSelecionada.ingredientes[0]);
    // Serial.println(bebidaSelecionada.ingredientes[1]);
    // Serial.println(bebidaSelecionada.ingredientes[2]);
    // Serial.println(bebidaSelecionada.ingredientes[3]);

    Serial.println("----------");
    Serial.println((tamanhoRecipiente * bebidaSelecionada.ingredientes[0]) / 100);
    Serial.println((tamanhoRecipiente * bebidaSelecionada.ingredientes[1]) / 100);
    Serial.println((tamanhoRecipiente * bebidaSelecionada.ingredientes[2]) / 100);
    Serial.println((tamanhoRecipiente * bebidaSelecionada.ingredientes[3]) / 100);
    volumes[0] = (tamanhoRecipiente * bebidaSelecionada.ingredientes[0]) / 100;
    volumes[1] = (tamanhoRecipiente * bebidaSelecionada.ingredientes[1]) / 100;
    volumes[2] = (tamanhoRecipiente * bebidaSelecionada.ingredientes[2]) / 100;
    volumes[3] = (tamanhoRecipiente * bebidaSelecionada.ingredientes[3]) / 100;
    // Serial.println(volumes[3]);
    // insereliquido
    // delay(TEMPO_DE_ESPERA);  // tempo de espera para a bebida ficar pronta

    lcd.clear();
    selecionaUsuario(posicao);
    estado = true;
    instanteAnteriorDeDeteccao = millis();
}

void motorPasso(int vel, int sentido, int voltas, int tmp)
{
    mp.setSpeed(vel);
    for (int i = 0; i < (32 * voltas); i++)
    {
        mp.step(passosPorGiro * sentido);
    }
    delay(tmp);
}

// SETUP
void setup()
{
    Serial.begin(115200);
    //enviaPraEEPROM();

    le();
    lcd.begin(20, 4);
    pinMode(53, OUTPUT);
    pinMode(51, OUTPUT);
    pinMode(49, OUTPUT);
    pinMode(47, OUTPUT);

    digitalWrite(53, HIGH);
    digitalWrite(51, HIGH);
    digitalWrite(49, HIGH);
    digitalWrite(47, HIGH);

    pinMode(velmotor, OUTPUT);
    pinMode(mla, OUTPUT);
    pinMode(mlb, OUTPUT);
    digitalWrite(mla, LOW);
    digitalWrite(mlb, LOW);
    analogWrite(velmotor, vel);

    pinMode(pinoSensor, INPUT); // DEFINE O PINO COMO ENTRADA

    int origem1 = digitalPinToInterrupt(2);
    attachInterrupt(origem1, tickDoEncoder, CHANGE);
    int origem2 = digitalPinToInterrupt(3);
    attachInterrupt(origem2, tickDoEncoder, CHANGE);
    inicial();

    Serial.println("LISTADEDDRINKS SIZE:");
    Serial.println(listaDeDrinks.size());
    imprimirLista();
}

// LOOP
void loop()
{
    insereLiquido();
    botao.process();
    int posicao = encoder.getPosition();

    if (posicao != posicaoAnterior)
    {
        if (tela == 0)
        {
            if (zerou == 0)
            {
                posicaoEncoder_tela1 = 0;
                zerou = 1;
            }
            else
            {
                selecionaUsuario(posicao);
            }
        }
        else if (tela == 3)
        {
            if (zerou == 3)
            {
                posicaoEncoder_tela2 = 0;
                zerou = 4;
            }
            else
            {
                bebidaPredefinida(posicao);
            }
        }
        else if (tela == 4)
        {
            if (zerou == 4)
            {
                posicaoEncoder_tela3 = 0;
                zerou = 5;
            }
            else
            {
                qtdRecipiente(posicao);
            }
        }
        encoder.setPosition(posicao);
    }
    posicaoAnterior = posicao;

    if (Serial.available() > 0)
    {
        String texto = Serial.readStringUntil('\n');
        texto.trim();
        //Serial.println("O TEXTO:");
        //Serial.println(texto);

        if (texto == "INICIOU")
        {
            listaDeDrinks.clear();
            EEPROM.put(0,0);
            Serial.println(texto);
        }
        else if (texto == "FINALIZOU")
        {
            Serial.println(texto);
            Serial.println("");
            imprimirLista();
            enviaPraEEPROM();

            le();
            Serial.println("\nLISTA PÓS-EEPROM\n");
            imprimirLista();
        }
        else if (texto != "INICIOU" && texto != "FINALIZOU")
        {
            adicionarDrinkALista(texto);
        }
    }
}