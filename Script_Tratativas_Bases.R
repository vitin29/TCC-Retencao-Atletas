########################################
######### pacotes utilizados ###########
########################################

library(readr)
library(tidyverse)

########################################
########## importando bases ############
########################################

TB_Transferencias_Empilhada <- read_csv("TCC Victor/01.Bases/TB_Transferencias_Empilhada.csv")
TB_Jogadores_Empilhada <- read_csv("TCC Victor/01.Bases/TB_Empilhada_Jogadores.csv")
TB_Estatisticas_Empilhada <- read_csv("TCC Victor/01.Bases/TB_Empilhada_Estatisticas.csv")

########################################
######### Tratamentos iniciais #########
########################################

# Cruzar informações entre Estatisticas e Jogadores (ID_Jogador + Time + Identifier)

Dados <- TB_Jogadores_Empilhada %>% 
  inner_join(TB_Estatisticas_Empilhada %>% 
               select(-Camp,-Ano,-Nacionalidade,-Jogador,-Numero),by = c("ID_Jogador","Time","Identifier"))

# Tratar No_Time_Desde e criar Elegíveis
# att 27-01-2024: Descobri que os jogadores NA's não precisam ser filtrados pois eles podem sim ter jogado aquela temporada,
# e jogadores que tem a data acima do fim do campeonato são em absoluta maioria jogadores que foram adquiridos ao final da temporada(Empréstimo),
# ou já saíram do clube e voltaram algumas temporadas após. Como esses casos totalizam 478 ~ 23% dos dados eu vou considerar um valor ausente, visto que
# o inner join com a tabela estatísticas já me coloca a par de que foram jogadores elegíveis aquela temporada
# Remover os q

# Dados <- Dados %>% 
#   mutate(No_time_desde = as.Date(No_time_desde, format = "%d/%m/%Y")) %>% 
#   filter(!is.na(No_time_desde)) %>% 
#   mutate(Elegivel = case_when(Identifier == "BRA1_2022" & No_time_desde <= as.Date("13/11/2022", format = "%d/%m/%Y")~ 1,
#                               Identifier == "BRA1_2023" & No_time_desde <= as.Date("06/12/2023", format = "%d/%m/%Y")~ 1,
#                               TRUE ~ 0)) %>% 
#   filter(Elegivel == 1)

Dados <- Dados %>% 
  mutate(No_time_desde = as.Date(No_time_desde, format = "%d/%m/%Y")) %>% 
  mutate(No_time_desde=case_when(Identifier == "BRA1_2022" & No_time_desde <= as.Date("13/11/2022", format = "%d/%m/%Y")~ No_time_desde,
                                 Identifier == "BRA1_2023" & No_time_desde <= as.Date("06/12/2023", format = "%d/%m/%Y")~ No_time_desde,
                                 TRUE ~ NA))

########################################
##### trazendo variável resposta #######
########################################

# Regras para Variável Resposta.
# 1. A nível Time+Ano+ID_Jogador se tiver Tipo_Registro = Saída Y=1
# 2. Senão se mais Entradas Y=0 senão se mais Saídas Y=1
# 2. Se saídas = Entradas: 
#      Se Houver: Tipo_Entrada = Entrada + Fim_Emprestimo Y=0,
#      Senao se: Tipo_Entrada = Retorno_Emprestimo + Saida Emprestimo & Destino igual Y=0
#      Se não: Y=1

TB_Transferencias_Saidas <- TB_Transferencias_Empilhada %>% 
  mutate(
    Tipo_Registro = case_when(
      Status == "Saída" & grepl("Fim do empréstimo", Quantia_Paga) ~ "Fim_Emprestimo",
      Status == "Entrada" & grepl("Fim do empréstimo", Quantia_Paga) ~ "Retorno_Emprestimo",
      Status == "Saída" & grepl("mpréstimo", Quantia_Paga) ~ "Saida_Emprestimo",
      Status == "Entrada" & grepl("mpréstimo", Quantia_Paga) ~ "Entrada_Emprestimo",
      Status == "Entrada" ~ "Entrada",
      Status == "Saída" ~ "Saída"
    )
  ) %>% 
  group_by(ID_Jogador, Time, identifier) %>%
  mutate(
    n_saida   = sum(Status == "Saída"),
    n_entrada = sum(Status == "Entrada"),
    
    Nao_Retencao = case_when(
      # 1) Se existir "Saída" pura no vetor, Y=1 (saiu)
      "Saída" %in% Tipo_Registro ~ 1,
      
      # 2) Se n_saida > n_entrada => Y=1
      n_saida > n_entrada ~ 1,
      
      # 3) Se n_saida < n_entrada => Y=0
      n_saida < n_entrada ~ 0,
      
      # 4) Se n_saida == n_entrada => regras de desempate
      n_saida == n_entrada ~ case_when(
        
        # 4a) Se exatamente Tipo_Registro = c("Entrada", "Fim_Emprestimo"), => 0
        identical(sort(Tipo_Registro), sort(c("Entrada", "Fim_Emprestimo"))) ~ 0,
        
        # 4b) Se Tipo_Registro = c("Retorno_Emprestimo", "Saida_Emprestimo") e Destino[1] == Destino[2], => 0
        identical(sort(Tipo_Registro), sort(c("Retorno_Emprestimo","Saida_Emprestimo"))) &
          Destino[1] == Destino[2] ~ 0,
        # 4c) Se Tipo_Registro = c(2*"Retorno_Emprestimo", 2*"Saida_Emprestimo") e Destino[1:2] == Destino[3:4], => 0
        identical(sort(Tipo_Registro),c("Retorno_Emprestimo", "Retorno_Emprestimo", "Saida_Emprestimo", "Saida_Emprestimo")) &
          identical(sort(c(Destino[1],Destino[2])),sort(c(Destino[3],Destino[4]))) ~ 0,
        
        # 4d) Caso contrário => 1
        TRUE ~ 1
      )
    )
  ) %>%
  ungroup() %>%
  distinct(ID_Jogador,Time,identifier,Nao_Retencao)

