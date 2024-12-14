<img width="150" src="images/EEUM_logo_EN.jpg"> 

# PI24 - Real-Time Speech Synthesis 
**Authors:**
- [Beatriz Monteiro](https://github.com/5ditto)
- [Daniel Du](https://github.com/ddu72)
- [Daniel Furtado](https://github.com/danielfurtado11)
- [Miguel Gomes](https://github.com/MayorX500)
- [Moisés Antunes](https://github.com/MoisesA14)
- [Telmo Maciel](https://github.com/telmomaciel9)

# Introduction

The goal of this project is to develop a low-latency, high-quality audio synthesis real-time text-to-speech (TTS) system. 
The project is set up to take advantage of microservices concepts in order to facilitate modularity, scalability, and adaptability.
The architecture guarantees effective functioning and facilitates future extensions by breaking the system up into discrete parts, each of which is in charge of carrying out particular functions.

The system was designed to be able to run on a large variety of hardware, from small devices to large cloud servers.

## Project Scope

This project's main objective was to create a reliable TTS system that could perform the following tasks:

##### Process text inputs:
- Could accept inputs in the form of structured SSML (Speech Synthesis Markup Language) or natural language text.
- Prepares the input for synthesis by apllying advanced normalization and techniques. 

##### Generate Real-Time Audio:
- Capable of producing audio streams with minimal latency.
- Ensures high-quality audio output, with a focus on naturalness and intelligibility.

##### Supports Modular Deployment:
- The system is designed to be modular, allowing for easy integration of new components and updates on existing ones.
- The system can be deployed in a microservices architecture, allowing for scalability and adaptability.

##### Utilizability:
- The system is designed to be usable by a wide range of users, from developers to end-users.
- The system offers a simple API for easy integration into other systems.

##### Facilitates Customization:
- The system is designed to be easily customizable, allowing for the integration of new voices, languages, and other features.
- The system is designed to be easily extendable, allowing for the integration of new components and features.

The project was designed to meet real-world demands for customizable, efficient, and scalable voice synthesis, making it ideal for applications such as virtual assistants, customer service bots, and accessible technology solutions.


