
for(N in c(10,100,1000)) print(sum(sample(0:1,N,replace=T)))

media <- 12 * (1^2/2 - 0^2/2)
var <- function(x) ( x^3/3)-(x^2/2)+(x/4)   ## integral de (x-1/2)^2 * 1 dx para ser aplicada entre 0 e 1 
variancia <- 12 * (var(1) - var(0))
media
variancia

dist_a = rnorm(10000,media,sd=variancia^0.5)
hist(dist_a)

    amostra_total <- 0
    for (i in 1:12) {
      amostras <- runif(12000, min = 0, max = 1)
      amostra_total <- amostra_total + amostras 
    }
    media <- mean(amostra_total)
    variancia <- sd(amostra_total)^2
    media
    variancia

hist(amostra_total)

library("triangle")

media <- c()
variancia <- c()
for(n in 1:1000){
    u <- 0
    v <- 0
    for(i in 1:10){
        X <- rtriangle(1000,i,20+i,10+1)
        u <-  mean(X) + u
        v <- sd(X)^2 + v
    }
    media <- c(media,u)
    variancia <- c(variancia,v)
}
mean(media)
mean(variancia)

hist(u)

z <- rnorm(1000,0,1) * rnorm(1000,0,1)
hist(z)

z <- rnorm(1000,0,1) / rnorm(1000,0,1)
hist(z)

len = 3000
tam <- c(2,5,10)

for(t in 1:3 ){
    conjunto <- c()
for(l in 1:len){
x1 <- -Inf
for(t2 in 1:tam[t] )  x1 <- max(x1,rnorm(1,0,1))
conjunto <- c(conjunto,x1)
    }
hist(conjunto)}


aprox <- function(n){
z <- n *rnorm(1000,0,1) ^2
hist(z)}
for(h in 1:4) aprox(h)

z <- exp(rnorm(1000,0,1))
hist(z)
