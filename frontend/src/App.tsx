function App() {
  return (
    // This div is the background (Slate 900)
    <div className="min-h-screen bg-slate-900 text-white p-8">
      
      {/* This is the Header Box */}
      <header className="max-w-4xl mx-auto border-b border-slate-800 pb-6 mb-8">
        <h1 className="text-4xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
          Zenith Tasks
        </h1>
        <p className="text-slate-400 mt-2">
          Your backend is active. Ready to fetch data.
        </p>
      </header>

      {/* This is a placeholder for your future Todo List */}
      <main className="max-w-4xl mx-auto">
        <div className="bg-slate-800/50 border border-slate-700 p-12 rounded-2xl border-dashed text-center">
          <p className="text-slate-500 font-medium">
            No tasks found. Time to connect the API.
          </p>
        </div>
      </main>

    </div>
  );
}

export default App;