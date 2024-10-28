// src/components/AudioPlayer.js
import React from "react";
import ReactAudioPlayer from "react-audio-player";

function AudioPlayer({ audioURL }) {
  return (
    <div className="bg-white p-6 shadow-lg rounded-lg w-full max-w-md text-center">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Áudio Gerado</h2>
      <ReactAudioPlayer src={audioURL} controls className="w-full mb-4" />
      <a href={audioURL} download="audio.mp3" className="text-blue-600 font-medium hover:underline">
        Baixar áudio
      </a>
    </div>
  );
}

export default AudioPlayer;