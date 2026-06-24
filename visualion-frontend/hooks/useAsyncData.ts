// hooks/useAsyncData.ts
"use client";

import { useEffect, useState, useCallback } from "react";
import { APIError } from "@/service/api";

interface UseAsyncDataOptions<T> {
  onError?: (error: APIError) => void;
  onSuccess?: (data: T) => void;
  retryDelay?: number;
  maxRetries?: number;
}

interface UseAsyncDataReturn<T> {
  data: T | null;
  loading: boolean;
  error: APIError | null;
  retry: () => Promise<void>;
  reset: () => void;
}

export function useAsyncData<T>(
  fetchFn: () => Promise<T>,
  options: UseAsyncDataOptions<T> = {}
): UseAsyncDataReturn<T> {
  const { onError, onSuccess, retryDelay = 1000, maxRetries = 3 } = options;
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<APIError | null>(null);
  const [retries, setRetries] = useState(0);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await fetchFn();
      setData(result);
      setRetries(0);
      onSuccess?.(result);
    } catch (err) {
      const apiError = err instanceof APIError ? err : new APIError(500, String(err));
      setError(apiError);
      onError?.(apiError);

      // Auto-retry on certain errors
      if (retries < maxRetries && (apiError.status === 500 || apiError.status === 503)) {
        setTimeout(() => {
          setRetries(r => r + 1);
        }, retryDelay);
      }
    } finally {
      setLoading(false);
    }
  }, [fetchFn, onError, onSuccess, retryDelay, maxRetries, retries]);

  useEffect(() => {
    setTimeout(() => fetchData(), 0);
  }, [fetchData]);

  const retry = useCallback(async () => {
    setRetries(0);
    await fetchData();
  }, [fetchData]);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(true);
    setRetries(0);
  }, []);

  return { data, loading, error, retry, reset };
}
