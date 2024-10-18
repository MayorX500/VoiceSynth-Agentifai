g++ -o date_normalizer date_normalizer.cpp $(pkg-config --cflags --libs libcurl) -std=c++11

g++ -o main_normalizer mainNormalizer.cpp dateNormalization.cpp numNormalizer.cpp -lcurl -std=c++11
