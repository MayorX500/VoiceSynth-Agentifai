// src/App.js
import React, { useState } from "react";
import InputForm from "./InputForm";
import AudioPlayer from "./AudioPlayer";
import axios from "axios";

function App() {
  const [audioURL, setAudioURL] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(true); // Novo estado para controlar a exibição do formulário

  const handleTextToSpeech = async (text, language) => {
    setLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/tts",
        { text, language },
        { responseType: 'blob' } // Adicione isso para indicar que você está esperando um blob
      );
  
      const audioBlob = new Blob([response.data], { type: "audio/wav" }); // Altere para "audio/wav"
      const audioURL = URL.createObjectURL(audioBlob);
      setAudioURL(audioURL);
      setShowForm(false); // Ocultar o formulário após a geração do áudio
    } catch (error) {
      console.error("Erro ao gerar áudio:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewInput = () => {
    setAudioURL(null); // Limpar a URL do áudio anterior
    setShowForm(true); // Mostrar o formulário novamente
  };

  return (
    <div className="flex flex-col items-center min-h-screen p-6 bg-gray-100">
      <h1 className="text-3xl font-bold mb-8 text-blue-600">Text-to-Speech Web App</h1>
      {showForm ? (
        <InputForm onSubmit={handleTextToSpeech} loading={loading} />
      ) : (
        <>
          {audioURL && <AudioPlayer audioURL={audioURL} />}
          <button 
            onClick={handleNewInput}
            className="mt-4 p-2 bg-blue-500 text-white rounded hover:bg-blue-700"
          >
            Submeter novo texto
          </button>
        </>
      )}
    </div>
  );
}

export default App;