# Atribuindo aos Dados
Dados <- Dados %>% 
  left_join(TB_Transferencias_Saidas %>% 
            mutate(identifier = case_when(Time %in% c("Atlético Goianiense","Avaí FC","Ceará SC","EC Juventude") &
                                            identifier == "BRA2_2022"~"BRA1_2022",
                                          Time %in% c("América Mineiro","Coritiba FC","Goiás EC","Santos FC") &
                                            identifier == "BRA2_2023"~"BRA1_2023",
                                          TRUE ~ identifier)),
            by = c("ID_Jogador","Time","Identifier"="identifier")) %>% 
  mutate(Nao_Retencao = ifelse(is.na(Nao_Retencao),0,1))

########################################
##### trazendo infos empréstimos #######
########################################

TB_Transferencias_Emprestimos<-TB_Transferencias_Empilhada %>% 
  mutate(
    Tipo_Registro = case_when(
      Status == "Saída" & grepl("Fim do empréstimo", Quantia_Paga) ~ "Fim_Emprestimo",
      Status == "Entrada" & grepl("Fim do empréstimo", Quantia_Paga) ~ "Retorno_Emprestimo",
      Status == "Saída" & grepl("mpréstimo", Quantia_Paga) ~ "Saida_Emprestimo",
      Status == "Entrada" & grepl("mpréstimo", Quantia_Paga) ~ "Entrada_Emprestimo",
      Status == "Entrada" ~ "Entrada",
      Status == "Saída" ~ "Saída"
    )) %>% 
  group_by(ID_Jogador, Time, identifier) %>%
  summarise(
    EhEmprestimo = case_when(
      any(Tipo_Registro %in% c("Entrada_Emprestimo",
                               "Saida_Emprestimo",
                               "Retorno_Emprestimo",
                               "Fim_Emprestimo")) ~ 1,
      TRUE ~ 0
    ),
    .groups = "drop"
  )

# Atribuindo e Tratando
Dados <- Dados %>% 
  left_join(TB_Transferencias_Emprestimos %>% 
              mutate(identifier = case_when(Time %in% c("Atlético Goianiense","Avaí FC","Ceará SC","EC Juventude") &
                                              identifier == "BRA2_2022"~"BRA1_2022",
                                            Time %in% c("América Mineiro","Coritiba FC","Goiás EC","Santos FC") &
                                              identifier == "BRA2_2023"~"BRA1_2023",
                                            TRUE ~ identifier)),
            by = c("ID_Jogador","Time","Identifier"="identifier")) %>%
  group_by(ID_Jogador, Time) %>%
  # ordena as linhas por ano (ou pelo seu identifier)
  arrange(Identifier, .by_group = TRUE) %>%
  mutate(
    EhEmprestimo = case_when(
      # se EhEmprestimo atual é NA E a lag(EhEmprestimo) for 1, então 1
      is.na(EhEmprestimo) & lag(EhEmprestimo, default = 0) == 1 ~ 1,
      # se EhEmprestimo atual é NA E a lead(EhEmprestimo) for 1, então 1
      is.na(EhEmprestimo) & lead(EhEmprestimo, default = 0) == 1~ 1,
      # se nao fica igual
      TRUE ~ EhEmprestimo)
  ) %>%
  ungroup() %>% mutate(
    # Onde é NA vira 0 e onde não é continua o valor
    EhEmprestimo = coalesce(EhEmprestimo, 0)
  )

