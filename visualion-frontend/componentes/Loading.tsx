import React from "react";

export function LoadingSpinner({
  message = "Cargando..."
}: {
  message?: string
}) {
  return (
    <div className="flex items-center justify-center p-12 bg-gray-900 border border-gray-800 rounded-lg">
      <div className="text-center">
        <div className="inline-block mb-4">
          <svg
            className="animate-spin h-8 w-8 text-indigo-500"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        </div>
        <p className="text-indigo-400 font-medium animate-pulse">{message}</p>
      </div>
    </div>
  );
}

export function LoadingSkeleton({
  rows = 3
}: {
  rows?: number
}) {
  return (
    <div className="space-y-4">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="bg-gray-900 p-4 rounded-lg border border-gray-800 animate-pulse">
          <div className="h-4 bg-gray-800 rounded w-3/4 mb-2"></div>
          <div className="h-3 bg-gray-800 rounded w-1/2"></div>
        </div>
      ))}
    </div>
  );
}
