import React from "react";
import Link from "next/link";

interface ErrorProps {
  title?: string;
  message: string;
  retry?: () => void;
  backLink?: string;
}

export function ErrorAlert({
  title = "Error",
  message,
  retry,
  backLink,
}: ErrorProps) {
  return (
    <div className="bg-red-900/20 border border-red-600/50 rounded-lg p-6">
      <div className="flex items-start gap-4">
        <div className="text-2xl">⚠️</div>
        <div className="flex-1">
          <h3 className="text-red-300 font-bold mb-2">{title}</h3>
          <p className="text-red-200 text-sm mb-4">{message}</p>

          <div className="flex gap-3 flex-wrap">
            {retry && (
              <button
                onClick={retry}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                🔄 Reintentar
              </button>
            )}
            {backLink && (
              <Link
                href={backLink}
                className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                ← Volver
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export function ErrorBoundary({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gray-950">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">😞</div>
          <h1 className="text-3xl font-bold text-gray-100 mb-2">
            Algo salió mal
          </h1>
          <p className="text-gray-400">
            Ocurrió un error inesperado en la aplicación
          </p>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-4 mb-6">
          <p className="text-gray-400 text-sm font-mono break-words">
            {error.message}
          </p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={reset}
            className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-3 rounded-lg font-medium transition-colors"
          >
            🔄 Reintentar
          </button>
          <Link
            href="/"
            className="flex-1 bg-gray-700 hover:bg-gray-600 text-white px-4 py-3 rounded-lg font-medium text-center transition-colors"
          >
            🏠 Inicio
          </Link>
        </div>
      </div>
    </div>
  );
}

export function WarningAlert({
  message,
  onDismiss,
}: {
  message: string;
  onDismiss?: () => void;
}) {
  return (
    <div className="bg-yellow-900/20 border border-yellow-600/50 rounded-lg p-4 flex items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <span className="text-xl">⚡</span>
        <p className="text-yellow-200 text-sm">{message}</p>
      </div>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="text-yellow-300 hover:text-yellow-200 font-bold"
        >
          ✕
        </button>
      )}
    </div>
  );
}

export function SuccessAlert({
  message,
  onDismiss,
}: {
  message: string;
  onDismiss?: () => void;
}) {
  return (
    <div className="bg-green-900/20 border border-green-600/50 rounded-lg p-4 flex items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <span className="text-xl">✅</span>
        <p className="text-green-200 text-sm">{message}</p>
      </div>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="text-green-300 hover:text-green-200 font-bold"
        >
          ✕
        </button>
      )}
    </div>
  );
}