########################################
####### criando book variáveis #########
########################################

Dados_Analiticos <- Dados %>% 
  mutate(Valor_Mercado = case_when(str_detect(`Valor Mercado`, "mil")~as.numeric(gsub(",",".",gsub("[^0-9,]", "", `Valor Mercado`))),
                                   str_detect(`Valor Mercado`, "\\bmi\\b")~as.numeric(gsub(",",".",gsub("[^0-9,]", "", `Valor Mercado`)))*1000,
                                   TRUE ~ NA),
         Nacionalidade  = as.factor(ifelse(`País de Origem` == "Brasil","Brasileiro","Estrangeiro")),
         Posicao = as.factor(Posição),
         Camisa = as.factor(Numero_da_Camisa),
         Data_de_Nascimento = as.Date(str_sub(Data_de_Nascimento, 1, 10), format = "%d/%m/%Y"),
         Idade = case_when(Identifier == "BRA1_2022" ~ as.numeric(as.Date("13/11/2022", format = "%d/%m/%Y")-Data_de_Nascimento),
                                Identifier == "BRA1_2023" ~ as.numeric(as.Date("06/12/2023", format = "%d/%m/%Y")- Data_de_Nascimento),
                                TRUE ~ NA),
         Idade= trunc(Idade/365),
         Altura = as.numeric(str_replace_all(str_remove_all(Altura,"m"),",",".")),
         Pe_favorito = as.factor(Pe),
         Tempo_no_Clube = case_when(Identifier == "BRA1_2022" ~ as.numeric(as.Date("13/11/2022", format = "%d/%m/%Y")-No_time_desde),
                                    Identifier == "BRA1_2023" ~ as.numeric(as.Date("06/12/2023", format = "%d/%m/%Y")- No_time_desde),
                                    TRUE ~ NA),
         No_plantel = ifelse(No_plantel == "-",0,as.numeric(No_plantel)),
         Jogos = ifelse(grepl("Não",Jogos),0,as.numeric(Jogos)),
         Gols = ifelse(Gols == "-",0,as.numeric(Gols)),
         Assistencias = ifelse(Assistencias== "-",0,as.numeric(Assistencias)),
         Cartoes_amarelos = ifelse(Cartoes_amarelos== "-",0,as.numeric(Cartoes_amarelos)),
         Expulsoes_dois_amarelos = ifelse(Expulsoes_dois_amarelos== "-",0,as.numeric(Expulsoes_dois_amarelos)),
         Expulsoes_vermelho_direto = ifelse(Expulsoes_vermelho_direto== "-",0,as.numeric(Expulsoes_vermelho_direto)),
         Suplente_utilizado = ifelse(Suplente_utilizado== "-",0,as.numeric(Suplente_utilizado)),
         Substituicoes = ifelse(Substituicoes== "-",0,as.numeric(Substituicoes)),
         Pontos_por_jogo = as.numeric(str_replace_all(Pontos_por_jogo,",",".")),
         Minutos_jogados = ifelse(Minutos_jogados == " ",0,as.numeric(str_remove_all(Minutos_jogados,"'"))),
         Minutos_jogados = coalesce(Minutos_jogados,0),
         EhEmprestimo = as.factor(EhEmprestimo)
         ) %>% 
  select(Nome_Jogador = `Nome Jogador`,Identifier,ID_Jogador,Time,Data_de_Nascimento,Valor_Mercado,Nacionalidade,
         Posicao,Camisa,Idade,Altura,Pe_favorito,Tempo_no_Clube,No_plantel,Jogos,Gols,Assistencias,
         Cartoes_amarelos,Expulsoes_dois_amarelos,Expulsoes_vermelho_direto,Suplente_utilizado,Substituicoes,
         Pontos_por_jogo,Minutos_jogados,EhEmprestimo,Nao_Retencao)

# Análise Descritiva

Dados_Analiticos %>% 
  summary()

Dados_Analiticos %>% 
  ggplot(aes(y=Idade_dias,group = Nao_Retencao))+
  geom_boxplot()+
  theme_minimal()

########################################
############## Modelagem ###############
########################################

ajuste <- glm(Nao_Retencao ~ .,data = Dados_Analiticos[,c(5,7:26)],family = binomial)
summary(ajuste2)

ajuste2 <- glm(Nao_Retencao ~ .,data = Dados_Analiticos[,c(5,7:10,12,14:26)],family = binomial)
step(ajuste2)


ajuste3 <- glm(Nao_Retencao ~ .,data = Dados_Analiticos[,c(7:10,12,14:26)],family = binomial)
 
library(glmnet)
glmnet(x=Dados_Analiticos[,c(7:10,12,14:26)],y = Dados_Analiticos$Nao_Retencao)
