function ErrorFallback() {
  return (
    <div className="flex h-screen items-center justify-center bg-gray-950">
      <div className="flex flex-col items-center gap-4">
        <p className="text-white text-lg font-medium">Something went wrong</p>
        <button
          onClick={() => (window.location.href = "/")}
          className="text-sm text-gray-400 hover:text-white transition-colors"
        >
          Go back home
        </button>
      </div>
    </div>
  );
}

export default ErrorFallback;
