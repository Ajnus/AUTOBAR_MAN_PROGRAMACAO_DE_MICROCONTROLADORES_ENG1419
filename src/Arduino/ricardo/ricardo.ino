#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>
#include <RotaryEncoder.h>
#include <GFButton.h>
#include <EEPROM.h>
#include <LinkedList.h>

#define TOTALGARRAFAS 4
#define QTDUSUARIOS 5
#define TEMPO_DE_ESPERA 10000

// Inicialização dos componentes
hd44780_I2Cexp lcd;
RotaryEncoder encoder(2, 3);
GFButton botao(A1);

// Variáveis globais
struct Drink
{
    int id;
    char nome[20];
    float preco;
    int ingredientes[TOTALGARRAFAS];
};

//indedxof pra pegar o string DRINK(ID PREÇO PP1 PP2 PP3 PP4 NOME)
const String nomes[5] = {"Ricardo", "Gralha", "Jam", "Guilherme", "Jan"};
int usuarioSelecionado = 0;
Drink bebidaSelecionada;
int posicaoAnterior = 0;
int tela = 0;
int posicaoEncoder_tela1 = 0;
int posicaoEncoder_tela2 = 0;
int posicaoEncoder_tela3 = 0;
int tamanhoRecipiente = 0;
int endereco = 0;
int zerou = 0;

Drink newDrink1;
Drink newDrink2;
Drink newDrink3;
Drink newDrink4;
Drink newDrink5;

LinkedList<Drink> listaDeDrinks;

// funcoes Auxiliares

void tickDoEncoder()
{
    encoder.tick();
}

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
