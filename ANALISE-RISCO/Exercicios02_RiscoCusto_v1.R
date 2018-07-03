  #
  ############################################
  #      Análise de Risco                    #
  #      Segunda Lista de exercícios         #
  #      GRUPO: Doutorado                    #
  ############################################
  #
  # Constantes do sistema
  # Quantidade de cenários
  Ns=3000
  # Tamanho do gasoduto
  tamanhoDoGasodutoEmKm = 260
  # acrescer, ou não, 30 km na malha do gasoduto
  contingencia <- 30 
  probabilidade <- c(0.35, 0.36, 0.37, 0.38, 0.39, 0.40) # probabilidade de ocorrer aumento na malha do gasoduto
  # Normalização de Kilometragem
  tubosPorKm <- 1000/8
  juncoesPorKm <- 1000/8
  # Cores para diferenciar os graficos  
  cor <- c("red", "green", "blue", "black", "yellow", "lightgrey", "green")
  # bibliotecas utilizadas
  library (triangle)
  # 
  # Tubulação é o item 1 da especificação
  simularCustoTubulacaoPorTubo <- 
    rtriangle(Ns, 725, 790, 740)
  #
  # O custo para cavar 1Km de vala corresponde a multiplicacao do tempo de trabalho pelo custo de homem/hora
    # Tempo para cavar vala é o item 2 do arquivo base
    # Custo do Trabalho por hora é o item 3 do arquivo base
    cavarKm <- cbind (rtriangle(Ns, 12, 25, 16), rtriangle(Ns, 17, 23, 18.5))
  #  
  # Transporte da Tubulação é o item 4 do arquivo base
  # Assumindo que a distância nao importa e que trata-se do custo para transportar cada tubo de 8M 
  simularCustoTransporteTubulacaoPorTubo <- rtriangle(Ns, 6.1, 7.4, 6.6) 
  #
  # Custo de Soldagem será o produto entre o tempo de soldagem (item 5) e o custo do trabalho (item3)
    # Tempo de Soldagem dos tubos é o item 5 do arquivo base
    # Custo do Trabalho por hora é o item 3 do arquivo base
    #
    soldarTubo  <- cbind (rtriangle(Ns, 4, 5, 4.5), rtriangle(Ns, 17, 23, 18.5))
    # 
  # Sistema de Filtragem é o item 6 do arquivo base
  simularCustoSistemaFiltragem <- rtriangle (Ns, 165000, 188000, 173000)
  
  # Custo de Acabamento é o item 7 do arquivo base
  simularCustoAcabamentoPorKm <- rtriangle (Ns, 14000, 17000, 15000) 
  #
  # Montar cenarios
  custoFinal <- NULL
  # for (i in 1:length(probabilidade)){
    custoOpcao<- matrix(nrow=3000, ncol=6)
  #
    evento <- rbinom (Ns,1, 0.35) # probabilidade de acrescimo na malha
    Cenarios <- cbind (simularCustoTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       cavarKm[,1] * cavarKm[, 2]  * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoTransporteTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia),  
                       soldarTubo [,1] * soldarTubo [,2] * juncoesPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoSistemaFiltragem, 
                       simularCustoAcabamentoPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), evento)
    custoOpcao[,1] <- apply(Cenarios[,1:6],M=1,sum)
  #
    evento <- rbinom (Ns,1, 0.36) # probabilidade de acrescimo na malha
    Cenarios <- cbind (simularCustoTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       cavarKm[,1] * cavarKm[, 2]  * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoTransporteTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia),  
                       soldarTubo [,1] * soldarTubo [,2] * juncoesPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoSistemaFiltragem, 
                       simularCustoAcabamentoPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), evento)
    custoOpcao[,2] <- apply(Cenarios[,1:6],M=1,sum)
  #
    evento <- rbinom (Ns,1, 0.37) # probabilidade de acrescimo na malha
    Cenarios <- cbind (simularCustoTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       cavarKm[,1] * cavarKm[, 2]  * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoTransporteTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia),  
                       soldarTubo [,1] * soldarTubo [,2] * juncoesPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoSistemaFiltragem, 
                       simularCustoAcabamentoPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), evento)
    custoOpcao[,3] <- apply(Cenarios[,1:6],M=1,sum)
  #
    evento <- rbinom (Ns,1, 0.38) # probabilidade de acrescimo na malha
    Cenarios <- cbind (simularCustoTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       cavarKm[,1] * cavarKm[, 2]  * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoTransporteTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia),  
                       soldarTubo [,1] * soldarTubo [,2] * juncoesPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoSistemaFiltragem, 
                       simularCustoAcabamentoPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), evento)
    custoOpcao[,4] <- apply(Cenarios[,1:6],M=1,sum)
  #
    evento <- rbinom (Ns,1, 0.39) # probabilidade de acrescimo na malha
    Cenarios <- cbind (simularCustoTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       cavarKm[,1] * cavarKm[, 2]  * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoTransporteTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia),  
                       soldarTubo [,1] * soldarTubo [,2] * juncoesPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoSistemaFiltragem, 
                       simularCustoAcabamentoPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), evento)
    custoOpcao[,5] <- apply(Cenarios[,1:6],M=1,sum)
  #
    evento <- rbinom (Ns,1, 0.40) # probabilidade de acrescimo na malha
    Cenarios <- cbind (simularCustoTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       cavarKm[,1] * cavarKm[, 2]  * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoTransporteTubulacaoPorTubo * tubosPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia),  
                       soldarTubo [,1] * soldarTubo [,2] * juncoesPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), 
                       simularCustoSistemaFiltragem, 
                       simularCustoAcabamentoPorKm * (tamanhoDoGasodutoEmKm + evento * contingencia), evento)
    custoOpcao[,6] <- apply(Cenarios[,1:6],M=1,sum)
  # Visualização - dividido por 4 preço do dolar e dividido por 10 (de milhar para dezena de milh)
custoOpcao[,1] <- custoOpcao[,1] / 10 /4
custoOpcao[,2] <- custoOpcao[,2] / 10 /4
custoOpcao[,3] <- custoOpcao[,3] / 10 /4
custoOpcao[,4] <- custoOpcao[,4] / 10 /4
custoOpcao[,5] <- custoOpcao[,5] / 10 /4
custoOpcao[,6] <- custoOpcao[,6] / 10 /4
  # Cada cenario foi agregado a uma coluna do custoFinal do Gasoduto para plotagem
  # custoFinal <- cbind(custoFinal, custoOpcao)      
  # }
  # Plotagem dos gráficos
par(mfrow = c(2, 3))
for (i in 1:length(probabilidade)){
hist(custoOpcao[,i])
}
  par(mfrow = c(1, 1))
 for (i in 1:length(probabilidade)){
    plot (ecdf(custoOpcao[,i]), 
          main = NULL, 
          col = cor[i], 
          lwd = 1, 
          add=(i-1), 
          xlab = "em 10.000 dólares", 
          ylab = "Frequência",
          xlim=c(min(custoOpcao[,1]), max(custoOpcao[,i])), 
          ylim=c(0, 1))
#
 }
  
# Final da função CustoGasoduto