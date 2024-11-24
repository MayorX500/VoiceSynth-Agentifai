#!/bin/bash

# Test different sentence lengths
sentences=(
        "Olá"
        "Obrigado"
        "Como estás"
        "Até amanhã"
        "Vamos ao cinema"
        "Está um dia bonito hoje"
        "Preciso de comprar pão na padaria"
        "O cão correu atrás da bola no parque"
        "Ela leu o livro todo numa tarde chuvosa"
        "O professor explicou a lição com muita paciência"
        "Eles decidiram viajar pelo país durante as férias"
        "O sol brilhava intensamente no céu sem nuvens"
        "No inverno, gostamos de beber chá quente junto à lareira"
        "A cidade estava cheia de luzes e decorações de Natal"
        "Estudamos juntos na biblioteca para preparar o exame final"
        "O concerto foi magnífico, com músicos talentosos e melodias emocionantes"
        "Depois de uma longa caminhada, descansaram à sombra de uma árvore"
        "Ela preparou uma surpresa especial para o aniversário do irmão"
        "Os cientistas descobriram uma nova espécie de planta na floresta tropical"
        "A exposição de arte contemporânea atraiu muitos visitantes este ano"
        "Apesar da chuva, decidiram continuar com o piquenique no parque"
        "Os atletas treinaram arduamente para se prepararem para a competição"
        "A biblioteca oferece uma vasta coleção de livros e recursos digitais"
        "Durante a viagem, aprenderam muito sobre as culturas locais e tradições"
        "Com determinação e esforço, alcançou todos os seus objetivos profissionais"
        "No fim de semana, planearam visitar a aldeia histórica e explorar as ruínas antigas"
)
mkdir -p output

for sentence in "${sentences[@]}"; do
        echo "Processing sentence: $sentence"
        sh run.sh -t "$sentence" -c "config/intlex_config.json" -o "output/$sentence.wav"
done