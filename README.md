# Simulador de Escalonamento de Processos
Este projeto é um simulador gráfico de algoritmos de escalonamento de processos, desenvolvido como trabalho final da disciplina de Sistemas Operacionais.
O objetivo deste README é explicar como preparar o ambiente, executar o simulador e utilizar a interface gráfica.

---
## Requisitos
Para executar o projeto, recomenda-se utilizar:
- Visual Studio Code;
- Python 3.13.14;
- Extensão Python instalada no Visual Studio Code.

O projeto foi desenvolvido e testado no **Visual Studio Code**, por isso essa é a IDE recomendada para abrir e executar o simulador.
Caso o Python não esteja instalado, ele pode ser instalado pelo site oficial do Python ou, em alguns casos, pela Microsoft Store.

---
## Como abrir o projeto
1. Abra o Visual Studio Code;
2. Clique em **File > Open Folder**, ou, se o VSCode estiver em português **Arquivo > Abrir Pasta**;
3. Selecione a pasta principal do projeto;
4. Caso apareça uma notificação solicitando a instalação da extensão Python, clique em **Install** ou **Sim**;
5. Caso o VSCode solicite a instalação/configuração do ambiente Python ou UV, aceite a instalação.

---
## Como executar o simulador
Existem duas formas principais de executar o simulador.

### Opção 1 — Executar pelo botão de Run do VSCode
1. Abra o projeto no VSCode;
2. Localize e abra o arquivo **gui.py**;
3. Com o arquivo **gui.py** aberto, clique no botão de **Run** no canto superior direito da tela;
4. A interface gráfica do simulador será aberta.

### Opção 2 — Executar pelo terminal
1. Abra o projeto no VSCode;
2. Abra um novo terminal em **Terminal > New Terminal**, ou **Terminal > Novo Terminal**;
3. No terminal, execute:
> python gui.py
4. Pressione **Enter**.

Se o comando acima não funcionar, execute o arquivo usando o caminho absoluto.
Exemplo no Windows:
> python "C:\Users\lfonseca\OneDrive - Septodont\Pessoal - Luan\APRENDIZAGEM\Sistemas Operacionais 01-26\Entrega-TrabalhoFinalSO\gui.py"

**Importante: O uso aspas é obrigatório quando o caminho possuir espaços no nome das pastas, como no exemplo acima.**

---
## Como utilizar a interface gráfica
Ao executar o arquivo **gui.py**, será aberta a janela principal do simulador.
A interface permite:
- cadastrar processos (1);
- remover processos cadastrados (1);
- escolher o algoritmo de escalonamento (2);
- configurar o quantum no Round Robin (2);
- executar a simulação (3);
- resetar a simulação (3);
- visualizar o gráfico de Gantt (4);
- consultar as métricas médias da simulação (5).

<img width="500" alt="interface_grafica" src="https://github.com/user-attachments/assets/49eb423b-634a-4a86-b736-f0448782c94b" />

---
## Cadastro de processos
Para adicionar um processo, preencha os campos disponíveis na seção **Adicionar processo**.

### Campos do processo
- **Nome**: identificação do processo, por exemplo **P1**, **P2** ou **Processo A**;
- **Arrival**: tempo de chegada do processo no sistema;
- **Burst**: tempo total de CPU necessário para o processo terminar;
- **Priority**: prioridade do processo.

Depois de preencher os campos, clique em **Adicionar**.
O processo será exibido na tabela acima do cadastro de processos.

## Regras para cadastro
Os campos devem seguir as seguintes regras:
- O campo **Nome** não pode estar vazio;
- O campo **Arrival** deve ser um número inteiro maior ou igual a **0**;
- O campo **Burst** deve ser um número inteiro maior que **0**;
- O campo **Priority** deve ser um número inteiro maior ou igual a **0**.

No projeto, a prioridade segue a convenção **Menor valor numérico = maior prioridade**.
Exemplo: priority = 1 tem maior prioridade que priority = 5.

<img width="500" alt="cadastro_processo" src="https://github.com/user-attachments/assets/d97445d5-9204-433b-b999-3cc6a260208c" />

<img width="300" alt="processo_adicionado" src="https://github.com/user-attachments/assets/5583232c-4413-4594-80f4-11133e08a3cd" />

---
## Remoção de processos
Para remover um processo cadastrado:
1. Selecione o processo na tabela;
2. Clique em **Remover selecionado**.

O processo será removido da tabela e não será considerado na próxima simulação.

<img width="500" alt="remover_processo" src="https://github.com/user-attachments/assets/a18b5d98-046d-400a-829a-4ffa62d3d398" />

<img width="300" alt="processo_removido" src="https://github.com/user-attachments/assets/95e62e2f-198f-4747-99da-2f1988bfc1c1" />

