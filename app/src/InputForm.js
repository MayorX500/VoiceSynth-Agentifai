// src/InputForm.js
import React, { useState } from "react";

function InputForm({ onSubmit, loading }) {
  const [text, setText] = useState("");
  const [language, setLanguage] = useState("pt");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(text, language);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col items-center bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Converta o texto em áudio</h2>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Digite o texto aqui..."
        className="mb-4 p-4 w-full border rounded-md border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
        rows="5"
      />
      <div className="mb-4 w-full">
        <label className="block text-gray-600 mb-1">Selecione o idioma:</label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="p-2 w-full border rounded-md border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          <option value="pt">Português</option>
          <option value="en">Inglês</option>
        </select>
      </div>
      <button
        type="submit"
        disabled={loading}
        className={`p-2 w-full bg-blue-500 text-white font-semibold rounded-md transition duration-200 hover:bg-blue-600 focus:ring-4 focus:ring-blue-300 ${
          loading ? "cursor-not-allowed opacity-50" : ""
        }`}
      >
        {loading ? "Gerando áudio..." : "Enviar"}
      </button>
    </form>
  );
}

export default InputForm;