---
## Seleção do algoritmo de escalonamento
Na seção **Scheduler**, selecione o algoritmo desejado.
Os algoritmos disponíveis são:
- **FIFO**;
- **SJF**;
- **Priority**;
- **Round Robin**.

## Algoritmos disponíveis
### FIFO
O algoritmo **FIFO** executa primeiro o processo que chegou primeiro.
Nesta versão, ele é **não-preemptivo**, ou seja, quando um processo começa a executar, ele permanece na CPU até terminar.

### SJF (Shortest Job First)
O algoritmo **SJF** seleciona o processo com menor **Burst** entre os processos disponíveis.
Nesta versão, ele é **não-preemptivo**.

### Priority
O algoritmo **Priority** seleciona o processo com maior prioridade.
Nesta versão, o algoritmo de prioridade é **não-preemptivo**.

### Round Robin
O algoritmo **Round Robin** distribui a CPU entre os processos utilizando um valor de **quantum**.
O quantum representa a quantidade máxima de ticks consecutivos que um processo pode executar antes de ser interrompido, caso ainda não tenha terminado.
Ao selecionar **Round Robin**, o campo **Quantum** será habilitado.
O valor do quantum deve ser um número inteiro maior que **0**.

<img width="500" alt="selecao_algoritmo" src="https://github.com/user-attachments/assets/10a54e3f-eb50-48a4-bed9-0d0d8ca9aa8b" />

<img width="300" alt="selecao_quantum" src="https://github.com/user-attachments/assets/441a7297-2023-40cb-bed9-8557719148d1" />

---
## Executando a simulação
Antes de executar a simulação, certifique-se de que:
1. Pelo menos um processo foi cadastrado.
2. O algoritmo de escalonamento foi selecionado.
3. Caso o algoritmo seja Round Robin, o quantum foi informado corretamente.

Depois, clique em **Run**.

Ao final da simulação, serão exibidos:
- o gráfico de Gantt;
- a média de turnaround time;
- a média de waiting time.

---
## Resetando os resultados
Após executar uma simulação, é possível limpar os resultados clicando em **Reset**.
O botão **Reset** limpa:
- o gráfico de Gantt;
- a média de turnaround time exibida;
- a média de waiting time exibida.

O botão **Reset** não remove os processos cadastrados na tabela.

---
## Exemplo de teste rápido
Para testar rapidamente o simulador, cadastre os seguintes processos:

| Nome | Arrival | Burst | Priority |
| ---- | ------- | ----- | -------- |
|  P1  |    0    |   5   |    1     |
|  P2  |    1    |   3   |    2     |
|  P3  |    2    |   4   |    0     |

Depois:
1. Selecione um algoritmo de escalonamento;
2. Clique em **Run**;
3. Observe o gráfico de Gantt e as métricas exibidas.

<img width="500" alt="executado" src="https://github.com/user-attachments/assets/0a1564e2-f0a3-4bf0-a72b-9adc7bd1878b" />

---
## Interpretação dos resultados
### Gráfico de Gantt
O gráfico de Gantt mostra a ordem e o intervalo de execução dos processos na CPU.
Cada bloco colorido representa um processo executando durante determinado intervalo de tempo.
O eixo inferior representa os ticks da simulação.

### Avg Turnaround
Representa o tempo médio entre a chegada dos processos e sua finalização.
Fórmula utilizada: 
**turnaround_time = finish_time - arrival_time**

### Avg Waiting
Representa o tempo médio que os processos passaram aguardando para utilizar a CPU.
Fórmula utilizada: 
**waiting_time = turnaround_time - burst_time**

---
## Possíveis problemas e soluções
### O comando 'python gui.py' não funciona
Verifique se:
1. O Python está instalado.
2. O terminal está aberto na pasta correta do projeto.
3. O arquivo **gui.py** está na pasta atual.
4. O comando **python** está reconhecido pelo sistema operacional.

### O VSCode não reconhece o Python
Tente as seguintes alternativas:
1. Feche e abra novamente o VSCode.
2. Instale a extensão Python no VSCode.
3. Selecione o interpretador Python correto.
4. Reinstale o Python, se necessário.

### A interface gráfica não abre
Verifique se o arquivo correto está sendo executado, **gui.py**.
Também verifique se não há mensagens de erro no terminal.

### A simulação não executa
Verifique se pelo menos um processo foi adicionado antes de clicar em **Run**.
A simulação não inicia se a lista de processos estiver vazia.

---
## Observações finais
A interface gráfica foi criada para facilitar o uso do simulador e a visualização dos resultados, permitindo comparar diferentes algoritmos de escalonamento de forma simples.

## Autor
Desenvolvido por **Luan Garcia da Fonseca**.
